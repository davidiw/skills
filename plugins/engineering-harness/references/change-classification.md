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
authority, lifetime, consumers, failure/proof and action limits; for resource
boundaries distinguish own/borrow/transfer, and for reusable evidence distinguish
immutable evidence identity from mutable labels; reuse accepted
profile/owner evidence and read exact catalog entries only for unresolved meanings.

For a behavioral change, state the observable promise and relevant failure
conditions before implementation, independently of the proposed mechanism.
Choose a focused proof seam now and exercise it early; the
[iteration proof contract](../skills/verification-and-operations/references/evidence-contract.md#focused-iteration-proof)
defines when component fixtures are insufficient.

## Scope expansion gate

**2. Establish scope before production edits.** Reuse the user request, accepted
contract and prior approvals. Read owner skills and inspect evidence as needed to
resolve scope; the gate applies to edits, not investigation.

For consequential changes, keep a concise decision in the existing task packet:
behavior/owner, accepted boundary, authority and any unapproved expansion. Use a
table only when several boundaries make it useful. Routine implementation choices
within the accepted feature need neither separate approval nor another scope form.

An explicit request can authorize a concrete expanded behavior. Ask only when a
material change to product, authority, lifetime, compatibility or shared-owner
semantics is outside the authority already given. A private helper, disabled
flag, technical necessity or agent-authored design cannot authorize that change.
Do not rewrite the accepted contract to authorize your implementation.

Leave unresolved or unapproved boundaries untouched while completing independent
authorized work. Before returning a pending boundary, use the
[approval handback](scope-approval.md). Reuse the resulting approval within its
limits instead of asking again.

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

### Challenge a consequential correctness mechanism

After reading the relevant authority and owner, and **before dependent edits**,
record a concise decision in the existing checkpoint: observable guarantee;
a plausible counterexample to the proposed mechanism; legitimate behavior it
must still allow; and whether the mechanism survives or must change. Use the
existing task packet, without a separate document or retrospective claim.
“Considered safety” is not a concrete challenge.

Compare the smallest materially different alternative when it changes correctness,
compatibility or complexity; no alternatives quota, extra document or agent.
Retaining the mechanism is valid when the concrete path already excludes the
counterexample. This applies to consequential correctness choices, not every edit.

## 4. Coordinate bounded execution

This builder workflow owns generic execution allocation. Once scope and authority
are established, meaningful bounded operational effort defaults to the least-expensive
capable available context. This includes repository search, caller tracing, log
summaries, mechanical documentation/fixtures/checks, code writing, and
long-running commands. The coordinator retains unresolved ambiguity,
architecture, contract/scope decisions, and acceptance or finding adjudication.
Delegation never authorizes an unresolved or unapproved boundary.

Give each write worker one precise assignment: accepted owner and invariant;
allowed scope and exact files/seams; required regression/failure proof;
non-goals and blocked boundaries; a proportional time/token or investigation
budget; and the required result/evidence handback. Give a command worker the
exact command, snapshot, timeout/budget, permitted environment and retained
output. A worker reports useful artifacts, findings, command results, or a
concrete blocker when available; it does not consume turns narrating that it is
waiting.

Reuse the existing task or review packet for later workers, reviewers,
corrections, and command delegation rather than repeating repository search or
already-completed tests. It records the revision; inspected/changed paths;
commands and results; retained artifacts and findings; authoritative sources;
and unresolved decisions. For consequential resource-bearing work, the handback
identifies resources created/owned, borrowed or transferred; permitted destructive
operations; what remains usable after close; and delayed callbacks/resources
that may outlive close. For evaluation/artifact work, identify immutable inputs,
producer/build and model/configuration provenance, mutable labels/adjudications,
and changes that invalidate baseline compatibility. Omit these fields when
irrelevant; ordinary UI or parser edits need neither.

When multiple workers change cooperating owners, the coordinator makes one short
composition pass after handback and before any independent adversarial review:
which sequences cross changed owners, and what happens at every transition?
Record one to three highest-risk cross-owner scenarios in the existing stable
review packet, including teardown/re-entry or delayed completion when meaningful,
and point to focused composition regressions. Surface the seams as neutral
reviewer questions, not expected findings. This adds no agent, independent gate,
or review budget. Update the packet only for the changed snapshot or newly
relevant evidence. This execution assignment is not an independent review:
required fresh-review separation still uses the [assurance handoff](assurance-handoff.md).

## 5. Implement and prove; 6. close gates

Stay within recorded boundaries and use focused tests at the actual failure seam.
Complete the [focused iteration proof](../skills/verification-and-operations/references/evidence-contract.md#focused-iteration-proof)
before independent readiness review; the coordinator owns the composed outcome
across delegated components. Keep final broad regression pending until freeze.
New evidence changing scope returns to checkpoint 2 before editing that boundary.
Design/plan requests stop at the proposal: production stays unchanged and planned
implementation checks/reviews remain prospective.

For recorded required gates, use the [fresh review handoff](assurance-handoff.md)
after implementation on the corrected snapshot. Address findings and review corrections before completion.
Unavailable required independence remains pending; builder reasoning cannot
substitute. Record dispositions and evidence without restating settled contracts.
