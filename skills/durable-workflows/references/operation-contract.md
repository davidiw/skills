# Durable Operation Contract

Record these fields before choosing an implementation:

| Field | Decision |
| --- | --- |
| Logical operation and target | What fact or effect is requested? |
| Admission boundary | Which atomic commit makes acceptance truthful? |
| Stable identity | How are retries and duplicates recognized? |
| Authority envelope | Which account, tenant, epoch, role, or capability is captured? |
| States and transitions | Which commands or events move the lifecycle? |
| Checkpoint | What bounded progress can resume without redoing committed work? |
| Effects | Which are transactional, outboxed, retryable, compensating, or best-effort? |
| Coalescing key | Which equivalent requests collapse? |
| Successor rule | Can newer intent supersede old work, and where is fencing checked? |
| Retry policy | Which failures retry, with what operation-owned backoff and limit? |
| Cancellation | What is cancelable, and what remains committed? |
| Terminal record | What proves success, failure, cancellation, or supersession? |
| Observability | Which bounded metadata explains progress and failure? |
| Retention | When can operation state and payload references be removed? |

An adapter is acceptable only if it can implement this contract without a
second hidden lifecycle.
