# Profile Discovery

Brownfield adoption starts with inspection, not a blank capability checklist.

Run these commands from the installed plugin root (the parent of `references/`).

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

When a reviewer rejects a positive detector finding, retain its original
`suggested`, confidence, and evidence fields, set the accepted project/capability
value to false, and add this to that discovery finding:

```json
"review": {
  "decision": "rejected",
  "rationale": "This provider supplies local labels; it calls no external service.",
  "authority": "Repository adoption review"
}
```

Use the actual repository authority and reason. Scanner 5 evidence includes
source-content SHA-256 digests. A rejection applies only to that scanner version
and unchanged evidence, confidence, and content. New or changed evidence needs
review; never refresh its hashes while carrying forward an unreviewed rejection.
This is a detector decision, not an exception to an active invariant. Keep
profiles containing hashes of private source under that repository's data policy.

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

- a high-confidence capability or sensitive-data signal is recorded as disabled
  without a matching reviewed rejection;
- a recorded source-of-truth path disappeared;
- the profile remains proposed;
- the profile and package use incompatible policy release lines.

It warns when an enabled capability loses all detector evidence because removal
cannot be inferred safely. Medium and low signals are review leads, not gate
failures. Detector evidence changing within an already enabled capability is
not meaningful drift by itself.

## Methodology registration audit

Source proposals also locate conventional testing, review and performance policy
files. Existing arbitrary `sources` keys support repository-specific locations.
For cross-cutting system review, use `--audit-methodology PROFILE` and optional
repeated `--policy REPOSITORY_PATH` arguments; this is separate from capability
and policy-version drift, so it can diagnose an older profile without migrating it.
A nonzero result identifies missing registration/ownership, unresolved paths or
the known circular “before explicit skill work” pointer. It does not change files,
execute a referenced command or establish evidence acceptance. Full methodology
coverage still needs source inspection; see
[methodology ownership](../skills/verification-and-operations/references/methodology.md).
