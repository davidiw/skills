import json
import os
from pathlib import Path
import select
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest

sys.dont_write_bytecode = True

ROOT = Path.cwd().resolve()
if not all((ROOT / name).is_file()
           for name in ("inventory.py", "client.py", "DESIGN.md")):
    raise RuntimeError("Run from the frozen repository scratch copy")

sys.path.insert(0, str(ROOT))
import inventory
import client


WORKER = r'''
import json
import os
import select
import sys

sys.dont_write_bytecode = True
import inventory

def emit(value):
    print(json.dumps(value), flush=True)

def command():
    readable, _, _ = select.select([sys.stdin], [], [], 12.0)
    if not readable:
        raise TimeoutError("parent command timed out")
    line = sys.stdin.readline()
    if not line:
        raise RuntimeError("parent command stream closed")
    return line.strip()

db = None
try:
    path, operation_id, sku, quantity, hold, fail = json.loads(sys.argv[1])
    db = inventory.connect(path)
    emit({"event": "ready", "pid": os.getpid()})
    if command() != "start":
        raise RuntimeError("expected start")
    emit({"event": "attempting", "pid": os.getpid()})

    def callback():
        row = db.execute(
            "SELECT operation_id, sku, quantity, status "
            "FROM operations WHERE operation_id = ?", (operation_id,)
        ).fetchone()
        stock = db.execute(
            "SELECT quantity FROM stock WHERE sku = ?", (sku,)
        ).fetchone()
        emit({
            "event": "callback",
            "operation": None if row is None else list(row),
            "stock": None if stock is None else stock[0],
            "in_transaction": db.in_transaction,
        })
        if hold and command() != "release":
            raise RuntimeError("expected release")
        if fail:
            raise RuntimeError("intentional callback failure")

    result = inventory.reserve(
        db, operation_id, sku, quantity, before_commit=callback
    )
    emit({"event": "result", "result": result})
except BaseException as exc:
    emit({
        "event": "error",
        "type": type(exc).__name__,
        "message": str(exc),
    })
finally:
    if db is not None:
        db.close()
'''


class ReservationProcess:
    def __init__(self, path, operation_id, sku, quantity,
                 hold=False, fail=False):
        args = [str(path), operation_id, sku, quantity, hold, fail]
        self.process = subprocess.Popen(
            [sys.executable, "-B", "-c", WORKER, json.dumps(args)],
            cwd=str(ROOT),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
        )
        self.buffer = bytearray()
        self.events = []

    def send(self, command):
        self.process.stdin.write((command + "\n").encode("utf-8"))
        self.process.stdin.flush()

    def read_event(self, timeout=10.0):
        deadline = time.monotonic() + timeout
        while True:
            index = self.buffer.find(b"\n")
            if index >= 0:
                line = bytes(self.buffer[:index])
                del self.buffer[:index + 1]
                event = json.loads(line.decode("utf-8"))
                self.events.append(event)
                return event
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise AssertionError(
                    "Timed out waiting for child event; seen: "
                    + repr(self.events)
                )
            readable, _, _ = select.select(
                [self.process.stdout], [], [], remaining
            )
            if not readable:
                continue
            chunk = os.read(self.process.stdout.fileno(), 65536)
            if not chunk:
                raise AssertionError(
                    "Child output closed before expected event; seen: "
                    + repr(self.events)
                )
            self.buffer.extend(chunk)

    def has_output(self, timeout):
        if self.buffer:
            return True
        readable, _, _ = select.select(
            [self.process.stdout], [], [], timeout
        )
        return bool(readable)

    def stop(self):
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=2.0)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=2.0)
        for stream in (
            self.process.stdin,
            self.process.stdout,
            self.process.stderr,
        ):
            if stream is not None:
                try:
                    stream.close()
                except OSError:
                    pass


class ReservationContractTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(
            prefix="reservation-review-", dir=str(ROOT)
        )
        self.addCleanup(self.scratch.cleanup)
        self.path = Path(self.scratch.name) / "stock.sqlite"
        self.db = inventory.connect(self.path)
        self.addCleanup(lambda: self.db.close())
        inventory.initialize(self.db, "A", 5)
        inventory.initialize(self.db, "B", 4)

    def reopen(self):
        self.db.close()
        self.db = inventory.connect(self.path)

    def snapshot(self, db=None):
        if db is None:
            db = self.db
        return (
            db.execute(
                "SELECT sku, quantity FROM stock ORDER BY sku"
            ).fetchall(),
            db.execute(
                "SELECT operation_id, sku, quantity, status "
                "FROM operations ORDER BY operation_id"
            ).fetchall(),
        )

    def expected(self, operation_id, sku, quantity, status):
        return {
            "operation_id": operation_id,
            "sku": sku,
            "quantity": quantity,
            "status": status,
        }

    def no_callback(self):
        self.fail("A replay or invalid call invoked before_commit")

    def spawn(self, operation_id, sku, quantity, hold=False, fail=False):
        child = ReservationProcess(
            self.path, operation_id, sku, quantity, hold, fail
        )
        self.addCleanup(child.stop)
        ready = self.expect(child, "ready")
        self.assertEqual(ready["pid"], child.process.pid)
        self.assertNotEqual(ready["pid"], os.getpid())
        return child

    def expect(self, child, event_name):
        event = child.read_event()
        self.assertEqual(event["event"], event_name, repr(event))
        return event

    def start(self, child):
        child.send("start")
        self.expect(child, "attempting")

    def finish(self, child):
        while True:
            event = child.read_event()
            if event["event"] in ("result", "error"):
                break
            self.assertEqual(event["event"], "callback", repr(event))
        child.process.wait(timeout=10.0)
        self.assertEqual(child.process.returncode, 0)
        stderr = child.process.stderr.read().decode("utf-8", "replace")
        self.assertEqual(stderr, "")
        return event

    def test_schema_setup_and_availability(self):
        self.assertIsInstance(self.db, sqlite3.Connection)
        tables = {
            row[0] for row in self.db.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        self.assertEqual(tables, {"stock", "operations"})
        expected_columns = {
            "stock": [
                ("sku", "TEXT", 0, 1),
                ("quantity", "INTEGER", 1, 0),
            ],
            "operations": [
                ("operation_id", "TEXT", 0, 1),
                ("sku", "TEXT", 1, 0),
                ("quantity", "INTEGER", 1, 0),
                ("status", "TEXT", 1, 0),
            ],
        }
        for table, columns in expected_columns.items():
            rows = self.db.execute("PRAGMA table_info(" + table + ")")
            actual = [(r[1], r[2], r[3], r[5]) for r in rows]
            self.assertEqual(actual, columns)
        self.assertEqual(client.LABEL, "Availability")
        self.assertEqual(
            client.availability(self.db, "A"),
            {"sku": "A", "available": 5},
        )
        before = self.snapshot()
        with self.assertRaises(ValueError):
            client.availability(self.db, "missing")
        self.assertEqual(self.snapshot(), before)
        self.reopen()
        self.assertEqual(
            client.availability(self.db, "B"),
            {"sku": "B", "available": 4},
        )

    def test_invalid_inputs_do_not_mutate_or_call_callback(self):
        cases = []
        for operation_id in ("", None, 1, True, b"id", [], {}):
            cases.append((operation_id, "A", 1))
        for quantity in (True, False, 0, -1, 1.0, "1", None, [], {}):
            cases.append(("invalid", "A", quantity))
        for sku in ("missing", "", None, [], {}):
            cases.append(("invalid", sku, 1))
        before = self.snapshot()
        for args in cases:
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    inventory.reserve(
                        self.db, *args, before_commit=self.no_callback
                    )
                self.assertEqual(self.snapshot(), before)
                self.assertFalse(self.db.in_transaction)
        result = inventory.reserve(self.db, "valid-after-errors", "A", 1)
        self.assertEqual(
            result, self.expected("valid-after-errors", "A", 1, "reserved")
        )

    def test_reserved_result_persists_and_replays_after_reopen(self):
        # A whitespace-only ID is nonempty and therefore valid.
        first = inventory.reserve(self.db, " ", "A", 3)
        self.assertEqual(first, self.expected(" ", "A", 3, "reserved"))
        inventory.reserve(self.db, "consume-rest", "A", 2)
        self.assertEqual(
            client.availability(self.db, "A"),
            {"sku": "A", "available": 0},
        )
        before = self.snapshot()
        self.reopen()
        replay = inventory.reserve(
            self.db, " ", "A", 3, before_commit=self.no_callback
        )
        self.assertEqual(replay, first)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(self.db.in_transaction)
        self.assertIn((" ", "A", 3, "reserved"), before[1])

    def test_insufficient_result_persists_and_replays_after_reopen(self):
        first = inventory.reserve(self.db, "too-many", "A", 6)
        self.assertEqual(
            first, self.expected("too-many", "A", 6, "insufficient")
        )
        self.assertEqual(
            client.availability(self.db, "A"),
            {"sku": "A", "available": 5},
        )
        inventory.reserve(self.db, "later", "A", 1)
        before = self.snapshot()
        self.reopen()
        replay = inventory.reserve(
            self.db, "too-many", "A", 6, before_commit=self.no_callback
        )
        self.assertEqual(replay, first)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(self.db.in_transaction)
        self.assertIn(("too-many", "A", 6, "insufficient"), before[1])

    def test_operation_id_is_global_and_mismatch_is_nonmutating(self):
        inventory.reserve(self.db, "global", "A", 2)
        self.reopen()
        before = self.snapshot()
        for sku, quantity in (("B", 2), ("A", 1), ("missing", 2)):
            with self.subTest(sku=sku, quantity=quantity):
                with self.assertRaises(ValueError):
                    inventory.reserve(
                        self.db, "global", sku, quantity,
                        before_commit=self.no_callback,
                    )
                self.assertEqual(self.snapshot(), before)
                self.assertFalse(self.db.in_transaction)
        self.assertEqual(
            inventory.reserve(
                self.db, "global", "A", 2,
                before_commit=self.no_callback,
            ),
            self.expected("global", "A", 2, "reserved"),
        )

    def test_callback_sees_changes_before_commit_for_both_outcomes(self):
        observer = inventory.connect(self.path)
        self.addCleanup(observer.close)
        for operation_id, quantity, status in (
            ("callback-reserved", 2, "reserved"),
            ("callback-insufficient", 6, "insufficient"),
        ):
            with self.subTest(status=status):
                before = self.snapshot()
                old_quantity = client.availability(observer, "A")["available"]
                new_quantity = (
                    old_quantity - quantity
                    if status == "reserved" else old_quantity
                )
                calls = []

                def callback():
                    calls.append(True)
                    self.assertTrue(self.db.in_transaction)
                    row = self.db.execute(
                        "SELECT operation_id, sku, quantity, status "
                        "FROM operations WHERE operation_id = ?",
                        (operation_id,),
                    ).fetchone()
                    self.assertEqual(
                        row, (operation_id, "A", quantity, status)
                    )
                    self.assertEqual(
                        self.db.execute(
                            "SELECT quantity FROM stock WHERE sku = 'A'"
                        ).fetchone()[0],
                        new_quantity,
                    )
                    self.assertEqual(self.snapshot(observer), before)
                    self.assertEqual(
                        client.availability(observer, "A"),
                        {"sku": "A", "available": old_quantity},
                    )

                result = inventory.reserve(
                    self.db, operation_id, "A", quantity,
                    before_commit=callback,
                )
                self.assertEqual(
                    result, self.expected(operation_id, "A", quantity, status)
                )
                self.assertEqual(calls, [True])
                self.assertFalse(self.db.in_transaction)
                self.assertEqual(
                    client.availability(observer, "A"),
                    {"sku": "A", "available": new_quantity},
                )
                self.assertIn(
                    (operation_id, "A", quantity, status),
                    self.snapshot(observer)[1],
                )

    def test_callback_exception_rolls_back_both_outcomes_and_allows_retry(self):
        observer = inventory.connect(self.path)
        self.addCleanup(observer.close)
        for operation_id, quantity, status in (
            ("rollback-reserved", 2, "reserved"),
            ("rollback-insufficient", 6, "insufficient"),
        ):
            with self.subTest(status=status):
                before = self.snapshot()
                failure = RuntimeError("intentional callback failure")
                calls = []

                def callback():
                    calls.append(True)
                    self.assertTrue(self.db.in_transaction)
                    self.assertIsNotNone(self.db.execute(
                        "SELECT 1 FROM operations WHERE operation_id = ?",
                        (operation_id,),
                    ).fetchone())
                    self.assertEqual(self.snapshot(observer), before)
                    raise failure

                with self.assertRaises(RuntimeError) as caught:
                    inventory.reserve(
                        self.db, operation_id, "A", quantity,
                        before_commit=callback,
                    )
                self.assertIs(caught.exception, failure)
                self.assertEqual(calls, [True])
                self.assertFalse(self.db.in_transaction)
                self.assertEqual(self.snapshot(), before)
                self.assertEqual(self.snapshot(observer), before)
                self.reopen()
                self.assertEqual(self.snapshot(), before)
                self.assertEqual(
                    inventory.reserve(self.db, operation_id, "A", quantity),
                    self.expected(operation_id, "A", quantity, status),
                )

    def test_independent_process_contention_resolves_without_overdraw(self):
        first = self.spawn("first", "A", 5, hold=True)
        second = self.spawn("second", "A", 5)
        self.assertNotEqual(first.process.pid, second.process.pid)
        self.start(first)
        staged = self.expect(first, "callback")
        self.assertTrue(staged["in_transaction"])
        self.assertEqual(
            staged["operation"], ["first", "A", 5, "reserved"]
        )
        self.assertEqual(staged["stock"], 0)
        self.start(second)
        self.assertEqual(
            client.availability(self.db, "A"),
            {"sku": "A", "available": 5},
        )
        self.assertEqual(self.snapshot()[1], [])
        self.assertFalse(
            second.has_output(0.2),
            "Second operation completed while first outcome was uncommitted",
        )
        first.send("release")
        self.assertEqual(
            self.finish(first),
            {"event": "result",
             "result": self.expected("first", "A", 5, "reserved")},
        )
        self.assertEqual(
            self.finish(second),
            {"event": "result",
             "result": self.expected("second", "A", 5, "insufficient")},
        )
        self.assertEqual(
            client.availability(self.db, "A"),
            {"sku": "A", "available": 0},
        )
        self.assertEqual(self.snapshot()[1], [
            ("first", "A", 5, "reserved"),
            ("second", "A", 5, "insufficient"),
        ])

    def test_independent_process_same_id_replays_or_rejects_mismatch(self):
        for mismatch in (False, True):
            with self.subTest(mismatch=mismatch):
                operation_id = "same-id-" + str(mismatch)
                # Separate SKU for the second subcase avoids coupling its stock.
                first_sku = "B" if mismatch else "A"
                first_quantity = 2
                second_sku = "A" if mismatch else first_sku
                before = self.snapshot()
                first = self.spawn(
                    operation_id, first_sku, first_quantity, hold=True
                )
                second = self.spawn(
                    operation_id, second_sku, first_quantity
                )
                self.start(first)
                self.expect(first, "callback")
                self.start(second)
                self.assertFalse(second.has_output(0.2))
                first.send("release")
                first_result = self.finish(first)
                self.assertEqual(
                    first_result,
                    {"event": "result", "result": self.expected(
                        operation_id, first_sku, first_quantity, "reserved"
                    )},
                )
                second_result = self.finish(second)
                if mismatch:
                    self.assertEqual(second_result["event"], "error")
                    self.assertEqual(second_result["type"], "ValueError")
                else:
                    self.assertEqual(second_result, first_result)
                self.assertEqual(
                    [e for e in second.events if e["event"] == "callback"],
                    [],
                )
                old_stock = dict(before[0])
                old_stock[first_sku] -= first_quantity
                self.assertEqual(dict(self.snapshot()[0]), old_stock)
                self.assertEqual(
                    len(self.snapshot()[1]), len(before[1]) + 1
                )

    def test_independent_process_rollback_releases_waiting_reservation(self):
        first = self.spawn("will-rollback", "A", 5, hold=True, fail=True)
        second = self.spawn("after-rollback", "A", 5)
        self.start(first)
        self.expect(first, "callback")
        self.start(second)
        self.assertFalse(second.has_output(0.2))
        self.assertEqual(
            client.availability(self.db, "A"),
            {"sku": "A", "available": 5},
        )
        first.send("release")
        failure = self.finish(first)
        self.assertEqual(failure["event"], "error")
        self.assertEqual(failure["type"], "RuntimeError")
        self.assertEqual(
            self.finish(second),
            {"event": "result", "result": self.expected(
                "after-rollback", "A", 5, "reserved"
            )},
        )
        self.reopen()
        self.assertEqual(
            client.availability(self.db, "A"),
            {"sku": "A", "available": 0},
        )
        self.assertEqual(
            self.snapshot()[1],
            [("after-rollback", "A", 5, "reserved")],
        )
        self.assertEqual(
            inventory.reserve(self.db, "will-rollback", "A", 5),
            self.expected("will-rollback", "A", 5, "insufficient"),
        )

    def test_multiple_independent_processes_return_business_results(self):
        children = [
            self.spawn("race-" + str(index), "A", 2)
            for index in range(4)
        ]
        self.assertEqual(
            len({child.process.pid for child in children}), 4
        )
        for child in children:
            child.send("start")
        for child in children:
            self.expect(child, "attempting")
        results = []
        for index, child in enumerate(children):
            event = self.finish(child)
            self.assertEqual(event["event"], "result", repr(event))
            result = event["result"]
            self.assertIn(result["status"], ("reserved", "insufficient"))
            self.assertEqual(
                result,
                self.expected(
                    "race-" + str(index), "A", 2, result["status"]
                ),
            )
            results.append(result)
            self.assertEqual(
                len([e for e in child.events if e["event"] == "callback"]),
                1,
            )
        self.assertEqual(
            sum(r["status"] == "reserved" for r in results), 2
        )
        self.assertEqual(
            sum(r["status"] == "insufficient" for r in results), 2
        )
        self.reopen()
        self.assertEqual(
            client.availability(self.db, "A"),
            {"sku": "A", "available": 1},
        )
        self.assertEqual(len(self.snapshot()[1]), 4)
        before = self.snapshot()
        for result in results:
            self.assertEqual(
                inventory.reserve(
                    self.db,
                    result["operation_id"],
                    result["sku"],
                    result["quantity"],
                    before_commit=self.no_callback,
                ),
                result,
            )
        self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
