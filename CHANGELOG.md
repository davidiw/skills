# Changelog

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
