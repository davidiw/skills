# Post-Review Adversarial Review

This is one bounded independent challenge after normal exact-revision review,
only for high-risk work named by repository policy.

## Budget

- One pass.
- Ten elapsed minutes or three investigation threads, whichever occurs first.
- At most five findings.
- Diff and immediate dependencies on a concrete execution path only.
- Reuse existing review receipts and evidence. Run focused tests only to prove
  or disprove the current hypothesis.

A thread is one failure hypothesis, its plausible path, and direct validation.
Opening it consumes the budget even if abandoned. Independent evidence
gathering is not a separate allowance.

## Finding threshold

Mark `BLOCK` only when all are present:

1. a plausible execution path introduced or changed by the reviewed diff;
2. evidence that the path violates a named invariant;
3. a material consequence such as corruption, data loss, security or privacy
   breach, incorrect product behavior, or compatibility failure.

Speculative fragility and architecture preference are non-blocking follow-ups.
Report severity and confidence. Compress uninvestigated observations into one
line or omit them.

## Handback

The reviewer changes no files and performs no fixes. Return the exact revision,
threads used, evidence reused, focused commands, and ordered findings. The
author corrects blockers. The new exact revision receives a delta-scoped review
of those corrections, never another general audit.
