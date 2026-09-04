# Changelog

## 0.3.2 - 2026-09-04

- Document the verified GitHub marketplace installation flow.
- Clarify that local installation requires the checkout root rather than its
  parent directory, and validate that both installation commands remain
  discoverable.

No profile migration is required because package policy is unchanged.

## 0.3.1 - 2026-09-04

- Add a repository-local Codex marketplace that exposes the root
  `engineering-harness` plugin.
- Validate marketplace metadata against the plugin manifest and public package
  contract.

No profile migration is required because invariant, activation, routing, and
evidence semantics are unchanged.

## 0.3.0 - 2026-09-04

- Correct the public package URLs for the `davidiw/skills` repository.
- Restrict multiple-client discovery to consumer surfaces rather than backend
  `server` and `api` roots.
- Require a generated marker or combined generator/output evidence instead of
  treating ordinary rendering code as a generated artifact.
- Ignore standard CMake build and fetched-dependency trees during discovery.
- Reserve physical-device discovery for hardware, firmware, and physical design
  evidence rather than Android or iOS scaffolding alone.
- Add false-positive regression tests for all three detector corrections.

Migration from 0.2.x:

1. rerun profile drift or generate a fresh proposal with scanner version 2;
2. review changed detector evidence against repository facts;
3. do not automatically disable an accepted capability merely because a
   heuristic no longer detects it.

## 0.2.0 - 2026-09-04

- Consolidate every invariant under one normative owner skill and distinguish
  consuming skills.
- Replace public specialist selection with `bootstrap`, `adopt`, `change`, and
  `harden` workflows.
- Add evidence-backed profile discovery, accepted-profile drift checks, scoped
  invariant exceptions, and harness policy versioning.
- Move adversarial review, fault injection, and exact proof from architecture
  hardening to verification and operations.
- Expand deterministic proportionality and public-package validation.
- License the package under the permissive BSD 3-Clause license.

Migration from 0.1.x:

1. replace invariant `skills` arrays with `owner_skill` and `consumed_by`;
2. update project profiles to schema 2 with `harness_policy_version`, `status`,
   and `exceptions`;
3. review generated capability proposals before accepting them;
4. route adversarial review and fault evidence through
   `verification-and-operations`.

## 0.1.0 - 2026-09-04

- Initial staged Engineering Harness package.
