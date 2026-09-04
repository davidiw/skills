from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from profile_repository import check_drift, propose_profile, scan_repository  # noqa: E402
from render_invariants import OUTPUT, render  # noqa: E402
from validate_profile import validate_profile  # noqa: E402


class ProfileValidationTest(unittest.TestCase):
    def load_example(self, name: str) -> dict[str, object]:
        path = ROOT / "templates" / name
        return json.loads(path.read_text(encoding="utf-8"))

    def test_examples_and_self_profile_are_valid(self) -> None:
        paths = [
            ROOT / "templates" / "project-profile.minimal.json",
            ROOT / "templates" / "project-profile.local-first.json",
            ROOT / "engineering-harness.json",
        ]
        for path in paths:
            with self.subTest(path=path.name):
                self.assertEqual(validate_profile(json.loads(path.read_text())), [])

    def test_unknown_invariant_is_rejected(self) -> None:
        profile = self.load_example("project-profile.minimal.json")
        profile["enforcement"]["invented-invariant"] = {
            "rung": "owner",
            "owner": "src/nowhere.ts",
        }

        self.assertIn("unknown invariant: invented-invariant", validate_profile(profile))

    def test_invalid_rung_is_rejected(self) -> None:
        profile = self.load_example("project-profile.local-first.json")
        profile["enforcement"]["durable-admission"]["rung"] = "documented-ish"

        self.assertTrue(
            any("durable-admission.rung is invalid" in error for error in validate_profile(profile))
        )

    def test_non_boolean_capability_is_rejected(self) -> None:
        profile = self.load_example("project-profile.minimal.json")
        profile["capabilities"]["durable_work"] = "maybe"

        self.assertIn("capabilities.durable_work must be boolean", validate_profile(profile))

    def test_capability_vocabulary_comes_from_activation_catalog(self) -> None:
        profile = self.load_example("project-profile.minimal.json")
        profile["capabilities"]["invented_runtime"] = False

        self.assertIn(
            "capabilities must exactly match capability-activation.json",
            validate_profile(profile),
        )

    def test_empty_source_is_rejected(self) -> None:
        profile = self.load_example("project-profile.minimal.json")
        profile["sources"]["architecture"] = ""

        self.assertIn("sources.architecture is too short", validate_profile(profile))

    def test_active_capability_requires_its_invariants(self) -> None:
        profile = self.load_example("project-profile.local-first.json")
        del profile["enforcement"]["durable-admission"]

        self.assertIn(
            "missing enforcement for active invariant: durable-admission",
            validate_profile(profile),
        )

    def test_proposal_may_retain_review_required_owner(self) -> None:
        profile = self.load_example("project-profile.minimal.json")
        profile["status"] = "proposed"
        profile["enforcement"]["canonical-authority"]["owner"] = "review-required"

        self.assertEqual(validate_profile(profile), [])

    def test_accepted_profile_rejects_review_required_owner(self) -> None:
        profile = self.load_example("project-profile.minimal.json")
        profile["enforcement"]["canonical-authority"]["owner"] = "review-required"

        self.assertIn(
            "enforcement.canonical-authority.owner requires review",
            validate_profile(profile),
        )

    def test_foundational_boundary_requires_mechanical_enforcement(self) -> None:
        profile = self.load_example("project-profile.minimal.json")
        profile["enforcement"]["bounded-contracts"]["rung"] = "principle"

        self.assertIn(
            "active foundational boundary lacks mechanical enforcement or exception: bounded-contracts",
            validate_profile(profile),
        )

    def test_authorized_exception_allows_lower_foundational_rung(self) -> None:
        profile = self.load_example("project-profile.minimal.json")
        profile["enforcement"]["bounded-contracts"]["rung"] = "principle"
        profile["exceptions"].append(
            {
                "invariant": "bounded-contracts",
                "scope": "single internal parser module",
                "rationale": "The language has no import-boundary hook in the current toolchain.",
                "authority": "AGENTS.md#accepted-exceptions",
            }
        )

        self.assertEqual(validate_profile(profile), [])

    def test_absolute_source_and_discovery_paths_are_rejected(self) -> None:
        profile = self.load_example("project-profile.minimal.json")
        profile["sources"]["architecture"] = "/tmp/private/DESIGN.md"
        profile["discovery"] = {
            "scanner_version": 1,
            "repository_revision": "unversioned",
            "project_fields": {
                "sensitive_data": {"suggested": False, "confidence": "none", "evidence": []}
            },
            "capabilities": {
                name: {"suggested": False, "confidence": "none", "evidence": []}
                for name in profile["capabilities"]
            },
        }
        profile["discovery"]["capabilities"]["durable_work"] = {
            "suggested": True,
            "confidence": "high",
            "evidence": [{"rule": "job-path", "path": "/tmp/private/job.py"}],
        }

        errors = validate_profile(profile)

        self.assertIn("sources.architecture must be repository-relative", errors)
        self.assertIn(
            "discovery.capabilities.durable_work.evidence[0].path must be relative",
            errors,
        )

    def test_validation_does_not_mutate_profile(self) -> None:
        profile = self.load_example("project-profile.local-first.json")
        before = copy.deepcopy(profile)

        validate_profile(profile)

        self.assertEqual(profile, before)


