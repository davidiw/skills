---
name: using-engineering-harness
description: Bootstrap or adopt a repository, route ordinary change work, or harden demonstrated architecture friction while loading only the internal Engineering Harness skills required.
---

# Using Engineering Harness

This is the public entry point. Users choose a workflow, not specialist skills.

Review and assessment requests use **Change in review mode**: classify the
behavior being reviewed, even though the requested action is read-only. A
sensitive lifecycle review is consequential; read-only scope does not make its
subject minimal. For security/privacy assurance, load the applicable reviewer(s)
from the routing table directly and let their references supply implementation
contracts. An assurance-only request does not require every implementation
specialist or authorize fixes. Explicit assurance requests bypass the minimal
edit shortcut below.

**Assurance-only shortcut:** a request to assess security, authorization, or a
sensitive data lifecycle is an assurance review even if it never uses the word
“assurance.” Read the routing table, select `security-assurance` and/or
`privacy-assurance`, complete that review, and finish. Skip the implementation
owner inventory and specialist-loading steps below. If the user also requests
fixes, use the full Change route and then review the corrected snapshot.

For **Change** and **Harden**, read `change-classification.md` before applying
another installed workflow or inspecting solution code. If the resulting route
is non-minimal, read every selected owner skill before continuing. Another skill
may supplement this route, but does not replace it.

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
2. Read the repository's `AGENTS.md` or equivalent and locate the changed owner.
   For Change, apply the minimal test in
   [`change-classification.md`](../../references/change-classification.md)
   first. If it passes, use the existing edit/check path and finish; the
   inventory and risk-accounting steps below do not apply. Otherwise read the
   relevant design authority, work tracker, and operator-command index when
   present. Report conflicts rather than replacing repository decisions.
3. For **Adopt**, run `scripts/profile_repository.py` to create an evidence-backed
   proposal, review uncertain detections, assign repository enforcement owners,
   record approved exceptions, and mark the profile accepted.
4. For **Change** or **Harden**, use
   [`change-classification.md`](../../references/change-classification.md) to
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
   When the changed path affects sensitive data or authorization, select the
   applicable security/privacy assurance reviewers from the routing table.
   The invariant catalog does not limit the defects they may discover.
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
