import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_package import PLUGIN_ROOT, manifest_at_revision, validate_repository_layout, validate_runtime_boundary


class RepositoryLayoutTest(unittest.TestCase):
    def test_each_legacy_policy_root_is_rejected(self):
        for name in (".codex-plugin", "skills", "references", "templates"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                legacy = root / name
                legacy.mkdir()
                (legacy / "duplicate.md").write_text("competing policy")
                errors = []
                validate_repository_layout(root, errors)
                self.assertEqual(len(errors), 1)
                self.assertIn(f"legacy policy root {name} is forbidden", errors[0])

    def test_repository_scripts_and_nested_runtime_policy_are_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            (root / "scripts/generator.py").write_text("print('generated')\n")
            for name in (".codex-plugin", "skills", "references", "templates"):
                (root / "plugins/engineering-harness" / name).mkdir(parents=True)
            errors = []
            validate_repository_layout(root, errors)
            self.assertEqual(errors, [])

    def test_dangling_legacy_alias_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "skills").symlink_to(root / "missing-policy", target_is_directory=True)
            errors = []
            validate_repository_layout(root, errors)
            self.assertEqual(len(errors), 1)
            self.assertIn("legacy policy root skills is forbidden", errors[0])


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

    def test_historical_and_relocated_manifests_remain_readable(self):
        for revision in ("3eb0314e26a47397e03169c4d07facf7d19d12ee",
                         "4cbed8215ac195b892845efd146b15d57a36d7e2"):
            with self.subTest(revision=revision):
                manifest = json.loads(manifest_at_revision(revision))
                self.assertEqual(manifest["name"], "engineering-harness")
                self.assertEqual(manifest["version"], "0.5.0")

    def test_corpus_is_rejected_even_nested_in_runtime_references(self):
        leak = self.plugin / "references/evals/cases.json"
        leak.parent.mkdir()
        leak.write_text('{"expected_outcomes": ["answer"]}')
        errors = []
        validate_runtime_boundary(self.plugin, errors)
        self.assertTrue(any("development corpus" in error for error in errors), errors)

    def test_reference_links_and_embedded_file_links_stay_in_runtime(self):
        for text in ("[answer][policy]\n\n[policy]: ../../answers.md\n",
                     "<file:///outside/answers.md>",
                     '<a href="../../answers.md">answer</a>'):
            with self.subTest(text=text):
                (self.plugin / "references/leak.md").write_text(text)
                errors = []
                validate_runtime_boundary(self.plugin, errors)
                self.assertTrue(errors)

    def test_file_uris_cannot_bypass_runtime_link_checks(self):
        (self.plugin / "references/leak.md").write_text("[answers](file:///outside/evals/cases.json)")
        errors = []
        validate_runtime_boundary(self.plugin, errors)
        self.assertTrue(any("unsupported file/resource URI" in error for error in errors), errors)

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
