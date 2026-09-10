# Independent post-trial disposition

Complete reviewer receipt below, with local path prefixes replaced by symbolic
labels and the local receipt link mapped to its adjacent published artifact.
Original receipt SHA-256: `d30d7b8b15847336b6f30ad17384d0d2a7eec44593d513b92cc6685537431cce`.

The maintenance change remains ready for its separate PR at `e709a2f5090a3884caadfb23ba2637fd6d12e542`, with the previously recorded environment limitation disclosed. The workflow source at `ea958c9a923c556bf60b94cc3cfbbb2748fd9888` may proceed as a draft PR with an explicit pending natural acceptance gate. The connected workflow has not completed acceptance, and the declared trial budget is exhausted.

The complete known findings are:

| Finding | Severity / confidence | Classification and evidence |
|---|---|---|
| Natural operator execution and final implementation acceptance did not occur. | Acceptance blocker / high | **Budget limitation.** The corrective trial ended at 900 seconds after implementation. Operator context completed startup only. External post-trial tests cannot supply these missing natural stages. |
| The substantive worker read the installed 0.8.0 router despite the candidate-only assignment. | P2 / high | **Observed Harness execution deviation.** `natural-corrective-work-coordinator-native.json:459` records the read of `<installed-harness-0.8.0>/skills/using-engineering-harness/SKILL.md`. This prevents an unqualified claim of candidate-source adherence. It does not establish that the installed read caused a product defect or that another policy edit would solve it. |
| The frozen implementation retains the proposed integer maximum after its recorded withdrawal. | P2 / high | **Fixture-contract ambiguity plus incomplete scope correction.** The contract specifies positive integers without a maximum. The reviewer rejected treating `2**63 - 1` as an implied requirement; the planner withdrew that interpretation pending clarification. Nevertheless, `produced-task-snapshot/inventory.py:26` still rejects larger values, and the worker receipt describes the cap as accepted. The available native record does not establish that the worker received the withdrawal before interruption; this is a stale produced result, not evidence of knowingly ignoring delivered steering. |
| An existing empty-string SKU cannot be reserved. | P2 / high | **Produced-task implementation regression.** `produced-task-snapshot/inventory.py:22` rejects `not sku`. The frozen contract requires an existing SKU and makes the **operation ID** nonempty; it does not prohibit an existing empty-string SKU. `initialize(db, "", 3)` creates that existing key, but reservation raises `ValueError`. The focused test below fails on the produced snapshot and passes on the reference. |

No additional source-policy blocker was established within this correction scope. The previously reviewed five implementation corrections and six startup responsibilities remain resolved.

The actual corrective sequence supports these narrower positive conclusions:

- The initial reviewer inherited `danger-full-access`, completed only startup reads, and was correctly rejected before substantive review.
- The planner then used separate read-only and workspace-write coordinator roots. Their child reviewer, worker, and operator had the intended permissions, models, reasoning levels, and no-history startup calls.
- The valid reviewer challenged the plan and authored eleven substantive tests before worker implementation. The worker received the brief and reviewer receipt.
- The reviewer explicitly challenged the integer-bound interpretation. The planner recorded its withdrawal and sought clarification; that correction did not reach the frozen result before interruption.
- The worker implemented and performed local checks. The natural operator and final reviewer acceptance stages remain absent.

There were **seven model contexts in the corrective repeat**: the primary, one invalid startup reviewer, two supporting coordinators, and three valid role contexts. The separate coordinator exports are essential; the primary export alone is not the complete tree. The earlier hypothesis about a long-lived session causing permission inheritance remains **unproven**. The corrective trial’s initial inheritance mismatch is independently observed.

[posttrial-validation.json](posttrial-validation.json) is now available. Its raw logs show all **7 reservation + 2 hook + 11 natural-reviewer methods passing**, with zero skips and unchanged source/test hashes. These are useful external development results, not natural operator execution. The eleven-test file exactly matches the natural reviewer’s authored Python block, SHA-256 `ab0c432dca8bcfe489eec1bdcfc068d138fcbefa99009660cc3960cc65c6d7f7`. The existing-empty-SKU path is outside those checks’ coverage.

The maintenance reviewer’s 55-method result and prior package/plugin/skill validations remain applicable. The broader suites retain the disclosed single baseline loopback-bind `PermissionError`; they should not be described as wholly green. Original archive-validation failures should remain preserved alongside the corrected Git-backed results.

The smallest justified follow-up is to retain these outcomes and submit separate PR descriptions that distinguish source qualification from pending natural acceptance. Another policy correction or trial campaign is not justified by this review. Any later connected completion needs resolution of the quantity-domain ambiguity, application of the resulting scope decision, correction of the existing-SKU regression, and completion of the missing stages under a newly declared budget. Preserve the interrupted snapshot rather than modifying its historical result.

This is the additional deterministic check for the operator. It uses an in-memory database and does not modify the snapshot:

```bash
python3 - <scratch>/produced-task-snapshot <<'REVIEWER_PY'
import hashlib
from pathlib import Path
import sys
import types
import unittest

ROOT = Path(sys.argv[1]).resolve()
SOURCE = ROOT / "inventory.py"
raw = SOURCE.read_bytes()
inventory = types.ModuleType("reviewed_inventory")
exec(compile(raw, str(SOURCE), "exec"), inventory.__dict__)

class ExistingSkuAcceptance(unittest.TestCase):
    def test_existing_empty_text_sku_is_accepted(self):
        db = inventory.connect(":memory:")
        try:
            inventory.initialize(db, "", 3)
            self.assertEqual(
                inventory.reserve(db, "blank-sku", "", 1),
                {"operation_id": "blank-sku", "sku": "",
                 "quantity": 1, "status": "reserved"})
            self.assertEqual(
                db.execute(
                    "SELECT quantity FROM stock WHERE sku = ''"
                ).fetchone()[0],
                2)
        finally:
            db.close()

print("source_sha256=" + hashlib.sha256(raw).hexdigest())
unittest.main(argv=[sys.argv[0]], verbosity=2)
REVIEWER_PY
```

For the control, run the same script with `<workflow-source>/evals/conditional-role-reference` as its argument. My observed results were produced snapshot: **one error**; reference: **one pass**.

Exact reviewed boundaries:

- Workflow runtime: `ea958c9a923c556bf60b94cc3cfbbb2748fd9888`.
- Workflow retained-evaluator artifact commit: `4798b9aa7767c57124368c31260a0510589c55c7`.
- Maintenance: `e709a2f5090a3884caadfb23ba2637fd6d12e542`.
- Produced `inventory.py`: SHA-256 `ab1365bf613970466c9ea75c8b7e23ac675645cb5109e44948910f2f61c76d36`.
- Produced snapshot manifest: SHA-256 `dc04cb944f545d4c6e95cfc0bf61acd205e2d7a4e27598f6837964f6b665f8a7`.
- All five manifest files and all seven native-context source hashes matched the supplied records.

The workflow README modification and new evidence-report directory being prepared concurrently are excluded from this frozen review; their eventual artifact commit needs a scoped check. Native evidence supports fresh role startup and scoped assignments, but opaque payload portions cannot be independently reconstructed. No natural final implementation review exists to assess. Caller-owned transactions, callback reentrancy, and other unspecified behavior were not turned into new requirements.

Reviewer context remained independent of builder private reasoning. I used public assignments, frozen source, contracts, receipts, and native execution evidence; no production changes were made.