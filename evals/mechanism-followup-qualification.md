# Follow-up fixture qualification

This is deterministic fixture qualification, not a new natural trial or a revision
of the original results. The runtime and original result directory are byte-for-byte
unchanged from `34edf084597fdd53ef54edb6832e83f164e3fd2c`.
The local `challenge-correction` task now has a minimal current-corpus expectation;
its fixture and original retained scores/observations are preserved.

Personally executed:

- `python3 -m unittest discover -s tests -p test_mechanism_fixtures.py`: 8 checks pass.
- `python3 -m unittest discover -s tests -p test_mechanism_followup.py`: 8 checks pass.
- `python3 -m unittest discover -s tests`: 131 tests pass.
- `python3 scripts/validate_package.py`: package/profile/link validation passes.

| Qualified surface | Positive and distinguishing evidence |
| --- | --- |
| Fixed transform | Exact substitutions, ordinary inaccurate text, repeated/literal labels; rejects changed content and unknown refs; actual service returns input/output root fields, including duplicate names across schemas |
| Fixed selection | Both actual service selectors, duplicate-name qualified proof on all/exact/filtered pages, equivalent JSON encodings, preserved argument copies; rejects wrong slot, negation, trailing content and unproven plain name |
| Fixed card | Producer → serialized wire → consumer for preview and summary operations; omitted/empty/populated lines; every submitted field preserved, including colliding collection_action metadata |
| Fixed receipt | Complete pass/allowed skip and valid reuse; rejects partial, duplicate/missing/mixed-run/failing/forbidden-skip/malformed/nonstandard-JSON reports, interrupted/nonzero execution and missing/changed cache evidence |
| New recovery case | Original cannot recover stranded work; evaluator reference permits deadline takeover and valid completion, rejects expired/displaced claims, preserves output on rejection and across process exit; two separate competing processes admit one claim |
| Recovery counterexample | Reusing worker-name identity across takeover admits the earlier claimant's output; the same schedule rejects that claimant under generation-bound completion |

Recovery commands run through the real fixture `worker` entry points in separate
Python processes against one temporary SQLite database. The reference mechanism
and expected results live only under repository `tests/`, outside the trial fixture
and runtime. No reference implementation or evaluator assertions are supplied to
the agent. The fixture's own smoke test is runnable and passes before implementation.

Qualification is scoped to accepted contracts: root schema discovery, the declared
label proofs, JSON submitted fields, the local receipt protocol and consistent
caller-supplied queue clocks. It does not prove all implementations defect-free,
all possible schema/catalog semantics, physical/provider behavior, or natural
review acceptance. An evidenced defect discovered later still invalidates a clean
control; expected labels do not overrule evidence.

The proposed follow-up is [separately predeclared](mechanism-followup.md). No new
model campaign has been launched and no comparative outcome is claimed.
