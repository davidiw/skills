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

    def test_lf_records_preserve_unicode_and_accept_crlf(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"report.jsonl"
            events=[{"kind":"start","run_id":"r\u2028x","expected":["a"]},
                    {"kind":"result","run_id":"r\u2028x","id":"a","status":"pass",
                     "metadata":{"text":"left\u0085right\u2029"}},
                    {"kind":"done","run_id":"r\u2028x","ok":True}]
            p.write_bytes("\r\n".join(json.dumps(e,ensure_ascii=False) for e in events).encode()+b"\r\n")
            self.assertTrue(reuse(issue(p,0),p))

    def test_duplicate_members_and_non_lf_delimiters_are_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"report.jsonl"
            duplicate=(b'{"kind":"start","run_id":"r","expected":["a"]}\n'
                       b'{"kind":"result","run_id":"r","id":"a","status":"pass",'
                       b'"metadata":{"x":1,"\\u0078":2}}\n'
                       b'{"kind":"done","run_id":"r","ok":true}')
            for raw in (duplicate,
                        b'{"kind":"start","run_id":"r","expected":["a"]}\r'
                        b'{"kind":"result","run_id":"r","id":"a","status":"pass"}\r'
                        b'{"kind":"done","run_id":"r","ok":true}'):
                p.write_bytes(raw)
                with self.subTest(raw=raw[:20]):
                    with self.assertRaises(ValueError):
                        issue(p,0)
