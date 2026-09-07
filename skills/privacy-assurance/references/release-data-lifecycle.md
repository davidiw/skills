# Release Data-Lifecycle Privacy Review

Start from the complete candidate's sensitive-data inventory and declared
purposes. Record the snapshot, launch population, data categories, processors,
and environments available for inspection. Discover flows from schemas, routes,
SDK/configuration, jobs, logging wrappers, exports, and backup/restore tooling;
reconcile those paths with repository privacy decisions.

## Inventory before investigation

For each applicable category, trace collection through all destinations and
writers. The inventory includes unchanged, legacy, and alternate paths.

| Lifecycle area | Questions to carry into the coverage matrix |
| --- | --- |
| Collection and import | What is collected from users, devices, providers, or inference, for which principal, purpose, and consent? |
| Canonical and derived state | Which records, projections, caches, embeddings, and inferred attributes inherit sensitivity? |
| Operational metadata | What can event names, telemetry, AI traces, logs, audits, error reports, and identifiers disclose? |
| Processors and AI | Which services or models receive data, under which purpose, retention, and deletion contract? |
| Disclosure and exports | Which users, support/admin actors, share links, downloads, notifications, and temporary artifacts receive it? |
| Retention and expiry | Which owner bounds each representation's lifetime, including temporary identities and dormant accounts? |
| Erasure and delayed writers | What revokes buffered callbacks, jobs, retries, imports, and reconstruction after deletion? |
| Backups and restore | What remains in backups, for how long, who can restore it, and how is erased authority/data prevented from returning? |
| Legacy and shadow storage | Which old tables, buckets, indexes, replicas, log sinks, and alternate pipelines still retain data? |

Create one row per data category and destination/processor with source evidence,
purpose/consent, reader/writer owner, retention/expiry, erasure/revocation method,
planned proof, and coverage status. Distinguish explicit policy from assumptions.
An exemption needs scoped evidence and repository authority; absence of access
to a processor or backup is an unavailable row, not a passing deletion claim.

## Follow and reconcile

Use the owning [`privacy lifecycle`](../../data-and-compatibility/references/privacy-lifecycle.md)
and [`authorization context`](../../interfaces-and-events/references/authorization-context.md)
contracts across each material path. Include post-erasure telemetry, restore,
export leftovers, consent changes, identity replacement, and independently
retained required audits where applicable. Use synthetic records for probes.
Live processor or backup operations require the existing authorized scope.

Reconcile final coverage against all discovered destinations and writers, then
return findings, retained-data limits, unavailable evidence, and readiness
implications under the shared
[`assurance review contract`](../../../references/assurance-review.md). A technical
review does not establish legal compliance, and deleting the primary database
record does not establish release-wide erasure.
