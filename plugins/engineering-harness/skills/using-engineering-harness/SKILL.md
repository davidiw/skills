---
name: using-engineering-harness
description: Route engineering changes and bug fixes, including authorization, consent, expiry, sensitive exports, shared contention, and provider contracts; bootstrap/adopt repositories, harden demonstrated friction, and coordinate security/privacy or pre-launch reviews. Keep ordinary edits minimal and load only required owners.
---

# Using Engineering Harness

Read repository instructions and the accepted owner contract. Implementation,
integration and publication stay within the user's respective authorization.
**Design/plan requests always keep production unchanged:** inspect, propose and
use synthetic proof; implementation checks/reviews remain prospective.

## Select the path

- **Minimal change:** local and reversible inside one accepted owner/contract,
  without changed sensitive semantics, shared contention, durable/external effects
  or migration. Use existing edits/focused checks and finish. Copy, pure parser/
  library and static-page work normally needs no specialist, scope document,
  catalog or assurance. Reclassify if the solution broadens.
- **Review only:** an already-fresh reviewer without builder history performs its
  assigned gate and records that status; do not delegate it again. Otherwise,
  release/launch gates and required or explicit independent reviews begin with the
  [handoff](../../references/assurance-handoff.md) before any reviewer-body read.
  The child must review the requested gate itself, not merely an adjacent lens.
  Other security/authorization reviews use [security](../security-assurance/SKILL.md);
  privacy/lifecycle reviews use [privacy](../privacy-assurance/SKILL.md). Combined
  reviews use fresh contexts when available. Whole-system reviews cover unchanged
  paths through release inventory mode; named flows/diffs use changed-path mode.
  Keep production unchanged and skip the builder checkpoints.
- **Other change or design:** complete the
  [builder checkpoints](../../references/change-classification.md) in order before
  designing or editing. Material expansion into a shared/cross-cutting responsibility
  or widened accepted contract needs explicit approval of the concrete proposal.
  **No production-edit call for a missing, invalid or pending scope row.** Continue
  independent authorized work.

**Adopt:** use the [profile helper](../../scripts/profile_repository.py) and
[discovery](../../references/profile-discovery.md). **Bootstrap:** start with
architecture foundations. **Harden:** start with architecture hardening.
All three retain the builder scope checkpoint.

Before policy conflict stops authorized work, apply
[precedence](../../references/precedence-and-exceptions.md). Before final branch
review/integration, apply [reviewable commits](../verification-and-operations/references/reviewable-commits.md)
and bind subsequent evidence to the resulting exact revision.
