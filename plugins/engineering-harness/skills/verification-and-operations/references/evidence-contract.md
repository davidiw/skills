# Evidence Contract

## Acceptance status

Track four independent fields:

| Field | Values |
| --- | --- |
| Implementation | absent, partial, implemented |
| Automated evidence | pending, failed, passed at exact revision |
| Physical/external evidence | not required, pending, failed, passed with environment |
| Release gate | blocked, override recorded, eligible |

## Executed receipt

An executed result binds:

- full source revision and dirty-state policy;
- contract identity and Engineering Harness policy version;
- exact command and pinned toolchain;
- timestamp and environment;
- device, provider, model, corpus, or hardware identity when material;
- discovered, completed, failed, and skipped counts;
- exit status and pass/fail/pending outcome;
- artifact and transcript locations plus content digests;
- explicit owner override, if policy permits one.

The verifier validates receipt shape and artifact digests before trusting the
outcome. When the operation has its own completion protocol, exit status alone is
insufficient: validate required terminal evidence and reconcile completion,
failures and policy-accepted skips before issuing **or reusing** success. Interrupted,
partial, failed-with-zero-exit, missing or corrupted evidence cannot become PASS.
Cache reuse must validate the applicable source/contract identity, artifact integrity
and completion evidence, not merely a prior PASS label. Preserve valid evidence
and useful caching; repositories own runner-specific enforcement of this contract.

A referenced test file, video script, or harness is implementation,
not evidence that it ran.

Performance evidence also records warm/cold state, dataset, competing work,
sample count, p50/p95/max where meaningful, and the threshold source. Distinguish
sample admission and measured correctness from optimization qualification; the
[owning methodology](methodology.md) decides which claim those results support. Developer
hardware can detect regressions but does not establish device release limits.

## Evidence identity and label identity

For retained replay, evaluation or regression artifacts used as evidence, the
immutable evidence identity cryptographically binds the exact captured inputs
(including source media or its digest where material), derived evidence and the
material producer/build, model, configuration and preprocessing provenance.
Include a rubric captured with the evidence when it determines its meaning.
Use a versioned canonical encoding or a manifest of verified content digests;
a hash covering only derived outputs while provenance remains editable is
insufficient. Verify referenced bytes against their digests before reuse.

Label identity is separate: human labels, adjudications and corrections refer to
the immutable evidence identity and have their own revision. Correcting a label
does not rewrite captured evidence. A comparison receipt binds both the evidence
identity and the label revision used, so changed labels may invalidate a scored
baseline even though the captured evidence identity is unchanged. State the
baseline's compatibility contract; do not infer compatibility from an unchanged
filename or manifest hash alone. Missing material provenance leaves reuse
unqualified, not retroactively reproducible.

Prove identity at the actual capture/export/replay seam with mutations:

| Mutation | Same evidence identity? |
| --- | --- |
| Correct a human label or criterion annotation | yes |
| Change captured observations or sampled input media | no |
| Change model identity or material configuration | no |
| Change preprocessing version | no |
| Change producer/build revision | no |
| Change rubric captured with the evidence | no |

This applies to reusable evidence, not every file, parser result or UI state;
ordinary wrappers do not need a provenance system.
