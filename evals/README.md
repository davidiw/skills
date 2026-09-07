# Evaluation Corpus

These cases test whether the package changes agent behavior, not whether its
files are well formed. Explicit-router runs diagnose specialist content. The
directional [`behavioral-matrix.json`](behavioral-matrix.json) uses natural
prompts with no skill name, runs each case in an isolated temporary repository,
and compares the same model and case with and without the installed package.

`negative` controls make over-engineering a first-class failure. The correct
result leaves small parser, library, static-site, CLI, and build work on existing
paths without adding durability, events, state machines, repositories,
compatibility programs, architecture documents, or operator infrastructure.
`positive` controls require the relevant capability machinery. `mixed` controls
require one bounded concern while excluding adjacent machinery.

## Run contract

1. Pin package revision, model, reasoning effort, harness policy version, and case ID.
   Supply those as evaluator metadata and instruct the agent not to use them for
   skill selection.
2. Provide only the case context and request plus the referenced fake repository
   when one exists. Treat that fixture as the repository root and prohibit
   inspection of the caller's current repository or parent directories. Permit
   read-only inspection of the skill and fixture; prohibit edits and external
   effects unless the case explicitly evaluates them. Do not leak prior
   conclusions between runs.
3. Capture selected skills, proposed/implemented artifacts, commands, and final
   response. Preserve the case request verbatim; natural-prompt runs must not add
   a skill name or routing triggers such as "exact revision," "audit," or
   "release." If the runtime cannot expose selected-skill order, record routing
   as unobservable rather than inferring it from polished final prose.
4. Score against [`rubric.md`](rubric.md), required outcomes, and forbidden
   outcomes. A forbidden destructive action or false evidence claim is a hard
   failure regardless of score.

For installed-versus-control runs, use separate fresh `CODEX_HOME` directories
and install the plugin only in the harness home. Do not pass
`--ignore-user-config` after installation: that option also ignores the
isolated home's plugin configuration and silently turns the harness arm into a
second control. Install independently into each fresh harness home, or reuse one
verified installed home sequentially; copying an installed `CODEX_HOME` does not
re-register its skill aliases. Verify plugin inventory in both homes before
model calls.
5. Preserve non-sensitive results with content hashes. Private fixtures and
   outputs remain outside Git and contribute only bounded aggregate scores.
6. Add trials or cases without discarding earlier results. Compare only runs
   whose package revision, policy version, model, fixture, and scoring version
   are explicit.

`scripts/validate_package.py` validates corpus shape and routing names. It does
not execute a model or claim behavioral success.

The retained historical non-statistical execution receipt is
[`results/0.4.0-directional.json`](results/0.4.0-directional.json). It records
selected run revisions, routing, scores, latency, token use, output digests, and
known model variance without treating structural validation as execution.
Its inputs are validated against the recorded Git revision and policy, not the
current corpus. It does not prove 0.5.0 behavior. The expanded matrix includes
synchronous authorization changes, telemetry after erasure, optional-audit
contention, purpose-scoped browser handoff, an uncatalogued threat, and local
documentation regeneration.

For a reliability claim, run repeated trials against one frozen package snapshot
with separate control and harness environments. Include an installed competing
diagnosis skill and real edits in isolated fixture copies; keep evaluator
metadata from influencing routing. Report all trials, routing misses and excess
loads, latency, cached and uncached tokens, and required/forbidden outcomes.
Explicit-router forward tests diagnose content and routing instructions; they
do not establish natural-prompt discovery or installed-versus-control benefit.
The bounded [0.5.0 development notes](results/0.5.0-forward-notes.md) retain
observed findings, routing misses, retests, and missing evidence from that work.

The candidate [assurance matrix](assurance-matrix.json) uses two trials per arm
on one frozen package snapshot. It adds natural security/privacy discovery,
preservation of existing sync/UI fences, copy-only work in a sensitive project,
and release-wide reviews of unchanged surfaces. A competing diagnosis skill is
present identically in both arms. Record observable tool reads separately from
unobservable selection; final prose alone is not routing evidence. Keep setup
outside model latency and preserve all attempts, timeouts, and failures.

Cases without a fixture are taxonomy fixtures until a realistic isolated
repository is added. Do not count them as end-to-end behavioral evidence.
