# Change Classification

This is internal routing, not a menu for users. Classify the requested outcome,
not its apparent line count. Existing repository policy may raise the class.
For review/assessment requests, classify the subject's impact and retain
read-only action scope. Requested security/privacy assurance selects its
reviewer directly, even when no implementation change is requested.

## Scope expansion gate

Check the proposed solution against the user's authorized outcome before any
implementation, including the minimal shortcut. Material expansion into a new
shared/cross-cutting responsibility or widening an accepted owner contract requires
**explicit user approval of that expansion before implementing it**. This includes
new shared protocols, subsystems, credential/session types, frameworks,
compatibility paths, or configuration axes when they introduce that expansion.
A local option or implementation detail plainly within the requested feature and
accepted owner contract does not require a second architecture approval.
Permission to implement a feature or fix does not by itself grant broader scope.
A feature flag, disabled default, private prototype in production code, or agent-
authored design note is not approval.

Measure expansion against the repository's accepted contracts before selecting a
solution or reassigning owners. A shared boundary gains material scope when it
supports new principal classes, credential purposes, lifetimes, state writers,
or client/provider compatibility obligations outside those contracts. Keeping
endpoint names unchanged or making added state private/in-memory does not, by
itself, establish that the accepted contract is preserved. Private implementation
detail that leaves those accepted semantics unchanged is not scope expansion.
If that contract prevents the requested feature, obtain approval
for the concrete contract change before implementing it; treating the boundary
as part of the feature does not supply approval.

When an unapproved expansion is proposed, first make the decision concrete: state the requested
outcome, the adjacent weakness and evidence, affected owners/contracts, the
smallest option within current scope, the proposed expansion and its compatibility,
privacy, operational, and maintenance costs. The approval handback must include
these alternatives and concrete tradeoffs; naming cost categories alone is
insufficient. Mark unknowns explicitly. Then ask the user to approve that
specific expansion, citing this gate. Do not implement the expansion while the
answer is pending. If the bounded option satisfies the request, use it and leave
adjacent work as a proposal; no approval question is needed for work that stays
within the authorized contract. Continue independent authorized work and report
any requested behavior that remains blocked.

Record the user's approval and its exact limits in the existing task/plan. Reuse
explicit approval already given in the session; do not reconfirm an unchanged
approved expansion. A broad instruction to finish or harden a feature, technical
necessity, a review finding, or silence does not supply missing scope authority.
Recheck this gate when investigation or implementation changes the proposed
solution, and pass the same scope boundary to delegated workers.

Before consequential production edits, record the **Scope expansion** decision
in the existing task/plan: accepted contract and owner; proposed new surface or
semantic change; and `none`, `approved`, or `pending`. For `approved`, cite the
concrete expansion proposal and the user's explicit affirmative response, or a
user instruction that itself names the expanded shared surface or contract;
record the approved limits. A request naming only the feature/outcome is implementation authority,
not that approval. For `none`, explain how the accepted shared contracts remain
unchanged; preserving old callers alone does not establish this. For `pending`,
make the decision handback above before editing that boundary. Recheck the record
before a proposed private adapter or parallel state store changes this decision.
Unrecorded or inferred expansion approval cannot pass this gate.

## Risk card

Record relevant fields; Scope expansion is required before consequential edits:

- **Authority:** which component owns the fact or behavior, and which principal,
  capability, purpose, consent, or lifecycle/expiry can authorize or revoke use?
- **Lifetime:** can accepted intent outlive the request, route, process, or
  device opportunity?
- **Boundaries:** does it cross a module, process, client, account, provider, or
  physical-device boundary?
- **Representation:** does it change persistent, wire, event, storage, cache,
  generated, or derived form?
- **Contention:** can it delay useful paint or monopolize a shared resource,
  including locks, connections, transactions, and serialized queues? Can an
  optional side effect delay a safety/correctness-critical action?
- **Sensitivity:** does it touch credentials, personal data, safety, money, or
  irreversible effects?
- **Evidence:** does correctness require a real provider, device, deployment,
  physical artifact, or historical corpus?
- **Scope expansion:** what new shared surface or new/widened owner contract does the
  solution introduce beyond the authorized outcome? Record `none`, or the
  concrete proposal with explicit user approval and limits, or `pending` with
  expansion implementation blocked under the gate above.
- **Action:** which of implementation, integration, metadata change,
  deployment, installation, migration, repair, or publication is authorized?

## Classes

### Minimal

A local, reversible implementation or behavior change inside one established
owner and contract, with no durable or external effect and a tight existing
test seam. Adding an optional parser field, changing copy, or correcting a pure
calculation is minimal unless repository policy raises it. Follow the ordinary
path; no specialist skill is required.

A deterministic regeneration of local documentation inside an unchanged
generator contract can also be minimal. Use its existing freshness check.
Stop classification here when these conditions hold: no scope-lock document,
full authority inventory, or explicit dominance-rule accounting is needed.

### Bounded

A product-rule or public-contract change that stays within one established
owner and has no cross-process lifetime, migration, shared-state, sensitive, or
irreversible consequence. State the changed invariant, use the existing path,
add focused proof at the owning seam, and stop. Load one specialist only when
its trigger actually applies.

### Consequential

Any persistent representation, cross-process contract, accepted durable work,
identity boundary, data destruction, changed sensitive-data path, shared-resource
contention, generated contract or safety-relevant artifact, physical behavior,
or external release action. Record a
scope lock, consumers and failure modes, compatibility or recovery plan, and
evidence requirements before production edits.

