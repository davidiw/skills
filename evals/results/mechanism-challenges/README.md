# Mechanism comparison: observed limits

**Improved overall judgment is not established.** The bounded comparison completed
all 40 planned invocations (20 per version, two trials per case), without model
reruns, timeouts, rescue prompts or production edits during review-only cases.
All attempts remain retained. A successful invocation is not a behavioral PASS.

Published comparator: v0.8.0 `d7f9ff8fbdf8bcfd734d79ef5a231e182acfd4b5`.
Its evaluation assembly is `586732f` and has the identical published runtime tree
`729bac60ad7de483fc7a7811313e72468120abdc`.
Evaluated candidate: `8d1fe8513c7fec667005eba8d001936bf473e8bb`, runtime tree
`598e41ed56a28fa56af64c639862058ac0f550ac`.
Both used identical prompts/fixtures/runner, Astra/medium, two concurrent lanes,
fresh homes, unmodified marketplace-installed runtime and the same pinned catalog.
The [plan](../../mechanism-campaign.md) predates model calls.

| Observed behavior | Published 0.8.0 | Evaluated candidate |
| --- | --- | --- |
| Useful exact-render implementation; scratch replay passes | 2/2 | 2/2 |
| Consequential checkpoint actually loaded | 0/2 | 0/2 |
| Declared transformation/false-rejection/schema paths caught | 2/2 | 2/2 |
| Command, query-scope and qualified-label paths caught | 2/2 | 2/2 |
| Displaced summary details caught through consumer | 2/2 | 2/2 |
| Completion, interrupted-zero and cache defects caught | 2/2 | 2/2 |
| Equivalent JSON command encoding defect caught | 2/2 | 2/2 |
| Derived metadata overwriting submitted field caught | 2/2 | 2/2 |
| Nonstandard JSON constant defect caught | 1/2 | 0/2 |
| Minimal typo completed without specialist/review machinery | 2/2 | 2/2 |

The builder fixture is a local existing-contract implementation, so it did not
exercise the intended consequential checkpoint. Candidate trial 2 explicitly
names both false-accept and legitimate-label challenges before edits, but none
read the changed checkpoint: this cannot establish activation or causal benefit.
The other builder summaries do not establish the complete new decision protocol.

All four purported fixed families had qualification defects. The display contract
promised an absent suppression consumer; the selection gate rejected equivalent
JSON encodings; derived card metadata overwrote an accepted submitted field; the
receipt parser accepted non-JSON `NaN`. Reviewers were right to flag these. One
baseline display review additionally blocked on nested fields while explicitly
assuming their support; applicability was ambiguous. These inputs do not support
a clean-control acceptance rate or an unequivocal false-positive comparison.
The candidate's two clean receipt reviews missed a materially present defect.
There is no full-matrix pass claim or claim of fewer user interventions/review rounds.

Corrections after the frozen comparison:

- Narrow the display fixture contract to the implemented discovery boundary;
  downstream summary construction is outside this adapter. Original findings
  remain valid against the original contract; they are not rescored away.
- Decode the strictly bounded target command's JSON string; retain invalid/trailing
  command rejection while allowing valid alternate encodings.
- Keep derived collection semantics separate from serialized submitted fields.
- Reject nonstandard JSON constants in the fixed receipt parser.
- Preserve repository exit-status policy in the generic completion wording;
  exit status alone is insufficient, rather than universally requiring zero.
- Fix relative-checkout argument redaction, which otherwise replaces ordinary
  periods in public metadata. This is a repository runner repair, not a new runner.

These corrections have deterministic checks and a bounded source/evidence delta
review. **They were not naturally rerun.** Neither the evaluated runtime's results
nor the original fixtures' scores are inherited onto the final revision.

## Evidence and cost

[Receipt](receipt.json) records native-normalized context IDs, historical IDs,
record/trace/fixture/runtime hashes, per-trial rubric assessments, reads and cost.
[Baseline](baseline-observations.json) and [candidate](candidate-observations.json)
excerpts retain every assistant message and tool call plus check/edit outputs.
Pure-read outputs, user/catalog messages and private reasoning are omitted from
these excerpts; complete native records remain privately retained by their hashes.
Fixture source and the exact evaluated commits remain in Git history.

Original public exports failed integrity validation because `--package .` caused
period redaction. Original exports and native bytes remain immutable. Separate
analysis views restore the exact metadata substitution, verify source/input/fixture
hashes and rebuild public records from native records using absolute path redaction.
The existing attribution validator verifies those derived views, native completion,
identities, usage and fixture hashes. Receipt reconciliation entries bind both
original and derived inventories. No model trial was replaced. A prior setup
argument error happened before any model invocation and is retained separately.

| Same-cohort metric | 0.8.0 | Candidate | Change |
| --- | ---: | ---: | ---: |
| Median invocation wall time | 58.28s | 59.03s | +1.3% |
| Total input tokens | 1,440,297 | 1,402,900 | -2.6% |
| Uncached input | 252,201 | 260,500 | +3.3% |
| Output tokens | 26,805 | 26,390 | -1.5% |
| Native contexts | 20 | 20 | unchanged |

These small differences establish neither efficiency nor reliability improvement.
System skills/app recommendations and a duplicated global `find-skills` declaration
are inherited; their native catalog declarations/hashes are retained. The pinned
catalog is equivalent between versions, no personal custom agents were used, and
all comparison contexts were fresh. No live provider/device facts were claimed.
Source-review cost is separate and unavailable from the parent launcher.

## Follow-up, outside this bounded campaign

- Use a genuinely consequential builder probe before claiming checkpoint activation;
  do not force small pure-library work into governance to satisfy an eval.
- Qualify repaired controls in a separately predeclared natural comparison before
  claiming clean-implementation acceptance or better first-review reliability.
- Track the source review's initial misses and candidate receipt-review misses;
  do not add JSON-specific prose or another specialist to explain them away.
