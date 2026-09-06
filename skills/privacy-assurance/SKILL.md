---
name: privacy-assurance
description: Review sensitive data use, derivation, disclosure, retention, expiry, and erasure, including telemetry and delayed writers. Use for consequential privacy-sensitive changes or an explicitly requested privacy assurance review.
---

# Privacy Assurance

Find material privacy defects across the changed data lifecycle, including
obligations absent from the current harness vocabulary. Read the shared
[`assurance review contract`](../../references/assurance-review.md) before review.
Consume the [invariant catalog](../../references/invariants.json); the data owner
retains normative ownership of privacy lifecycle semantics.

1. Follow sensitive source data into each derived representation and recipient.
   Include activity metadata, AI telemetry, logs, audits, caches, and artifacts;
   payload minimization alone does not establish non-sensitivity.
2. Apply the owning
   [`privacy lifecycle`](../data-and-compatibility/references/privacy-lifecycle.md)
   contract. Check purpose, consent, retention, and erasure against repository
   decisions. Demand scoped evidence for exemptions and distinguish an unknown
   policy from an implementation that demonstrably violates one.
3. Trace expiry and erasure through queued, buffered, and concurrent writers.
   Challenge a telemetry flush or reconstruction after removal and a replaced
   identity receiving stale work. Check that erasure revokes future authority.
4. Review disclosure during account, capability, or consent changes, including
   synchronous export stages and temporary outputs. Use the owning
   [`authorization context`](../interfaces-and-events/references/authorization-context.md)
   contract; label already-disclosed data and external erasure limits honestly.
5. Report reachable privacy violations with evidence, impact, confidence, and
   coverage limits even when no invariant names the defect. Do not claim legal
   compliance from this technical review.

For credential or session authority defects, use `security-assurance` at the
shared seam. Before stopping work or changing scope, apply
[`precedence-and-exceptions.md`](../../references/precedence-and-exceptions.md).

The review is complete when every scoped sensitive representation and late
writer has a disposition, and unproven erasure or review coverage is explicit.
