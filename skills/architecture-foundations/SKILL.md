---
name: architecture-foundations
description: Establish or repair system authority, quality scenarios, ownership boundaries, dependency direction, and composition. Use for new subsystems, architecture decisions, boundary changes, or brownfield ownership ambiguity; not for routine local edits within an established owner.
---

# Architecture Foundations

Choose **Design** for a new system or subsystem and **Deepen** for a brownfield
area. Preserve existing architecture sources instead of generating a parallel
document set.

Use the [invariant catalog](../../references/invariants.json) as normative.
Interpret only entries whose `owner_skill` names this skill; consume other
entries without redefining them.

## Workflow

1. Locate product constraints, architecture authority, domain language, and
   current enforcement. Distinguish accepted design from proposals and history.
2. Write observable quality scenarios for the requested behavior. Include the
   stimulus, operating condition, expected response, and measurable bound.
3. Trace at least one success path and each material failure path through UI or
   caller, policy, persistence, external effects, recovery, and publication.
4. Build an ownership map: authoritative facts, canonical behaviors,
   representations, resources, and their writers. Resolve unowned or multiply
   owned state before drawing module boxes.
5. Set allowed dependency directions and identify the composition root.
   Framework, storage, provider, and transport details point inward through
   adapters; deterministic product policy does not point outward to them.
6. Apply a surface budget. Every added interface, state store, event, job,
   compatibility adapter, configuration axis, and generated artifact must name
   its owner, proof, observability, and deletion condition.
7. Select one end-to-end slice that proves the boundary. Generalize only after
   the slice exposes a repeated shape.
8. Move each important rule to the appropriate rung in the
   [enforcement ladder](../../references/enforcement-ladder.md). Install cheap,
   deterministic enforcement when declaring a foundational boundary. Use
   `verification-and-operations` for adversarial, fault, physical, or
   exact-revision proof.

For scenario and ownership formats, read
[`quality-and-ownership.md`](references/quality-and-ownership.md). In an
existing complex area, also read
[`brownfield-deepening.md`](references/brownfield-deepening.md).

## Guardrails

- Business capability and state ownership determine boundaries; file size and
  framework conventions are only signals.
- A process or service split requires independent lifecycle, failure,
  deployment, scaling, or trust needs. Replaceability alone does not justify it.
- Ordinary CRUD uses validation and an aggregate boundary; formal state
  machines serve meaningful transitions, replay, or recovery.
- Prefer deleting a duplicate path or representation before wrapping both in a
  new abstraction.

Before stopping work or changing the requested workflow, apply
[`precedence-and-exceptions.md`](../../references/precedence-and-exceptions.md)
and name the exact rule.

The work is complete when every changed fact, behavior, representation, and
effect has one owner; dependency direction and composition are explicit; the
selected slice works through failure and recovery; and no speculative surface
was added.
