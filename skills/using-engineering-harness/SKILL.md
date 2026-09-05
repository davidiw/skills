---
name: using-engineering-harness
description: Bootstrap or adopt a repository, route ordinary change work, or harden demonstrated architecture friction while loading only the internal Engineering Harness skills required.
---

# Using Engineering Harness

This is the public entry point. Users choose a workflow, not specialist skills.

## Workflows

- **Bootstrap:** establish authority, constraints, capability profile, and the
  cheapest useful boundaries for a new repository or major subsystem.
- **Adopt:** inspect a brownfield repository, propose a capability profile with
  evidence and confidence, reconcile it with repository decisions, and add
  only justified enforcement.
- **Change:** implement an ordinary feature, fix, migration, or refactor. Route
  internally by risk and keep the public workflow proportional.
- **Harden:** investigate demonstrated architecture divergence or recurring
  friction, consolidate ownership, repair the root cause, and prevent recurrence.

Read [`precedence-and-exceptions.md`](../../references/precedence-and-exceptions.md)
before a harness recommendation could stop work, request authority, or alter
the repository's chosen workflow.

## Route

1. Identify the workflow from the user's request; do not ask the user to pick
   an internal skill.
2. Read the repository's `AGENTS.md` or equivalent, design authority, work
   tracker, and operator-command index. Report conflicts rather than replacing
   repository decisions.
3. For **Adopt**, run `scripts/profile_repository.py` to create an evidence-backed
   proposal, review uncertain detections, assign repository enforcement owners,
   record approved exceptions, and mark the profile accepted.
4. For **Change** or **Harden**, read
   [`change-classification.md`](../../references/change-classification.md) and
   build the smallest applicable internal risk card.
5. Name the authoritative fact or behavior, its owner, requested outcome,
   non-goals, and authorized action scopes.
6. Use the single linked routing table and dominance rules in
   `change-classification.md`. For every material risk-card signal, either name
   the selected owner skill or the exact dominance rule that excludes it. Read
   every selected specialist from the table's direct `SKILL.md` link before
   proposing work or evidence. A minimal change normally selects no specialist;
   several triggers on one path form one integrated analysis. Do not infer an
   owner skill's policy from the invariant catalog or answer a non-minimal
   request from the router alone.
7. For consequential work, identify active invariants in
   [`invariants.json`](../../references/invariants.json) and their current
   enforcement rungs and exceptions. Reuse existing documents and commands.
8. Execute the user's task. Internal classification is not a substitute for work
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

The route is complete when the selected public workflow is clear, internal
routing is proportional, every material risk has one owner, and irrelevant
specialists and artifacts remain unloaded.
