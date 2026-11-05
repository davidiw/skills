from pathlib import Path
import tempfile
import unittest
from capture import capture, revise
from reuse import replay


class ReplayTest(unittest.TestCase):
    def test_intact_and_changed_file_at_same_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "media.txt"
            original = Path("testdata.txt").read_bytes()
            path.write_bytes(original)
            record = capture({"x": 1}, [2], ["event"], path, {"p": 1},
                             "producer", "build", "model", {"c": 1},
                             "rubric", "label", 1, {"score": 1})
            ref = record["reference"]
            self.assertEqual(replay(ref, record, {"x": 1}, [2], ["event"]), original)
            revise(record, "new", 2, {"score": 3})
            self.assertEqual(record["reference"], ref)
            self.assertEqual(replay(ref, record, {"x": 1}, [2], ["event"]), original)
            path.write_bytes(b"different media at the same path")
            with self.assertRaises(ValueError):
                replay(ref, record, {"x": 1}, [2], ["event"])


if __name__ == "__main__":
    unittest.main()
