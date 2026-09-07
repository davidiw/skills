---
name: architecture-foundations
description: Establish or repair system authority, quality scenarios, ownership boundaries, dependency direction, composition, and scarce runtime-resource admission. Use for new subsystems, architecture decisions, boundary changes, constrained resource pools, or brownfield ownership ambiguity; not for routine local edits within an established owner.
---

# Architecture Foundations

Own new/ambiguous responsibility, dependency direction and shared-resource
contention. Use accepted architecture; consult relevant [invariants](../../references/invariants.json)
only when interpretation is unresolved. Do not redesign an established owner
merely to name it. The router's pre-edit scope decision applies before choosing
new shared state, protocols or configuration.

1. Name the observable outcome, accepted owner/contract and approved scope.
   Resolve competing writers or unowned state before selecting module boundaries.
2. Trace success and material failure through policy, state and effects. Define
   a measurable response under the relevant operating condition.
3. Keep domain policy inward of framework/provider/storage adapters; name the
   composition root and each added surface's owner, proof and removal condition.
4. For scarce pools or optional work blocking critical progress, read
   [resource governance](references/runtime-resource-governance.md). Preserve its
   applicable finite-pool/per-activity contracts. For serialized contention,
   execute the incumbent-writer proof: another optional writer is stalled holding
   the resource **before** the critical action starts; critical commit must finish
   by a bounded deadline while that writer remains stalled. Omission of this
   invocation's audit callback is not that proof.
5. Prove one small slice and add recurrence checks at its seam. Delete duplicate
   state/paths before introducing abstraction. Separate local/fake evidence from
   unexecuted physical or deployment proof.

Read [quality/ownership](references/quality-and-ownership.md) for a new design's
scenario formats; [brownfield deepening](references/brownfield-deepening.md) when
existing ownership is unclear. Use verification only for an independent campaign
or exact/physical gate, not ordinary focused tests.

Done means one owner per changed fact/effect, demonstrated failure behavior and
no unapproved shared surface. Apply [precedence](../../references/precedence-and-exceptions.md)
if a policy conflict changes the authorized workflow.
