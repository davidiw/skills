# Compatibility and Migrations

## Supported profile

Record each independently evolving axis:

| Axis | Current writer | Live readers | Accepted range | Evidence | Removal gate |
| --- | --- | --- | --- | --- | --- |
| Persistent schema | | | | | |
| Storage layout | | | | | |
| Wire/API | | | | | |
| Event/message | | | | | |
| Sync/bootstrap | | | | | |
| Worker/job payload | | | | | |
| Generated artifact | | | | | |
| Operator/repair tooling | | | | | |

## Migration contract

Define source profiles, destination profile, owner, admission condition, locks,
state record, atomic transitions, failure points, structural validation,
performance budget, and rollback binary. Recovery must combine durable state
with actual storage reality and fail closed on unexplained dual authority.

Test real representative data rather than placeholder bytes. Include pending
operations, tombstones, provider/checkpoint state, media or external references,
and any state capable of changing execution after upgrade.

Compatibility prose is removed only after deployed-consumer evidence proves
the state unreachable and the removal release is named.
