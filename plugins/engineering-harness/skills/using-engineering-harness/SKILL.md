---
name: using-engineering-harness
description: "Route engineering changes, debugging, code review, domain/architecture decisions and cross-cutting methodology: evidence standards, testing infrastructure, review/safety/compatibility policy, and reusable harness behavior. Adopt repositories, harden friction, and coordinate security/privacy or UX/UI/brand reviews. Keep ordinary fixes minimal."
---

# Using Engineering Harness

Read repository instructions and the accepted owner contract. For consequential
work, discover its canonical policy and enforcement owner through
`engineering-harness.json`; a task need not name this skill. Implementation,
integration and publication stay within the user's respective authorization.
Harness owns the engineering workflow; use other skills only for a distinct
utility or an explicit user/repository requirement, not a second overlapping
workflow. Their tools do not choose scope, owners or review gates.
**Design/plan requests always keep production unchanged:** inspect, propose and
use synthetic proof; implementation checks/reviews remain prospective.

## Select the path

- **Minimal change:** local and reversible inside one accepted owner/contract,
  with settled experience intent and without changed sensitive semantics, shared
  contention, durable/external effects or migration. Use existing edits/focused checks
  and finish. Copy, pure parser/library and static-page work normally needs no specialist, scope document,
  catalog or assurance. Reclassify if the solution broadens.
  If the cause remains unresolved, use the conditional
  [diagnosis method](../verification-and-operations/references/diagnosis.md);
  reading a method does not require its owner skill or an architecture exercise.
- **Review only:** an already-fresh reviewer without builder history performs its
  assigned gate and records that status; do not delegate it again. Otherwise,
  release/launch gates and required or explicit independent reviews begin with the
  [handoff](../../references/assurance-handoff.md) before any reviewer-body read.
  The child must review the requested gate itself, not merely an adjacent lens.
  Other security/authorization reviews use [security](../security-assurance/SKILL.md);
  privacy/lifecycle reviews use [privacy](../privacy-assurance/SKILL.md). Combined
  reviews use fresh contexts when available. Whole-system reviews cover unchanged
  paths through release inventory mode; named flows/diffs use changed-path mode.
  For engineering-methodology or performance-evidence assessment, use
  [verification and operations](../verification-and-operations/SKILL.md).
  For UX/UI/brand critique, select the [experience owner](../../references/experience-routing.md).
  Other code reviews use the [change-review method](../verification-and-operations/references/change-review.md).
  Keep production unchanged and skip the builder checkpoints.
- **Other change or design:** complete the
  [builder checkpoints](../../references/change-classification.md) in order before
  designing or editing. Material expansion into a shared/cross-cutting responsibility
  or widened accepted contract needs explicit approval of the concrete proposal.
  **No production-edit call for a missing, invalid or pending scope row.** Continue
  independent authorized work. For decomposable authorized execution, use the
  builder's bounded worker assignment rather than making the coordinator repeat
  worker search, edits, or long commands.

**Adopt:** use the [profile helper](../../scripts/profile_repository.py) and
[discovery](../../references/profile-discovery.md). **Bootstrap:** start with
architecture foundations. **Harden:** start with architecture hardening.
All three retain the builder scope checkpoint.

Before policy conflict stops authorized work, apply
[precedence](../../references/precedence-and-exceptions.md). When the user or
repository authorizes PR delivery, including a standing user preference, apply
[PR delivery](../verification-and-operations/references/reviewable-commits.md#pr-delivery)
at the first coherent commit. Before final branch
review/integration, apply [reviewable commits](../verification-and-operations/references/reviewable-commits.md)
and bind subsequent evidence to the resulting exact revision.
