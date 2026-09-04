#!/usr/bin/env python3
"""Validate Engineering Harness structure, routing, and generated artifacts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from render_invariants import OUTPUT, render
from validate_profile import validate_profile


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "using-engineering-harness",
    "architecture-foundations",
    "durable-workflows",
    "interfaces-and-events",
    "application-composition",
    "data-and-compatibility",
    "architecture-hardening",
    "verification-and-operations",
}
EXPLICIT_ONLY = {"using-engineering-harness", "architecture-hardening"}
RUNGS = {
    "principle",
    "owner",
    "audit",
    "local_check",
    "ci_check",
    "runtime_guard",
    "fault_test",
}
LINK_PATTERN = re.compile(r"\[[^]]+\]\(([^)]+)\)")
SHA_PATTERN = re.compile(r"`[0-9a-f]{40}`")


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
        require((path.parent / target_path).resolve().exists(), f"{path}: broken link {target}", errors)


def validate_skills(errors: list[str]) -> None:
    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    names = {path.parent.name for path in skill_files}
    require(names == EXPECTED_SKILLS, f"skill set mismatch: {sorted(names)}", errors)
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
        validate_links(path, errors)
        for reference in (path.parent / "references").glob("*.md"):
            validate_links(reference, errors)


def validate_invariants(errors: list[str]) -> None:
    path = ROOT / "references" / "invariants.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    require(document.get("schema_version") == 1, "invariant schema_version must be 1", errors)
    invariants = document.get("invariants", [])
    require(len(invariants) == 20, "the initial constitution must contain 20 invariants", errors)
    ids: set[str] = set()
    for item in invariants:
        invariant_id = item.get("id")
        require(isinstance(invariant_id, str) and bool(invariant_id), "invariant id is required", errors)
        require(invariant_id not in ids, f"duplicate invariant: {invariant_id}", errors)
        ids.add(invariant_id)
        require(bool(item.get("statement")), f"{invariant_id}: statement is required", errors)
        require(bool(item.get("activates_when")), f"{invariant_id}: activation is required", errors)
        require(item.get("default_rung") in RUNGS, f"{invariant_id}: invalid default rung", errors)
        skills = item.get("skills", [])
        require(bool(skills) and set(skills) <= EXPECTED_SKILLS, f"{invariant_id}: invalid skill owner", errors)
    require(OUTPUT.exists() and OUTPUT.read_text(encoding="utf-8") == render(), "generated invariant documentation is stale", errors)


def validate_profiles(errors: list[str]) -> None:
    for path in sorted((ROOT / "templates").glob("project-profile.*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        for error in validate_profile(document):
            errors.append(f"{path}: {error}")


def validate_evals(errors: list[str]) -> None:
    path = ROOT / "evals" / "cases.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    require(document.get("schema_version") == 1, "eval schema_version must be 1", errors)
    require(document.get("rubric_version") == 1, "eval rubric_version must be 1", errors)
    cases = document.get("cases", [])
    require(len(cases) >= 10, "at least ten evaluation cases are required", errors)
    ids: set[str] = set()
    classes = {"minimal", "bounded", "consequential", "stabilization"}
    for case in cases:
        case_id = case.get("id")
        require(isinstance(case_id, str) and bool(case_id), "eval case id is required", errors)
        require(case_id not in ids, f"duplicate eval case: {case_id}", errors)
        ids.add(case_id)
        require(case.get("expected_class") in classes, f"{case_id}: invalid class", errors)
        skills = case.get("expected_skills", [])
        require(bool(skills) and skills[0] == "using-engineering-harness", f"{case_id}: router must be first", errors)
        require(set(skills) <= EXPECTED_SKILLS, f"{case_id}: unknown skill", errors)
        require(len(case.get("required_outcomes", [])) >= 2, f"{case_id}: requires two outcomes", errors)
        require(bool(case.get("forbidden_outcomes")), f"{case_id}: forbidden outcomes required", errors)
        fixture = case.get("fixture")
        if fixture is not None:
            fixture_path = (path.parent / fixture).resolve()
            require(fixture_path.is_dir(), f"{case_id}: fixture directory is missing", errors)
            require((fixture_path / "AGENTS.md").is_file(), f"{case_id}: fixture AGENTS.md is missing", errors)


def validate_manifest_and_sources(errors: list[str]) -> None:
    manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    require(manifest.get("name") == "engineering-harness", "unexpected plugin name", errors)
    require(manifest.get("skills") == "./skills/", "manifest must expose ./skills/", errors)
    require(manifest.get("license") == "UNLICENSED", "manifest and LICENSE policy differ", errors)
    prompts = manifest.get("interface", {}).get("defaultPrompt", [])
    require(isinstance(prompts, list) and 1 <= len(prompts) <= 3, "manifest requires one to three prompts", errors)
    sources = (ROOT / "SOURCES.md").read_text(encoding="utf-8")
    require(len(SHA_PATTERN.findall(sources)) >= 14, "SOURCES.md must pin reviewed repositories", errors)


def main() -> int:
    errors: list[str] = []
    validate_manifest_and_sources(errors)
    validate_skills(errors)
    validate_invariants(errors)
    validate_profiles(errors)
    validate_evals(errors)
    for path in [ROOT / "README.md", ROOT / "SOURCES.md"]:
        validate_links(path, errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("engineering-harness package is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
