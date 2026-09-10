# Review an engineering change

Use for a general code/PR review. Explicit security/privacy or release assurance
retains its own coverage contract. This method is usable directly by a reviewer;
loading Verification and Operations is not a prerequisite.

1. Bind the requested diff or named implementation to its actual snapshot. Find
   the accepted outcome, scope/non-goals and repository standards through existing
   profile/document pointers. Infer a comparison base only when unambiguous; state
   the choice. A missing spec limits coverage; inspect available contracts rather
   than inventing a setup procedure or blocking all useful review.
2. Inspect accepted behavior and repository standards along the execution path.
   For correctness boundaries (validators, sanitizers, normalizers, identity
   resolution, completion detection), challenge both an invalid case that could
   pass and a valid case that could be rejected or damaged. Trace downstream
   protections before reporting a defect; challenge the reviewer's hypothesis too.
   A green suite does not cover omitted behavior: inspect coverage and use focused
   checks at the concrete seam.
3. Match coverage to the claim: identify relevant variants and actual consumers
   in a compact working map or existing record, not a new mandatory document.
   Consider applicable input/output schemas, selectors, success/failure paths,
   partial/complete evidence and preview-backed/summary-only consumers. Do not
   claim the family is covered from one variant. Follow the existing delta-review
   contract when a correction displaces behavior or information.
4. Block only on an evidenced plausible path, an applicable accepted requirement
   and material consequence. Smells are questions, not standards. A limited
   preservation guarantee does not require proving all original prose or health
   claims true. Separate source inspection, author-reported checks, personally
   executed checks and physical/provider evidence. A clean corrected implementation
   is a valid result; finding something is not the objective.
5. Return the complete currently known blocker set together, with snapshot,
   source/contract locations, severity/confidence, execution path and evidence.
   Consolidate duplicate symptoms while retaining affected paths; separate
   nonblocking advice and unavailable coverage. Preserve prior dispositions.

Both lenses normally fit the same review context. Use the existing
[handoff](../../../references/assurance-handoff.md) for required independence,
correction scope, complete receipts and initial-review misses; this method adds no
automatic fanout or new independent gate. Review remains read-only.
