import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_package import PLUGIN_ROOT, validate_runtime_boundary


class RuntimePackageTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.plugin = self.root / "engineering-harness"
        shutil.copytree(PLUGIN_ROOT, self.plugin, ignore=shutil.ignore_patterns("__pycache__"))

    def test_isolated_runtime_has_all_links_and_runs_adoption_helpers(self):
        errors = []
        validate_runtime_boundary(self.plugin, errors)
        self.assertEqual(errors, [])
        target = self.root / "target"
        target.mkdir()
        (target / "main.py").write_text("print('hello')\n")
        result = subprocess.run([sys.executable, "-B", str(self.plugin / "scripts/profile_repository.py"), str(target)],
                                cwd=self.root, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        profile = target / "engineering-harness.json"
        profile.write_text(result.stdout)
        self.assertEqual(json.loads(result.stdout)["status"], "proposed")
        checked = subprocess.run([sys.executable, "-B", str(self.plugin / "scripts/validate_profile.py"), str(profile)],
                                 cwd=self.root, text=True, capture_output=True)
        self.assertEqual(checked.returncode, 0, checked.stderr)

    def test_corpus_is_rejected_even_nested_in_runtime_references(self):
        leak = self.plugin / "references/evals/cases.json"
        leak.parent.mkdir()
        leak.write_text('{"expected_outcomes": ["answer"]}')
        errors = []
        validate_runtime_boundary(self.plugin, errors)
        self.assertTrue(any("development corpus" in error for error in errors), errors)

    def test_links_and_symlinks_cannot_escape_to_repository_evidence(self):
        outside = self.root / "answers.md"
        outside.write_text("expected outcomes")
        (self.plugin / "references/leak.md").write_text("[answers](../../answers.md)")
        (self.plugin / "references/alias.md").symlink_to(outside)
        errors = []
        validate_runtime_boundary(self.plugin, errors)
        self.assertTrue(any("external file link" in error for error in errors), errors)
        self.assertTrue(any("symlink" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
