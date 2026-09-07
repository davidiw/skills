# Change Classification

## Minimal and bounded work

Minimal means a local reversible edit inside one accepted owner/contract, without
changed sensitive semantics, shared contention, durable/external effects, or
migration. Use existing focused checks; no specialist or scope artifact required.
Bounded product-rule work inside an established owner normally needs at most one
specialist. A sensitive repository does not make unrelated copy consequential.

## Consequential checkpoint

Persistent/wire evolution, cross-process lifetime, identity/authorization,
sensitive collection/use/disclosure/erasure, shared contention, physical proof,
or external release actions require the router's pre-edit scope decision.
Record only relevant authority, lifetime, consumers, failure/proof, and action
limits. An accepted profile and owner contract suffice; consult specific catalog
entries only when their interpretation is unresolved.

## Scope expansion gate

Material expansion into a new shared/cross-cutting responsibility or widening an
accepted owner contract requires explicit user approval before implementation.
Measure scope against accepted semantics **before choosing a solution**: supported
principals, purposes, lifetimes, writers, and compatibility obligations. If the
accepted boundary does not support the requested behavior, mark it `pending`
unless an explicit approved proposal covers that change. A flag, disabled default,
private/in-memory implementation, preserved old callers, necessity, design note,
or feature request cannot supply that approval. A local implementation choice
plainly within the requested feature and existing contract requires no second
architecture approval.

Use the router's per-boundary decision table before any production-edit call.
`none` needs evidence of supported behavior and unchanged accepted semantics.
`approved` cites the concrete expansion proposal plus explicit user approval and
limits. A feature request that predates that proposal cannot be its approval.
Otherwise mark `pending`, preserve that boundary and continue independently
supported work. Reuse a clear affirmative response to a concrete proposal.

Example: a callback contract resolves only durable principals; the feature asks
for short-lived principals. Expiry in an account owner may be supported, but a new
callback subject resolver or grant store is a pending expansion even when private,
provider-specific or in memory. Preserving old callers does not preserve the
accepted set of principals/lifetimes. An unaccepted draft and a smaller invented
alternative both need approval if they cross that boundary. Use the conditional
[approval handback](scope-approval.md); do not rewrite the accepted contract to
make an unapproved implementation appear authorized.

## Primary-owner routing

Choose the owner of the **unresolved decision**, not every matching vocabulary.
For a critical action blocked by optional work, the obligation is progress despite
an independently stalled writer already holding shared contention. Read the
[resource proof](../skills/architecture-foundations/references/runtime-resource-governance.md#critical-progress-against-an-incumbent-optional-writer)
before proposing a fix; callback reordering alone does not resolve that obligation.

| Unresolved decision | Primary implementation skill |
| --- | --- |
| New ownership/dependency boundary, shared scarce pool or serialized contention | [architecture foundations](../skills/architecture-foundations/SKILL.md) |
| Work must survive its initiator; admission/replay/recovery | [durable workflows](../skills/durable-workflows/SKILL.md) |
| External/public contract, mutable authorization, purpose-scoped credential, event delivery | [interfaces and events](../skills/interfaces-and-events/SKILL.md) |
| UI/domain/platform composition or useful-paint ownership | [application composition](../skills/application-composition/SKILL.md) |
| Persistent identity, sync/migration, sensitive derivation/retention/erasure | [data and compatibility](../skills/data-and-compatibility/SKILL.md) |
| Demonstrated recurring divergence or root-cause consolidation | [architecture hardening](../skills/architecture-hardening/SKILL.md) |
| Exact release/evidence campaign, operator tooling, physical proof | [verification and operations](../skills/verification-and-operations/SKILL.md) |

Add a second owner only when a distinct unresolved obligation needs it. An owner
can consume another owner's contract reference without loading that whole skill.
A synchronous authority fence does not need durable workflows. UI observing a job
does not alone need composition; an internal adapter does not alone need interface
review; focused tests do not alone require verification. Existing ownership does
not need an architecture exercise. Repeated symptoms justify hardening, not cleanup.

## Record assurance gates; review after building

- **Security:** consequential change to/new exposure of trust or authorization
  decisions, credentials, principal/purpose binding, or revocation semantics.
- **Privacy:** consequential change to sensitive collection, use, disclosure,
  derivation, retention, expiry, or erasure.

A correction of those semantics still selects its gate. Carrying credentials,
preserving an existing account fence, routine connectivity wakes/UI stale-result
suppression, or the presence of sensitive data alone does not. Explicit review
requests use the router's direct assurance shortcut. Builders record required
gates and hand off the corrected snapshot; they do not preload assurance bodies.

Repository-required independent gates also cover material persistence/migration,
deletion/durable-state, public/provider contracts and high-risk architecture.
Release gates and explicit independent-review requests require the specified
context separation. Use the [handoff](assurance-handoff.md); do not add such gates
to ordinary bounded work merely because those nouns appear.
