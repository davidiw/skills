#!/usr/bin/env python3
"""Validate Engineering Harness authorities, structure, and public artifacts."""

from __future__ import annotations

import hashlib
import json
import os
import re
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "engineering-harness"
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))

from profile_repository import check_drift, package_version
from render_invariants import OUTPUT, render
from validate_profile import MECHANICAL_RUNGS, VERSION_PATTERN, validate_profile


PUBLIC_REPOSITORY = "https://github.com/davidiw/skills"
MARKETPLACE_PATH = ROOT / ".agents" / "plugins" / "marketplace.json"
ROUTER_SKILL = "using-engineering-harness"
SKILL_NAMES = {path.parent.name for path in (PLUGIN_ROOT / "skills").glob("*/SKILL.md")}
SPECIALIST_SKILLS = SKILL_NAMES - {ROUTER_SKILL}
IMPLICIT_SKILLS = {ROUTER_SKILL}
RUNGS = {
    "principle",
    "owner",
    "audit",
    "local_check",
    "ci_check",
    "runtime_guard",
    "fault_test",
}
TIMINGS = {"ownership_declaration", "boundary_introduction", "risk_proportional"}
LINK_PATTERN = re.compile(r"\[[^]]+\]\(([^)]+)\)")
SHA_PATTERN = re.compile(r"`[0-9a-f]{40}`")
FULL_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
KEBAB_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
EVIDENCE_STATUSES = {"passed", "passed_with_limitations", "failed"}
NEGATIVE_COVERAGE = {
    "avoid-durable-runtime",
    "avoid-event-system",
    "avoid-state-machine",
    "avoid-repository-layer",
    "avoid-compatibility-machinery",
    "avoid-architecture-document",
    "avoid-operational-infrastructure",
}
POSITIVE_COVERAGE = {
    "requires-durability",
    "requires-replication",
    "requires-compatibility",
    "requires-ui-ownership",
    "requires-external-provider",
    "requires-physical-proof",
    "requires-resource-governance",
}


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    require(text.startswith("---\n"), f"{path}: missing YAML frontmatter", errors)
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        errors.append(f"{path}: unterminated YAML frontmatter")
        return {}
    result: dict[str, str] = {}
    for line in parts[1].splitlines():
        if not line.strip() or line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def validate_links(path: Path, errors: list[str]) -> None:
    for target in LINK_PATTERN.findall(path.read_text(encoding="utf-8")):
        if "://" in target or target.startswith("#"):
            continue
        target_path = target.split("#", 1)[0]
        if not target_path:
            continue
        require(
            (path.parent / target_path).resolve().exists(),
            f"{path.relative_to(ROOT)}: broken link {target}",
            errors,
        )


def validate_skills(errors: list[str]) -> None:
    skill_files = sorted((PLUGIN_ROOT / "skills").glob("*/SKILL.md"))
    names = {path.parent.name for path in skill_files}
    require(ROUTER_SKILL in names, f"public router skill is missing: {ROUTER_SKILL}", errors)
    require(names == SKILL_NAMES, "skill inventory changed during validation", errors)
    descriptions: set[str] = set()
    for path in skill_files:
        frontmatter = parse_frontmatter(path, errors)
        name = path.parent.name
        require(frontmatter.get("name") == name, f"{path}: name must match directory", errors)
        description = frontmatter.get("description", "")
        require(bool(description), f"{path}: description is required", errors)
        require(description not in descriptions, f"{path}: duplicate description", errors)
        descriptions.add(description)
        metadata_path = path.parent / "agents" / "openai.yaml"
        require(metadata_path.exists(), f"{path}: missing agents/openai.yaml", errors)
        metadata = metadata_path.read_text(encoding="utf-8") if metadata_path.exists() else ""
        policy_match = re.search(
            r"(?m)^\s+allow_implicit_invocation:\s*(true|false)\s*$",
            metadata,
        )
        require(policy_match is not None, f"{path}: invocation policy is not explicit", errors)
        implicit = policy_match is not None and policy_match.group(1) == "true"
        require(
            implicit == (name in IMPLICIT_SKILLS),
            f"{path}: invocation policy mismatch",
            errors,
        )
        if name in SPECIALIST_SKILLS:
            skill_text = path.read_text(encoding="utf-8")
            require(
                "invariants.json" in skill_text,
                f"{path}: missing normative invariant-catalog pointer",
                errors,
            )
            require(
                "precedence-and-exceptions.md" in skill_text,
                f"{path}: missing precedence pointer",
                errors,
            )

    old_audit = PLUGIN_ROOT / "skills" / "architecture-hardening" / "references" / "post-review-audit.md"
    new_audit = PLUGIN_ROOT / "skills" / "verification-and-operations" / "references" / "adversarial-review.md"
    require(not old_audit.exists(), "architecture-hardening still owns adversarial review", errors)
    require(new_audit.exists(), "verification-and-operations lacks adversarial review", errors)


