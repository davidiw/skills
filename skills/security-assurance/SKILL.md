---
name: security-assurance
description: Review changed authorization and trust boundaries for exploitable behavior, including session confusion, purpose-scoped credentials, mutable grants, and blocked critical actions. Use for consequential security-sensitive changes or an explicitly requested security assurance review.
---

# Security Assurance

Find material security defects in the changed execution paths, including threats
the harness has not named yet. Read the shared
[`assurance review contract`](../../references/assurance-review.md) before review.
Consume the [invariant catalog](../../references/invariants.json); implementation
owners retain normative ownership of their behavior.

1. Identify assets, principals, entry points, trust assumptions, and the
   attacker-controlled inputs or timing on the requested path.
2. Trace credential issuance, audience, purpose, use, exchange, and revocation.
   Check whether a handoff or provider credential can accidentally establish a
   broader session. Apply the owning
   [`authorization context`](../interfaces-and-events/references/authorization-context.md)
   contract to sensitive reads and effects, including synchronous operations.
3. Challenge revocation and expiry during waits, callbacks, and multi-stage
   effects. Test the check/use boundary and stale result publication, not just
   rejection at entry.
4. Follow dependencies of critical actions such as revocation. Determine whether
   optional audit or telemetry can block them through locks, transactions,
   connection pools, or queues. Required audit behavior needs an explicit
   failure contract; do not assume all audit is optional.
5. Prove or disprove concrete hypotheses with the smallest focused checks.
   Report newly identified vulnerabilities even without an invariant ID, with
   prerequisites, consequence, confidence, and coverage limits.

For sensitive retention or erasure consequences, use `privacy-assurance` at the
shared seam. Before stopping work or changing scope, apply
[`precedence-and-exceptions.md`](../../references/precedence-and-exceptions.md).

The review is complete when the scoped threats have dispositions and evidence,
and any remaining required coverage or independent review is explicit.
