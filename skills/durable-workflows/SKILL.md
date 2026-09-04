---
name: durable-workflows
description: Design or correct work that must survive its initiating request, route, process, device opportunity, or provider callback. Use for jobs, imports, sync, AI tasks, background execution, retries, replay, cancellation, coalescing, and successor semantics; not for synchronous CRUD that can safely end with its caller.
---

# Durable Workflows

Define the lifecycle before selecting a queue, scheduler, workflow engine, or
database representation.

Use the [invariant catalog](../../references/invariants.json) as normative.
Interpret only entries whose `owner_skill` names this skill; consume other
entries without redefining them.

## Workflow

1. State the admission promise. If the caller may be told "accepted," identify
   the atomic write after which losing that caller cannot lose the intent.
2. Define stable operation identity, authority context, idempotency key,
   payload reference, state, attempt policy, checkpoint, timestamps, and
   terminal result. Store private payloads in their owning protected store, not
   observability or review artifacts.
3. Model domain state plus command or event as a deterministic transition with
   declarative effects. Persist any correctness-critical effect or outbox
   record atomically with the transition.
4. Define retries, duplicate admission, timeout, process death, partial effect,
   lost acknowledgment, poison input, and whether cancellation is supported.
   Do not add a cancellation state when the product has no cancellation
   behavior. Specify which failures may retry and which require operator or
   user action.
5. Define coalescing and successor policy by logical target. A newer intent may
   supersede an older one, but the older executor must fence every commit,
   acknowledgment, and publication after supersession.
6. Capture account, tenant, user, or device authority at admission. Validate it
   before execution and every persistent or externally visible effect.
7. Bound each noninteractive unit by rows, pages, bytes, calls, or time. Yield
   between committed units so interactive work can run after the current unit.
   If the operation holds a constrained runtime pool, consume the
   [`resource admission contract`](../architecture-foundations/references/runtime-resource-governance.md)
   without redefining its admission or reclamation policy.
8. Expose start, truthful coarse phase or measured units, retryability,
   supported cancellation, and terminal state without turning ephemeral UI
   state into the workflow owner. Never synthesize byte or percentage progress
   when the executor cannot measure it.
9. Define expected recovery for the relevant rows of the
   [failure matrix](references/failure-matrix.md). Use
   `verification-and-operations` to execute fault injection and record evidence.
   When admission crosses a request boundary, include process death and a lost
   acknowledgment after the admission commit unless that boundary cannot
   exhibit either failure.
10. Only then choose the smallest adapter that satisfies the
    [operation contract](../../templates/durable-operation.md).

## Guardrails

- A wake event is not durable admission. A timer, widget future, isolate, or
  provider callback may wake the owner but does not become the owner.
- Cancellation, supersession, retention, leases, and compensation are product
  or adapter decisions, not boilerplate states. Mark an unspecified decision
  open or unsupported instead of silently inventing behavior.
- Backoff belongs to the specific operation or provider. Connectivity recovery
  may wake eligible work once; it does not erase operation-specific backoff.
- Last-request-wins requires a stable equivalence key and publication fence;
  wall-clock recency alone is not a correctness rule.
- Do not add a general job framework for a one-time migration when a small
  atomic journal has the required states.

Before stopping work or changing the requested workflow, apply
[`precedence-and-exceptions.md`](../../references/precedence-and-exceptions.md)
and name the exact rule.

The workflow is complete when accepted intent survives termination, every
state is idempotent, stale authority and superseded work cannot commit or
publish, resource units are bounded, and replay tests prove recovery.
