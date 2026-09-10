import unittest,tempfile,json
from pathlib import Path
from receipts import issue,reuse
class ReceiptTest(unittest.TestCase):
    def test_complete(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"report.jsonl"
            events=[{"kind":"start","run_id":"r","expected":["a"]},{"kind":"result","run_id":"r","id":"a","status":"pass"},{"kind":"done","run_id":"r","ok":True}]
            p.write_text("\n".join(json.dumps(e) for e in events))
            self.assertTrue(reuse(issue(p,0),p))
