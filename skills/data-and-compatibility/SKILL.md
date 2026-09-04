---
name: data-and-compatibility
description: Evolve persistent or replicated data safely. Use for schema, storage layout, sync, identity, account or tenant fencing, tombstones, projections, caches, migrations, live repairs, mixed client/server versions, and rollback; not for transient in-memory structures.
---

# Data and Compatibility

Compatibility is a consumer behavior claim, not a version comparison or an
unchanged field name.

Use the [invariant catalog](../../references/invariants.json) as normative.
Interpret only entries whose `owner_skill` names this skill; consume other
entries without redefining them.

## Workflow

1. Identify authoritative source, canonical state, observations, projections,
   caches, transport forms, generated forms, and every writer. Define how each
   non-authoritative representation rebuilds or invalidates.
2. Specify stable identity, collision domain, account or tenant authority,
   time and timezone semantics, units, provenance, and deletion lifecycle.
3. Inventory deployed readers and writers by persisted, wire, event, storage,
   worker, and operational capability. Include rollback binaries and tools.
4. State the supported predecessor profiles and coexistence window from
   deployment evidence. Do not add compatibility for hypothetical or
   unreachable states.
5. Design migration, adoption, or repair as an idempotent state transition with
   explicit ownership, locks or compare-and-set fencing, interruption points,
   validation, and recovery. Preserve the source until authority transfer is
   proven when the contract requires it.
6. Keep remote absence non-destructive. Deletion requires a tombstone, erasure,
   same-identity conflict collapse, or verified lossless representation move.
7. Prefer additive readers and writers during coexistence. A reader may accept
   newer generations when required capabilities are validated and operators
   own mixed-version evidence; a numeric minimum alone does not prove semantic
   compatibility.
8. For online repair, use bounded selection, stable identity, idempotency,
   compare-and-set preconditions, checkpointing, rate limits, and live-writer
   conflict handling. Service shutdown is a risk decision, not a default.
9. Define representative upgrade, interruption, retry, coexistence, stale
   authority, downgrade or supported rollback, and deletion scenarios.
   `verification-and-operations` owns adversarial execution and evidence.
10. Record adapter removal conditions, telemetry, and the exact release that
    makes cleanup safe.

Read [`representations-and-reconciliation.md`](references/representations-and-reconciliation.md)
for replicated data. Read
[`compatibility-and-migrations.md`](references/compatibility-and-migrations.md)
for version changes. Read [`live-repair.md`](references/live-repair.md) for
online correction of existing records.

Before stopping work or changing the requested workflow, apply
[`precedence-and-exceptions.md`](../../references/precedence-and-exceptions.md)
and name the exact rule.

The change is complete when every deployed consumer has a tested interpretation,
interruption cannot create ambiguous authority or blank state, destructive
meaning is explicit, and rollback/removal conditions are operationally real.
