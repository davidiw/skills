from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_package import validate_experience_matrix


class ExperiencePilotTest(unittest.TestCase):
    def setUp(self):
        self.matrix = json.loads((ROOT / 'evals/experience-matrix.json').read_text())
        self.cases = {c['id']: c for c in json.loads((ROOT / 'evals/cases.json').read_text())['cases']}

    def errors(self, matrix=None, cases=None):
        errors = []
        validate_experience_matrix(matrix or self.matrix, cases or self.cases, errors)
        return errors

    def test_unrestricted_network_or_missing_boundary_fails(self):
        for change in [{'sandbox_network_access': True}, {'command_boundary': None}]:
            matrix = {**self.matrix, **change}
            self.assertTrue(any('command boundary' in e for e in self.errors(matrix)))

    def test_pilot_is_valid(self):
        self.assertEqual(self.errors(), [])

    def test_brand_and_unavailable_rendering_cannot_be_replaced(self):
        for case_id in ['experience-brand', 'experience-no-render']:
            with self.subTest(case_id=case_id):
                matrix = copy.deepcopy(self.matrix)
                matrix['case_ids'][matrix['case_ids'].index(case_id)] = 'authorization-export'
                self.assertTrue(any('required' in e for e in self.errors(matrix)))

    def test_restraint_coverage_cannot_be_replaced(self):
        matrix = copy.deepcopy(self.matrix)
        matrix['case_ids'][matrix['case_ids'].index('experience-typo')] = 'authorization-export'
        self.assertTrue(any('four restraint' in e for e in self.errors(matrix)))

    def test_brand_is_not_reduced_to_interface_only(self):
        cases = copy.deepcopy(self.cases)
        cases['experience-brand']['expected_skills'] = ['using-engineering-harness', 'interface-design']
        self.assertTrue(any('brand-and-language' in e for e in self.errors(cases=cases)))

    def test_duplicate_unknown_or_explicit_prompts_fail(self):
        matrix = copy.deepcopy(self.matrix)
        matrix['case_ids'][-1] = matrix['case_ids'][0]
        self.assertTrue(self.errors(matrix))
        matrix['case_ids'][-1] = 'missing-case'
        self.assertTrue(any('unknown' in e for e in self.errors(matrix)))
        cases = copy.deepcopy(self.cases)
        cases['experience-brand']['request'] = 'Use $brand-and-language.'
        self.assertTrue(any('names a skill' in e for e in self.errors(cases=cases)))


if __name__ == '__main__':
    unittest.main()
