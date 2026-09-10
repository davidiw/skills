#!/usr/bin/env python3
"""External evaluator: python3 reservation_acceptance.py FROZEN_TASK_ROOT"""
import argparse
import hashlib
import importlib
import json
import multiprocessing as mp
from pathlib import Path
import platform
import queue
import sys
import tempfile
import traceback
import unittest

sys.dont_write_bytecode = True
ROOT = None
TIMEOUT = 10.0

def modules(root):
    sys.path.insert(0, str(root))
    importlib.invalidate_caches()
    inventory = importlib.import_module("inventory")
    client = importlib.import_module("client")
    for module in (inventory, client):
        if Path(module.__file__).resolve().parent != Path(root).resolve():
            raise RuntimeError("module resolved outside frozen task root")
    return inventory, client

def manifest(root):
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file() and not {".git", "__pycache__"}.intersection(p.relative_to(root).parts)
    }

def reserve_child(root, db_path, args, ready, start, attempts, output, timeout):
    db = None
    try:
        inventory, _ = modules(root)
        db = inventory.connect(db_path)
        reported = False
        def trace(sql):
            nonlocal reported
            if not reported and sql.lstrip().upper().startswith(
                    ("BEGIN", "UPDATE", "INSERT", "DELETE", "REPLACE")):
                attempts.put(mp.current_process().pid)
                reported = True
        db.set_trace_callback(trace)
        ready.put(mp.current_process().pid)
        if not start.wait(timeout):
            raise TimeoutError("start barrier")
        result = inventory.reserve(db, *args)
        output.put({"pid": mp.current_process().pid, "result": result})
    except BaseException:
        output.put({"pid": mp.current_process().pid, "error": traceback.format_exc()})
    finally:
        if db is not None:
            db.close()

def result(op, sku, quantity, status):
    return {"operation_id": op, "sku": sku, "quantity": quantity, "status": status}

class Injected(Exception):
    pass

