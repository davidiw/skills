# Unpublished 0.5.0 natural-prompt evaluation

This evaluates one frozen candidate; it does not publish or tag 0.5.0.
The earlier [development notes](../0.5.0-forward-notes.md) are unchanged and remain
explicit-router development evidence with their original limitations.

## Inputs and isolation

- Base: `d3ca0a071d98dc67896a0ee9f743c771d2bdca02`.
- Frozen candidate: `a4c32393382b9b2a9ad6f7f35bf2b8b0374795aa`.
- Policy: unpublished `0.5.0`; CLI `0.153.4`; model `gpt-5.6-luna`, medium effort.
- Fourteen cases, two repeats per control/harness arm: 56 planned trials.
- Two concurrent CLI processes maximum; 240-second timeout per model invocation.
- Each trial receives a fresh fixture repository and home. Plugin inventory is
  checked in both arms. The competing diagnosis skill is identical in both.
- Prompts contain the frozen case context and request, without a skill name,
  expected outcomes, or evaluator instructions about workflow choice.
- The installed harness cache excludes `evals/`, `tests/`, and `.git/` to keep
  expected outcomes outside the runtime skill resources. Policy files retain
  their frozen hashes. This is a masked-runtime test, not a claim that the
  unmodified distribution prevents evaluation-data access.

The [snapshot manifest](snapshot.json) records input hashes and the replayable
[candidate Git bundle](candidate.bundle). The [runner](run_matrix.py) and
[runner checks](test_runner.py) record the clean-run procedure. Setup time is
excluded from model latency. Each execution receipt retains actual tool events,
final messages, fixture diffs/hashes, inventory, model usage, and timeout status;
local paths and credential values are redacted before publication.

Fresh homes isolate plugin installation but do not suppress every user-level
skill. A release-privacy control read the existing `code-review` skill. Its
current content matches the recorded tool output; the hash and event are recorded
in [run metadata](run-metadata.json). The complete runtime skill catalog was not
captured. Replay therefore preserves the candidate and observable inputs, but
cannot claim exact reconstruction of all discovery competition. A future
controlled campaign should pin the full catalog before starting.

## Invalid pilot

The first attempt was stopped after a harness trial read `evals/cases.json` from
the installed plugin cache. Those expected outcomes contaminated the trial.
The collector retained five completed records before interruption in
[`invalid-pilot/manifest.json`](invalid-pilot/manifest.json). The final
[attempt ledger](invalid-pilot/attempt-ledger.json) retains all 56 queued entries:
seven completed model records (including two finalized during shutdown) and 49
cancelled/setup-failure records. The pilot runner is retained alongside them.
Every pilot record is excluded from clean scores.
The restart uses the same frozen policy with runtime evaluation material hidden.
No behavioral failures are removed from the clean matrix.

## Scoring

Assess actual required and forbidden outcomes separately from observed skill
reads. Final prose naming a skill is not evidence that its instructions were
loaded. Controls receive no penalty for lacking plugin-specific skill reads.
Apply the frozen six-dimension rubric to relevant behavior: a direct control
review and the candidate's assurance-only router path are both valid routes.
Absence of inapplicable machinery is proportional behavior. A directional pass
requires at least 10/12, every required outcome, no critical forbidden effect,
and no fabricated execution. Preserve unsupported security claims separately
from fabricated tool execution; a correct core finding can still be a partial
case result when a required evidence distinction is missing.

Review-only trials start in fresh contexts without author reasoning. That
is context isolation, not evidence of organizational independence. Trials that
implement and then review in the same context must disclose self-review and
any required independent gate. This matrix does not prove parallel reviewer
orchestration on a production-sized system.

## Assessment: do not publish 0.5.0

The requested metadata, narrower assurance dominance rules, and release-wide
modes are implemented. This candidate improves explicit-review discovery and
preserves restraint, but the frozen behavior does not justify a release gate.

The harness has **18/28 directional passes**, versus **13/28 controls**. A pass
requires the full case contract, so a correct core finding can still miss on
confidence, coverage, principal binding, or evidence distinctions. These totals
are not vulnerability detection rates and do not establish statistical benefit.

| Case | Control passes | Harness passes |
| --- | ---: | ---: |
| `natural-security-review` | 0/2 | 1/2 |
| `natural-privacy-review` | 0/2 | 2/2 |
| `authorization-export` | 0/2 | 0/2 |
| `erasure-telemetry` | 2/2 | 2/2 |
| `critical-audit` | 0/2 | 0/2 |
| `handoff-session` | 1/2 | 1/2 |
| `uncatalogued-assurance` | 0/2 | 1/2 |
| `provider-wake-restraint` | 2/2 | 2/2 |
| `ui-fence-restraint` | 2/2 | 1/2 |
| `sensitive-copy-restraint` | 2/2 | 2/2 |
| `tiny-cli-restraint` | 2/2 | 2/2 |
| `pure-library-parser-restraint` | 2/2 | 1/2 |
| `release-security-surface` | 0/2 | 1/2 |
| `release-privacy-lifecycle` | 0/2 | 2/2 |

