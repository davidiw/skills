from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/engineering-harness'
sys.path.insert(0, str(PLUGIN / 'scripts'))
from profile_repository import audit_methodology, propose_profile


class MethodologyAuditTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.profile = json.loads((PLUGIN / 'templates/project-profile.minimal.json').read_text())
        self.profile['sources'] = {}

    def write(self, path, text='Canonical repository policy\n'):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        return target

    def register(self, path='docs/performance_testing.md'):
        self.write(path)
        self.profile['sources']['my_policy'] = path
        self.profile['enforcement']['typed-exact-evidence'] = {
            'rung': 'local_check', 'owner': 'checks/qualify.py', 'artifacts': [path, 'checks/test_qualify.py']}
        self.write('checks/qualify.py', 'raise RuntimeError("audit must never execute policy commands")\n')
        self.write('checks/test_qualify.py')

    def test_pr3_circular_explicit_invocation_pointer_is_reported(self):
        self.write('AGENTS.md', 'Before `$using-engineering-harness` work, read engineering-harness.json.\n')
        self.profile['sources']['agent_rules'] = 'AGENTS.md'
        self.assertTrue(any('circular Harness trigger' in e for e in audit_methodology(self.root, self.profile)))
        self.write('AGENTS.md', 'For cross-cutting evidence/testing policy changes, consult the Engineering Harness and its accepted profile.\n')
        self.assertEqual(audit_methodology(self.root, self.profile), [])

    def test_pr9_policy_missing_from_profile_is_not_invisible(self):
        self.write('docs/performance_testing.md')
        self.assertTrue(any('unregistered methodology' in e for e in audit_methodology(self.root, self.profile)))
        self.assertEqual(propose_profile(self.root)['sources']['performance_evidence'], 'docs/performance_testing.md')

    def test_registration_is_independent_of_key_name_and_does_not_execute(self):
        self.register()
        self.assertEqual(audit_methodology(self.root, self.profile), [])

    def test_registering_only_the_document_does_not_name_enforcement(self):
        self.write('docs/performance_testing.md')
        self.profile['sources']['performance_evidence'] = 'docs/performance_testing.md'
        self.assertTrue(any('lacks an enforcement owner/rung' in e for e in audit_methodology(self.root, self.profile)))

    def test_missing_check_and_owner_are_reported(self):
        for path in ['checks/qualify.py', 'checks/test_qualify.py']:
            with self.subTest(path=path):
                self.register()
                (self.root / path).unlink()
                self.assertTrue(any('missing' in e for e in audit_methodology(self.root, self.profile)))

    def test_custom_policy_can_be_explicitly_audited_without_a_new_schema(self):
        self.write('spec/host-admission.md')
        self.assertEqual(audit_methodology(self.root, self.profile), [])
        self.assertTrue(audit_methodology(self.root, self.profile, ['spec/host-admission.md']))
        self.register('spec/host-admission.md')
        self.assertEqual(audit_methodology(self.root, self.profile, ['spec/host-admission.md']), [])

    def test_ordinary_test_files_do_not_trigger_registration_work(self):
        self.write('tests/test_parser.py')
        self.assertEqual(audit_methodology(self.root, self.profile), [])

    def test_policy_path_cannot_escape_via_absolute_traversal_or_symlink(self):
        with tempfile.TemporaryDirectory() as outside:
            secret = Path(outside) / 'policy.md'; secret.write_text('outside')
            (self.root / 'linked.md').symlink_to(secret)
            for path in [str(secret), '../policy.md', 'linked.md']:
                with self.subTest(path=path):
                    self.assertTrue(any('escaping' in e for e in audit_methodology(self.root, self.profile, [path])))

    def test_cli_returns_failure_for_gap_and_success_for_registered_policy(self):
        self.write('docs/performance_testing.md')
        profile = self.root / 'engineering-harness.json'
        def run():
            profile.write_text(json.dumps(self.profile))
            return subprocess.run([sys.executable, str(PLUGIN/'scripts/profile_repository.py'), str(self.root),
                                   '--audit-methodology', str(profile)], text=True, capture_output=True)
        self.assertEqual(run().returncode, 1)
        self.register()
        result = run()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['findings'], [])

    def test_invalid_profile_is_rejected_before_audit(self):
        self.assertTrue(audit_methodology(self.root, {'sources': []}))

class MethodologyCorpusTest(unittest.TestCase):
    def test_regressions_cannot_be_deleted_or_made_explicit(self):
        sys.path.insert(0, str(ROOT/'scripts'))
        from validate_package import validate_methodology_matrix
        matrix = json.loads((ROOT/'evals/methodology-matrix.json').read_text())
        cases = {c['id']: c for c in json.loads((ROOT/'evals/cases.json').read_text())['cases']}
        errors = []
        validate_methodology_matrix(matrix, cases, errors)
        self.assertEqual(errors, [])
        for case_id in matrix['case_ids']:
            modified = copy.deepcopy(matrix);modified['case_ids'].remove(case_id)
            errors = [];validate_methodology_matrix(modified, cases, errors)
            self.assertTrue(errors)
        cases['methodology-trigger']['request'] = 'Use verification-and-operations.'
        errors = [];validate_methodology_matrix(matrix, cases, errors)
        self.assertTrue(errors)

    def test_synthetic_qualification_is_policy_driven(self):
        for name in ['methodology-single-pair', 'methodology-qualified']:
            root=ROOT/'evals/fixtures'/name
            result=subprocess.run([sys.executable,'-m','unittest','test_qualify.py'],cwd=root,text=True,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            result=subprocess.run([sys.executable,'qualify.py'],cwd=root,text=True,capture_output=True)
            expected='pending' if name.endswith('single-pair') else 'accepted'
            self.assertEqual(json.loads(result.stdout)['qualification'],expected)


if __name__ == '__main__':
    unittest.main()
