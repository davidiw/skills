---
name: privacy-assurance
description: Review changed sensitive data collection, use, disclosure, derivation, retention, expiry, and erasure, or inventory the complete release data lifecycle for launch and external privacy review. Sensitive data presence alone does not trigger a campaign.
---

# Privacy Assurance

If this context built the change or contains its design reasoning, the next step
is the [fresh-context handoff](../../references/assurance-handoff.md), including
agent-tool discovery. Do not conduct or claim independent review in the builder,
or claim delegation unavailable without checking the deferred tool catalog.

Find material privacy defects across the requested data lifecycle, including
obligations absent from the current harness vocabulary. Read the shared
[`assurance review contract`](../../references/assurance-review.md) before review.
Use relevant accepted data contracts; consult specific [catalog entries](../../references/invariants.json) only
when needed. The data owner retains lifecycle ownership.

## Select mode

- **Changed-path privacy review:** review the named flow or diff when it changes
  collection, use, disclosure, derivation, retention, expiry, or erasure, or when
  review is requested. Preserving those contracts in routine scheduling or
  presentation work stays with its implementation owners.
- **Release data-lifecycle review:** for a pre-launch or external privacy-readiness
  campaign, read [`release-data-lifecycle.md`](references/release-data-lifecycle.md).
  Inventory sensitive data and every destination/processor first, including
  unchanged paths, then build the coverage matrix and investigate each lifecycle.

## Investigate scoped lifecycles

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
