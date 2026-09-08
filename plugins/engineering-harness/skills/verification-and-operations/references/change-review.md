# Review an engineering change

Use for a general code/PR review. Explicit security/privacy or release assurance
retains its own coverage contract. This method is usable directly by a reviewer;
loading Verification and Operations is not a prerequisite.

1. Bind the requested diff or named implementation to its actual snapshot. Find
   the accepted outcome, scope/non-goals and repository standards through existing
   profile/document pointers. Infer a comparison base only when unambiguous; state
   the choice. A missing spec limits coverage; inspect available contracts rather
   than inventing a setup procedure or blocking all useful review.
2. Inspect both obligations within the applicable surface: does behavior satisfy
   the accepted request, including failures and omissions, and does it respect
   repository standards? Follow callers/dependencies needed to establish a defect.
   A green test suite does not prove omitted behavior is implemented. Read its
   coverage before relying on it; use focused checks to challenge concrete paths.
3. Treat design smells as questions until there is a demonstrated consequence or
   accepted rule. Do not impose a generic smell catalog, document layout or
   refactoring preference. Distinguish required behavior from optional improvement.
4. Return one complete blocking set with snapshot, source/spec locations,
   severity/confidence, execution path and evidence; separate nonblocking advice
   and unavailable coverage. Consolidate duplicate findings across the two lenses.

Both lenses normally fit the same review context. Use the existing
[handoff](../../../references/assurance-handoff.md) for required independence,
correction scope, complete receipts and initial-review misses; this method adds no
automatic fanout or new independent gate. Review remains read-only.
