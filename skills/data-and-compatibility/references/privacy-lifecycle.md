# Privacy Inheritance and Erasure

Apply `privacy-lifecycle` to every representation reached by the changed flow.
Trace source data into derived values, event metadata, AI telemetry, logs,
audits, caches, exports, and temporary artifacts. A health-activity event can be
sensitive even when its payload omits measurements or free text.

For each representation, identify its purpose, reader/writer owner, retention,
expiry/erasure action, and whether it can be rebuilt. Inherit the source's
obligations by default. A different classification or retention period needs
evidence and repository authority, with exact scope; the word “audit,” hashing,
or a pseudonymous identifier is not that evidence. A separately required audit
may retain only its explicitly authorized data for its defined purpose and
duration. Record unresolved policy instead of inventing an exemption.

Erasure is both a data operation and an authorization transition. Order
revocation and removal so a delayed callback, buffered telemetry batch, retry,
import, or concurrent writer cannot recreate erased rows. Fence commits against
the lifecycle owner, including telemetry writers. Use an existing epoch,
tombstone, or atomic precondition where it establishes the contract; do not add
a parallel lifecycle store by default. A revived or replacement identity must
not inherit an old writer's authority.

Test a write admitted before expiry and committed afterward, telemetry flushed
after erasure, concurrent deletion and import, and reconstruction from a cache
or export. Include required retained-audit behavior when applicable. Keep
retention facts, deletion evidence, and any inability to erase external copies
explicit; reporting an erasure success must match the actual boundary.