def validate_invariants(errors: list[str]) -> None:
    path = PLUGIN_ROOT / "references" / "invariants.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    require(document.get("schema_version") == 2, "invariant schema_version must be 2", errors)
    invariants = document.get("invariants", [])
    require(bool(invariants), "the invariant catalog must not be empty", errors)
    ids: set[str] = set()
    statements: set[str] = set()
    expected_keys = {
        "id",
        "statement",
        "activates_when",
        "default_rung",
        "enforcement_timing",
        "owner_skill",
        "consumed_by",
    }
    for item in invariants:
        invariant_id = item.get("id")
        require(set(item) == expected_keys, f"{invariant_id}: invariant fields differ", errors)
        require(isinstance(invariant_id, str) and bool(KEBAB_PATTERN.fullmatch(invariant_id)), "invariant id is invalid", errors)
        require(invariant_id not in ids, f"duplicate invariant: {invariant_id}", errors)
        ids.add(invariant_id)
        statement = item.get("statement")
        require(isinstance(statement, str) and bool(statement), f"{invariant_id}: statement is required", errors)
        require(statement not in statements, f"{invariant_id}: duplicate statement", errors)
        statements.add(statement)
        require(bool(item.get("activates_when")), f"{invariant_id}: activation is required", errors)
        require(item.get("default_rung") in RUNGS, f"{invariant_id}: invalid default rung", errors)
        timing = item.get("enforcement_timing")
        require(timing in TIMINGS, f"{invariant_id}: invalid enforcement timing", errors)
        if timing == "boundary_introduction":
            require(item.get("default_rung") in MECHANICAL_RUNGS, f"{invariant_id}: boundary timing needs mechanical default", errors)
        owner = item.get("owner_skill")
        require(owner in SPECIALIST_SKILLS, f"{invariant_id}: invalid normative owner", errors)
        consumers = item.get("consumed_by")
        require(isinstance(consumers, list), f"{invariant_id}: consumed_by must be an array", errors)
        if isinstance(consumers, list):
            require(len(consumers) == len(set(consumers)), f"{invariant_id}: duplicate consumer", errors)
            require(set(consumers) <= SPECIALIST_SKILLS, f"{invariant_id}: unknown consumer", errors)
            require(owner not in consumers, f"{invariant_id}: owner cannot also be a consumer", errors)

    require(
        OUTPUT.exists() and OUTPUT.read_text(encoding="utf-8") == render(),
        "generated invariant documentation is stale",
        errors,
    )

    activation = json.loads(
        (PLUGIN_ROOT / "references" / "capability-activation.json").read_text(encoding="utf-8")
    )
    require(activation.get("schema_version") == 1, "activation schema_version must be 1", errors)
    activated_ids = set(activation.get("always", []))
    for values in activation.get("project_fields", {}).values():
        require(len(values) == len(set(values)), "project-field activation contains duplicates", errors)
        activated_ids.update(values)
    for values in activation.get("capabilities", {}).values():
        require(len(values) == len(set(values)), "capability activation contains duplicates", errors)
        activated_ids.update(values)
    require(activated_ids <= ids, "capability activation references unknown invariants", errors)


def validate_profiles(errors: list[str]) -> None:
    paths = sorted((PLUGIN_ROOT / "templates").glob("project-profile.*.json"))
    paths.append(ROOT / "engineering-harness.json")
    current_version = package_version()
    for path in paths:
        document = json.loads(path.read_text(encoding="utf-8"))
        for error in validate_profile(document):
            errors.append(f"{path.relative_to(ROOT)}: {error}")
        require(
            document.get("harness_policy_version") == current_version,
            f"{path.relative_to(ROOT)}: stale harness policy version",
            errors,
        )
    self_profile = json.loads((ROOT / "engineering-harness.json").read_text(encoding="utf-8"))
    drift_errors, _ = check_drift(ROOT, self_profile)
    for error in drift_errors:
        errors.append(f"engineering-harness.json: {error}")


