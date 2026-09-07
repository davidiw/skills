---
name: durable-workflows
description: Design or correct work that must survive its initiating request, route, process, device opportunity, or provider callback. Use for jobs, imports, sync, AI tasks, background execution, retries, replay, cancellation, coalescing, and successor semantics; not for synchronous CRUD that can safely end with its caller.
---

# Durable Workflows

Own work that must outlive its initiator. Preserve the existing admission and
executor; consult relevant [invariants](../../references/invariants.json) only
when accepted contracts leave a decision unresolved.

1. Name the admission commit after which losing the caller cannot lose accepted
   intent; a wake/timer/UI future is not that commit.
2. Define operation identity, idempotency, protected payload reference, state,
   attempts, checkpoints and terminal result. Persist critical effects atomically
   with the transition; deterministic policy produces declarative effects.
3. Specify applicable retry, timeout, partial-effect, lost-acknowledgment and
   poison-input behavior. Cancellation, leases and compensation require product
   semantics; do not invent states for unsupported behavior.
4. Define coalescing/equivalence and successors. Superseded executors must fence
   commits, acknowledgments and publication. A connectivity wake must preserve
   operation/provider backoff and avoid duplicate admission.
5. Consume [authorization context](../interfaces-and-events/references/authorization-context.md)
   for authority-dependent work and [privacy lifecycle](../data-and-compatibility/references/privacy-lifecycle.md)
   for sensitive retries/late writes. Preserving an existing fence alone does not
   select assurance or another implementation specialist.
6. Bound noninteractive units by rows/pages/bytes/calls/time; yield between
   commits. For constrained pools, consume [resource governance](../architecture-foundations/references/runtime-resource-governance.md).
   Report measured units or truthful coarse phases, never invented percentages.
7. Exercise relevant rows in the [failure matrix](references/failure-matrix.md).
   Request-boundary admission needs process-death and lost-ack tests unless those
   failures are impossible. Owner-focused checks do not require another skill.

Use the [operation template](../../templates/durable-operation.md) only when a
new lifecycle needs recording. A small atomic journal may suffice; do not add a
general job framework. Done means accepted intent survives, replay is idempotent,
and stale executors cannot publish. Apply [precedence](../../references/precedence-and-exceptions.md)
for workflow conflicts.
