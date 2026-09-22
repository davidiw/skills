# Pre-Acceptance Adversarial Review

This is one bounded independent challenge after focused evidence and cheap
preflight but before a costly matrix or final exact-head acceptance, only for
high-risk work named by repository policy. Security/privacy assurance
uses [`assurance-review.md`](../../../references/assurance-review.md); its
coverage is not capped by this architecture-audit budget.

Use the [independent handoff](../../../references/assurance-handoff.md) for actual
context separation, packet reuse, complete known blockers, delta review and
initial-review misses. Correct the complete blocker set, delta-review the
affected seams, freeze the resulting candidate, and run one final exact-head
acceptance. A cheap preflight failure prevents the costly matrix from starting.

## Budget

- One pass.
- Ten elapsed minutes or three investigation threads, whichever occurs first.
- Investigate within the budget; return every currently known blocker.
- Diff and immediate dependencies on a concrete execution path only.
- Reuse existing review receipts and evidence. Run focused tests only to prove
  or disprove the current hypothesis.

A thread is one failure hypothesis, its plausible path, and direct validation.
Opening it consumes the budget even if abandoned. Independent evidence
gathering is not a separate allowance.

## Finding threshold

Mark `BLOCK` only when all are present:

1. a plausible execution path introduced or changed by the reviewed diff;
2. evidence that the path violates a named invariant, repository requirement,
   or explicitly described security/privacy obligation, including a newly
   identified threat absent from the catalog;
3. a material consequence such as corruption, data loss, security or privacy
   breach, incorrect product behavior, or compatibility failure.

Speculative fragility and architecture preference are non-blocking follow-ups.
Absence of an invariant ID does not downgrade an evidenced material defect.
Report severity and confidence. Mark uninvestigated areas explicitly; do not silently imply coverage.

## Handback

The reviewer changes no files and performs no fixes. Return the exact revision,
threads used, evidence reused, focused commands, and ordered findings. The
author corrects blockers in one batch. The new exact revision receives a
delta-scoped review of corrections, directly affected seams and regressions,
then freezes for one final exact-head acceptance. Reopen unchanged scope only
for expanded scope, invalidated assumptions or newly reachable surfaces. A final
acceptance blocker still requires affected checks after its correction.