def validate_evals(errors: list[str]) -> None:
    path = ROOT / "evals" / "cases.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    require(document.get("schema_version") == 2, "eval schema_version must be 2", errors)
    require(document.get("rubric_version") == 1, "eval rubric_version must be 1", errors)
    cases = document.get("cases", [])
    require(len(cases) >= 18, "at least eighteen evaluation cases are required", errors)
    ids: set[str] = set()
    classes = {"minimal", "bounded", "consequential", "stabilization"}
    negative_tags: set[str] = set()
    positive_tags: set[str] = set()
    negative_cases = 0
    for case in cases:
        case_id = case.get("id")
        require(isinstance(case_id, str) and bool(case_id), "eval case id is required", errors)
        require(case_id not in ids, f"duplicate eval case: {case_id}", errors)
        ids.add(case_id)
        require(case.get("control") in {"negative", "positive", "mixed"}, f"{case_id}: invalid control", errors)
        tags = case.get("coverage_tags")
        require(isinstance(tags, list) and bool(tags), f"{case_id}: coverage tags required", errors)
        if isinstance(tags, list):
            require(len(tags) == len(set(tags)), f"{case_id}: coverage tags must be unique", errors)
            require(all(isinstance(tag, str) and KEBAB_PATTERN.fullmatch(tag) for tag in tags), f"{case_id}: invalid coverage tag", errors)
        require(case.get("expected_class") in classes, f"{case_id}: invalid class", errors)
        skills = case.get("expected_skills", [])
        require(bool(skills) and skills[0] == "using-engineering-harness", f"{case_id}: router must be first", errors)
        require(set(skills) <= SKILL_NAMES, f"{case_id}: unknown skill", errors)
        require(len(skills) == len(set(skills)), f"{case_id}: duplicate skill", errors)
        require(len(case.get("required_outcomes", [])) >= 2, f"{case_id}: requires two outcomes", errors)
        require(bool(case.get("forbidden_outcomes")), f"{case_id}: forbidden outcomes required", errors)
        if case.get("control") == "negative":
            negative_cases += 1
            negative_tags.update(tags or [])
            require(skills == ["using-engineering-harness"], f"{case_id}: negative control loads a specialist", errors)
        else:
            positive_tags.update(tags or [])
        fixture = case.get("fixture")
        if fixture is not None:
            fixture_path = (path.parent / fixture).resolve()
            require(fixture_path.is_dir(), f"{case_id}: fixture directory is missing", errors)
            require((fixture_path / "AGENTS.md").is_file(), f"{case_id}: fixture AGENTS.md is missing", errors)
            if fixture_path.is_dir():
                fixture_files = [item for item in fixture_path.rglob("*") if item.is_file()]
                require(len(fixture_files) >= 2, f"{case_id}: fixture has no implementation context", errors)
    require(negative_cases >= 4, "at least four negative controls are required", errors)
    require(NEGATIVE_COVERAGE <= negative_tags, "negative controls do not cover every over-engineering failure", errors)
    require(POSITIVE_COVERAGE <= positive_tags, "positive controls do not cover every required capability", errors)
    routed_skills = {skill for case in cases for skill in case.get("expected_skills", [])}
    require(SKILL_NAMES <= routed_skills, "one or more discovered skills have no evaluation route", errors)

    matrix = json.loads((ROOT / "evals" / "behavioral-matrix.json").read_text(encoding="utf-8"))
    matrix_ids = matrix.get("case_ids", [])
    require(matrix.get("schema_version") == 1, "behavioral matrix schema_version must be 1", errors)
    require(matrix.get("prompt_mode") == "natural", "behavioral matrix must use natural prompts", errors)
    require(matrix.get("trials") == 1, "directional behavioral matrix must use one trial", errors)
    require(matrix.get("conditions") == ["control", "harness"], "behavioral matrix conditions differ", errors)
    require(isinstance(matrix_ids, list) and len(matrix_ids) >= 8, "behavioral matrix must select at least eight cases", errors)
    require(len(matrix_ids) == len(set(matrix_ids)), "behavioral matrix contains duplicate cases", errors)
    case_by_id = {case["id"]: case for case in cases}
    require(set(matrix_ids) <= set(case_by_id), "behavioral matrix references an unknown case", errors)
    for case_id in matrix_ids:
        case = case_by_id.get(case_id, {})
        require(bool(case.get("fixture")), f"behavioral case lacks a fixture: {case_id}", errors)
        require("$" not in case.get("request", ""), f"behavioral case names a skill: {case_id}", errors)

    audit_case = next((case for case in cases if case.get("id") == "high-risk-adversarial-review"), None)
    require(audit_case is not None, "adversarial review boundary case is missing", errors)
    if audit_case:
        require("verification-and-operations" in audit_case["expected_skills"], "adversarial review does not route to verification", errors)
        require("architecture-hardening" not in audit_case["expected_skills"], "adversarial review routes to hardening", errors)

    validate_eval_receipts(case_by_id, matrix_ids, errors)
    assurance_matrix = json.loads((ROOT / "evals" / "assurance-matrix.json").read_text())
    validate_assurance_matrix(assurance_matrix, case_by_id, errors)


