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
