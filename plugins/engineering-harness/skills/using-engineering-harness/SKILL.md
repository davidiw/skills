---
name: using-engineering-harness
description: Route engineering changes and bug fixes, including authorization, consent, expiry, sensitive exports, shared contention, and provider contracts; bootstrap/adopt repositories, harden demonstrated friction, and coordinate security/privacy or pre-launch reviews. Keep ordinary edits minimal and load only required owners.
---

# Using Engineering Harness

Use the requested workflow: **bootstrap**, **adopt**, **change**, or **harden**.
Read the target repository's instructions and accepted owner contract. Keep
implementation, integration, and publication within the user's authorization.
For a **design/plan request**, permitted work is inspection, a proposed correction
and synthetic proof. Keep existing production files unchanged. Apply the scope and
primary-owner checkpoints, then return the design; do not enter implementation or
claim corrected-code review. Planned implementation gates remain prospective.

## Review-only shortcut

An already-fresh delegated reviewer with no builder history performs its assigned
review here and reports that context status; do not delegate the same gate again.
Otherwise, for a **release/launch gate or explicit independent review**, the initial agent
coordinates the [handoff](../../references/assurance-handoff.md) before loading any
reviewer body. The fresh reviewer must cover the requested gate itself; delegating
only an adjacent privacy/security lens does not independently review the parent’s lens.
Other required independent gates use the same handoff.
Otherwise, security/authorization review selects [security assurance](../security-assurance/SKILL.md);
privacy/data-lifecycle review selects [privacy assurance](../privacy-assurance/SKILL.md).
For launch/whole-system readiness, use their release inventory mode, including
unchanged paths. A named flow or diff uses changed-path mode. Review only; skip
the builder sequence. Combined reviews use fresh contexts when available.

## Builder sequence — finish each checkpoint before the next

1. **Minimal test.** A local reversible edit inside one accepted owner/contract,
   without changed sensitive semantics, shared contention, durable/external
   effects, or migration, uses the existing edit/test path and finishes. Copy,
   pure parser/library, and static-page changes normally stop here: no specialist,
   scope document, catalog, or assurance. Recheck if the solution broadens.
2. **Inspect before designing.** For other changes, read the short
   [classification and primary-owner route](../../references/change-classification.md).
   Establish the accepted contract before selecting a fix or new state store.
3. **Decide each boundary before edits.** Complete this small table in the task
   record or user-visible checkpoint, **one row per requested behavior/owner**:

   | Behavior and accepted owner/source | Already supported by accepted contract? Evidence | Scope expansion | Approval source and exact limits | Allowed work / blocked boundary |
   | --- | --- | --- | --- | --- |

   `none` requires positive contract evidence and unchanged accepted semantics.
   If the contract excludes the behavior, that row is `pending`. It becomes
   `approved` only when the user has approved a **concrete boundary expansion**;
   repeating the feature request in the approval cell is invalid. Approval of an
   outcome does not approve a new means of crossing an excluded shared boundary.
   A private alternate path/store still expands the owner's responsibility.
   **Do not issue a production-edit tool call for a missing/invalid/pending row.**
   Implement independent `none`/`approved` rows. For pending rows use the compact
   [approval handback](../../references/scope-approval.md): read and complete its
   decision fields before returning pending work. Reuse actual proposal
   approval within its limits; do not ask again for an approved design.
4. **Primary owner first.** Name and read one implementation specialist for the
   unresolved decision in **authorized work** before designing the fix; naming it without reading its
   decision guide does not complete this checkpoint. Add another only for a distinct obligation the primary owner cannot
   resolve; consequential work generally needs at most two before evidence
   justifies more. Read relevant contract sections, not the entire invariant
   catalog. Reuse accepted profile/owner evidence. Record required security/privacy
   gates when semantics change. Do not read security/privacy reviewer `SKILL.md`
   bodies in a builder/design context; those bodies go to the fresh reviewer.
5. **Implement and prove.** Stay inside the recorded boundary. Use focused tests
   at the actual failure seam. When new evidence changes the scope decision,
   return to checkpoint 3 before editing that boundary.
6. **Close recorded gates.** After implementation, obtain required reviews of the
   corrected snapshot in fresh assurance contexts using the
   [review handoff](../../references/assurance-handoff.md). Address findings and
   review corrections before claiming completion. If separate review is unavailable,
   report the pending gate; do not silently substitute builder reasoning.

For **adopt**, use the runtime [profile helper](../../scripts/profile_repository.py)
and [discovery procedure](../../references/profile-discovery.md). For **bootstrap**,
start with architecture foundations; **harden** starts with architecture hardening.
These workflows retain the same scope checkpoint. Before a policy conflict could
stop authorized work, apply [precedence](../../references/precedence-and-exceptions.md).

Before final branch review or integration, apply
[reviewable commits](../verification-and-operations/references/reviewable-commits.md)
and bind subsequent evidence to the resulting exact revision.
