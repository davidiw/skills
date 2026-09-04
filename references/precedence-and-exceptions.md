# Precedence and Exceptions

Apply instructions in this order:

1. applicable safety, legal, platform, and repository constraints;
2. explicit user intent and repository-authoritative product or architecture
   decisions;
3. Engineering Harness defaults and recommendations.

The harness does not silently replace an established repository decision. If
the repository and harness disagree, report the decision, the conflicting
harness rule, and the consequence, then follow the higher-precedence direction
unless an applicable safety constraint prohibits it.

## Invariant exceptions

A repository may accept a scoped invariant exception. Record it in
`engineering-harness.json` with:

- invariant ID;
- exact scope;
- rationale;
- repository authority that accepted it;
- optional removal condition.

An agent does not invent or broaden an exception. The invariant remains active
outside its recorded scope. Higher-precedence safety constraints are not
waived by a profile exception.

## Workflow effects

When harness guidance would stop requested work, request more authority, or
materially change the requested workflow, identify the exact invariant ID or
skill/reference heading responsible and explain why it applies.

Authorization is scoped, not ceremonial. One explicit instruction may
authorize several named stages. Reuse that authority without repeated
confirmation while target, scope, and risk remain unchanged. A request for a
narrower action never implies an unmentioned external, destructive,
deployment, installation, repair, or publication action.
