# Batch import contract

`work.py` owns validated batch import. Each item is normalized once and invalid
items are reported without preventing independent valid items from completing.
The coordinator owns whether a proposed named archive destination or retry
policy changes this contract. Existing `test_work.py` is the focused regression
seam; `test_report.py` checks the local generated report.

The shared report output is the accepted bounded result. A change that crosses
an accepted persisted customer-archive handoff is high risk and requires one
fresh bounded adversarial review and an exact-head acceptance matrix. Proposed
per-partner destinations and recovery retention do not create that handoff
until their architecture and scope are accepted. That matrix is expensive. The
existing local checks are the cheapest available evidence; they must be
interpreted before choosing further work.
