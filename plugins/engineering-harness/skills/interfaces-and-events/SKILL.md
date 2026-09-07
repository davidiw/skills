---
name: interfaces-and-events
description: Define public or independently consumed contracts and mutable authorization boundaries. Use for APIs, providers, messages, consumer compatibility, purpose-scoped credentials, consent, and sensitive reads or effects; not for private functions without a trust boundary.
---

# Interfaces and Events

Own public/provider contracts, mutable authorization and event delivery. Use the
accepted contract; consult relevant [invariants](../../references/invariants.json)
only for unresolved interpretation. Private adapter details alone need no new
interface exercise.

1. Name producers/consumers, trust boundary, authoritative decisions and supported
   versions. Include alternate callers when they share this contract.
2. For authority-dependent reads/effects or credential changes, read
   [authorization context](references/authorization-context.md) before editing.
   Bind principal/account, capability, purpose, consent and lifecycle. Prove the
   local atomic effect fence and report non-atomic provider-read residual exposure.
   Record changed-semantics assurance gates for the corrected snapshot.
3. Define identity, absence, units/time, validation, errors, idempotency and partial
   failure only where the changed contract needs them. Reuse canonical decisions.
4. For events/streams/webhooks, read [event delivery](references/event-delivery.md):
   committed truth, delivery/recovery, consumer order and version coexistence.
   A wake is not durable truth; in-process notifications need no invented transport.
5. Use focused tests for invalidation during calls, denial at the actual effect
   owner, supported consumers and relevant replay/order failures. A permissive
   fake cannot prove an atomic authorization fence.

Use [consumer contract](references/consumer-contract.md) for a new public contract;
consume the [privacy lifecycle](../data-and-compatibility/references/privacy-lifecycle.md)
when changed activity/telemetry or temporary outputs inherit sensitive data.
Additional owner skills require unresolved obligations, not these reference reads.

Done means consumers have consistent semantics, compatibility evidence is scoped,
and the builder has closed recorded gates via the
[assurance handoff](../../references/assurance-handoff.md). Apply
[precedence](../../references/precedence-and-exceptions.md) for workflow conflicts.
