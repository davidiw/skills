#!/usr/bin/env python3
"""Reviewer-owned receipt acceptance. Usage: python3 receipt_acceptance.py REPO_ROOT"""
import copy
import hashlib
import json
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

ROOT = Path(sys.argv[1]).resolve()
SOURCE = ROOT / "evals/fixtures/review-run-b/receipts.py"
M = types.ModuleType("reviewed_receipts")
exec(compile(SOURCE.read_bytes(), str(SOURCE), "exec"), M.__dict__)
REPORT = Path("synthetic-report.jsonl")
BASE = [
    {"kind": "start", "run_id": "r", "expected": ["a", "optional_ui"]},
    {"kind": "result", "run_id": "r", "id": "a", "status": "pass"},
    {"kind": "result", "run_id": "r", "id": "optional_ui", "status": "skip"},
    {"kind": "done", "run_id": "r", "ok": True},
]
def encode(events, sep="\n", terminal=False):
    return (sep.join(json.dumps(e, ensure_ascii=False) for e in events)
            + (sep if terminal else "")).encode("utf-8")

def issued(raw, code=0, interrupted=False, snapshot="s1"):
    with patch.object(Path, "read_bytes", return_value=raw):
        return M.issue(REPORT, code, interrupted=interrupted, snapshot=snapshot)

def reused(receipt, raw, snapshot="s1"):
    with patch.object(Path, "read_bytes", return_value=raw):
        return M.reuse(receipt, REPORT, snapshot=snapshot)

VALID, INVALID = {}, {}
for sep_name, sep in [("lf", "\n"), ("crlf", "\r\n")]:
    for terminal in [False, True]:
        VALID[f"{sep_name}_{terminal}"] = encode(BASE, sep, terminal)
for char in ["\u0085", "\u2028", "\u2029"]:
    for location in ["run_id", "extra"]:
        ev = copy.deepcopy(BASE)
        if location == "run_id":
            for e in ev:
                e["run_id"] = "r" + char + "x"
        else:
            ev[1]["extra"] = {"text": "left" + char + "right"}
        VALID[f"unicode_{ord(char):x}_{location}"] = encode(ev, terminal=True)
ev = copy.deepcopy(BASE)
ev[2]["status"] = "pass"
VALID["optional_pass"] = encode(ev)
ev = copy.deepcopy(BASE)
ev[1]["extra"] = {"left": {"x": 1}, "right": {"x": 2}}
VALID["separate_objects_same_key"] = encode(ev)
GOOD = encode(BASE)
for name, index, field, value in [
    ("failed", 1, "status", "fail"), ("forbidden_skip", 1, "status", "skip"),
    ("wrong_run", 2, "run_id", "other"), ("not_done", 3, "kind", "result"),
    ("false_ok", 3, "ok", False), ("numeric_ok", 3, "ok", 1),
    ("empty_inventory", 0, "expected", []),
    ("string_inventory", 0, "expected", "a"),
    ("duplicate_inventory", 0, "expected", ["a", "a"]),
    ("nonstring_id", 0, "expected", [1]), ("empty_id", 0, "expected", [""]),
    ("empty_run", 0, "run_id", ""), ("unknown_result", 1, "id", "unknown"),
    ("nan", 1, "extra", float("nan")), ("inf", 1, "extra", float("inf")),
    ("negative_inf", 1, "extra", float("-inf")),
]:
    ev = copy.deepcopy(BASE); ev[index][field] = value
    INVALID[name] = encode(ev)
for name, events in [
    ("missing_done", BASE[:-1]), ("after_done", BASE + [BASE[1]]),
    ("duplicate_done", BASE + [BASE[-1]]),
    ("duplicate_result", BASE[:2] + [BASE[1]] + BASE[2:]),
    ("missing_result", BASE[:1] + BASE[2:]),
    ("missing_start", BASE[1:]), ("empty", []),
    ("nonobject", [None] + BASE[1:]),
]:
    INVALID[name] = encode(events)
INVALID.update(blank_record=GOOD + b"\n\n", leading_blank=b"\n" + GOOD,
               invalid_utf8=GOOD + b"\xff", bare_cr=encode(BASE, "\r"),
               extra_json=GOOD + b"{}", truncated=GOOD[:-1])
for char in ["\u0085", "\u2028", "\u2029"]:
    INVALID[f"not_record_separator_{ord(char):x}"] = encode(BASE, char)
for name, index, fragment in [
    ("kind", 0, '"kind":"ignored","kind":"start"'),
    ("run", 0, '"run_id":"other","run_id":"r"'),
    ("inventory", 0, '"expected":[],"expected":["a","optional_ui"]'),
    ("result_id", 1, '"id":"wrong","id":"a"'),
    ("status", 1, '"status":"fail","status":"pass"'),
    ("ok", 3, '"ok":false,"ok":true'),
    ("same_value", 3, '"ok":true,"ok":true'),
    ("escaped", 3, r'"o\u006b":false,"ok":true'),
    ("nested", 1, '"metadata":{"x":1,"x":2}'),
    ("nested_array", 1, r'"metadata":[{"x":1,"\u0078":2}]'),
]:
    lines = [json.dumps(e) for e in BASE]
    # Append duplicates after ordinary fields; the last-value parser otherwise accepts.
    lines[index] = lines[index][:-1] + "," + fragment + "}"
    INVALID["duplicate_" + name] = "\n".join(lines).encode()

class ReceiptAcceptance(unittest.TestCase):
    def test_execution_and_cache_boundaries(self):
        receipt = issued(GOOD)
        before = copy.deepcopy(receipt)
        for code, interrupted in [(1, False), (-1, False), (0, True)]:
            with self.subTest(code=code, interrupted=interrupted):
                with self.assertRaises(ValueError):
                    issued(GOOD, code, interrupted)
        self.assertFalse(reused(receipt, GOOD, "s2"))
        self.assertFalse(reused(receipt, GOOD + b"\n"))
        for changes in [{"status": "FAIL"}, {"digest": "wrong"}, {"snapshot": "s2"}]:
            self.assertFalse(reused(dict(receipt, **changes), GOOD))
        with patch.object(Path, "read_bytes", side_effect=FileNotFoundError):
            self.assertFalse(M.reuse(receipt, REPORT, snapshot="s1"))
        self.assertEqual(receipt, before)
        self.assertTrue(reused(receipt, GOOD))

def valid_check(raw):
    def check(self):
        receipt = issued(raw)
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["snapshot"], "s1")
        self.assertEqual(receipt["digest"], hashlib.sha256(raw).hexdigest())
        self.assertTrue(reused(receipt, raw))
    return check

def invalid_check(raw):
    def check(self):
        with self.assertRaises((ValueError, KeyError, TypeError, AttributeError)):
            issued(raw)
        # Matching bytes/digest must not bypass completion validation.
        forged = {"status": "PASS", "snapshot": "s1",
                  "digest": hashlib.sha256(raw).hexdigest()}
        self.assertFalse(reused(forged, raw))
        good_receipt = issued(GOOD)
        self.assertFalse(reused(good_receipt, raw))
        self.assertTrue(reused(good_receipt, GOOD))
    return check

for name, raw in VALID.items():
    setattr(ReceiptAcceptance, "test_valid_" + name, valid_check(raw))
for name, raw in INVALID.items():
    setattr(ReceiptAcceptance, "test_invalid_" + name, invalid_check(raw))
print("source_sha256=" + hashlib.sha256(SOURCE.read_bytes()).hexdigest())
print("valid_cases=%d invalid_cases=%d" % (len(VALID), len(INVALID)))
unittest.main(argv=[sys.argv[0]], verbosity=1)
