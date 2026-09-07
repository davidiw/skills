import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "engineering-harness"
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts"))
from validate_package import validate_assurance_matrix


class AssuranceMatrixTest(unittest.TestCase):
    def setUp(self):
        self.matrix = json.loads((ROOT / "evals/assurance-matrix.json").read_text())
        self.cases = {case["id"]: case for case in
                      json.loads((ROOT / "evals/cases.json").read_text())["cases"]}

    def test_complete_matrix_is_valid(self):
        errors = []
        validate_assurance_matrix(self.matrix, self.cases, errors)
        self.assertEqual(errors, [])

    def test_missing_restraint_coverage_cannot_pass(self):
        self.matrix["case_ids"].remove("ui-fence-restraint")
        errors = []
        validate_assurance_matrix(self.matrix, self.cases, errors)
        self.assertIn("assurance matrix: missing discovery, restraint, release, or scope coverage", errors)

    def test_each_scope_regression_is_required(self):
        for case_id in ("temporary-account-oauth-scope", "approved-provider-broker-design"):
            with self.subTest(case_id=case_id):
                matrix = copy.deepcopy(self.matrix)
                matrix["case_ids"].remove(case_id)
                errors = []
                validate_assurance_matrix(matrix, self.cases, errors)
                self.assertIn("assurance matrix: missing discovery, restraint, release, or scope coverage", errors)

    def test_single_trial_or_missing_control_is_rejected(self):
        for field, value in (("trials", 1), ("conditions", ["harness"]), ("concurrency", 3)):
            matrix = copy.deepcopy(self.matrix)
            matrix[field] = value
            errors = []
            validate_assurance_matrix(matrix, self.cases, errors)
            self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