class ReservationAcceptance(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="reservation-evaluator-")
        self.addCleanup(self.temp.cleanup)
        self.path = str(Path(self.temp.name) / "inventory.sqlite")
        self.inventory, self.client = modules(ROOT)
        self.db = self.inventory.connect(self.path)
        self.addCleanup(self.db.close)

    def seed(self, quantity=5):
        self.inventory.initialize(self.db, "a", quantity)
        self.inventory.initialize(self.db, "b", 4)

    def state(self, db=None):
        db = self.db if db is None else db
        return (
            [tuple(r) for r in db.execute("SELECT sku,quantity FROM stock ORDER BY sku")],
            [tuple(r) for r in db.execute("SELECT operation_id,sku,quantity,status "
                                         "FROM operations ORDER BY operation_id")],
        )

    def available(self, quantity, sku="a", db=None):
        actual = self.client.availability(self.db if db is None else db, sku)
        self.assertEqual(actual, {"sku": sku, "available": quantity})
        self.assertIs(type(actual["available"]), int)

    def run_processes(self, jobs, lock_schedule=False):
        ctx = mp.get_context("spawn")
        ready, attempts, output = ctx.Queue(), ctx.Queue(), ctx.Queue()
        start = ctx.Event()
        processes = [
            ctx.Process(target=reserve_child, args=(
                str(ROOT), self.path, job, ready, start, attempts, output, TIMEOUT))
            for job in jobs
        ]
        locked = False
        try:
            for process in processes:
                process.start()
            pids = {ready.get(timeout=TIMEOUT) for _ in jobs}
            self.assertEqual(len(pids), len(jobs))
            if lock_schedule:
                # Children already connected. Hold the writer until every child
                # reaches its first transaction/write statement.
                self.db.execute("BEGIN IMMEDIATE")
                locked = True
            start.set()
            if lock_schedule:
                attempted = {attempts.get(timeout=TIMEOUT) for _ in jobs}
                self.assertEqual(attempted, pids)
                self.db.rollback()
                locked = False
            replies = [output.get(timeout=TIMEOUT) for _ in jobs]
            for process in processes:
                process.join(TIMEOUT)
                self.assertFalse(process.is_alive(), "child did not exit")
                self.assertEqual(process.exitcode, 0)
            self.assertEqual({reply["pid"] for reply in replies}, pids)
            for reply in replies:
                self.assertNotIn("error", reply, reply.get("error"))
            return [reply["result"] for reply in replies]
        except queue.Empty as error:
            raise AssertionError("bounded child/barrier timeout") from error
        finally:
            if locked:
                self.db.rollback()
            start.set()
            for process in processes:
                if process.pid is not None:
                    if process.is_alive():
                        process.terminate()
                    process.join(TIMEOUT)
            for q in (ready, attempts, output):
                q.close()
                q.join_thread()

    def test_schema_and_public_consumer(self):
        self.seed(0)
        tables = {row[0] for row in self.db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")}
        self.assertEqual(tables, {"stock", "operations"})
        for table, expected in {
            "stock": [("sku", "TEXT", 1), ("quantity", "INTEGER", 0)],
            "operations": [("operation_id", "TEXT", 1), ("sku", "TEXT", 0),
                           ("quantity", "INTEGER", 0), ("status", "TEXT", 0)],
        }.items():
            info = self.db.execute("PRAGMA table_info(" + table + ")").fetchall()
            self.assertEqual([(r[1], r[2].upper(), r[5]) for r in info], expected)
            for row in info:
                if row[1] not in ("sku" if table == "stock" else "operation_id",):
                    self.assertEqual(row[3], 1)
        observer = self.inventory.connect(self.path)
        try:
            self.available(0, db=observer)
            self.available(4, "b", observer)
            with self.assertRaises(ValueError):
                self.client.availability(observer, "missing")
        finally:
            observer.close()

    def test_reserved_retry_after_process_exit(self):
        self.seed(5)
        expected = result("persist", "a", 2, "reserved")
        self.assertEqual(self.run_processes([("persist", "a", 2)]), [expected])
        self.assertEqual(self.run_processes([("persist", "a", 2)]), [expected])
        self.available(3)
        self.assertEqual(self.state()[1], [("persist", "a", 2, "reserved")])
        def forbidden_hook():
            self.fail("recorded retry invoked hook")
        self.assertEqual(self.inventory.reserve(
            self.db, "persist", "a", 2, before_commit=forbidden_hook), expected)

    def test_final_unit_competing_processes(self):
        self.seed(1)
        replies = self.run_processes(
            [("one", "a", 1), ("two", "a", 1)], lock_schedule=True)
        self.assertEqual(sorted(r["status"] for r in replies), ["insufficient", "reserved"])
        self.assertEqual({r["operation_id"] for r in replies}, {"one", "two"})
        for reply in replies:
            self.assertEqual(reply, result(reply["operation_id"], "a", 1, reply["status"]))
        self.available(0)
        self.assertEqual(self.state()[1], sorted(
            (r["operation_id"], "a", 1, r["status"]) for r in replies))

    def test_same_operation_competing_processes(self):
        self.seed(3)
        expected = result("same", "a", 2, "reserved")
        self.assertEqual(self.run_processes(
            [("same", "a", 2), ("same", "a", 2)], lock_schedule=True), [expected, expected])
        self.available(1)
        self.assertEqual(self.state()[1], [("same", "a", 2, "reserved")])

    def test_insufficient_result_persists(self):
        self.seed(1)
        expected = result("short", "a", 2, "insufficient")
        self.assertEqual(self.run_processes([("short", "a", 2)]), [expected])
        self.available(1)
        self.assertEqual(self.state()[1], [("short", "a", 2, "insufficient")])
        # Test-only replenishment distinguishes a stored outcome from recomputation.
        self.db.execute("UPDATE stock SET quantity=3 WHERE sku='a'")
        self.db.commit()
        self.assertEqual(self.run_processes([("short", "a", 2)]), [expected])
        def forbidden_hook():
            self.fail("recorded insufficient retry invoked hook")
        self.assertEqual(self.inventory.reserve(
            self.db, "short", "a", 2, before_commit=forbidden_hook), expected)
        self.available(3)
        self.assertEqual(self.inventory.reserve(self.db, "new", "a", 2),
                         result("new", "a", 2, "reserved"))
        self.available(1)

    def test_invalid_arguments_and_global_id_conflicts_do_not_mutate(self):
        self.seed(5)
        self.inventory.reserve(self.db, "recorded", "a", 1)
        before = self.state()
        bad = [("recorded", "b", 1), ("recorded", "a", 2),
               ("recorded", "a", True), ("new", "missing", 1), ("new", None, 1)]
        bad += [(op, "a", 1) for op in ("", None, 3, True, [], {})]
        bad += [("new", "a", quantity) for quantity in
                (0, -1, True, False, 1.5, "1", None, [], {})]
        for args in bad:
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    self.inventory.reserve(self.db, *args)
                self.assertEqual(self.state(), before)
        # Nonempty is the contract; it does not prohibit whitespace IDs.
        self.assertEqual(self.inventory.reserve(self.db, " ", "a", 1),
                         result(" ", "a", 1, "reserved"))

    def test_hook_rollback_and_committed_visibility(self):
        self.seed(5)
        observer = self.inventory.connect(self.path)
        try:
            for op, quantity, status, uncommitted_quantity in [
                ("rollback_reserved", 2, "reserved", 3),
                ("rollback_insufficient", 9, "insufficient", 5),
            ]:
                with self.subTest(status=status):
                    before = self.state()
                    seen = []
                    def fail_before_commit():
                        seen.append(self.state())
                        self.assertEqual(self.state(observer), before)
                        self.available(5, db=observer)
                        raise Injected("rollback oracle")
                    with self.assertRaises(Injected):
                        self.inventory.reserve(self.db, op, "a", quantity,
                                               before_commit=fail_before_commit)
                    self.assertEqual(len(seen), 1)
                    self.assertEqual(seen[0][0], [("a", uncommitted_quantity), ("b", 4)])
                    self.assertEqual(seen[0][1], [(op, "a", quantity, status)])
                    self.assertEqual(self.state(), before)
                    self.assertEqual(self.state(observer), before)
            self.assertEqual(self.inventory.reserve(self.db, "rollback_reserved", "a", 2),
                             result("rollback_reserved", "a", 2, "reserved"))
            self.available(3, db=observer)
        finally:
            observer.close()

def main():
    global ROOT, TIMEOUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()
    ROOT, TIMEOUT = args.root.resolve(), args.timeout
    if TIMEOUT <= 0:
        parser.error("--timeout must be positive")
    before = manifest(ROOT)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ReservationAcceptance)
    outcome = unittest.TextTestRunner(verbosity=2).run(suite)
    after = manifest(ROOT)
    report = {
        "command": sys.argv,
        "python": sys.version,
        "platform": platform.platform(),
        "source_before": before,
        "source_after": after,
        "source_unchanged": before == after,
        "evaluator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "tests": outcome.testsRun,
        "failures": [str(t) for t, _ in outcome.failures],
        "errors": [str(t) for t, _ in outcome.errors],
        "skipped": outcome.skipped,
    }
    print(json.dumps(report, sort_keys=True))
    return 0 if (outcome.wasSuccessful() and outcome.testsRun == 7
                 and not outcome.skipped and before == after) else 1

if __name__ == "__main__":
    sys.exit(main())
