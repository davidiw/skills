---
name: security-assurance
description: Review altered or newly exposed trust/authorization boundaries, or inventory the complete release attack surface for launch and external security review. Use changed-path assurance for a named flow or diff and release-surface assurance for a system-wide campaign.
---

# Security Assurance

Find material security defects in the requested scope, including threats
the harness has not named yet. Read the shared
[`assurance review contract`](../../references/assurance-review.md) before review.
Consume the [invariant catalog](../../references/invariants.json); implementation
owners retain normative ownership of their behavior.

## Select mode

- **Changed-path assurance:** review the named flow or diff and the dependencies
  needed to assess it. Preserve existing fences through implementation checks;
  mere presence of credentials or account state does not trigger this review.
- **Release-surface assurance:** for a pre-launch or external security-readiness
  campaign, read [`release-surface.md`](references/release-surface.md). Build the
  externally reachable/trust-boundary inventory and coverage matrix first,
  including unchanged and legacy surfaces, then investigate its hypotheses.

## Investigate scoped paths

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
