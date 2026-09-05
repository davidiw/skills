# Change Classification

This is internal routing, not a menu for users. Classify the requested outcome,
not its apparent line count. Existing repository policy may raise the class.

## Risk card

Record only fields that are relevant:

- **Authority:** which component owns the fact or behavior?
- **Lifetime:** can accepted intent outlive the request, route, process, or
  device opportunity?
- **Boundaries:** does it cross a module, process, client, account, provider, or
  physical-device boundary?
- **Representation:** does it change persistent, wire, event, storage, cache,
  generated, or derived form?
- **Contention:** can it delay useful paint or monopolize a shared resource?
- **Sensitivity:** does it touch credentials, personal data, safety, money, or
  irreversible effects?
- **Evidence:** does correctness require a real provider, device, deployment,
  physical artifact, or historical corpus?
- **Action:** which of implementation, integration, metadata change,
  deployment, installation, migration, repair, or publication is authorized?

## Classes

### Minimal

A local, reversible implementation or behavior change inside one established
owner and contract, with no durable or external effect and a tight existing
test seam. Adding an optional parser field, changing copy, or correcting a pure
calculation is minimal unless repository policy raises it. Follow the ordinary
path; no specialist skill is required.

### Bounded

A product-rule or public-contract change that stays within one established
owner and has no cross-process lifetime, migration, shared-state, sensitive, or
irreversible consequence. State the changed invariant, use the existing path,
add focused proof at the owning seam, and stop. Load one specialist only when
its trigger actually applies.

### Consequential

Any persistent representation, cross-process contract, accepted durable work,
identity boundary, data destruction, sensitive-data path, shared-resource
contention, generated/physical artifact, or external release action. Record a
scope lock, consumers and failure modes, compatibility or recovery plan, and
evidence requirements before production edits.

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
| Scarce runtime pools, protected progress, admission, or cooperative reclamation | [`architecture-foundations`](../skills/architecture-foundations/SKILL.md) |
| Work must survive its initiator | [`durable-workflows`](../skills/durable-workflows/SKILL.md) |
| Public API, cross-process message or event, external provider, trust boundary, or independently evolving contract | [`interfaces-and-events`](../skills/interfaces-and-events/SKILL.md) |
| UI/domain/assistant/platform parity or useful-paint ownership | [`application-composition`](../skills/application-composition/SKILL.md) |
| Persistent identity, sync, migration, deletion, repair, or mixed versions | [`data-and-compatibility`](../skills/data-and-compatibility/SKILL.md) |
| Demonstrated recurring architecture divergence, consolidation, or hotspot root-cause repair | [`architecture-hardening`](../skills/architecture-hardening/SKILL.md) |
| Exact evidence, adversarial review, fault injection, operator tooling, release, generated artifact, or physical proof | [`verification-and-operations`](../skills/verification-and-operations/SKILL.md) |

When several signals describe one execution path, load the smallest set that
owns the path. Do not run independent architecture exercises for each signal.

## Dominance rules

- Do not add `architecture-foundations` merely to name an owner inside an
  established design.
- Do not add `application-composition` merely because a UI observes a durable
  operation; add it when cross-surface semantics or useful-paint ownership is
  itself changing.
- Do not add `data-and-compatibility` for a private operation record with no
  migration, replication, identity, deletion, or mixed-version consequence.
- Do not add `interfaces-and-events` for an internal adapter interface already
  owned by `application-composition`; add it for public, trust-boundary, or
  independently evolving contracts.
- Do not add `interfaces-and-events` for a synchronous in-process notification
  inside one established owner. Add it when delivery, transport, independent
  consumers, or a public event contract is changing.
- Do not add `verification-and-operations` because another skill requires
  focused tests. Add it for exact-revision gates, generated or physical proof,
  machine/operator tooling, repair, release, deployment, or publication.