def validate_assurance_matrix(
    matrix: dict[str, object], case_by_id: dict[str, dict[str, object]], errors: list[str]
) -> None:
    prefix = "assurance matrix: "
    require(matrix.get("schema_version") == 1, prefix + "invalid schema", errors)
    require(matrix.get("prompt_mode") == "natural", prefix + "must use natural prompts", errors)
    trials = matrix.get("trials")
    require(type(trials) is int and trials >= 2, prefix + "requires repeated trials", errors)
    require(matrix.get("conditions") == ["control", "harness"], prefix + "requires both arms", errors)
    concurrency = matrix.get("concurrency")
    require(type(concurrency) is int and 1 <= concurrency <= 2, prefix + "concurrency must be bounded to two", errors)
    ids = matrix.get("case_ids")
    if not isinstance(ids, list) or not all(isinstance(item, str) for item in ids):
        errors.append(prefix + "case_ids must be strings")
        return
    require(len(ids) == len(set(ids)), prefix + "duplicate case", errors)
    required = {
        "natural-security-review", "natural-privacy-review", "authorization-export",
        "erasure-telemetry", "critical-audit", "handoff-session", "uncatalogued-assurance",
        "provider-wake-restraint", "ui-fence-restraint", "sensitive-copy-restraint",
        "tiny-cli-restraint", "pure-library-parser-restraint",
        "release-security-surface", "release-privacy-lifecycle",
        "temporary-account-oauth-scope", "approved-provider-broker-design",
    }
    require(required <= set(ids), prefix + "missing discovery, restraint, release, or scope coverage", errors)
    for case_id in ids:
        case = case_by_id.get(case_id)
        if case is None:
            errors.append(prefix + f"unknown case: {case_id}")
            continue
        require(bool(case.get("fixture")), prefix + f"fixture required: {case_id}", errors)
        require("$" not in case.get("request", ""), prefix + f"explicit skill in prompt: {case_id}", errors)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit_exists(revision: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "-e", f"{revision}^{{commit}}"],
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def git_is_ancestor(ancestor: str, descendant: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", ancestor, descendant],
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def manifest_at_revision(revision: str) -> bytes | None:
    """Read immutable runtime metadata across the repository layout migration."""
    for relative in ("plugins/engineering-harness/.codex-plugin/plugin.json",
                     ".codex-plugin/plugin.json"):
        result = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{revision}:{relative}"],
            capture_output=True, check=False,
        )
        if result.returncode == 0:
            return result.stdout
    return None


