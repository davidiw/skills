# Durable Operation Contract

| Decision | Contract |
| --- | --- |
| Logical target | {Stable fact or resource} |
| Admission boundary | {Atomic durable commit} |
| Operation identity | {Idempotency key} |
| Authority envelope | {Account, tenant, epoch, role, capability} |
| States | {Lifecycle and terminal states} |
| Checkpoint | {Bounded resumable unit} |
| Effects | {Transactional, outboxed, idempotent, compensating} |
| Coalescing | {Equivalent-intent key} |
| Successor policy | {Supersession and fence points} |
| Retry/backoff | {Operation-owned policy} |
| Cancellation | {Cancelable boundary and retained facts} |
| Terminal record | {Success, failure, cancellation, or supersession evidence} |
| Observability | {Allowlisted fields and user-visible state} |
| Retention | {Cleanup trigger} |

## Fault matrix

- {Named deterministic fault boundary and expected recovered state.}

An adapter is acceptable only when it implements this contract without a
second hidden lifecycle.
