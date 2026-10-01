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

## Focused iteration proof

State the user-visible promise before implementation and prove it early during
iteration at its actual failure seam, independently of the proposed mechanism.
Before independent readiness review, complete that focused proof. Record the promise,
the production composition and defaults that reach it, the focused command or
observation, and any prerequisite that remains unproven. For a flow crossing
owners or configuration, exercise the real production assembly/default path and
the relevant alternate state; a component test or a fixture-only injection does
not establish that composition.

When a claim depends on packaged startup, rendered deployment configuration or
a UI/API connection, cover that entrypoint rather than rebuilding its wiring in
the fixture. Use existing harnesses and keep simulated providers at their external
boundary. Separate local composition evidence from deployed/external proof.

Do not make a prerequisite appear true by enabling it only in the test fixture
when whether production supplies it is part of the claim (for example, fixture
login, a feature flag, provider availability, or configuration). Test setup may
model an accepted prerequisite, but the evidence must identify it and separately
prove or leave pending the production path that supplies it. Add negative
boundary cases from the stated assumptions, and demonstrate their sensitivity
with an old-code failure or a bounded mutation when practical. A browser,
end-to-end harness, or new test framework is not a default requirement for a
local fix; use the smallest existing proof that reaches the seam.
When a focused command can run locally, execute the failing case rather than
inferring failure from source inspection. If sensitivity cannot be exercised,
record that gap rather than claiming the proof complete.
The failure must reach the intended assertion, not fail at compilation or setup.
Restore the candidate and retain the passing result with the negative evidence;
do not mutate live systems for sensitivity checks.

Iteration proof is deliberately not final acceptance. Run a broad/full
regression only after known corrections are closed and the candidate is frozen
for final landing or a required final gate. Do not consume it while iterating or
awaiting review unless the user explicitly requests a diagnostic full run. An
early PR may carry focused evidence and an explicit pending full regression;
opening it neither implies merge authority nor converts pending work to passing
evidence.

A PR-only handoff remains iteration: completing the code does not itself select
the final acceptance stage. Leave broad regression pending until the task reaches
the repository's final landing/review gate with its prerequisites closed, or the
user explicitly requests final acceptance or a diagnostic full run.

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
