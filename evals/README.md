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
5. Preserve non-sensitive results with content hashes. Private fixtures and
   outputs remain outside Git and contribute only bounded aggregate scores.
6. Add trials or cases without discarding earlier results. Compare only runs
   whose package revision, policy version, model, fixture, and scoring version
   are explicit.

`scripts/validate_package.py` validates corpus shape and routing names. It does
not execute a model or claim behavioral success.

Cases without a fixture are taxonomy fixtures until a realistic isolated
repository is added. Do not count them as end-to-end behavioral evidence.
