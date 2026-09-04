---
name: architecture-hardening
description: Harden a demonstrated recurring architecture hotspot or run a high-risk post-review adversarial audit. Use when the user explicitly asks to harden, simplify, grill, or audit a concrete hotspot, or repository policy mandates an audit for the current high-risk diff; ordinary implementation and review skip it.
---

# Architecture Hardening

Invoke this skill explicitly for recurring architectural friction or the
high-risk audit named by a repository workflow. Ordinary reviewed changes skip
it.

Choose one mode.

## Hotspot mode

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
6. Add one mechanical boundary or fault test and deliberately violate it to
   prove that it catches the regression.
7. Reassess the original failure. Defer cosmetic decomposition and unrelated
   hotspots.

Read [`hotspot-method.md`](references/hotspot-method.md) before changing a
brownfield boundary.

## Post-review audit mode

Read [`post-review-audit.md`](references/post-review-audit.md) and follow its
budget exactly. The auditor is read-only, performs no correction, and does not
start a recursive audit. Corrections receive exact-revision, delta-scoped
review.

Hotspot mode is complete when the demonstrated coordination cost is lower and
the owning rule rejects a regression. Audit mode is complete when its bounded
report is returned, including an explicit `PASS` or evidence-backed `BLOCK`.
