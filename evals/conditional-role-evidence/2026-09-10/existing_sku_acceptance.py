import hashlib
from pathlib import Path
import sys
import types
import unittest

ROOT = Path(sys.argv[1]).resolve()
SOURCE = ROOT / "inventory.py"
raw = SOURCE.read_bytes()
inventory = types.ModuleType("reviewed_inventory")
exec(compile(raw, str(SOURCE), "exec"), inventory.__dict__)

class ExistingSkuAcceptance(unittest.TestCase):
    def test_existing_empty_text_sku_is_accepted(self):
        db = inventory.connect(":memory:")
        try:
            inventory.initialize(db, "", 3)
            self.assertEqual(
                inventory.reserve(db, "blank-sku", "", 1),
                {"operation_id": "blank-sku", "sku": "",
                 "quantity": 1, "status": "reserved"})
            self.assertEqual(
                db.execute(
                    "SELECT quantity FROM stock WHERE sku = ''"
                ).fetchone()[0],
                2)
        finally:
            db.close()

print("source_sha256=" + hashlib.sha256(raw).hexdigest())
unittest.main(argv=[sys.argv[0]], verbosity=2)
