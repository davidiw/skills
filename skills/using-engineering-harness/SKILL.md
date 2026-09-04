---
name: using-engineering-harness
description: Classify a proposed engineering change and select only the Engineering Harness skills its risks require.
---

# Using Engineering Harness

Use this explicit router when the right engineering workflow is unclear or a
consequential initiative needs a preflight.

## Route

1. Read the repository's `AGENTS.md` or equivalent, design authority, work
   tracker, and operator-command index. Local policy wins.
2. Read [`change-classification.md`](../../references/change-classification.md)
   and build the smallest applicable risk card.
3. Name the authoritative fact or behavior, its owner, the requested outcome,
   explicit non-goals, and the external actions actually authorized.
4. Classify the work as exactly one of `minimal`, `bounded`, `consequential`,
   or `stabilization`. Use those labels verbatim.
5. Use the single linked routing table and dominance rules in
   `change-classification.md`. Read each selected specialist from the table's
   direct `SKILL.md` link. Report exact names and never invent generic skill
   labels. A `minimal` change normally selects no specialist. Several triggers
   on one execution path form one integrated analysis, not parallel
   architecture exercises.
6. For consequential work, identify active invariants in
   [`invariants.json`](../../references/invariants.json) and their current
   enforcement rungs. Reuse existing documents and commands.
7. Execute the user's task. A preflight is not a substitute for implementation
   unless the user requested analysis only.

## Proportionality

- A tiny CLI or static page normally needs one owner and focused proof, not a
  durable workflow or compatibility program.
- A state machine is justified by meaningful lifetime, replay, or transition
  rules, not by ordinary CRUD.
- Worktrees, queues, release trains, and immutable evidence are activated by
  repository policy or real integration risk, not imposed universally.
- A vendor runtime is selected after the required durability and failure
  contract is explicit.

The route is complete when the response states one exact class, exact selected
specialist names or `none`, every material risk has one owner, and irrelevant
specialists and artifacts are explicitly omitted.
