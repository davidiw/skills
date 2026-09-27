from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "engineering-harness"
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts"))

from profile_repository import check_drift, propose_profile, scan_repository  # noqa: E402
from render_invariants import OUTPUT, render  # noqa: E402
from validate_package import validate_eval_receipt  # noqa: E402
from validate_profile import validate_profile  # noqa: E402


class ProfileValidationTest(unittest.TestCase):
    def load_example(self, name: str) -> dict[str, object]:
        path = PLUGIN_ROOT / "templates" / name
        return json.loads(path.read_text(encoding="utf-8"))

    def test_examples_and_self_profile_are_valid(self) -> None:
        paths = [
            PLUGIN_ROOT / "templates" / "project-profile.minimal.json",
            PLUGIN_ROOT / "templates" / "project-profile.local-first.json",
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
            (repository / "mobile").mkdir()
            (repository / "mobile" / "app.dart").write_text("import 'package:flutter/widgets.dart';\n")

            profile = propose_profile(repository)

        self.assertEqual(profile["status"], "proposed")
        self.assertTrue(profile["capabilities"]["durable_work"])
        self.assertTrue(profile["capabilities"]["multiple_clients"])
        self.assertEqual(validate_profile(profile), [])
        evidence = profile["discovery"]["capabilities"]["durable_work"]["evidence"]
        self.assertTrue(evidence)
        self.assertTrue(all(not Path(item["path"]).is_absolute() for item in evidence))

    def test_backend_server_and_api_roots_are_not_multiple_clients(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            (repository / "server").mkdir()
            (repository / "server" / "main.py").write_text("def serve():\n    pass\n")
            (repository / "api").mkdir()
            (repository / "api" / "routes.py").write_text("def route():\n    pass\n")

            scan = scan_repository(repository)

        self.assertFalse(scan["capabilities"]["multiple_clients"]["suggested"])

    def test_rendering_code_is_not_a_generated_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            (repository / "src").mkdir()
            (repository / "src" / "render_view.py").write_text("def render_view():\n    return '<p>Hi</p>'\n")

            scan = scan_repository(repository)

        self.assertFalse(scan["capabilities"]["generated_artifacts"]["suggested"])

    def test_cmake_build_dependencies_do_not_activate_capabilities(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            dependency = repository / ".cxx" / "Release" / "_deps" / "worker"
            dependency.mkdir(parents=True)
            (dependency / "generate_jobs.py").write_text("# Generated by tool; do not edit.\n")

            scan = scan_repository(repository)

        self.assertFalse(any(item["suggested"] for item in scan["capabilities"].values()))

    def test_generator_and_output_paths_identify_generated_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            (repository / "tools").mkdir()
            (repository / "tools" / "generate_models.py").write_text("def main():\n    pass\n")
            (repository / "src" / "generated").mkdir(parents=True)
            (repository / "src" / "generated" / "model.py").write_text("MODEL = {}\n")

            scan = scan_repository(repository)

        self.assertTrue(scan["capabilities"]["generated_artifacts"]["suggested"])

    def test_mobile_scaffolding_does_not_require_physical_proof(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            (repository / "android").mkdir()
            (repository / "android" / "build.gradle").write_text("plugins {}\n")
            (repository / "ios").mkdir()
            (repository / "ios" / "Podfile").write_text("platform :ios, '15.0'\n")

            scan = scan_repository(repository)

        self.assertFalse(scan["capabilities"]["physical_devices"]["suggested"])
        self.assertFalse(scan["capabilities"]["multiple_clients"]["suggested"])

    def test_read_only_ai_dependency_is_not_an_ai_action_capability(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            (repository / "src").mkdir()
            (repository / "src" / "summarizer.py").write_text(
                "from openai import OpenAI\n\ndef summarize(text):\n    return text[:80]\n"
            )

            scan = scan_repository(repository)

        self.assertFalse(scan["capabilities"]["ai_mediated_actions"]["suggested"])

    def test_ai_action_owner_and_provider_identify_ai_mediated_actions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            action = repository / "src" / "assistant" / "actions.py"
            action.parent.mkdir(parents=True)
            action.write_text(
                "from openai import OpenAI\n\ndef execute_action(tool_call):\n    return tool_call\n"
            )

            scan = scan_repository(repository)

        self.assertTrue(scan["capabilities"]["ai_mediated_actions"]["suggested"])

    def test_unrelated_ai_import_and_local_action_do_not_combine(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            (repository / "src").mkdir()
            (repository / "src" / "summary.py").write_text(
                "from openai import OpenAI\n\ndef summarize(text):\n    return text[:80]\n"
            )
            (repository / "src" / "local_command.py").write_text(
                "def execute_action(command):\n    return command\n"
            )

            scan = scan_repository(repository)

        self.assertFalse(scan["capabilities"]["ai_mediated_actions"]["suggested"])

    def test_in_process_event_names_do_not_imply_delivery(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            (repository / "src").mkdir()
            (repository / "src" / "events.py").write_text(
                "class EventBus:\n    def publish(self, event):\n        return event\n"
            )

            scan = scan_repository(repository)

        self.assertFalse(scan["capabilities"]["event_delivery"]["suggested"])

    def test_stream_transport_identifies_event_delivery(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            (repository / "src").mkdir()
            (repository / "src" / "stream.py").write_text(
                "CONTENT_TYPE = 'text/event-stream'\n"
            )

            profile = propose_profile(repository)

        self.assertTrue(profile["capabilities"]["event_delivery"])
        self.assertIn("committed-event-truth", profile["enforcement"])
        self.assertNotIn("publication-classes", profile["enforcement"])

    def test_explicit_runtime_resource_owner_identifies_constrained_resources(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            owner = repository / "firmware" / "runtime_resource_manager.cpp"
            owner.parent.mkdir(parents=True)
            owner.write_text("bool reserve_control_plane_memory();\n")

            profile = propose_profile(repository)

        self.assertTrue(profile["capabilities"]["constrained_runtime_resources"])
        self.assertIn("resource-admission-and-reclamation", profile["enforcement"])

    def test_borrowed_resources_activate_without_constrained_resource_signal(self) -> None:
        for physical, adapters in ((True, False), (False, True), (True, True)):
            with self.subTest(physical=physical, adapters=adapters):
                with tempfile.TemporaryDirectory() as directory:
                    repository = Path(directory)
                    paths = []
                    if physical:
                        paths.append("hardware/camera.py")
                    if adapters:
                        paths.extend(("adapters/camera.py", "adapters/analysis.py"))
                    for relative in paths:
                        path = repository / relative
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_text(
                            "class AnalysisLease:\n"
                            "    def __init__(self, camera):\n"
                            "        self.borrowed_camera = camera\n"
                            "    def close(self):\n"
                            "        self.borrowed_camera.close()\n"
                        )
                    profile = propose_profile(repository)
                self.assertEqual(profile["capabilities"]["physical_devices"], physical)
                self.assertEqual(profile["capabilities"]["multiple_adapters"], adapters)
                self.assertFalse(profile["capabilities"]["constrained_runtime_resources"])
                self.assertIn("resource-admission-and-reclamation", profile["enforcement"])
                self.assertEqual(
                    profile["enforcement"]["resource-admission-and-reclamation"],
                    {"rung": "principle", "owner": "review-required"},
                )
                self.assertEqual(validate_profile(profile), [])

    def test_plain_parser_does_not_activate_resource_enforcement(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            (repository / "parser.py").write_text("def parse(stream): return list(stream)\n")
            profile = propose_profile(repository)
        self.assertNotIn("resource-admission-and-reclamation", profile["enforcement"])

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
        document = json.loads((PLUGIN_ROOT / "references" / "invariants.json").read_text())
        skill_names = {path.parent.name for path in (PLUGIN_ROOT / "skills").glob("*/SKILL.md")}
        ids = [item["id"] for item in document["invariants"]]
        self.assertEqual(len(ids), len(set(ids)))
        for item in document["invariants"]:
            with self.subTest(invariant=item["id"]):
                self.assertIsInstance(item["owner_skill"], str)
                self.assertIn(item["owner_skill"], skill_names)
                self.assertNotIn(item["owner_skill"], item["consumed_by"])
                self.assertTrue(set(item["consumed_by"]) <= skill_names)


class SkillInvocationPolicyTest(unittest.TestCase):
    def test_router_is_implicit_and_specialists_are_explicit_only(self) -> None:
        skill_names = {path.parent.name for path in (PLUGIN_ROOT / "skills").glob("*/SKILL.md")}
        router = "using-engineering-harness"

        for name in skill_names:
            metadata = PLUGIN_ROOT / "skills" / name / "agents" / "openai.yaml"
            with self.subTest(skill=name):
                self.assertTrue(metadata.is_file())
                text = metadata.read_text()
                expected = "true" if name == router else "false"
                self.assertIn(f"allow_implicit_invocation: {expected}", text)


class MarketplaceMetadataTest(unittest.TestCase):
    def test_public_repository_identifiers_match(self) -> None:
        manifest = json.loads((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text())
        schema = json.loads(
            (PLUGIN_ROOT / "references" / "project-profile.schema.json").read_text()
        )

        self.assertEqual(manifest["homepage"], "https://github.com/davidiw/skills")
        self.assertEqual(manifest["repository"], "https://github.com/davidiw/skills")
        self.assertEqual(
            schema["$id"],
            "https://github.com/davidiw/skills/project-profile.schema.json",
        )

    def test_marketplace_exposes_only_runtime_plugin(self) -> None:
        manifest = json.loads((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text())
        marketplace = json.loads(
            (ROOT / ".agents" / "plugins" / "marketplace.json").read_text()
        )

        self.assertEqual(marketplace["name"], "davidiw-skills")
        self.assertEqual(marketplace["interface"], {"displayName": "David's Skills"})
        self.assertEqual(
            marketplace["plugins"],
            [
                {
                    "name": manifest["name"],
                    "source": {"source": "local", "path": "./plugins/engineering-harness"},
                    "policy": {
                        "installation": "AVAILABLE",
                        "authentication": "ON_INSTALL",
                    },
                    "category": "Developer Tools",
                }
            ],
        )


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

    def test_directional_receipt_is_bound_to_current_cases_and_aggregates(self) -> None:
        cases = json.loads((ROOT / "evals" / "cases.json").read_text())["cases"]
        matrix_ids = json.loads(
            (ROOT / "evals" / "behavioral-matrix.json").read_text()
        )["case_ids"]
        receipt = json.loads(
            (ROOT / "evals" / "results" / "0.4.0-directional.json").read_text()
        )
        case_by_id = {case["id"]: case for case in cases}
        errors: list[str] = []

        validate_eval_receipt(
            receipt,
            case_by_id,
            matrix_ids,
            errors,
            label="test receipt",
        )

        self.assertEqual(errors, [])

        stale = copy.deepcopy(receipt)
        stale["aggregate"]["harness_score"] += 1
        errors = []
        validate_eval_receipt(
            stale,
            case_by_id,
            matrix_ids,
            errors,
            label="stale receipt",
        )

        self.assertIn("stale receipt: aggregate.harness_score differs", errors)

        malformed = copy.deepcopy(receipt)
        malformed["results"][0]["harness_wall_time_ms"] = "slow"
        errors = []
        validate_eval_receipt(
            malformed,
            case_by_id,
            matrix_ids,
            errors,
            label="malformed receipt",
        )

        self.assertIn(
            "malformed receipt: tiny-cli-restraint: harness_wall_time_ms must be a nonnegative integer",
            errors,
        )

        incomplete_control = copy.deepcopy(receipt)
        durable = next(
            result
            for result in incomplete_control["results"]
            if result["case_id"] == "durable-photo-analysis"
        )
        durable["control_score"] = 10
        durable["control_pass"] = True
        incomplete_control["aggregate"]["control_score"] += 2
        incomplete_control["aggregate"]["control_passes"] += 1
        errors = []
        validate_eval_receipt(
            incomplete_control,
            case_by_id,
            matrix_ids,
            errors,
            label="incomplete control",
        )

        self.assertIn(
            "incomplete control: durable-photo-analysis: control pass does not follow the rubric",
            errors,
        )

        honest_failure = copy.deepcopy(receipt)
        honest_failure["status"] = "failed"
        honest_failure["results"][0]["harness_required_outcomes_met"] = 2
        honest_failure["results"][0]["harness_pass"] = False
        honest_failure["aggregate"]["harness_passes"] -= 1
        errors = []
        validate_eval_receipt(
            honest_failure,
            case_by_id,
            matrix_ids,
            errors,
            label="honest failure",
        )

        self.assertEqual(errors, [])

        missing_revision = copy.deepcopy(receipt)
        missing_revision["scored_source_revision"] = "0" * 40
        errors = []
        validate_eval_receipt(
            missing_revision,
            case_by_id,
            matrix_ids,
            errors,
            label="missing revision",
        )

        self.assertIn(
            "missing revision: scored_source_revision is not retained in this repository",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
