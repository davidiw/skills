#!/usr/bin/env python3
"""Reviewer addendum: python3 reservation_hook_acceptance.py FROZEN_TASK_ROOT"""
import hashlib
import importlib
from pathlib import Path
import sqlite3
import sys
import unittest

sys.dont_write_bytecode = True
ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT))
inventory = importlib.import_module("inventory")
SOURCE = Path(inventory.__file__).resolve()
if SOURCE != ROOT / "inventory.py":
    raise RuntimeError("inventory resolved outside supplied root")
SOURCE_HASH = hashlib.sha256(SOURCE.read_bytes()).hexdigest()

class HookRollbackAcceptance(unittest.TestCase):
    def check_hook(self, quantity):
        db = inventory.connect(":memory:")
        try:
            inventory.initialize(db, "a", 5)
            calls = []
            def once():
                calls.append(1)
                if len(calls) == 1:
                    raise sqlite3.OperationalError("database is locked")
            with self.assertRaises(sqlite3.OperationalError):
                inventory.reserve(db, "hook", "a", quantity, before_commit=once)
            self.assertEqual(
                [tuple(r) for r in db.execute("SELECT sku,quantity FROM stock")],
                [("a", 5)])
            self.assertEqual(list(db.execute("SELECT * FROM operations")), [])
        finally:
            db.close()

    def test_reserved_hook_failure_cannot_be_retried_into_success(self):
        self.check_hook(2)

    def test_insufficient_hook_failure_cannot_be_retried_into_success(self):
        self.check_hook(9)

suite = unittest.defaultTestLoader.loadTestsFromTestCase(HookRollbackAcceptance)
outcome = unittest.TextTestRunner(verbosity=2).run(suite)
unchanged = hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_HASH
print("source_sha256=" + SOURCE_HASH)
print("source_unchanged=" + str(unchanged))
sys.exit(0 if outcome.wasSuccessful() and outcome.testsRun == 2
         and not outcome.skipped and unchanged else 1)
