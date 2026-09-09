from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import validate_package


def module(relative):
    spec = importlib.util.spec_from_file_location('fixture', ROOT / 'evals/fixtures' / relative)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class MethodReconciliationTest(unittest.TestCase):
    def test_second_implicit_workflow_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            plugin = Path(directory) / 'plugin'
            shutil.copytree(ROOT / 'plugins/engineering-harness', plugin)
            with patch.object(validate_package, 'PLUGIN_ROOT', plugin):
                errors = []
                validate_package.validate_skills(errors)
                self.assertEqual(errors, [])
                path = plugin / 'skills/architecture-foundations/agents/openai.yaml'
                path.write_text(path.read_text().replace('allow_implicit_invocation: false',
                                                        'allow_implicit_invocation: true'))
                validate_package.validate_skills(errors)
                self.assertTrue(any('invocation policy mismatch' in e for e in errors))

    def test_authoring_policy_registration_cannot_be_removed_silently(self):
        from profile_repository import audit_methodology
        profile = json.loads((ROOT / 'engineering-harness.json').read_text())
        self.assertEqual(audit_methodology(ROOT, profile), [])
        path = profile['sources']['skill_authoring_policy']
        altered = copy.deepcopy(profile)
        altered['enforcement']['typed-exact-evidence']['artifacts'].remove(path)
        self.assertTrue(any('lacks an enforcement owner/rung' in e
                            for e in audit_methodology(ROOT, altered)))

    def test_focused_cohort_preserves_methods_and_minimal_control(self):
        matrix = json.loads((ROOT / 'evals/method-reconciliation-matrix.json').read_text())
        self.assertEqual(set(matrix['case_ids']), {'methods-diagnosis', 'methods-domain',
                                                 'methods-review', 'methodology-restraint'})
        self.assertEqual(matrix['conditions'], ['control', 'harness'])
        self.assertIs(type(matrix['trials']), int)
        self.assertGreater(matrix['trials'], 0)
        self.assertEqual(matrix['prompt_mode'], 'natural')
        self.assertEqual(matrix['command_boundary'], 'offline-browser')

    def test_diagnosis_fixture_distinguishes_lists_from_single_use_input(self):
        preview = module('methods-diagnosis/preview.py').preview
        expected = {'count': 2, 'total': 10}
        self.assertEqual(preview(['7', '3']), expected)
        self.assertNotEqual(preview(iter(['7', '3'])), expected)

    def test_review_fixture_has_three_independently_reachable_contract_defects(self):
        apply = module('methods-review/promo.py').apply
        self.assertEqual(apply(100, 'SAVE10'), 90)
        self.assertNotEqual(apply(10, 'SAVE10'), 10)
        self.assertNotEqual(apply(100, 'save10'), 100)
        self.assertNotEqual(apply(12.345, 'OTHER'), round(12.345, 2))

    def test_retained_receipt_exports_unique_context_ids(self):
        receipt = json.loads((ROOT / 'evals/results/method-reconciliation/receipt.json').read_text())
        for run in receipt['runs']:
            contexts = [c for t in run['trials'] for c in t['contexts']]
            self.assertEqual(len({c['id'] for c in contexts}), len(contexts))
            self.assertTrue(all('recorded_id' in c for c in contexts))
        review = next(t for t in receipt['runs'][0]['trials']
                      if t['case_id'] == 'methods-review' and t['arm'] == 'control')
        self.assertEqual(len(review['contexts']), 3)
        self.assertEqual(len({c['recorded_id'] for c in review['contexts']}), 1)

    def test_domain_fixture_has_distinct_existing_facts(self):
        participating = module('methods-domain/participation.py').participating
        has_access = module('methods-domain/access.py').has_access
        member = {'participation': 'paused', 'paid_through': 10}
        self.assertFalse(participating(member))
        self.assertTrue(has_access(member, 5))
        self.assertFalse(has_access(member, 10))
