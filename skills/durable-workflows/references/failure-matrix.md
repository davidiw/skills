# Durable Failure Matrix

Select rows that the real execution path can encounter and define the expected
recovered state. This workflow owns its focused failure fixtures.
`verification-and-operations` owns independent fault campaigns and exact
evidence; it uses named boundaries rather than timing-dependent sleeps.

| Boundary | Required question |
| --- | --- |
| Before admission commit | Can the caller distinguish rejection from acceptance? |
| After admission, before execution | Does restart discover the intent exactly once logically? |
| During a bounded unit | Is the prior checkpoint valid and retryable? |
| After local commit, before external effect | Can the effect resume without duplicating the fact? |
| After external effect, before acknowledgment | Is replay idempotent or reconciled? |
| During cancellation | Which committed facts remain authoritative? |
| After successor admission | Can the predecessor still commit, acknowledge, or publish? |
| After authority change | Can stale work affect the newly active account or tenant? |
| While offline or provider-limited | Is intent preserved with operation-specific backoff? |
| During process or device termination | Does foreground/background ownership resume correctly? |
| On poison input | Is failure bounded, visible, and non-amplifying? |
| During terminal-state publication | Can observers recover from a missed notification? |