class ProfileDiscoveryTest(unittest.TestCase):
    def test_minimal_fixture_does_not_activate_capabilities(self) -> None:
        fixture = ROOT / "evals" / "fixtures" / "tiny-cli"

        scan = scan_repository(fixture)

        self.assertFalse(any(item["suggested"] for item in scan["capabilities"].values()))

    def test_discovery_proposes_capabilities_with_relative_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            (repository / "server" / "jobs").mkdir(parents=True)
            (repository / "server" / "jobs" / "photo_job.py").write_text("def retry_checkpoint():\n    pass\n")
            (repository / "web").mkdir()
            (repository / "web" / "app.tsx").write_text("import 'react-dom';\n")

            profile = propose_profile(repository)

        self.assertEqual(profile["status"], "proposed")
        self.assertTrue(profile["capabilities"]["durable_work"])
        self.assertTrue(profile["capabilities"]["multiple_clients"])
        self.assertEqual(validate_profile(profile), [])
        evidence = profile["discovery"]["capabilities"]["durable_work"]["evidence"]
        self.assertTrue(evidence)
        self.assertTrue(all(not Path(item["path"]).is_absolute() for item in evidence))

    def test_new_high_confidence_capability_is_meaningful_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            (repository / "README.md").write_text("Small tool\n")
            profile = propose_profile(repository)
            profile["status"] = "accepted"
            profile["enforcement"]["canonical-authority"]["owner"] = "README.md"
            (repository / "jobs").mkdir()
            (repository / "jobs" / "task.py").write_text("def run():\n    pass\n")

            errors, _ = check_drift(repository, profile)

        self.assertTrue(any("new high-confidence capability: durable_work" in error for error in errors))


class GeneratedInvariantTest(unittest.TestCase):
    def test_rendered_catalog_is_current(self) -> None:
        self.assertEqual(OUTPUT.read_text(encoding="utf-8"), render())

    def test_catalog_has_exactly_one_owner_and_distinct_consumers(self) -> None:
        document = json.loads((ROOT / "references" / "invariants.json").read_text())
        skill_names = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        ids = [item["id"] for item in document["invariants"]]
        self.assertEqual(len(ids), len(set(ids)))
        for item in document["invariants"]:
            with self.subTest(invariant=item["id"]):
                self.assertIsInstance(item["owner_skill"], str)
                self.assertIn(item["owner_skill"], skill_names)
                self.assertNotIn(item["owner_skill"], item["consumed_by"])
                self.assertTrue(set(item["consumed_by"]) <= skill_names)


class EvaluationCorpusTest(unittest.TestCase):
    def test_negative_controls_cover_all_overengineering_failures(self) -> None:
        document = json.loads((ROOT / "evals" / "cases.json").read_text())
        negative = [case for case in document["cases"] if case["control"] == "negative"]
        tags = {tag for case in negative for tag in case["coverage_tags"]}

        self.assertGreaterEqual(len(negative), 4)
        self.assertEqual(
            {
                "avoid-durable-runtime",
                "avoid-event-system",
                "avoid-state-machine",
                "avoid-repository-layer",
                "avoid-compatibility-machinery",
                "avoid-architecture-document",
                "avoid-operational-infrastructure",
            }
            - tags,
            set(),
        )
        for case in negative:
            self.assertEqual(case["expected_skills"], ["using-engineering-harness"])

    def test_positive_controls_retain_required_capability_cases(self) -> None:
        document = json.loads((ROOT / "evals" / "cases.json").read_text())
        tags = {
            tag
            for case in document["cases"]
            if case["control"] != "negative"
            for tag in case["coverage_tags"]
        }

        self.assertTrue(
            {
                "requires-durability",
                "requires-replication",
                "requires-compatibility",
                "requires-ui-ownership",
                "requires-external-provider",
                "requires-physical-proof",
            }
            <= tags
        )


if __name__ == "__main__":
    unittest.main()
