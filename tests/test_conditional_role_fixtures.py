"""Evaluator-owned checks for the frozen conditional-role fixtures."""
import importlib.util
import multiprocessing
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "evals" / "fixtures" / "role-reservation"
REFERENCE = ROOT / "evals" / "conditional-role-reference"


def module(name, root=FIXTURE, filename=None):
    spec = importlib.util.spec_from_file_location(name, root / ((filename or name) + ".py"))
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def reserve_in_process(source, path, operation_id, start, results):
    sys.path.insert(0, source)
    import inventory
    db = inventory.connect(path)
    try:
        start.wait(5)
        results.put(inventory.reserve(db, operation_id, "sku", 1))
    finally:
        db.close()


class ConditionalRoleFixtures(unittest.TestCase):
    def test_initial_fixture_fails_while_reference_preserves_retries(self):
        initial, reference = module("inventory"), module("reference", REFERENCE, "inventory")
        for implementation, expected in ((initial, 0), (reference, 1)):
            with tempfile.TemporaryDirectory() as directory:
                db = implementation.connect(Path(directory) / "stock.db")
                try:
                    implementation.initialize(db, "sku", 2)
                    implementation.reserve(db, "one", "sku", 1)
                    implementation.reserve(db, "one", "sku", 1)
                    self.assertEqual(db.execute("SELECT quantity FROM stock WHERE sku = 'sku'").fetchone()[0], expected)
                finally:
                    db.close()

    def test_reference_distinct_processes_do_not_overdraw_and_retry_persists(self):
        inventory, client = module("reference", REFERENCE, "inventory"), module("client")
        context = multiprocessing.get_context("spawn")
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "stock.db")
            db = inventory.connect(path)
            try:
                inventory.initialize(db, "sku", 1)
            finally:
                db.close()
            start, results = context.Event(), context.Queue()
            processes = [context.Process(target=reserve_in_process,
                                         args=(str(REFERENCE), path, operation, start, results))
                         for operation in ("first", "second")]
            for process in processes:
                process.start()
            start.set()
            for process in processes:
                process.join(10)
                self.assertEqual(process.exitcode, 0)
            observed = [results.get(timeout=2) for _ in processes]
            self.assertEqual(sorted(result["status"] for result in observed), ["insufficient", "reserved"])
            successful = next(result for result in observed if result["status"] == "reserved")
            db = inventory.connect(path)
            try:
                self.assertEqual(client.availability(db, "sku"), {"sku": "sku", "available": 0})
                self.assertEqual(inventory.reserve(db, successful["operation_id"], "sku", 1), successful)
            finally:
                db.close()

    def test_reference_retry_rejection_and_rollback(self):
        inventory, client = module("reference", REFERENCE, "inventory"), module("client")
        with tempfile.TemporaryDirectory() as directory:
            db = inventory.connect(Path(directory) / "stock.db")
            try:
                inventory.initialize(db, "sku", 2)
                result = inventory.reserve(db, "one", "sku", 1)
                self.assertEqual(result, {"operation_id": "one", "sku": "sku", "quantity": 1, "status": "reserved"})
                self.assertEqual(inventory.reserve(db, "one", "sku", 1), result)
                self.assertEqual(client.availability(db, "sku"), {"sku": "sku", "available": 1})
                with self.assertRaises(ValueError):
                    inventory.reserve(db, "one", "sku", 2)
                with self.assertRaises(RuntimeError):
                    inventory.reserve(db, "two", "sku", 1, before_commit=lambda: (_ for _ in ()).throw(RuntimeError()))
                self.assertEqual(client.availability(db, "sku"), {"sku": "sku", "available": 1})
            finally:
                db.close()

    def test_minimal_fixture_remains_local(self):
        path = ROOT / "evals" / "fixtures" / "role-minimal" / "client.py"
        namespace = {}
        exec(path.read_text(), namespace)
        self.assertEqual(namespace["LABEL"], "Availabilty")
        self.assertEqual(namespace["availability"](3), {"available": 3})
