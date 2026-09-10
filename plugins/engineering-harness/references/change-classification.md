# Builder Checkpoints

Complete each checkpoint before advancing. Minimal changes and review-only work
have already exited through the router.

## 1. Inspect and classify before choosing a fix

Establish the accepted owner/source and semantics: supported principals, purposes,
lifetimes, writers and compatibility obligations. Do this before selecting a fix
or state store. Persistent/wire evolution, cross-process lifetime, identity/
authorization, sensitive collection/use/disclosure/erasure, shared contention,
physical proof, shared testing/evidence/review policy and external release actions
are consequential. Record relevant
authority, lifetime, consumers, failure/proof and action limits; reuse accepted
profile/owner evidence and read exact catalog entries only for unresolved meanings.

## Scope expansion gate

**2. Decide every requested behavior/owner before production edits.** Record in
an existing task record or user-visible checkpoint; reuse settled rows and update
them when new evidence changes scope:

| Behavior and accepted owner/source | Already supported? Evidence | Scope expansion | Approval source/exact limits | Allowed work / blocked boundary |
| --- | --- | --- | --- | --- |

Material expansion into a shared/cross-cutting responsibility or widening an
accepted contract needs explicit user approval before implementation:

- `none`: positive evidence that the behavior is supported and accepted semantics
  remain unchanged. A local choice plainly within the feature and contract needs
  no separate architecture approval.
- `approved`: the concrete boundary-expansion proposal, explicit user approval
  and exact limits. Reuse a clear affirmative response within those limits.
- `pending`: the contract excludes the behavior and no approved proposal covers
  it. Leave this boundary untouched; implement independent authorized rows.

Finish this checkpoint in an earlier assistant message or a completed
record-only write, **before reading the primary-owner skill or issuing a
production-edit call**. Creating the record inside the production-edit call does
not complete this checkpoint.

**No production-edit tool call for a missing, invalid or pending row.** A flag,
disabled default, private/in-memory path/store, preserved old callers, necessity,
design note or feature request is not scope approval. Repeating the outcome or
citing a feature request that predates the proposal cannot approve its new means.
Do not rewrite the accepted contract to authorize your own implementation.

For example, a durable-principal callback contract does not support short-lived
principals merely because a new resolver/grant store is private or provider-specific.
Expiry in the account owner may remain authorized; expanding callback subjects/
lifetimes is pending. An unaccepted draft and a smaller invented alternative both
need approval if they cross that boundary. Before returning pending work, complete
the [approval handback](scope-approval.md).

## 3. Read the primary owner before designing

Choose and **read** one implementation skill for the unresolved decision in
**authorized work**; naming it alone does not complete this checkpoint:

| Decision | Primary implementation skill |
| --- | --- |
| Domain semantics/ownership/dependencies, shared scarce pools or serialized contention | [architecture foundations](../skills/architecture-foundations/SKILL.md) |
| Admission/replay/recovery; work outlives its initiator | [durable workflows](../skills/durable-workflows/SKILL.md) |
| Public/provider contracts, mutable authorization, credential purpose, events | [interfaces and events](../skills/interfaces-and-events/SKILL.md) |
| Meaningful UX/UI/brand decision | [experience routing](experience-routing.md), then its one primary owner |
| UI/domain/platform composition, useful-paint ownership | [application composition](../skills/application-composition/SKILL.md) |
| Persistent identity, sync/migration, sensitive derivation/retention/erasure | [data and compatibility](../skills/data-and-compatibility/SKILL.md) |
| Recurring divergence/root-cause consolidation | [architecture hardening](../skills/architecture-hardening/SKILL.md) |
| Evidence standards, testing/review methodology, benchmarks, operations | [verification and operations](../skills/verification-and-operations/SKILL.md) |

Bounded work normally needs one specialist; consequential work generally at most
two before evidence justifies more. Another owner needs a distinct unresolved
obligation; consuming its contract reference alone needs no skill-body load.
Synchronous fencing need not load durable workflows; observing a job need not load
composition; internal adapters need not load interfaces; focused tests need not
load verification. Existing ownership needs no architecture exercise; hardening
needs recurring evidence.

For critical progress blocked by optional work, read the
[incumbent-writer proof](../skills/architecture-foundations/references/runtime-resource-governance.md#critical-progress-against-an-incumbent-optional-writer)
before proposing a fix. Prove progress while another writer already holds shared
contention; moving the current callback is insufficient.

Record required assurance gates now; reviewer bodies belong in fresh reviewers,
never builders/designers:

- **Security:** consequential changes/new exposure of trust, authorization,
  credentials, principal/purpose binding or revocation semantics.
- **Privacy:** consequential changes to sensitive collection, use, disclosure,
  derivation, retention, expiry or erasure.

Corrections of these semantics still require the gate. Credentials or sensitive
data alone do not; neither do connectivity wakes/UI stale-result fixes preserving
existing fences. Repository-required independent gates also cover material
persistence/migration, deletion/durable state, public/provider contracts and
high-risk architecture. Release gates and explicit independent reviews require
their context separation; ordinary bounded work does not acquire gates merely
by containing these nouns.

## Conditional consequential handoff

After accepted scope and the primary owner has established the proposed mechanism,
consequential implementation/design work uses the existing conditional
[four-role handoff](assurance-handoff.md#conditional-four-role-workflow). An
explicit request may also select it. Minimal work remains local unless separation
is explicitly requested. The handoff does not alter classification, scope, or
required gates; design-only work remains proposal-only.

## 4. Implement and prove; 5. close gates

Stay within recorded boundaries and use focused tests at the actual failure seam.
New evidence changing scope returns to checkpoint 2 before editing that boundary.
Design/plan requests stop at the proposal: production stays unchanged and planned
implementation checks/reviews remain prospective.

For recorded required gates, use the [fresh review handoff](assurance-handoff.md)
after implementation on the corrected snapshot. Address findings and review corrections before completion.
Unavailable required independence remains pending; builder reasoning cannot
substitute. Record dispositions and evidence without restating settled contracts.