[Normalized scores](scores.json) link to retained per-trial assessments.
Security/privacy cases were graded in separate read-only reviewer contexts;
restraint cases were graded by the parent against diffs and actual test output.
[Observed routing](routing.json) records complete skill text in successful tool
reads; it does not infer selection from the final answer.

### What worked

- Natural security and privacy prompts read the router and correct specialist in
  all four harness trials. Both release privacy trials met the whole-lifecycle
  inventory/coverage requirements; one of two release security trials met its
  full matrix contract.
- All ten harness restraint trials (provider wake, UI guard, sensitive copy,
  tiny CLI, pure library) avoided security/privacy skill reads. They introduced
  no extra architecture or operational systems.
- Review-only trials found the core session-confusion, telemetry-resurrection,
  path-traversal, unchanged legacy export, and restore defects. Existing catalog
  vocabulary did not prevent reporting path traversal.

### What still blocks confidence

- Neither export correction loaded the required assurance specialists or
  performed the required corrected-snapshot security/privacy review. One
  selected only the competing diagnosis skill. Residual exposure and fault
  coverage were also inconsistent; a control retained a permission-revocation
  disclosure reproduced by the independent grader.
- Neither critical-audit harness trial loaded security assurance or completed
  the full shared-contention/bounded-progress proof. Recognizing another audit
  writer did not consistently translate into a sufficient correction and proof.
- Some security findings overstate unimplemented token-service replay behavior.
  Confidence, snapshot, coverage, and reviewer-status handbacks remain uneven.
  Release security trial 1 lacked the required coverage matrix.
- Provider and UI harness trials omitted their frozen expected implementation
  specialists despite correct narrow edits. One UI trial omitted a stale-switch
  check; one library trial introduced an error-type regression at year bounds
  ([reviewer probes](assessments/ordinal-review-probes.json)). These are distinct
  from assurance over-routing.

The next iteration should target the diagnosis-to-assurance handoff for actual
boundary changes and reliable completion evidence: scoped review of the corrected
snapshot, explicit non-atomic residual exposure, bounded contention proof, and a
reconciled release coverage matrix. Pin the entire runtime skill catalog in the
next frozen campaign. Keep the independent reviewer separation and the existing
resource/verification design; these results do not justify adding more skills or
claiming that an external review would find only minor issues.

## Execution results

All 56 clean trials completed with exit code zero and no timeout. The final
[integrity audit](integrity-audit.json) found correct arm separation, identical
source/competitor hashes, and no recorded reads of expected outcomes or external
effects. Its scope is recorded command events and metadata, not an independent
sandbox or network audit. The [sanitized execution receipt](manifest.json)
retains every clean trial.

| Measured quantity | Control (28 trials) | Harness (28 trials) |
| --- | ---: | ---: |
| Median model invocation | 52.671 seconds | 77.465 seconds |
| Total model invocation time | 1,521.304 seconds | 2,241.914 seconds |
| Input tokens, including cache | 2,627,865 | 4,969,029 |
| Cached input tokens | 2,223,872 | 4,350,208 |
| Uncached input tokens | 403,993 | 618,821 |
| Output tokens | 52,732 | 80,265 |
| Reported reasoning output tokens | 18,036 | 25,269 |

[Per-trial metrics](metrics.json) are derived by [summarize_results.py](summarize_results.py).
Do not add reasoning tokens to output tokens without the provider's accounting
contract. Runs use fixed case/arm order; setup is outside the timing window, and
cache warming and service variance are not controlled. These are descriptive
measurements from one model and two repeats per arm, not statistical evidence of
cost or reliability improvement.

## Replay

Clone `candidate.bundle`, then check out the recorded candidate revision. Run
`run_matrix.py` with absolute `--package`, `--matrix`, and a fresh `--output` path;
the matrix lives at `evals/assurance-matrix.json` in that checkout. The procedure
requires the recorded Codex CLI/model, a local authenticated CLI, and the
competing diagnosis skill (override `--auth` or `--competing-skill` when needed).
Credentials are never part of this receipt. Preserve the runtime exclusions and
do not expose the evaluation corpus to model tool reads. Use `redact_paths.py`
for remaining local path strings and mapping keys after the runner's credential
redaction; retain the public receipt only after checking it.

The candidate bundle reproduces the evaluated policy. This result directory and
its reporting scripts were added after the freeze and do not change that policy.
