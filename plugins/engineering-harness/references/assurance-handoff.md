# Independent Review Handoff

Use for recorded independent gates: consequential trust/security or sensitive-data
lifecycle changes; repository-required persistence, migration, deletion, durable
state, public/provider contract or high-risk architecture review; release gates;
and explicit independent-review requests. Ordinary bounded work needs focused
builder checks, not a reviewer by default.

## Fresh context after focused builder checks

Prefer a configured general read-only reviewer role when available; otherwise
use a fresh generic agent. Do not require a user's role inventory or create one
agent role per skill domain. Roles own model/reasoning, sandbox and a narrow
mandate; skills own policy and review methods. Keep role instructions short and
free of copied invariant, scope, testing, assurance and release checklists.
Astra suits difficult root work and consequential reviews; select reasoning
proportionally rather than giving scouts/mechanical workers maximum reasoning.

Discover the runtime's agent tools before claiming delegation unavailable. If tools
are deferred, search their names/descriptions for **agent**, **spawn**, or
**delegate** (for example the runtime's `ALL_TOOLS` catalog); absence from the
initial visible tool list is not evidence of absence. Use the supported spawn
operation with **no builder-history fork** (`fork_context: false` or the runtime's
equivalent). Record an actual unavailable/error result when fallback is necessary.

Save a compact, readable review packet and its content hash before launching.
Identify the recipient as the **fresh reviewer**, the actual no-history
spawn setting, and exact assigned reviewer `SKILL.md` paths. The reviewer reads
those entry points directly; it need not rediscover the router or spawn another
reviewer for this same gate. Batch independent source/contract/skill reads.
Include requested outcome, acceptance criteria, scope/non-goals, exact commit plus
worktree diff/file hashes, relevant authoritative contracts, already-executed
commands/results and permitted review actions. Give source locations so the
reviewer can inspect independently. Exclude private builder reasoning, design
justifications, expected findings and persuasive safety conclusions.

The observable launch must derive its **entire assignment** from that packet.
A no-history flag proves history separation, not the contents of an opaque message.
If delegation encrypts/hides the assignment, use an existing permitted fresh-session
API with observable packet-file/stdin input instead; do not add a launcher framework.
For example, a new `codex exec` session can receive only the saved packet on stdin,
with the selected model/effort, read-only sandbox and final receipt file. Record
that actual generic launch and any configured role settings applied; do not call it
a named custom-agent invocation unless the runtime did so. Never use resume/fork
for the first review, or bypass disabled delegation or execution permissions.
If no auditable fresh launch is available, report **freshness verified / handoff
content unavailable** where applicable and leave full independence evidence pending.
Keep raw reviewer traces outside the builder context; read the compact final receipt.

One fresh reviewer may cover security and privacy on the same bounded execution
path. Separate additional contexts only for distinct coverage obligations; do not
create one agent per label. Broad release campaigns retain scoped lens ownership.

The reviewer loads only the required review skill(s) and supporting contracts in
that fresh context: [security](../skills/security-assurance/SKILL.md),
[privacy](../skills/privacy-assurance/SKILL.md), or the repository's required
reviewer. It may run permitted synthetic checks; it makes no production edits or
live probes. Loading a reviewer skill inside the builder never satisfies an
independent gate. If fresh contexts are unavailable, label **self-review** and
leave the required independent gate pending.

## Complete handback, then bounded correction review

Ask for the **complete currently known blocking set in one pass**, each with
severity, confidence, concrete execution path and evidence; non-blocking follow-ups;
explicitly unreviewed/unavailable areas; exact reviewed snapshot and evidence used;
and actual reviewer-context status. A time/coverage limit must remain visible.

Finish focused checks before handoff, then wait for the complete handback.
Use bounded waits of roughly 30–60 seconds where supported, not repeated short
polls or progress-only messages. Do not alter the reviewed snapshot or react to
partial findings before the complete blocker set arrives; continue only independent
work outside that snapshot. Correct the blocker set within authorized scope. Request
a **delta-scoped independent review**, reusing the independent reviewer context
when available, of corrections, directly affected seams and
introduced regressions, preserving the earlier receipt and coverage limits.
Do not restart unchanged scope unless a correction expands scope, invalidates an
assumption or exposes a newly reachable surface. A late blocker materially present
and reasonably discoverable in the initial snapshot is an **initial-review miss**,
unless its area was explicitly unreviewed/unavailable. Record that classification
against the earlier receipt to measure convergence; never hide it as a new defect.

Completion records the reviewed snapshot(s), context separation, findings and
disposition, misses and remaining gates. Record custom/generic role, actual child model/reasoning, skills loaded and
freshness evidence. Measure builder and reviewer tokens/time separately when observable. This uses available tools, not a new orchestration
runtime; context separation plus evidence satisfies independence, skill selection
alone does not.
