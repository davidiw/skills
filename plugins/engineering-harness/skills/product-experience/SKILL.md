---
name: product-experience
description: Diagnose or shape user jobs, task flows, information priority, navigation, and recovery. Use when a meaningful product experience decision is unresolved or UX critique is requested; not for settled presentation fixes.
---

# Product Experience

Own what people are trying to accomplish and how they understand, complete, and
recover from that task. Use accepted product decisions; a request to improve a
screen is not a request to replace its purpose.

1. Establish the user, usage situation, job, intended outcome, and accepted
   surface/owner from repository evidence. Reuse settled facts. Mark material
   unknowns instead of inventing personas or research.
2. Inspect the current path and available rendered experience before selecting a
   correction. Separate observed friction from source inference and untested
   human-outcome hypotheses. For meaningful experience claims, use the
   [rendered-evidence contract](../interface-design/references/rendered-evidence.md).
3. Decide whether friction concerns product/IA, flow/state, visual treatment,
   language, or implementation. Rank blocked tasks, misleading consequences and
   inaccessible recovery ahead of polish. For navigation or multi-state flows,
   read [tasks and recovery](references/tasks-and-recovery.md).
4. Propose the smallest correction. An added card or destination may worsen the
   existing job; integration into an accepted surface may be better. That judgment
   does not approve an IA or product-contract change. Use the router's existing
   scope decision before implementation; pending boundaries remain untouched.
5. Implement authorized work and verify the relevant sequence and states. Specify
   observable success without claiming measured comprehension or engagement from
   expert inspection. Preserve useful behavior even when presentation changes.

UI craft belongs to interface-design only when a visual decision remains;
identity/wording belongs to brand-and-language when unresolved. Consume those
contracts without automatic skill fanout. Application Composition owns useful
loading and shared semantics; Durable Workflows owns persistence/recovery mechanics;
authorization remains with its existing owner. Consult exact relevant
[invariants](../../references/invariants.json) only for unresolved engineering
obligations, and [precedence](../../references/precedence-and-exceptions.md) for conflicts.

Done means the in-scope friction has a bounded correction or concrete approval
handback, relevant experience evidence, and explicit limits. Ordinary successful
work needs a short result, not a scorecard or repeated scope table. Critique stays
read-only unless edits are requested; required independent review uses the existing
fresh-review handoff, not a skill loaded into the builder.
