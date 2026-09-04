# Harness Versioning

`.codex-plugin/plugin.json` is the authoritative Engineering Harness version.
Projects record that value as `harness_policy_version`; evaluation and evidence
receipts record it as the policy version under which the result was produced.

Engineering Harness uses semantic versions:

- **Patch:** corrections that do not change invariant meaning, activation,
  routing, profile interpretation, or required evidence.
- **Minor:** additive compatible capabilities, detectors, templates, evals, or
  guidance. Before 1.0, a behavior-changing policy or schema correction also
  increments the minor version and requires migration notes.
- **Major:** after 1.0, any removal, rename, or changed meaning of an invariant;
  newly mandatory activation or enforcement for existing profiles; incompatible
  profile/schema changes; or changed authorization and evidence semantics.

Every release has a `CHANGELOG.md` entry. Behavior-changing entries identify
affected invariants, activation rules, profiles, or enforcement and include a
bounded migration. Profile drift accepts patch differences. It requires review
and migration when the policy release line changes: major after 1.0, or minor
while the package remains 0.x.

Public releases use immutable `v<version>` Git tags matching the plugin
manifest. Stable installation instructions pin that tag. `main` remains the
explicit development/nightly channel and is never cited as immutable evidence.
Creating or pushing a tag and publishing a release remain separately authorized
actions.

Historical evidence remains valid for the exact policy version it names; it is
not silently upgraded to satisfy a newer policy.
