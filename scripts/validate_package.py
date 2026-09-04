#!/usr/bin/env python3
"""Validate Engineering Harness authorities, structure, and public artifacts."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

from profile_repository import check_drift, package_version
from render_invariants import OUTPUT, render
from validate_profile import MECHANICAL_RUNGS, VERSION_PATTERN, validate_profile


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_REPOSITORY = "https://github.com/davidiw/skills"
ROUTER_SKILL = "using-engineering-harness"
SKILL_NAMES = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
SPECIALIST_SKILLS = SKILL_NAMES - {ROUTER_SKILL}
EXPLICIT_ONLY = {ROUTER_SKILL}
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
KEBAB_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
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
    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
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
        explicitly_disabled = (
            metadata_path.exists()
            and "allow_implicit_invocation: false"
            in metadata_path.read_text(encoding="utf-8")
        )
        require(
            explicitly_disabled == (name in EXPLICIT_ONLY),
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

    old_audit = ROOT / "skills" / "architecture-hardening" / "references" / "post-review-audit.md"
    new_audit = ROOT / "skills" / "verification-and-operations" / "references" / "adversarial-review.md"
    require(not old_audit.exists(), "architecture-hardening still owns adversarial review", errors)
    require(new_audit.exists(), "verification-and-operations lacks adversarial review", errors)


def validate_invariants(errors: list[str]) -> None:
    path = ROOT / "references" / "invariants.json"
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
        (ROOT / "references" / "capability-activation.json").read_text(encoding="utf-8")
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
    paths = sorted((ROOT / "templates").glob("project-profile.*.json"))
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

    audit_case = next((case for case in cases if case.get("id") == "high-risk-adversarial-review"), None)
    require(audit_case is not None, "adversarial review boundary case is missing", errors)
    if audit_case:
        require("verification-and-operations" in audit_case["expected_skills"], "adversarial review does not route to verification", errors)
        require("architecture-hardening" not in audit_case["expected_skills"], "adversarial review routes to hardening", errors)


def validate_manifest_sources_and_version(errors: list[str]) -> None:
    manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    require(manifest.get("name") == "engineering-harness", "unexpected plugin name", errors)
    require(manifest.get("skills") == "./skills/", "manifest must expose ./skills/", errors)
    require(manifest.get("homepage") == PUBLIC_REPOSITORY, "manifest homepage is incorrect", errors)
    require(manifest.get("repository") == PUBLIC_REPOSITORY, "manifest repository is incorrect", errors)
    require(
        manifest.get("license") == "BSD-3-Clause",
        "manifest and LICENSE policy differ",
        errors,
    )
    version = manifest.get("version", "")
    require(isinstance(version, str) and bool(VERSION_PATTERN.fullmatch(version)), "manifest version is not semantic", errors)
    prompts = manifest.get("interface", {}).get("defaultPrompt", [])
    require(isinstance(prompts, list) and 1 <= len(prompts) <= 3, "manifest requires one to three prompts", errors)
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    first_release = re.search(r"^## ([0-9]+\.[0-9]+\.[0-9]+)\b", changelog, re.MULTILINE)
    require(bool(first_release) and first_release.group(1) == version, "CHANGELOG latest release differs from manifest", errors)
    sources = (ROOT / "SOURCES.md").read_text(encoding="utf-8")
    require(len(SHA_PATTERN.findall(sources)) >= 14, "SOURCES.md must pin reviewed repositories", errors)
    require("independent synthesis" in sources.lower(), "SOURCES.md must state provenance model", errors)


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
    validate_manifest_sources_and_version(errors)
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