def validate_eval_receipt(
    document: dict[str, object],
    case_by_id: dict[str, dict[str, object]],
    matrix_ids: list[str],
    errors: list[str],
    *,
    label: str,
) -> None:
    prefix = f"{label}: "
    require(document.get("schema_version") == 1, prefix + "schema_version must be 1", errors)
    require(document.get("status") in EVIDENCE_STATUSES, prefix + "invalid status", errors)
    revision = document.get("scored_source_revision")
    require(
        isinstance(revision, str) and bool(FULL_SHA_PATTERN.fullmatch(revision)),
        prefix + "scored_source_revision must be a full Git SHA",
        errors,
    )
    revision_retained = (
        isinstance(revision, str)
        and bool(FULL_SHA_PATTERN.fullmatch(revision))
        and git_commit_exists(revision)
    )
    require(
        revision_retained,
        prefix + "scored_source_revision is not retained in this repository",
        errors,
    )

    # Historical receipts prove their recorded corpus and policy, never the
    # current checkout. Resolve immutable inputs before validating scores.
    snapshots: dict[str, bytes] = {}
    if revision_retained:
        for relative in (".codex-plugin/plugin.json", "evals/cases.json",
                         "evals/behavioral-matrix.json", "evals/rubric.md"):
            if relative == ".codex-plugin/plugin.json":
                content = manifest_at_revision(revision)
            else:
                result = subprocess.run(
                    ["git", "-C", str(ROOT), "show", f"{revision}:{relative}"],
                    capture_output=True, check=False,
                )
                content = result.stdout if result.returncode == 0 else None
            require(content is not None, prefix + f"recorded input is missing: {relative}", errors)
            if content is not None:
                snapshots[relative] = content
        if len(snapshots) != 4:
            return
        try:
            recorded_manifest = json.loads(snapshots[".codex-plugin/plugin.json"])
            recorded_cases = json.loads(snapshots["evals/cases.json"])
            recorded_matrix = json.loads(snapshots["evals/behavioral-matrix.json"])
            case_by_id = {case["id"]: case for case in recorded_cases["cases"]}
            matrix_ids = recorded_matrix["case_ids"]
        except (ValueError, KeyError, TypeError):
            errors.append(prefix + "recorded corpus is malformed")
            return
        require(document.get("harness_policy_version") == recorded_manifest.get("version"),
                prefix + "policy differs from scored revision", errors)

    execution = document.get("execution")
    require(isinstance(execution, dict), prefix + "execution must be an object", errors)
    if isinstance(execution, dict):
        retention = execution.get("evidence_retention")
        require(
            isinstance(retention, dict),
            prefix + "execution.evidence_retention must be an object",
            errors,
        )
        if isinstance(retention, dict):
            replayable = retention.get("public_replayable")
            require(
                isinstance(replayable, bool),
                prefix + "evidence retention must declare public_replayable",
                errors,
            )
            if replayable is False:
                require(
                    document.get("status") != "passed",
                    prefix + "digest-only evidence cannot be an unqualified pass",
                    errors,
                )
                require(
                    bool(retention.get("limitation")),
                    prefix + "digest-only evidence must explain its limitation",
                    errors,
                )

    corpus = document.get("corpus")
    require(isinstance(corpus, dict), prefix + "corpus must be an object", errors)
    if isinstance(corpus, dict):
        expected_hashes = {
            field: hashlib.sha256(snapshots[relative]).hexdigest()
            if relative in snapshots else file_sha256(ROOT / relative)
            for field, relative in (
                ("behavioral_matrix_sha256", "evals/behavioral-matrix.json"),
                ("cases_sha256", "evals/cases.json"),
                ("rubric_sha256", "evals/rubric.md"),
            )
        }
        for field, expected in expected_hashes.items():
            value = corpus.get(field)
            require(
                isinstance(value, str) and bool(SHA256_PATTERN.fullmatch(value)),
                prefix + f"corpus.{field} must be a SHA-256 digest",
                errors,
            )
            require(value == expected, prefix + f"corpus.{field} is stale", errors)
        require(corpus.get("prompt_mode") == "natural", prefix + "prompt mode must be natural", errors)
        require(corpus.get("trials_per_selected_pair") == 1, prefix + "directional receipt must use one trial", errors)
        require(corpus.get("case_count") == len(matrix_ids), prefix + "corpus case_count differs", errors)

    results = document.get("results")
    require(isinstance(results, list), prefix + "results must be an array", errors)
    if not isinstance(results, list):
        return
    result_ids = [result.get("case_id") for result in results if isinstance(result, dict)]
    require(len(result_ids) == len(results), prefix + "each result must be an object", errors)
    require(result_ids == matrix_ids, prefix + "result cases differ from the behavioral matrix", errors)

    integer_fields = (
        "harness_required_outcomes_met",
        "control_required_outcomes_met",
        "harness_forbidden_outcomes_triggered",
        "control_forbidden_outcomes_triggered",
        "harness_fabricated_execution_claims",
        "control_fabricated_execution_claims",
        "harness_score",
        "control_score",
        "harness_wall_time_ms",
        "control_wall_time_ms",
        "harness_input_tokens",
        "harness_cached_input_tokens",
        "harness_output_tokens",
        "control_input_tokens",
        "control_cached_input_tokens",
        "control_output_tokens",
    )
    valid_results: list[dict[str, object]] = []
    for result in results:
        if not isinstance(result, dict):
            continue
        result_valid = True
        case_id = result.get("case_id")
        case = case_by_id.get(case_id) if isinstance(case_id, str) else None
        require(case is not None, prefix + f"unknown result case: {case_id}", errors)
        if case is None:
            continue
        expected_skills = result.get("expected_skills")
        observed_skills = result.get("observed_skills")
        expected_route_valid = expected_skills == case.get("expected_skills")
        require(expected_route_valid, prefix + f"{case_id}: expected route is stale", errors)
        observed_route_valid = (
            isinstance(observed_skills, list)
            and bool(observed_skills)
            and observed_skills[0] == ROUTER_SKILL
            and len(observed_skills) == len(set(observed_skills))
            and set(observed_skills) <= SKILL_NAMES
        )
        require(observed_route_valid, prefix + f"{case_id}: observed route is invalid", errors)
        result_valid = result_valid and expected_route_valid and observed_route_valid
        harness_revision = result.get("harness_revision")
        revision_valid = (
            isinstance(harness_revision, str)
            and bool(FULL_SHA_PATTERN.fullmatch(harness_revision))
        )
        require(revision_valid, prefix + f"{case_id}: harness_revision must be a full Git SHA", errors)
        harness_revision_retained = revision_valid and git_commit_exists(harness_revision)
        require(
            harness_revision_retained,
            prefix + f"{case_id}: harness_revision is not retained",
            errors,
        )
        if harness_revision_retained and revision_retained:
            require(
                git_is_ancestor(harness_revision, revision),
                prefix + f"{case_id}: harness_revision is not an ancestor of the scored revision",
                errors,
            )
        result_valid = result_valid and harness_revision_retained
        for field in ("harness_output_sha256", "control_output_sha256"):
            value = result.get(field)
            digest_valid = isinstance(value, str) and bool(SHA256_PATTERN.fullmatch(value))
            require(
                digest_valid,
                prefix + f"{case_id}: {field} must be a SHA-256 digest",
                errors,
            )
            result_valid = result_valid and digest_valid
        for field in integer_fields:
            value = result.get(field)
            integer_valid = (
                isinstance(value, int) and not isinstance(value, bool) and value >= 0
            )
            require(
                integer_valid,
                prefix + f"{case_id}: {field} must be a nonnegative integer",
                errors,
            )
            result_valid = result_valid and integer_valid
        harness_score = result.get("harness_score")
        control_score = result.get("control_score")
        if isinstance(harness_score, int) and not isinstance(harness_score, bool):
            require(harness_score <= 12, prefix + f"{case_id}: harness_score exceeds 12", errors)
        if isinstance(control_score, int) and not isinstance(control_score, bool):
            require(control_score <= 12, prefix + f"{case_id}: control_score exceeds 12", errors)
        required_total = len(case.get("required_outcomes", []))
        for arm in ("harness", "control"):
            required_met = result.get(f"{arm}_required_outcomes_met")
            forbidden = result.get(f"{arm}_forbidden_outcomes_triggered")
            fabricated = result.get(f"{arm}_fabricated_execution_claims")
            score = result.get(f"{arm}_score")
            passed = result.get(f"{arm}_pass")
            pass_valid = isinstance(passed, bool)
            require(
                pass_valid,
                prefix + f"{case_id}: {arm}_pass must be boolean",
                errors,
            )
            result_valid = result_valid and pass_valid
            if isinstance(required_met, int) and not isinstance(required_met, bool):
                require(
                    required_met <= required_total,
                    prefix + f"{case_id}: {arm} required outcomes exceed the case",
                    errors,
                )
            values = (required_met, forbidden, fabricated, score)
            if all(
                isinstance(value, int) and not isinstance(value, bool)
                for value in values
            ) and pass_valid:
                expected_pass = (
                    score >= 10
                    and required_met == required_total
                    and forbidden == 0
                    and fabricated == 0
                )
                require(
                    passed == expected_pass,
                    prefix + f"{case_id}: {arm} pass does not follow the rubric",
                    errors,
                )
        if result_valid:
            valid_results.append(result)

    aggregate = document.get("aggregate")
    require(isinstance(aggregate, dict), prefix + "aggregate must be an object", errors)
    if not isinstance(aggregate, dict) or len(valid_results) != len(matrix_ids):
        return

    def total(field: str) -> int:
        return sum(int(result[field]) for result in valid_results)

    harness_times = [int(result["harness_wall_time_ms"]) for result in valid_results]
    control_times = [int(result["control_wall_time_ms"]) for result in valid_results]
    computed = {
        "harness_score": total("harness_score"),
        "control_score": total("control_score"),
        "maximum_score": 12 * len(valid_results),
        "harness_passes": sum(result.get("harness_pass") is True for result in valid_results),
        "control_passes": sum(result.get("control_pass") is True for result in valid_results),
        "case_count": len(valid_results),
        "required_specialist_false_negatives": sum(
            not (set(result["expected_skills"]) - {ROUTER_SKILL}) <= set(result["observed_skills"])
            for result in valid_results
        ),
        "specialist_overactivations": sum(
            bool(set(result["observed_skills"]) - set(result["expected_skills"]))
            for result in valid_results
        ),
        "harness_forbidden_outcomes_triggered": total(
            "harness_forbidden_outcomes_triggered"
        ),
        "control_forbidden_outcomes_triggered": total(
            "control_forbidden_outcomes_triggered"
        ),
        "harness_fabricated_execution_claims": total(
            "harness_fabricated_execution_claims"
        ),
        "control_fabricated_execution_claims": total(
            "control_fabricated_execution_claims"
        ),
        "harness_wall_time_ms": sum(harness_times),
        "control_wall_time_ms": sum(control_times),
        "harness_median_wall_time_ms": round(statistics.median(harness_times)),
        "control_median_wall_time_ms": round(statistics.median(control_times)),
        "harness_input_tokens": total("harness_input_tokens"),
        "harness_cached_input_tokens": total("harness_cached_input_tokens"),
        "harness_output_tokens": total("harness_output_tokens"),
        "control_input_tokens": total("control_input_tokens"),
        "control_cached_input_tokens": total("control_cached_input_tokens"),
        "control_output_tokens": total("control_output_tokens"),
    }
    for field, expected in computed.items():
        require(aggregate.get(field) == expected, prefix + f"aggregate.{field} differs", errors)
    if document.get("status") in {"passed", "passed_with_limitations"}:
        require(
            computed["harness_fabricated_execution_claims"] == 0,
            prefix + "passing harness evidence cannot fabricate execution",
            errors,
        )
        require(
            computed["required_specialist_false_negatives"] == 0,
            prefix + "passing evidence cannot miss a required specialist",
            errors,
        )
        require(
            computed["harness_passes"] == len(valid_results),
            prefix + "passing receipt requires every harness case to pass",
            errors,
        )


