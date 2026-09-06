# Security and Privacy Assurance

The invariant catalog is a starting vocabulary, not a complete threat model.
Security and privacy reviewers consume its rules without restricting findings
to them. This workflow is an evidence-based review, not a claim of mathematical
verification, legal compliance, or exhaustive vulnerability absence.

## Scope and evidence

Bind the review to the changed execution paths and an identifiable snapshot:
commit plus worktree patch/content digests for local work, or the exact release
revision for a release gate. Use repository threat assumptions and privacy
decisions, checking them against the implementation. Trace immediate callers,
dependencies, and delayed consumers needed to assess the hypothesized harm.

Select security assurance for principal, credential, grant, trust, or effect
authority; select privacy assurance for sensitive data use, derivation,
retention, disclosure, and erasure. Use both when one path changes both. The
profile activates the obligation; a copy edit elsewhere in a sensitive project
does not require an assurance campaign.

Review independently of the implementation reasoning when possible, using a
separate reviewer with the raw scope, intended behavior, and source snapshot.
Do not seed it with the author's expected findings. If independent review is
unavailable, label a self-review and leave any required independent gate pending.

## Findings

A blocking finding requires:

1. a concrete, reachable execution path and its prerequisites;
2. evidence of a violated security/privacy obligation, whether from an existing
   invariant, repository requirement, or a newly identified threat;
3. a material consequence such as unauthorized access, session confusion,
   sensitive disclosure, retained data after erasure, or blocked revocation.

Record location, severity, confidence, evidence or focused reproduction, and
the smallest correction. For a new threat, explain the obligation and harm in
plain language; record a catalog gap separately. A missing invariant ID cannot
downgrade an evidenced defect. Conversely, a suggestive name or hypothetical
possibility without a reachable path is a question, not a proven blocker.

## Completion

Return ordered findings, reviewed snapshot, exercised hypotheses, and uncovered
paths. The reviewer changes no production files. Use synthetic data and focused
checks to test hypotheses. Review corrective changes at their affected seams.

Set coverage and time bounds from the requested assurance scope. The bounded
architecture audit's ten-minute/three-thread cap does not define assurance
completion. If a budget ends first, report coverage incomplete; do not describe
unexamined paths as passing. Release eligibility follows repository policy and
authorized exceptions, not the absence of findings in a limited pass.

Before stopping authorized work or requiring a new action, apply
[`precedence-and-exceptions.md`](precedence-and-exceptions.md).
