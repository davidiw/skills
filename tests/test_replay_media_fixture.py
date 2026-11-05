from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "evals/fixtures/replay-media-reuse"

# This oracle is outside the fixture offered to the evaluated agent. It applies a
# reference repair in a disposable copy to establish that the scenario is solvable.
REPAIRED_VERIFY = '''def verify(reference, record, pose, features, events, media_bytes):
    evidence = record["evidence"]
    return (reference == digest(evidence)
            and evidence["pose_hash"] == digest(pose)
            and evidence["features_hash"] == digest(features)
            and evidence["events_hash"] == digest(events)
            and evidence["media_sha256"] == sha256(media_bytes).hexdigest())
'''
PROBE = '''from pathlib import Path
from unittest.mock import patch
from capture import capture, revise, verify
from reuse import replay
import copy
p = Path("sample.txt")
p.write_bytes(b"original")
r = capture({"x":1}, [2], ["event"], p, {"p":1}, "prod", "build", "model", {"c":1}, "rubric", "label", 1, {"score":1})
ref = r["reference"]
evidence = copy.deepcopy(r["evidence"])
with patch.object(Path, "read_bytes", wraps=p.read_bytes) as read:
    assert replay(ref, r, {"x":1}, [2], ["event"]) == b"original"
    assert read.call_count == 1
for pose, features, events in [({"x":2}, [2], ["event"]), ({"x":1}, [3], ["event"]), ({"x":1}, [2], ["other"])]:
    assert not verify(ref, r, pose, features, events, b"original")
changed = copy.deepcopy(r); changed["evidence"]["model"] = "other"
assert not verify(ref, changed, {"x":1}, [2], ["event"], b"original")
revise(r, "new", 2, {"score":3})
assert r["reference"] == ref and r["evidence"] == evidence
assert replay(ref, r, {"x":1}, [2], ["event"]) == b"original"
p.write_bytes(b"changed")
try: replay(ref, r, {"x":1}, [2], ["event"])
except ValueError: pass
else: raise AssertionError("changed media accepted")
assert r["reference"] == ref and r["evidence"] == evidence
p.unlink()
try: replay(ref, r, {"x":1}, [2], ["event"])
except FileNotFoundError: pass
else: raise AssertionError("missing media accepted")
'''


class ReplayMediaFixtureTest(unittest.TestCase):
    def test_broken_fixture_and_reference_repair(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "fixture"
            shutil.copytree(FIXTURE, dest, ignore=shutil.ignore_patterns("__pycache__"))
            initial = subprocess.run([sys.executable, "-m", "unittest", "-v", "test_reuse"],
                                     cwd=dest, capture_output=True, text=True)
            self.assertNotEqual(initial.returncode, 0)
            self.assertIn("ValueError not raised", initial.stderr)
            capture = dest / "capture.py"
            text = capture.read_text()
            capture.write_text(text[:text.index("def verify(")] + REPAIRED_VERIFY)
            reuse = dest / "reuse.py"
            reuse.write_text(reuse.read_text().replace('return Path(record["media_path"]).read_bytes()',
                                                       'return media_bytes'))
            repaired = subprocess.run([sys.executable, "-m", "unittest", "-v", "test_reuse"],
                                      cwd=dest, capture_output=True, text=True)
            self.assertEqual(repaired.returncode, 0, repaired.stderr)
            probe = subprocess.run([sys.executable, "-c", PROBE], cwd=dest,
                                   capture_output=True, text=True)
            self.assertEqual(probe.returncode, 0, probe.stderr)


if __name__ == "__main__":
    unittest.main()
