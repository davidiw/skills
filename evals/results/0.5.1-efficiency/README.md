# 0.5.1 efficiency initiative: baseline attribution

Correctness baseline: immutable `v0.5.0`, commit
`e8efc6b70ac4a235981f2481e471917ede28139a`, and its final 84-trial Astra campaign.
Harness passed 42/42 required behavioral outcomes, including 8/8 scope boundaries,
with zero critical forbidden outcomes. Its original receipts remain unchanged.
This analysis precedes runtime optimization; it changes no prompt, fixture, rubric,
model, approval boundary or required review/evidence outcome.

`evals/attribute_costs.py` reconciles every per-invocation token counter against all
111 retained context totals. It emits no message content or private reasoning.
The compact [baseline summary](baseline-summary.json) records aggregate and case
costs. Detailed per-trial/context counters, read requests, packet/document sizes,
handback sizes and source hashes are retained outside Git; their digest is in the
summary. Run the analyzer with `--run RETAINED_RUN --runtime EXACT_RUNTIME
--output NEW_JSON`. Unit tests protect counter reconciliation, duplicate
counter handling, secret-content omission and distinguishing reads from generated
links. Structural tests are not behavioral evaluation.

The first focused experiment also produced JSON handoffs and inventories. The
analyzer now measures every added artifact format and verifies its retained hash;
packet/handoff filenames are hints, not proof of document purpose. A regression
test protects JSON inclusion and rejection of modified evidence. The original
baseline attribution remains immutable; an additional all-format derivation
reconciles the same counters without changing any baseline behavioral receipt.

Independent instrumentation review subsequently found missing trial-level
completeness/duplication checks and insufficient source-integrity qualification.
The analyzer now reconciles the planned/public/private trial inventory, unique
contexts, completion flags and trial totals in addition to invocation counters.
It rejects incomplete evidence; failed executions with complete counters retain
their failure status and measured cost. Rejected raw attempts remain retained.
Every runtime and post-run fixture file is checked against its recorded inventory.

For verified source attribution, supply `--integrity INVENTORY.json
--integrity-sha256 PINNED_SHA256`. The inventory maps run-relative paths to retained
SHA256 values: `public/run.json`, `public/manifest.json`, every private `record.json`
and each referenced raw session trace. Pin it from independently retained evidence,
not by hashing possibly modified inputs immediately before analysis and calling
that historical verification. The supplied inventory digest is itself checked.
Without it, the output explicitly labels trace/record integrity **unverified**;
newly computed hashes are fingerprints only. Regression tests cover missing and
duplicate contexts/trials, conflicting counters, and trace, record, runtime and
existing-fixture tampering. Earlier derivations remain unchanged; new verified
derivations must identify their retained trust source.

Legacy forked traces can contain ancestor session headers. Attribution uses the
first native header for context identity, retains the historical recorded ID
separately, and rejects repeated native contexts or invocations. This accommodates
the frozen runner's header-flattening behavior without rewriting its receipts.
Native parent/child classification additionally uses the first header and the
retained top-level `thread.started` identity. Custom configuration requires a
matching retained setup role-definition hash; a named role alone is insufficient.
Historical kind/configuration remain separate, and missing evidence is unavailable.
This corrects two flattened child labels in the development cohort without changing
any token totals or rewriting frozen receipts.
Completion requires the latest native turn to finish; a prior completion cannot
mask a pending or aborted follow-up. Copied ancestor turns are identified against
their retained native traces and cannot satisfy a child's completion check.
Reverification against released archives and the earlier pinned attribution
reproduced all original arm/case counters exactly; no baseline corruption or
counter correction was established. New reports bind the analyzer's own source
digest and expose execution failures as well as integrity status.

| Cost | Harness | Control | Increment |
| --- | ---: | ---: | ---: |
| Total input (cached included) | 8,095,695 | 5,296,115 | 2,799,580 (+52.9%) |
| Uncached input | 881,615 | 605,043 | 276,572 (+45.7%) |
| Output | 111,785 | 63,621 | 48,164 (+75.7%) |
| Median trial wall | 62.54 s | 52.03 s | +20.2% |
| Model invocations | 379 | 282 | 97 |
| Contexts | 55 | 56 | -1 |
| Observed skill bodies | 90 | 26 | 64 |

The extra output is concentrated. These five groups produce 76.7% of it and
81.3% of extra input. Each includes two trials per arm except unapproved scope,
which includes four.

