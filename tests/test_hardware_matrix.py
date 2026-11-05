from __future__ import annotations

import copy
import csv
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_package import validate_hardware_matrix


class HardwareMatrixTest(unittest.TestCase):
    def setUp(self):
        self.matrix = json.loads((ROOT / "evals/hardware-matrix.json").read_text())
        self.cases = {case["id"]: case for case in json.loads((ROOT / "evals/cases.json").read_text())["cases"]}

    def errors(self, matrix=None, cases=None):
        errors = []
        validate_hardware_matrix(matrix if matrix is not None else self.matrix,
                                 cases if cases is not None else self.cases, errors)
        return errors

    def test_matrix_and_invalid_mutations(self):
        self.assertEqual(self.errors(), [])
        for mutation in (lambda m: m["case_ids"].pop(),
                         lambda m: m["case_ids"].append("unknown"),
                         lambda m: m.update(command_boundary=None),
                         lambda m: m.update(trials=0)):
            matrix = copy.deepcopy(self.matrix)
            mutation(matrix)
            self.assertTrue(self.errors(matrix))
        cases = copy.deepcopy(self.cases)
        cases["hardware-narrow-cpl"]["control"] = "positive"
        self.assertTrue(self.errors(cases=cases))
        cases = copy.deepcopy(self.cases)
        cases["hardware-rotation"]["fixture"] = "../outside"
        self.assertTrue(self.errors(cases=cases))

    def test_release_fixture_reproduces_and_fixed_checker_detects_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "release"
            shutil.copytree(ROOT / "evals/fixtures/hardware-release", dest)
            def run():
                return subprocess.run([sys.executable, "release_check.py"], cwd=dest).returncode
            self.assertEqual(run(), 0)  # Demonstrates the existing false success.
            checker = dest / "release_check.py"
            checker.write_text(checker.read_text().replace('    for path in designs:',
                                                          '    if not designs:\n        return False\n    for path in designs:'))
            self.assertNotEqual(run(), 0)
            (dest / "designs/example").mkdir()
            (dest / "designs/example/manifest.json").write_text('{"name":"example"}')
            self.assertEqual(run(), 0)

    def test_board_fixture_reproduces_and_fixes_rotation_and_job(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "board"
            shutil.copytree(ROOT / "evals/fixtures/hardware-board", dest)
            def check():
                return subprocess.run([sys.executable, "check_board.py"], cwd=dest, capture_output=True, text=True)
            before = check()
            self.assertNotEqual(before.returncode, 0)
            self.assertIn("rotation must be 180", before.stdout)
            self.assertIn("job minimum via drill exceeds design", before.stdout)
            generator = dest / "generate_cpl.py"
            generator.write_text(generator.read_text().replace('c["footprint_rotation"]])',
                '(c["footprint_rotation"] + c["pad1_offset"]) % 360])'))
            subprocess.run([sys.executable, "generate_cpl.py"], cwd=dest, check=True)
            with (dest / "cpl.csv").open() as stream:
                self.assertEqual(next(csv.DictReader(stream))["rotation"], "180")
            self.assertNotEqual(check().returncode, 0)
            settings = json.loads((dest / "job-settings.json").read_text())
            settings["min_via_drill_mm"] = 0.25
            (dest / "job-settings.json").write_text(json.dumps(settings))
            self.assertEqual(check().returncode, 0)


if __name__ == "__main__":
    unittest.main()
