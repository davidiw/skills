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

Use the existing native fresh-agent launch when available. Send only the neutral
packet, or its location with a neutral instruction to read it. Do not append builder
reasoning, design persuasion or expected findings to any launch-message field.
Record the actual child identity, no-history setting, packet path/hash and reviewer
receipt. Keep raw reviewer reasoning outside the builder; consume the compact handback.

Distinguish context separation from transport visibility. A no-history launch proves
there was no automatic builder-history fork; it does not prove what was manually
sent. A saved packet and an observed child read establish their respective facts.
If the runtime retains an opaque assignment, record **assignment payload unavailable**;
do not claim its full contents were inspected, or infer either contamination or
neutrality from encryption. Opacity alone is not self-review or a failed gate, and
does not require a different launcher. Assess the actual handoff, context, source
inspection and review evidence. A concrete unresolved concern about forwarded
reasoning must remain pending until resolved; never invent evidence to close it.
Do not bypass disabled delegation or execution permissions.

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
