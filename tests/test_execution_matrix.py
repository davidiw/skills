from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_package import validate_execution_matrix


class ExecutionMatrixTest(unittest.TestCase):
    def setUp(self):
        self.matrix = json.loads((ROOT / "evals/execution-matrix.json").read_text())
        self.cases = {case["id"]: case for case in json.loads((ROOT / "evals/cases.json").read_text())["cases"]}

    def errors(self, matrix=None, cases=None):
        errors = []
        validate_execution_matrix(matrix or self.matrix, cases or self.cases, errors)
        return errors

    def test_candidate_matrix_is_valid(self):
        self.assertEqual(self.errors(), [])

    def test_required_a_to_e_cases_cannot_be_removed(self):
        for case_id in self.matrix["case_ids"]:
            with self.subTest(case_id=case_id):
                matrix = copy.deepcopy(self.matrix)
                matrix["case_ids"].remove(case_id)
                self.assertTrue(self.errors(matrix))

    def test_unknown_or_named_skill_prompt_fails(self):
        matrix = copy.deepcopy(self.matrix)
        matrix["case_ids"][-1] = "missing-case"
        self.assertTrue(self.errors(matrix))
        for request in ["Use verification-and-operations.", "Use $verification-and-operations."]:
            with self.subTest(request=request):
                cases = copy.deepcopy(self.cases)
                cases["execution-decomposable-batch"]["request"] = request
                self.assertTrue(self.errors(cases=cases))

    def test_missing_protected_boundary_fails(self):
        for change in [{"command_boundary": None}, {"sandbox_network_access": True}]:
            with self.subTest(change=change):
                self.assertTrue(self.errors({**self.matrix, **change}))

    def test_matrix_cannot_declare_runner_concurrency(self):
        self.assertTrue(self.errors({**self.matrix, "concurrency": 2}))


if __name__ == "__main__":
    unittest.main()
