# Profile Discovery

Brownfield adoption starts with inspection, not a blank capability checklist.

```bash
python3 scripts/profile_repository.py /path/to/repository \
  --output /path/to/repository/engineering-harness.json
```

The proposal records only relative evidence paths and detector names. It never
records source excerpts. High-confidence signals are proposed as enabled;
medium, low, and absent signals remain disabled but visible for review.

Before changing `status` from `proposed` to `accepted`:

1. inspect every enabled capability and uncertain signal;
2. correct false positives and false negatives using repository evidence;
3. replace each `review-required` enforcement owner with the actual repository
   path, command, or policy owner;
4. install cheap deterministic checks for foundational boundaries introduced by
   the repository, or record an authorized scoped exception;
5. retain discovery evidence so later reviewers can understand the proposal.

Commit the accepted profile with the repository. Proposed output may be
discarded and regenerated; accepted capability and exception decisions are
version-controlled repository policy.

Discovery is conservative and cannot prove a capability absent. Repository
decisions remain authoritative.

A provider SDK import is low-confidence evidence of AI use, not proof that the
model can mutate product state. AI-mediated action discovery requires action
execution evidence in the same action owner; unrelated repository files do not
combine into that claim. Likewise, a generic in-process event name is not an
independently consumed delivery contract; stream transport, outbox/inbox, or
another delivery owner supplies the high-confidence signal. Explicit runtime
resource budget, pool, or governor owners identify constrained resource
governance, while ordinary allocation calls remain review evidence at most.

## Drift

```bash
python3 scripts/profile_repository.py /path/to/repository \
  --check /path/to/repository/engineering-harness.json
```

The check fails for meaningful drift:

- a newly detected high-confidence capability is recorded as disabled;
- a recorded source-of-truth path disappeared;
- the profile remains proposed;
- the profile and package use incompatible policy release lines.

It warns when an enabled capability loses all detector evidence because removal
cannot be inferred safely. Medium and low signals are review leads, not gate
failures. Detector evidence changing within an already enabled capability is
not meaningful drift by itself.
