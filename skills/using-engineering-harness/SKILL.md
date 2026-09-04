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
5. Select from the exact specialist names below and read each linked
   `SKILL.md`. Report those exact names; never invent generic skill labels. A
   `minimal` change normally selects no specialist.

   | Trigger | Specialist |
   | --- | --- |
   | New subsystem, authority, ownership, dependency, or composition | [`architecture-foundations`](../architecture-foundations/SKILL.md) |
   | Accepted work can outlive its initiator | [`durable-workflows`](../durable-workflows/SKILL.md) |
   | Public API, process, client, provider, trust, message, or event contract | [`interfaces-and-events`](../interfaces-and-events/SKILL.md) |
   | UI/domain/assistant/platform parity, useful paint, or capability composition | [`application-composition`](../application-composition/SKILL.md) |
   | Persistence, identity, replication, migration, deletion, repair, or mixed versions | [`data-and-compatibility`](../data-and-compatibility/SKILL.md) |
   | Explicit recurring-hotspot work or high-risk adversarial audit | [`architecture-hardening`](../architecture-hardening/SKILL.md) |
   | Acceptance evidence, operator tooling, generated/physical proof, or external release action | [`verification-and-operations`](../verification-and-operations/SKILL.md) |

   Several triggers on one execution path form one integrated analysis, not
   parallel architecture exercises.
   Apply the dominance rules in `change-classification.md`: ordinary tests,
   owner naming, private durable storage, UI observation, and internal adapter
   contracts do not each justify another specialist.
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
