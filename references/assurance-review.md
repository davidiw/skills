# Security and Privacy Assurance

The invariant catalog is a starting vocabulary, not a complete threat model.
Security and privacy reviewers consume its rules without restricting findings
to them. This workflow is an evidence-based review, not a claim of mathematical
verification, legal compliance, or exhaustive vulnerability absence.

## Scope and evidence

Select the scope before investigating. **Changed-path assurance** covers the
named flow or diff and its relevant dependencies. **Release-surface security
assurance** and **release data-lifecycle privacy review** start from inventories
of the complete candidate system, including unchanged, legacy, and shadow paths.
Use those release modes when launch readiness or preparation for an external
security/privacy review is requested. Ordinary changes retain changed-path scope.

Bind either mode to an identifiable snapshot:
commit plus worktree patch/content digests for local work, or the exact release
revision for a release gate. Use repository threat assumptions and privacy
decisions, checking them against the implementation. In changed-path mode, trace immediate callers,
dependencies, and delayed consumers needed to assess the hypothesized harm.

Select security assurance for changes to or new exposure of trust/authorization
boundaries; select privacy assurance for changes to sensitive collection, use,
derivation, retention, disclosure, expiry, or erasure. Explicit assurance
requests select the appropriate reviewer regardless of whether code changed.
Carrying credentials or preserving existing fences does not itself select a
security reviewer; a sensitive project flag does not itself select a privacy
reviewer. Use both when the requested scope includes both concerns.

Release modes produce a coverage matrix before attacking individual paths.
Inventory entries name source evidence, owner, boundary/data category, planned
hypothesis, and status: unreviewed, reviewed with evidence, blocked, unavailable,
or not applicable with rationale. Inventory existence is not passing evidence.
Unreachable or out-of-scope claims require evidence or an explicit scope limit.

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

For release modes, reconcile the final coverage matrix against the initial
inventory and newly discovered surfaces/destinations. A clean diff does not
establish release readiness. Split independent security and privacy contexts
over the same snapshot when both are requested; share raw contracts and source,
then reconcile overlaps and conflicting dispositions. Preserve independent
review status and any unreviewed/unavailable rows in the handback.

Set coverage and time bounds from the requested assurance scope. The bounded
architecture audit's ten-minute/three-thread cap does not define assurance
completion. If a budget ends first, report coverage incomplete; do not describe
unexamined paths as passing. Release eligibility follows repository policy and
authorized exceptions, not the absence of findings in a limited pass.

Before stopping authorized work or requiring a new action, apply
[`precedence-and-exceptions.md`](precedence-and-exceptions.md).