Keep this in the existing task or plan; separate documents are needed only by
repository policy or material coordination risk. Scope compatibility/recovery
to the changed lifetime. A repository's `sensitive_data: true` activates privacy
obligations, but does not make unrelated copy or styling consequential.

### Stabilization

Recurring failures, repeated cross-layer guards, several representations of
one fact, or a broad high-risk correction. Freeze acceptance criteria and use
one stable evidence packet. Use architecture hardening for demonstrated
divergence; use verification and operations for a repository-mandated
adversarial review. Do not turn either into repository-wide cleanup.

## Skill routing

| Signal | Skill |
| --- | --- |
| New subsystem, ownership ambiguity, dependency direction, or composition | [`architecture-foundations`](../skills/architecture-foundations/SKILL.md) |
| Scarce runtime pools, serialized contention, critical action blocked by optional effects, admission, or cooperative reclamation | [`architecture-foundations`](../skills/architecture-foundations/SKILL.md) |
| Work must survive its initiator | [`durable-workflows`](../skills/durable-workflows/SKILL.md) |
| Public API, cross-process message or event, external provider, trust boundary, independently evolving contract, mutable authorization, or purpose-scoped credential | [`interfaces-and-events`](../skills/interfaces-and-events/SKILL.md) |
| UI/domain/assistant/platform parity or useful-paint ownership | [`application-composition`](../skills/application-composition/SKILL.md) |
| Persistent identity, sync, migration, deletion, repair, mixed versions, or sensitive data derivation/retention/erasure | [`data-and-compatibility`](../skills/data-and-compatibility/SKILL.md) |
| Demonstrated recurring architecture divergence, consolidation, or hotspot root-cause repair | [`architecture-hardening`](../skills/architecture-hardening/SKILL.md) |
| Exact-revision gate, independent adversarial or fault campaign, operator tooling, release, generated contract/safety proof, or physical proof | [`verification-and-operations`](../skills/verification-and-operations/SKILL.md) |
| Consequential modification or new exposure of a trust/authorization boundary; or requested changed-path or release-surface security assurance | [`security-assurance`](../skills/security-assurance/SKILL.md) |
| Consequential change to sensitive data collection, use, disclosure, derivation, retention, expiry, or erasure; or requested changed-path or release data-lifecycle assurance | [`privacy-assurance`](../skills/privacy-assurance/SKILL.md) |

When several signals describe one execution path, load the smallest set that
owns the path. Do not run independent architecture exercises for each signal.
During implementation, assurance follows the implementation owners and reviews
the resulting snapshot. For an assurance-only request, load the relevant
reviewer directly; it reads owning contracts through its references. This does
not imply permission to implement fixes. For altered trust/authorization or
privacy-lifecycle semantics, select the relevant reviewer(s) and record any
uncovered review scope under
[`assurance-review.md`](assurance-review.md).

Release-wide assurance starts from the externally reachable/trust-boundary and
sensitive-data inventories, including unchanged and legacy paths. It is selected
by the requested campaign scope, not inferred from an ordinary deployment or
version bump. Use the existing security/privacy specialists in their release
modes; an exact release gate may additionally select verification.

## Dominance rules

- Do not add `architecture-foundations` merely to name an owner inside an
  established design.
- Do not add `application-composition` merely because a UI observes a durable
  operation; add it when cross-surface semantics or useful-paint ownership is
  itself changing.
- Do not add `data-and-compatibility` for a private operation record with no
  migration, replication, identity, privacy lifecycle, deletion, or mixed-version consequence.
- Do not add `interfaces-and-events` for an internal adapter interface already
  owned by `application-composition`; add it for public, trust-boundary, or
  independently evolving contracts.
- Do not add `interfaces-and-events` for a synchronous in-process notification
  inside one established owner. Add it when delivery, transport, independent
  consumers, or a public event contract is changing.
- Do not add `verification-and-operations` because another skill requires
  focused success or failure tests. Add it for independent adversarial or fault
  campaigns, exact-revision gates, generated contract/safety or physical proof,
  machine/operator tooling, repair, release, deployment, or publication.
- Do not add verification for a local documentation regeneration or merely to
  invoke a security/privacy reviewer. Assurance reviewers own their scoped
  findings and consume shared evidence rules directly.
- Do not add `durable-workflows` merely because consent or authorization can
  change during a synchronous operation; the interface owner handles that fence.
- Do not add assurance for unrelated minimal edits in a sensitive repository.
  When consequential work changes both authorization and privacy lifecycle,
  neither reviewer dominates the other; review the shared path from both sides.
- Do not add `security-assurance` merely because a path carries credentials,
  account context, or existing authorization fences. Add it when the requested
  change modifies or newly exposes a trust/authorization boundary, or assurance
  is explicitly requested. A connectivity wake or caller-side account-race fix
  using the unchanged canonical fence stays with its implementation owners.
  Changing the fence's decisions or credential/session semantics crosses this
  boundary; preserving its existing contract does not.
- Do not add `privacy-assurance` merely because the repository contains sensitive
  data. Add it when the changed path alters collection, use, disclosure,
  derivation, retention, expiry, or erasure, or assurance is explicitly requested.
  Routine scheduling or presentation changes that preserve those contracts use
  their existing implementation checks.
