# Reconciled methods: competition probe and clean-catalog smoke

Both runs use frozen source **f075a93db1e50fbe1850066e7b615866e50da35d**, policy
**0.8.0 Unreleased**, unchanged natural prompts, Astra/medium, two lanes and the
existing protected runner. No policy changed between runs. Historical 0.7 and
older evidence remains unchanged. Twelve invocations completed without timeout,
setup failure or incomplete measured context.

## Result and preferred configuration

The paired competition probe completed four cases per arm with identical pinned
external-skill availability. All implementations/proposals/reviews were bounded
and materially correct. **Three Harness cases fail the no-overlapping-workflow-read
expectation**: debugging, domain clarification and general review loaded the old
external skill as well as Harness. The typo stayed minimal. Do not report this as
four complete Harness passes: it is one pass and three routing partials. Router
policy cannot reliably prevent a skill body being loaded before the router is read.

The external code-review workflow used three contexts. Harness consumed the new
change-review method in one context, despite also reading that external skill.
Both found the two targeted defects and an additional reachable rounding defect;
no extra finding is credited uniquely to Harness. Debugging regressions in both
arms fail the original generator implementation and pass the corrected one.
Domain proposals preserve the separate participation/access contracts and do not
create files. Only debugging implementation/tests and the requested README typo
change; review/proposal fixtures remain unchanged apart from sandbox scratch locks.

A subsequent **Harness-only smoke with the six overlapping catalog entries removed**
completed the same four cases successfully. It is a different catalog condition,
not another paired comparison or evidence of broad efficiency:

| Case | Clean-catalog behavior and observed reads |
| --- | --- |
| Single-use CSV generator | Router only; source inspection settled the cause, then a failing/passing generator regression and one-pass repair. No unnecessary diagnosis-reference load. |
| Ambiguous active membership | Router, Foundations, quality/ownership reference; distinguishes participation from paid access with concrete boundary examples; naming stays a proposal. |
| Promotion review | Router and change-review reference; one context; finds missing minimum, case normalization and undiscounted rounding gaps despite green existing tests. Read-only. |
| Typo | No skill bodies; README spelling only. |

Thus the methods work without the archived skills, while co-advertising duplicate
engineering entry points still produces unnecessary reads. The preferred setup
is one Harness engineering entry point plus distinct platform utilities. This
change does not restore, remove or modify any personal skill or installed plugin.

## Evidence and cost

[receipt.json](receipt.json) records exact runtime/input/catalog hashes, native
context identities, record/trace digests, observed skill reads and method-output
markers, final responses, fixture hash summaries, diffs and usage. Fixture summary
hashes use sorted-key JSON; after hashes exclude sandbox `.tmp/` scratch files.
Complete file inventories/diffs remain in retained records. A reference marker
proves returned guidance; command/read-byte attribution is not claimed complete.

Each run installs the unmodified package in fresh homes, verifies runtime hashes,
passes credential/egress preflight before auth copying, and removes auth copies
on completion. The existing attribution tool verifies native identity/completion,
integrity and token reconciliation against independently pinned inventories.
Those checks do not score behavior. Inherited host/system declarations remain
recorded; no hermetic or universal host-catalog claim is made. Personal custom
agents are not used. The control review's two generic children are recorded;
Harness uses one primary context per trial in both runs.

| Cohort/arm | Contexts | Median wall seconds | Input incl. cache | Uncached input | Output |
| --- | ---: | ---: | ---: | ---: | ---: |
| Competing catalog/control | 6 | 37.02 | 519,721 | 50,601 | 3,624 |
| Competing catalog/Harness | 4 | 47.49 | 307,933 | 47,197 | 3,187 |
| Clean catalog/Harness-only | 4 | 45.11 | 283,361 | 41,313 | 2,928 |

One trial per case/condition does not establish statistical superiority, an
isolated instruction effect or broad efficiency. Aggregate token differences
include the control review's extra contexts. Catalog removal and instruction
changes cannot be disentangled using these observations. The router is larger;
useful ownership clarity does not itself prove a cost reduction.

## Validation and limits

112 tests and all 17 required checks pass at the evaluated source. Negative
mutations verify that a second implicit specialist and missing authoring-policy
enforcement registration fail existing validators. Fixture checks establish the
single-use input distinction, separate domain facts and independently reachable
review failures. Independent source review found no blocker; final evidence review
is recorded separately against the later evidence-only revision.

The targeted diagnosis reference was exercised in the competing-catalog Harness
trial. The clean smoke correctly skipped it when source inspection resolved the
cause; difficult/unreproducible failures remain untested behavior. Authoring craft
and utility boundaries receive source/structural review, not a natural-effectiveness
claim. No new independent-review gate is introduced or proven by the generic
review fixture; existing required fresh-review policy remains unchanged. No live
provider, device, deployment or VitalThread execution is claimed.
