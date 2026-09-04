---
name: architecture-hardening
description: Find and repair demonstrated architecture divergence or recurring-friction hotspots through consolidation and recurrence prevention. Use when the user asks to harden, simplify, or grill a concrete hotspot; ordinary implementation, routine review, and adversarial proof use other workflows.
---

# Architecture Hardening

Invoke this skill for demonstrated architecture divergence or recurring
friction. Ordinary reviewed changes skip it. Verification and operations owns
adversarial review, fault injection, physical proof, and exact-revision evidence.

Use the [invariant catalog](../../references/invariants.json) as normative.
This skill consumes named invariants to find divergence; it does not redefine
their meaning.

## Workflow

1. Name the repeated failure, violated invariant, confirmed execution path,
   and current owner. Use incidents, churn, duplicated semantics, or repeated
   guards as evidence; file size alone is insufficient.
2. Freeze the bounded outcome and non-goals. Characterize current behavior at
   the owning seam, including the relevant failure path.
3. Test deletion before abstraction: remove a duplicate entry point,
   representation, compatibility path, or coordination state in the fixture.
4. If another generation token, persisted representation, mutation path, or
   cross-layer exception appears necessary, stop at a **fragility checkpoint**.
   Present the smallest simplifying options and their compatibility cost to the
   repository owner rather than burning cycles around the surface.
5. Move one vertical slice to one clear owner. Keep production writers
   serialized where they share state; parallelize independent evidence and
   disjoint modules.
6. Define the narrowest recurrence prevention at the repaired boundary. Install
   cheap deterministic enforcement when the boundary is introduced; request
   risk-proportional adversarial or fault evidence through
   `verification-and-operations`.
7. Reassess the original failure. Defer cosmetic decomposition and unrelated
   hotspots.

Read [`hotspot-method.md`](references/hotspot-method.md) before changing a
brownfield boundary.

Before stopping work or changing the requested workflow, apply
[`precedence-and-exceptions.md`](../../references/precedence-and-exceptions.md)
and name the exact rule.

Hardening is complete when demonstrated coordination cost is lower, one owner
governs the repaired path, and proportional recurrence prevention exists.
