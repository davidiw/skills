# Bounded conditional-role routing observation

Disposition: **connected acceptance remains pending**. This is a routing and
connected-flow observation, not evidence of improved reliability. PR #7's original
scope, snapshots, campaign records, and results are unchanged.

## Inputs and budget

The initial runtime candidate was `b737ab153801d2cba6c6bb7b7ffadc8323bd793b`;
the corrected runtime was `ea958c9a923c556bf60b94cc3cfbbb2748fd9888`.
Only `references/assurance-handoff.md` differs between the exported runtime inputs.
The fixture files and task prompt were identical apart from scratch paths.
The exact prompt templates and product contracts are in
[the frozen plan](../../conditional-role-verification-plan.md) and
[the fixtures](../../fixtures/role-reservation/DESIGN.md). Neither prompt directs
reviewer, worker, or operator launches.

The predeclared budget allowed two initial primary tasks, one corrective repeat
per task after a concrete reviewed correction, at most four primary tasks, eight
initial-pair auxiliary contexts and sixteen total, and 900 seconds per primary
including its supporting sessions. Actual use: three primary tasks and seven
auxiliary model contexts, including both supporting coordinators. Development
review and post-trial deterministic checks are separate from these model trials.
The successful minimal task was not repeated. No historical campaign was rerun.

## Observed routing

| Attempt | Result |
| --- | --- |
| Initial connected | Configured reviewer selected with fresh context, but effective permissions were unrestricted. Substantive reads began under that incompatible boundary. Outer coordinator stopped the attempt before worker implementation. No tracked production changes. |
| Minimal | Exactly one label correction; existing one-method display test and diff check passed. No agents launched. |
| Corrective connected | Startup-only gate detected incompatible inheritance, then used an existing read-only session for the configured reviewer and an existing workspace-write session for configured worker/operator. Reviewer challenged the proposal and authored eleven test methods; worker implemented. Interrupted at 900 seconds before operator execution or final acceptance. |

The interrupted CLI processes returned zero on termination; that is **not** a
completion or passing acceptance result. Supporting CLI sessions were also stopped.
The initial permission and read-scope failures remain retained observations.

The native evidence is [recorded separately](native.json). Resolved role mappings
for this installation are `reviewer` = Astra/high/read-only, `worker` =
Terra/medium/workspace-write, and `operator` = Luna/medium/workspace-write.
`explorer` = Luna/medium was available but not needed. The primary coordinated.
These are observed mappings, not required names or models for other installations.
Native role selection used `agent_type` and `fork_turns: none`, without model
substitution. Valid role contexts were retained for follow-up. Supporting generic
coordinators are identified separately. Native records show Codex 0.154.0 and bind
role, model, reasoning, and sandbox to the specific child contexts; role
self-description alone was not used as proof. Opaque assignment payloads remain
opaque; saved packets and observed reads provide separate scope evidence.

## Produced result and limits

The reviewer completed its proposal challenge at 07:52:38 UTC. The worker's first
production patch followed at 07:54:48 UTC. The reviewer authored the
[eleven-method artifact](test_reservations_review.py); its bytes exactly match the
trial's exported test file, SHA-256
`ab0c432dca8bcfe489eec1bdcfc068d138fcbefa99009660cc3960cc65c6d7f7`.
The [produced source](produced-inventory.py) and [source hashes](produced-source.json)
retain the interrupted implementation. They are not an accepted clean control.

Full contract acceptance remains unavailable. The fixture accepts positive integer
quantities without an upper bound while preserving SQLite INTEGER storage. The
trial reviewer identified this ambiguity, rejected the planner's proposed maximum
as an unapproved narrowing, and required clarification. The planner withdrew that
proposal and directed removal of explicit maximum validation. The frozen produced
source still contains the maximum check. The interrupted correction is incomplete.
The worker also read the installed 0.8.0 router despite assignment to the exact
candidate policy. There is no evidence that unrelated evaluator contents were read.
The independent reviewer additionally found that the produced code rejects an
existing empty-string SKU, although the frozen contract does not prohibit that key.
This is a produced-task regression outside the twenty methods' coverage. The
operator executed the added check once against each exact source: produced output
**one error**, corrected reference **one pass**, with unchanged source/test hashes.
Complete outputs are linked from [the added-check receipt](sku-validation.json). Its
[reviewer-authored check](existing_sku_acceptance.py) is retained unchanged.
These limits prevent treating the partial run as successful end-to-end routing.

The trial's operator performed startup only. Post-trial execution by the retained
development operator is separately reported below; it cannot retroactively complete
the Harness-selected operator or final-review stages.

## Deterministic qualification

Before the natural trials, the reviewer-authored seven-method evaluator and two
hook-exception checks passed unchanged against the corrected test-only reference.
The earlier reference passed the seven-method set but failed both later hook
checks; those failures were retained. The initial incomplete fixture produced 27
failure entries across seven methods, including subtests. Those entries are not 27
independent defects. The four focused repository fixture tests passed.

The full workflow suite ran 118 tests: 117 passed and one errored on a loopback bind
prohibited by the operator's unchanged sandbox. That error was also reproduced on
unchanged main. Package validation and methodology registration audit passed.
Official plugin and all thirteen skill validators passed on unchanged validated
manifest/skill bytes. Initial archive validation lacked historical Git objects;
identical source with Git history corrected that setup, retaining the failed runs.
No assertions or permissions were weakened to obtain a passing result.

The separate development operator executed all **20 methods successfully**:
seven external reservation checks, two hook checks, and eleven natural-reviewer
checks. Zero failures, errors, or skips; source and test hashes remained unchanged.
Complete outputs with local paths redacted are linked from
[the post-trial receipt](posttrial-validation.json). These checks do not cover the
unbounded integer-domain question and do not complete natural operator execution
or final reviewer acceptance.

The [complete independent disposition](independent-disposition.md) permits the
workflow source to proceed as a **draft PR with natural acceptance pending** and
finds maintenance ready for its separate PR. It establishes no additional source
policy blocker and does not justify another policy edit or trial campaign. The
produced snapshot is preserved with its defects. Any later connected completion
needs a resolved quantity-domain contract, the resulting scope correction, the
existing-SKU regression fixed, and the missing stages completed under a newly
declared budget. No such additional run is included here. The installed Harness remains at 0.8.0; agent definitions and global
settings remain preserved after the scoped cleanup. A nested Codex launch also
added one trust entry for its synthetic scratch root; the final audit removed only
that exact launch-created entry. Every other byte and parsed setting was preserved;
no original config file was restored wholesale. This transient configuration side
effect is retained as an additional trial limitation. No runtime upgrade, installation,
new agent set, framework, universal runner, merge, or release occurred. The earlier
long-lived session's root cause remains explicitly **unproven**. The current observed
permission inheritance does not establish that historical cause.
