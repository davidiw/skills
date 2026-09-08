---
name: architecture-hardening
description: Find and repair demonstrated architecture divergence or recurring-friction hotspots through consolidation and recurrence prevention. Use when the user asks to harden, simplify, or grill a concrete hotspot; ordinary implementation, routine review, and adversarial proof use other workflows.
---

# Architecture Hardening

Own demonstrated recurring divergence, not ordinary change review. Use accepted
contracts and specific [invariants](../../references/invariants.json) as evidence;
their owners retain normative interpretation.

1. Name the repeated failure, confirmed path and current owner from incidents,
   duplicated semantics or repeated guards. File size alone is insufficient.
2. Freeze the bounded outcome/non-goals. Apply the [scope gate](../../references/change-classification.md#scope-expansion-gate)
   before an adjacent discovery expands the repair; characterize the failure.
3. Read [hotspot method](references/hotspot-method.md). Test deletion of duplicate
   paths, representations or coordination state before adding abstraction.
4. If another token/store/mutation path/exception seems necessary, expose the
   smallest simplifying options and compatibility costs before implementing an
   unapproved expansion. Move one slice to one owner; serialize shared writers.
5. For a reusable engineering lesson, apply
   [methodology ownership](../verification-and-operations/references/methodology.md)
   in a separately authorized slice. Add narrow recurrence prevention and recheck the original failure. Use a
   separate verification campaign only when risk or repository policy calls for
   it. Defer cosmetic decomposition and unrelated hotspots.

Done means lower demonstrated coordination cost and one owner at the repaired
seam. Apply [precedence](../../references/precedence-and-exceptions.md) before a
workflow-changing stop.
