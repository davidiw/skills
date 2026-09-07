---
name: data-and-compatibility
description: Evolve persistent or replicated data and sensitive data lifecycles safely. Use for sync, identity, migration, repair, mixed versions, or privacy inheritance, retention, expiry, erasure, and delayed writers across data and telemetry.
---

# Data and Compatibility

Own persistent/replicated identity, migrations, retention, erasure and online
repair. Use accepted data contracts and profiles; consult relevant
[invariants](../../references/invariants.json) only when unresolved.

1. Identify canonical state and every writer, projection and cache on the changed
   path. Define non-authoritative rebuild/invalidation and stable identity.
2. For changed sensitive derivation, disclosure, retention or deletion, read
   [privacy lifecycle](references/privacy-lifecycle.md). Trace metadata and delayed
   writers: erasure revokes future authority. Record required privacy/security
   gates for post-build review, without loading their bodies into the builder.
3. For replicated forms, read [reconciliation](references/representations-and-reconciliation.md).
   Remote absence alone is not deletion; require explicit destructive semantics
   or verified lossless movement of the same identity.
4. For version evolution, read [migrations](references/compatibility-and-migrations.md).
   Identify supported deployed readers/writers and rollback tools from evidence;
   make authority transfer idempotent, interruption-safe and validated. Do not
   support hypothetical predecessors or infer compatibility from version numbers.
5. For live correction, read [repair](references/live-repair.md): bounded selection,
   stable identity, compare-and-set, checkpoints and live-writer conflict handling.
6. Test the relevant interruption, retry, stale writer, erasure and supported
   coexistence paths. State adapter removal conditions and unexecuted evidence.

Consume [authorization context](../interfaces-and-events/references/authorization-context.md)
where a mutable principal/capability/purpose/consent/lifecycle authorizes use.
A synchronous sensitive export does not imply migration or a durable framework.
Done means each actual consumer has a valid interpretation, destructive meaning
is explicit and authority stays unambiguous through recovery. Apply
[precedence](../../references/precedence-and-exceptions.md) for workflow conflicts.
