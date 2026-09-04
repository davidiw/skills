#!/usr/bin/env python3
"""Validate an engineering-harness profile without third-party packages."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNGS = {
    "principle",
    "owner",
    "audit",
    "local_check",
    "ci_check",
    "runtime_guard",
    "fault_test",
}


def _require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_profile(document: Any) -> list[str]:
    errors: list[str] = []
    _require(isinstance(document, dict), "profile must be a JSON object", errors)
    if not isinstance(document, dict):
        return errors

    _require(document.get("schema_version") == 1, "schema_version must be 1", errors)
    project = document.get("project")
    _require(isinstance(project, dict), "project must be an object", errors)
    if isinstance(project, dict):
        _require(isinstance(project.get("name"), str) and bool(project["name"]), "project.name is required", errors)
        _require(isinstance(project.get("kind"), str) and bool(project["kind"]), "project.kind is required", errors)
        _require(isinstance(project.get("sensitive_data"), bool), "project.sensitive_data must be boolean", errors)

    sources = document.get("sources")
    _require(isinstance(sources, dict), "sources must be an object", errors)
    if isinstance(sources, dict):
        for key, value in sources.items():
            _require(isinstance(key, str) and isinstance(value, str) and bool(value), f"sources.{key} must be a nonempty string", errors)

    capabilities = document.get("capabilities")
    _require(isinstance(capabilities, dict), "capabilities must be an object", errors)
    if isinstance(capabilities, dict):
        for key, value in capabilities.items():
            _require(isinstance(value, bool), f"capabilities.{key} must be boolean", errors)

    catalog = json.loads((ROOT / "references" / "invariants.json").read_text(encoding="utf-8"))
    known_ids = {item["id"] for item in catalog["invariants"]}
    enforcement = document.get("enforcement")
    _require(isinstance(enforcement, dict), "enforcement must be an object", errors)
    if isinstance(enforcement, dict):
        for invariant_id, entry in enforcement.items():
            _require(invariant_id in known_ids, f"unknown invariant: {invariant_id}", errors)
            _require(isinstance(entry, dict), f"enforcement.{invariant_id} must be an object", errors)
            if not isinstance(entry, dict):
                continue
            _require(entry.get("rung") in RUNGS, f"enforcement.{invariant_id}.rung is invalid", errors)
            _require(isinstance(entry.get("owner"), str) and bool(entry["owner"]), f"enforcement.{invariant_id}.owner is required", errors)
            artifacts = entry.get("artifacts", [])
            _require(isinstance(artifacts, list) and all(isinstance(value, str) and value for value in artifacts), f"enforcement.{invariant_id}.artifacts must be strings", errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {Path(argv[0]).name} <engineering-harness.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"{path}: {error}", file=sys.stderr)
        return 1
    errors = validate_profile(document)
    if errors:
        for error in errors:
            print(f"{path}: {error}", file=sys.stderr)
        return 1
    print(f"valid: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
