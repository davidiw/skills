# Live Data Repair

An online repair can coexist with writers when all of these are true:

- target rows are selected by stable identity and a bounded predicate;
- the corrected contract is already accepted by every live reader and writer;
- each mutation is idempotent and compare-and-set fenced against the inspected
  version or invalid shape;
- conflicts are skipped or retried from fresh state rather than overwritten;
- progress is checkpointed and resumable;
- batch size, rate, runtime, and blast radius are bounded;
- dry-run reports counts and categories without private row contents;
- completion re-queries the invalid predicate;
- rollback or compensation is defined for the actual mutation;
- the operation has separate authorization from code deployment.

Stop-the-world repair remains appropriate when identity is ambiguous, both old
and new writers can create conflicting shapes, the mutation cannot be fenced,
or partial application would violate correctness. Choose from these facts,
not from a blanket preference for either downtime or live mutation.