| Ranked case group | Extra output tokens | Extra input tokens |
| --- | ---: | ---: |
| Release security | 9,837 | 622,496 |
| Authorization/export | 7,056 | 551,732 |
| Release privacy | 6,806 | 481,966 |
| Correction review | 6,663 | 280,310 |
| Unapproved scope | 6,577 | 340,092 |
| Approved design (next largest) | 3,425 | 271,223 |

Output counters grouped by the actions in each model invocation show where to
investigate. Mixed commentary/tool responses remain in the tool group; this is
not a tokenizer split between prose and code.

| Invocation action | Harness output | Control output | Increment |
| --- | ---: | ---: | ---: |
| Writes code/artifacts, sometimes with commentary | 59,184 | 27,865 | 31,319 |
| Reads/other tools, sometimes with commentary | 23,591 | 11,118 | 12,473 |
| Final answers/handbacks | 12,836 | 10,982 | 1,854 |
| Checks, sometimes with commentary | 11,406 | 9,735 | 1,671 |
| Coordination, sometimes with commentary | 2,908 | 1,285 | 1,623 |
| Launch | 1,860 | 2,636 | -776 |

Final answers account for only 3.8% of incremental output. Calls that generate
artifacts/code account for 65.0%; they include required tests and implementation,
so the entire bucket is not removable verbosity. Hidden reasoning counters are
lower for Harness (3,744 versus 4,762); lowering reasoning is not the experiment.

The retained artifacts explain a concrete target: release reports are about
11 KB; release privacy also creates separate packet, initial inventory and context
receipt files. Correction reviews save 2.4–2.9 KB packets and 3.7–4.3 KB reports,
after fresh children have already returned their findings. Approved design plans
are 16.3–17.9 KB each (68.6 KB across four trials). Required blockers, lifecycle
limits and coverage remain essential; repeated serialization and contract prose
are candidates for compression. Scope decisions must still precede edits.

The analyzer also partitions measured invocation spend by already-loaded context
stage: discovery/competing context 787,752 input / 7,589 output; router stage
3,211,501 / 28,392; implementation-owner stage 1,439,239 / 34,770; reviewer stage
2,657,203 / 41,034. These are context-stage totals, not causal router or skill-token
charges: each request includes retained messages, source, tools and system context.
File bytes are recorded separately rather than inventing exact Astra tokenizer
counts. Primary contexts cost 6,185,011 input and 79,597 output; delegated reviewers
cost 1,910,684 input and 32,188 output. Per-context time includes waiting and overlaps
children, so it cannot be summed into trial latency.

Literal shell-read attribution recognizes 81 runtime body reads and 99 runtime
reference reads (180 requests), with no same-context repeats among those reads.
The broader original runner reports 90 skill bodies including competing skills
and 115 reference paths. Dynamic/partial commands explain the different observation
boundaries. Frequently loaded files are the router (41), authorization contract
(17), assurance-review (16), classification (13), privacy lifecycle (13), handoff
(13), security skill (13) and privacy skill (11). The router/classification/shared
review/handoff files are 5.4–6.1 KB each. Cross-context repeats include authorization,
handoff, privacy lifecycle and precedence; independent rereads of relevant source
and contracts are not automatically waste.

Multi-owner implementation is concentrated in the four approved-design trials:
interfaces and data compatibility address the distinct broker contract and
migration/lifecycle obligations. Other implementation routes already stay small.
Copy/static/parser/library/wake/UI controls have only 854 extra output tokens
combined, with no assurance overactivation. Broad fanout reduction or a minimal
path redesign is therefore a low priority.

Correction trials perform one current bounded review with security/spec and
standards contexts, report the full two-blocker set, and classify the pre-existing
grant defect as an initial-review miss. The supplied historical receipt is a
fixture, not a measured previous model round. No measured broad correction loop
justifies removing independent review. The extra correction cost is principally
packet/report/proof generation; the exact per-context counters remain available.

First optimization class: compact evidence representation and reuse. Preserve a
neutral saved packet, complete first-pass findings, release inventory/reconciliation,
exact snapshot/context evidence and every pending/unknown boundary. Avoid copying
contracts, reauthoring a child report and repeating the same evidence in several
artifacts. Measure focused release, export, correction and scope trials before
accepting the change. Later compression/targeted-read work is conditional on what
those measurements demonstrate. No new framework, invariant or skill is proposed.
