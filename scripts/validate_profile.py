#!/usr/bin/env python3
"""Validate an Engineering Harness profile without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACTIVATION_PATH = ROOT / "references" / "capability-activation.json"
CATALOG_PATH = ROOT / "references" / "invariants.json"
SCHEMA_PATH = ROOT / "references" / "project-profile.schema.json"
PROFILE_SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
VERSION_PATTERN = re.compile(
    PROFILE_SCHEMA["properties"]["harness_policy_version"]["pattern"]
)
MECHANICAL_RUNGS = {"local_check", "ci_check", "runtime_guard", "fault_test"}


def _require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def _is_type(value: Any, expected: str) -> bool:
    return {
        "array": lambda: isinstance(value, list),
        "boolean": lambda: isinstance(value, bool),
        "integer": lambda: isinstance(value, int) and not isinstance(value, bool),
        "number": lambda: isinstance(value, (int, float)) and not isinstance(value, bool),
        "object": lambda: isinstance(value, dict),
        "string": lambda: isinstance(value, str),
    }[expected]()


def _resolve_ref(root_schema: dict[str, Any], reference: str) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError(f"unsupported schema reference: {reference}")
    value: Any = root_schema
    for part in reference[2:].split("/"):
        value = value[part.replace("~1", "/").replace("~0", "~")]
    if not isinstance(value, dict):
        raise ValueError(f"schema reference is not an object: {reference}")
    return value


def _validate_schema(
    value: Any,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    path: str,
    errors: list[str],
) -> None:
    if "$ref" in schema:
        _validate_schema(value, _resolve_ref(root_schema, schema["$ref"]), root_schema, path, errors)
        return
    label = path or "profile"
    if "const" in schema:
        _require(value == schema["const"], f"{label} must equal {schema['const']}", errors)
    if "enum" in schema:
        _require(value in schema["enum"], f"{label} is invalid", errors)
    expected_type = schema.get("type")
    if expected_type:
        valid_type = _is_type(value, expected_type)
        _require(valid_type, f"{label} must be {expected_type}", errors)
        if not valid_type:
            return
    if isinstance(value, str):
        if "minLength" in schema:
            _require(len(value) >= schema["minLength"], f"{label} is too short", errors)
        if "pattern" in schema:
            _require(bool(re.fullmatch(schema["pattern"], value)), f"{label} has invalid format", errors)
    if isinstance(value, list):
        if schema.get("uniqueItems"):
            encoded = [json.dumps(item, sort_keys=True) for item in value]
            _require(len(encoded) == len(set(encoded)), f"{label} must contain unique items", errors)
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                _validate_schema(item, item_schema, root_schema, f"{path}[{index}]", errors)
    if not isinstance(value, dict):
        return

    properties = schema.get("properties", {})
    required = schema.get("required", [])
    for key in required:
        _require(key in value, f"{label}: missing field {key}", errors)
    additional = schema.get("additionalProperties", True)
    for key, item in value.items():
        child_path = f"{path}.{key}" if path else key
        if "propertyNames" in schema and "pattern" in schema["propertyNames"]:
            _require(
                bool(re.fullmatch(schema["propertyNames"]["pattern"], key)),
                f"{child_path}: invalid field name",
                errors,
            )
        if key in properties:
            _validate_schema(item, properties[key], root_schema, child_path, errors)
        elif additional is False:
            errors.append(f"{label}: unknown field {key}")
        elif isinstance(additional, dict):
            _validate_schema(item, additional, root_schema, child_path, errors)


def _relative_path(value: str) -> bool:
    without_fragment = value.split("#", 1)[0]
    path = Path(without_fragment[2:] if without_fragment.startswith("./") else without_fragment)
    return not path.is_absolute() and ".." not in path.parts


def validate_profile(document: Any) -> list[str]:
    errors: list[str] = []
    _validate_schema(document, PROFILE_SCHEMA, PROFILE_SCHEMA, "", errors)
    if not isinstance(document, dict):
        return errors

    activation = json.loads(ACTIVATION_PATH.read_text(encoding="utf-8"))
    catalog_document = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    catalog = {item["id"]: item for item in catalog_document["invariants"]}
    known_ids = set(catalog)
    known_capabilities = set(activation["capabilities"])
    status = document.get("status")
    project = document.get("project")
    sources = document.get("sources")
    capabilities = document.get("capabilities")
    enforcement = document.get("enforcement")
    exceptions = document.get("exceptions")

    if isinstance(sources, dict):
        for key, value in sources.items():
            if isinstance(value, str) and value:
                _require(_relative_path(value), f"sources.{key} must be repository-relative", errors)

    if isinstance(capabilities, dict):
        _require(
            set(capabilities) == known_capabilities,
            "capabilities must exactly match capability-activation.json",
            errors,
        )

    exception_ids: set[str] = set()
    exception_keys: set[tuple[str, str]] = set()
    if isinstance(exceptions, list):
        for index, entry in enumerate(exceptions):
            if not isinstance(entry, dict):
                continue
            invariant_id = entry.get("invariant")
            scope = entry.get("scope")
            _require(invariant_id in known_ids, f"exceptions[{index}].invariant is unknown", errors)
            if isinstance(invariant_id, str):
                exception_ids.add(invariant_id)
            if isinstance(invariant_id, str) and isinstance(scope, str):
                key = (invariant_id, scope)
                _require(key not in exception_keys, f"duplicate exception: {invariant_id} {scope}", errors)
                exception_keys.add(key)

    if isinstance(enforcement, dict):
        for invariant_id, entry in enforcement.items():
            _require(invariant_id in known_ids, f"unknown invariant: {invariant_id}", errors)
            if not isinstance(entry, dict):
                continue
            owner = entry.get("owner")
            if status == "accepted":
                _require(owner != "review-required", f"enforcement.{invariant_id}.owner requires review", errors)

        required_invariants = set(activation["always"])
        if isinstance(project, dict):
            for field, invariant_ids in activation.get("project_fields", {}).items():
                if project.get(field) is True:
                    required_invariants.update(invariant_ids)
        if isinstance(capabilities, dict):
            for capability, invariant_ids in activation["capabilities"].items():
                if capabilities.get(capability) is True:
                    required_invariants.update(invariant_ids)
        for invariant_id in sorted(required_invariants - set(enforcement)):
            errors.append(f"missing enforcement for active invariant: {invariant_id}")
        if status == "accepted":
            for invariant_id in sorted(known_ids & set(enforcement)):
                item = catalog[invariant_id]
                rung = enforcement[invariant_id].get("rung")
                if (
                    item["enforcement_timing"] == "boundary_introduction"
                    and rung not in MECHANICAL_RUNGS
                    and invariant_id not in exception_ids
                ):
                    errors.append(
                        f"active foundational boundary lacks mechanical enforcement or exception: {invariant_id}"
                    )
            for invariant_id in sorted(exception_ids - set(enforcement)):
                errors.append(f"exception requires active enforcement entry: {invariant_id}")

    discovery = document.get("discovery")
    if isinstance(discovery, dict):
        found_capabilities = discovery.get("capabilities")
        _require(
            isinstance(found_capabilities, dict) and set(found_capabilities) == known_capabilities,
            "discovery.capabilities must exactly match capability-activation.json",
            errors,
        )
        findings: list[tuple[str, Any]] = []
        fields = discovery.get("project_fields")
        if isinstance(fields, dict):
            findings.extend((f"discovery.project_fields.{name}", item) for name, item in fields.items())
        if isinstance(found_capabilities, dict):
            findings.extend((f"discovery.capabilities.{name}", item) for name, item in found_capabilities.items())
        for prefix, finding in findings:
            if not isinstance(finding, dict):
                continue
            evidence = finding.get("evidence")
            if not isinstance(evidence, list):
                continue
            if "review" in finding:
                _require(bool(evidence), f"{prefix}.review requires evidence", errors)
                _require(
                    all(isinstance(item, dict) and bool(item.get("sha256")) for item in evidence),
                    f"{prefix}.review requires content hashes", errors,
                )
                _require(finding.get("suggested") is True,
                         f"{prefix}.review requires a positive detection", errors)
                name = prefix.rsplit(".", 1)[1]
                decision_owner = project if prefix.startswith("discovery.project_fields.") else capabilities
                recorded = decision_owner.get(name) if isinstance(decision_owner, dict) else None
                _require(recorded is False, f"{prefix}.review conflicts with enabled decision", errors)
            for index, item in enumerate(evidence):
                if isinstance(item, dict) and isinstance(item.get("path"), str):
                    _require(
                        _relative_path(item["path"]),
                        f"{prefix}.evidence[{index}].path must be relative",
                        errors,
                    )
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
