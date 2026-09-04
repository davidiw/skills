from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from render_invariants import OUTPUT, render  # noqa: E402
from validate_profile import validate_profile  # noqa: E402


class ProfileValidationTest(unittest.TestCase):
    def load_example(self, name: str) -> dict[str, object]:
        path = ROOT / "templates" / name
        return json.loads(path.read_text(encoding="utf-8"))

    def test_examples_are_valid(self) -> None:
        for name in (
            "project-profile.minimal.json",
            "project-profile.local-first.json",
        ):
            with self.subTest(name=name):
                self.assertEqual(validate_profile(self.load_example(name)), [])

    def test_unknown_invariant_is_rejected(self) -> None:
        profile = self.load_example("project-profile.minimal.json")
        enforcement = profile["enforcement"]
        assert isinstance(enforcement, dict)
        enforcement["invented-invariant"] = {
            "rung": "owner",
            "owner": "src/nowhere.ts",
        }

        errors = validate_profile(profile)

        self.assertIn("unknown invariant: invented-invariant", errors)

    def test_invalid_rung_is_rejected(self) -> None:
        profile = self.load_example("project-profile.local-first.json")
        enforcement = profile["enforcement"]
        assert isinstance(enforcement, dict)
        entry = enforcement["durable-admission"]
        assert isinstance(entry, dict)
        entry["rung"] = "documented-ish"

        errors = validate_profile(profile)

        self.assertTrue(any("durable-admission.rung is invalid" in error for error in errors))

    def test_non_boolean_capability_is_rejected(self) -> None:
        profile = self.load_example("project-profile.minimal.json")
        capabilities = profile["capabilities"]
        assert isinstance(capabilities, dict)
        capabilities["durable_work"] = "maybe"

        errors = validate_profile(profile)

        self.assertIn("capabilities.durable_work must be boolean", errors)

    def test_active_capability_requires_its_invariants(self) -> None:
        profile = self.load_example("project-profile.local-first.json")
        enforcement = profile["enforcement"]
        assert isinstance(enforcement, dict)
        del enforcement["durable-admission"]

        errors = validate_profile(profile)

        self.assertIn(
            "missing enforcement for active invariant: durable-admission",
            errors,
        )

    def test_unknown_capability_is_rejected(self) -> None:
        profile = self.load_example("project-profile.minimal.json")
        capabilities = profile["capabilities"]
        assert isinstance(capabilities, dict)
        capabilities["telepathy"] = True

        errors = validate_profile(profile)

        self.assertIn("unknown capability: telepathy", errors)

    def test_unknown_top_level_field_is_rejected(self) -> None:
        profile = self.load_example("project-profile.minimal.json")
        profile["parallel_architecture"] = "shadow tracker"

        errors = validate_profile(profile)

        self.assertIn("unknown top-level field: parallel_architecture", errors)

    def test_duplicate_evidence_artifact_is_rejected(self) -> None:
        profile = self.load_example("project-profile.minimal.json")
        enforcement = profile["enforcement"]
        assert isinstance(enforcement, dict)
        entry = enforcement["canonical-authority"]
        assert isinstance(entry, dict)
        entry["artifacts"] = ["test/application.test.ts", "test/application.test.ts"]

        errors = validate_profile(profile)

        self.assertIn(
            "enforcement.canonical-authority.artifacts must be unique",
            errors,
        )

    def test_validation_does_not_mutate_profile(self) -> None:
        profile = self.load_example("project-profile.local-first.json")
        before = copy.deepcopy(profile)

        validate_profile(profile)

        self.assertEqual(profile, before)


class GeneratedInvariantTest(unittest.TestCase):
    def test_rendered_catalog_is_current(self) -> None:
        self.assertEqual(OUTPUT.read_text(encoding="utf-8"), render())

    def test_catalog_has_unique_ids_and_known_skills(self) -> None:
        document = json.loads(
            (ROOT / "references" / "invariants.json").read_text(encoding="utf-8")
        )
        ids = [item["id"] for item in document["invariants"]]
        self.assertEqual(len(ids), len(set(ids)))
        skill_names = {
            path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")
        }
        for item in document["invariants"]:
            with self.subTest(invariant=item["id"]):
                self.assertTrue(set(item["skills"]) <= skill_names)


class EvaluationCorpusTest(unittest.TestCase):
    def test_cases_are_unique_and_contain_negative_controls(self) -> None:
        document = json.loads(
            (ROOT / "evals" / "cases.json").read_text(encoding="utf-8")
        )
        cases = document["cases"]
        ids = [case["id"] for case in cases]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(cases), 10)
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertEqual(case["expected_skills"][0], "using-engineering-harness")
                self.assertGreaterEqual(len(case["required_outcomes"]), 2)
                self.assertTrue(case["forbidden_outcomes"])
                if "fixture" in case:
                    fixture = ROOT / "evals" / case["fixture"]
                    self.assertTrue((fixture / "AGENTS.md").is_file())


if __name__ == "__main__":
    unittest.main()
