# Security and Privacy Assurance

Evidenced threats can block without a cataloged invariant. Technical assurance is
not mathematical proof, legal compliance, or a claim of vulnerability absence.

## Scope and evidence

- **Changed path:** named flow/diff plus callers, dependencies and delayed consumers
  needed to assess harm.
- **Release security/data-lifecycle privacy:** launch, whole-system readiness or
  external-review preparation covers the entire candidate, including unchanged,
  legacy and shadow paths. A clean diff does not establish release readiness.

Bind evidence to the commit plus worktree patch/content hashes, or exact release
revision. Verify repository threat/privacy decisions against source. Security owns
changed/newly exposed trust or authorization boundaries; privacy owns changed
sensitive collection, use, derivation, disclosure, retention, expiry or erasure.
Explicit requests select their lens without requiring a diff; existing credentials,
fences or sensitive-project flags alone select neither. Use both for combined scope.

Keep **one release matrix**: source evidence, owner, boundary/data category,
hypothesis, and status: **unreviewed**, **reviewed with evidence**, **blocked**,
**unavailable**, or **not applicable with rationale**. Retain initial content before
probes through existing history or a permitted copy. Update cells and add discovered
rows; include the reconciled matrix in the final receipt, linking findings by ID.
State each finding and row-specific limit once. Inventory existence is not proof;
unreachable/out-of-scope claims need evidence or an explicit limit.

## Independence

An already-fresh reviewer without builder history performs the assigned gate and
records that status; it need not create its own child. Builders use the
[fresh-context handoff](assurance-handoff.md) after implementation checks.
Reviewer skills in the builder are **self-review**; unavailable required independent
review leaves that gate pending. Do not invent independence requirements for
review-only requests that lack them.

For combined campaigns, provide authorized fresh reviewers scope/non-goals,
snapshot, contracts, permitted effects and assigned coverage rows. One fresh context
can cover both lenses on a bounded path. Reconcile complete findings and uncovered
rows with actual context status; delegation and production-scale coverage are not
guaranteed.

## Findings and receipt

A blocker needs a reachable path/prerequisites, an evidenced obligation (repository
rule, invariant or newly evidenced threat), and material harm. Suggestive names or
hypothetical possibilities without reachability are questions. Explain uncatalogued
harm plainly and record any catalog gap separately; no invariant ID is required.
No production edits; use synthetic checks.

Return the **complete currently known blocker set once**, in four fields:

- **Snapshot/context:** exact revision/hashes, fresh/self-review status and context
  evidence.
- **Coverage/evidence:** exercised hypotheses, source locations and check/results;
  completed matrix for release review. Link retained commands/artifacts rather than
  reproducing their contents or contracts.
- **Disposition:** complete blocker set (empty when clean), nonblocking follow-ups
  and pending gates. Each finding includes location, severity/confidence,
  path/consequence, evidence/reproduction, smallest correction and relationship to
  prior review. Other sections reference its ID.
- **Limits:** shared proof limits and residual exposure once; row-specific limits
  stay in their matrix rows. Preserve every unreviewed/unavailable area.

Keep complete evidence behind the links. A clean changed-path receipt normally
needs 200–300 words plus references: a presentation target, never an investigation
budget. Expand blockers, pending boundaries, residual exposure and coverage gaps
enough to assess them. Release matrices and full finding details remain mandatory;
brevity cannot convert incomplete coverage into a pass.

Corrections use the handoff's delta scope and initial-review-miss rules; do not
drip-feed known blockers. Set coverage/time bounds from the request, not the
architecture audit's ten-minute/three-thread cap. If budget ends, report incomplete
coverage; unexamined paths do not pass. Release eligibility follows repository
policy and authorized exceptions, not absence of findings in a limited review.
Before stopping authorized work or requiring a new action, apply
[precedence and exceptions](precedence-and-exceptions.md).