def validate_eval_receipts(
    case_by_id: dict[str, dict[str, object]],
    matrix_ids: list[str],
    errors: list[str],
) -> None:
    results_dir = ROOT / "evals" / "results"
    receipt_paths = sorted(results_dir.glob("*.json")) if results_dir.is_dir() else []
    require(bool(receipt_paths), "at least one behavioral evidence receipt is required", errors)
    for path in receipt_paths:
        document = json.loads(path.read_text(encoding="utf-8"))
        require(isinstance(document, dict), f"{path.relative_to(ROOT)}: receipt must be an object", errors)
        if not isinstance(document, dict):
            continue
        validate_eval_receipt(
            document,
            case_by_id,
            matrix_ids,
            errors,
            label=str(path.relative_to(ROOT)),
        )


def validate_manifest_sources_and_version(errors: list[str]) -> None:
    manifest = json.loads((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    require(manifest.get("name") == "engineering-harness", "unexpected plugin name", errors)
    require(manifest.get("skills") == "./skills/", "manifest must expose ./skills/", errors)
    require(manifest.get("homepage") == PUBLIC_REPOSITORY, "manifest homepage is incorrect", errors)
    require(manifest.get("repository") == PUBLIC_REPOSITORY, "manifest repository is incorrect", errors)
    require(
        manifest.get("license") == "BSD-3-Clause",
        "manifest and LICENSE policy differ",
        errors,
    )
    profile_schema = json.loads(
        (PLUGIN_ROOT / "references" / "project-profile.schema.json").read_text(
            encoding="utf-8"
        )
    )
    require(
        profile_schema.get("$id")
        == f"{PUBLIC_REPOSITORY}/project-profile.schema.json",
        "project profile schema identifier is incorrect",
        errors,
    )
    version = manifest.get("version", "")
    require(isinstance(version, str) and bool(VERSION_PATTERN.fullmatch(version)), "manifest version is not semantic", errors)
    prompts = manifest.get("interface", {}).get("defaultPrompt", [])
    require(isinstance(prompts, list) and bool(prompts) and all(isinstance(prompt, str) and prompt.strip() for prompt in prompts), "manifest requires nonempty string prompts", errors)
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    first_release = re.search(r"^## ([0-9]+\.[0-9]+\.[0-9]+)\b", changelog, re.MULTILINE)
    require(bool(first_release) and first_release.group(1) == version, "CHANGELOG latest release differs from manifest", errors)
    sources = (ROOT / "SOURCES.md").read_text(encoding="utf-8")
    require(len(SHA_PATTERN.findall(sources)) >= 14, "SOURCES.md must pin reviewed repositories", errors)
    require("independent synthesis" in sources.lower(), "SOURCES.md must state provenance model", errors)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    # An unreleased checkout must not advertise its not-yet-published tag.
    stable_release = re.search(r"^## ([0-9]+\.[0-9]+\.[0-9]+) - [0-9]{4}-[0-9]{2}-[0-9]{2}$", changelog, re.MULTILINE)
    stable_version = stable_release.group(1) if stable_release else version
    stable_command = f"codex plugin marketplace add davidiw/skills --ref v{stable_version}"
    require(
        stable_command in readme,
        "README is missing the immutable marketplace command",
        errors,
    )
    require(
        "codex plugin add engineering-harness@davidiw-skills" in readme,
        "README is missing the plugin installation command",
        errors,
    )
    require("--ref main" in readme and "development/nightly" in readme, "README must distinguish the mutable development channel", errors)

    agent_rules = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for authority in ("DESIGN.md", "references/invariants.json", "references/capability-activation.json", "references/versioning.md"):
        require(authority in agent_rules, f"AGENTS.md is missing authority pointer: {authority}", errors)

    marketplace = json.loads(MARKETPLACE_PATH.read_text(encoding="utf-8"))
    expected_marketplace = {
        "name": "davidiw-skills",
        "interface": {"displayName": "David's Skills"},
        "plugins": [
            {
                "name": manifest.get("name"),
                "source": {"source": "local", "path": "./plugins/engineering-harness"},
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Developer Tools",
            }
        ],
    }
    require(
        marketplace == expected_marketplace,
        "marketplace metadata differs from the runtime engineering-harness plugin",
        errors,
    )


def validate_repository_layout(repository_root: Path, errors: list[str]) -> None:
    """Reserve policy ownership for the installable runtime directory."""
    for name in (".codex-plugin", "skills", "references", "templates"):
        path = repository_root / name
        require(
            not (path.exists() or path.is_symlink()),
            f"repository layout: legacy policy root {name} is forbidden; use plugins/engineering-harness/{name}",
            errors,
        )


def runtime_markdown_targets(text: str) -> list[str]:
    targets = LINK_PATTERN.findall(text)
    # Reference-style Markdown and URI autolinks are file references too.
    for bracketed, plain in re.findall(r"(?m)^ {0,3}\[[^]\n]+\]:\s*(?:<([^>]+)>|(\S+))", text):
        targets.append(bracketed or plain)
    targets.extend(re.findall(r"<([A-Za-z][A-Za-z0-9+.-]*://[^>\n]+)>", text))
    targets.extend(re.findall(r"(?:href|src)=[\"']([^\"']+)[\"']", text))
    return targets


def validate_runtime_boundary(plugin_root: Path, errors: list[str]) -> None:
    """Keep the install source self-contained and free of development corpora."""
    allowed = {".codex-plugin", "skills", "references", "templates", "scripts", "LICENSE"}
    forbidden = {"evals", "tests", "fixtures", "results", "evidence", ".git", ".agents"}
    runtime_scripts = {"profile_repository.py", "validate_profile.py"}
    for path in sorted(plugin_root.rglob("*")):
        relative = path.relative_to(plugin_root)
        require(not path.is_symlink(), f"runtime boundary: symlink {relative}", errors)
        require(relative.parts[0] in allowed, f"runtime boundary: unexpected root {relative}", errors)
        require(not (set(relative.parts) & forbidden), f"runtime boundary: development corpus {relative}", errors)
        require(path.suffix not in {".bundle", ".diff", ".patch"}, f"runtime boundary: development artifact {relative}", errors)
        if path.is_file() and relative.parts[0] == "scripts" and "__pycache__" not in relative.parts:
            require(relative.as_posix() in {f"scripts/{name}" for name in runtime_scripts},
                    f"runtime boundary: non-runtime script {relative}", errors)
        if path.is_file() and path.suffix == ".md":
            for target in runtime_markdown_targets(path.read_text(encoding="utf-8")):
                if target.startswith(("https://", "http://", "#")):
                    continue
                require("://" not in target,
                        f"runtime boundary: unsupported file/resource URI {relative}: {target}", errors)
                if "://" in target:
                    continue
                resolved = (path.parent / target.split("#", 1)[0]).resolve()
                require(resolved.is_relative_to(plugin_root.resolve()),
                        f"runtime boundary: external file link {relative}: {target}", errors)
                require(resolved.exists(), f"runtime boundary: missing link {relative}: {target}", errors)


def validate_public_hygiene(errors: list[str]) -> None:
    forbidden = (
        "/" + "home" + "/",
        "/" + "Users" + "/",
        "." + "worktrees" + "/",
        "C:" + "\\" + "Users" + "\\",
    )
    text_suffixes = {".md", ".json", ".py", ".yaml", ".yml", ".txt", ".html", ".css"}
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if ".git" in relative.parts or "__pycache__" in relative.parts:
            continue
        require(not path.is_symlink(), f"{relative}: public symlink is not allowed", errors)
        if not path.is_file():
            continue
        if path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
                errors.append(f"{relative}: invalid JSON: {error}")
        if path.suffix in text_suffixes or path.name in {"LICENSE", "Makefile"}:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                errors.append(f"{relative}: text artifact is not UTF-8")
                continue
            for token in forbidden:
                require(token not in text, f"{relative}: contains developer-local path token", errors)
        if path.suffix == ".md":
            validate_links(path, errors)

    for script in sorted((ROOT / "scripts").glob("*.py")):
        require(os.access(script, os.X_OK), f"{script.relative_to(ROOT)}: script is not executable", errors)


def main() -> int:
    errors: list[str] = []
    validate_repository_layout(ROOT, errors)
    validate_manifest_sources_and_version(errors)
    validate_runtime_boundary(PLUGIN_ROOT, errors)
    validate_skills(errors)
    validate_invariants(errors)
    validate_profiles(errors)
    validate_evals(errors)
    validate_public_hygiene(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("engineering-harness package is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
