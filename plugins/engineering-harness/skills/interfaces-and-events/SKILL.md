---
name: interfaces-and-events
description: Define public or independently consumed contracts and mutable authorization boundaries. Use for APIs, providers, messages, consumer compatibility, purpose-scoped credentials, consent, and sensitive reads or effects; not for private functions without a trust boundary.
---

# Interfaces and Events

Treat an interface as a durable consumer agreement, not a serialization detail.

Use the [invariant catalog](../../references/invariants.json) as normative.
Interpret only entries whose `owner_skill` names this skill; consume other
entries without redefining them.

## Workflow

1. Inventory producers, consumers, authoritative data, trust boundary, and
   independently deployed versions. Include workers, old clients, tools, and
   recovery processes rather than only the primary UI.
   For sensitive or authority-dependent operations, read
   [`authorization-context.md`](references/authorization-context.md). Bind
   principal/account, capability, purpose, consent, and lifecycle/expiry; fence
   synchronous reads and exports as well as durable effects. Credential or
   capability possession alone does not grant product authority.
2. Separate query, command, operation-status, and event contracts. A generic
   row or sync record is not automatically a product mutation API.
3. Specify identifiers, timestamps and timezones, units, ordering, pagination,
   optionality, null versus absence, provenance, validation limits, and error
   taxonomy at the boundary.
4. For mutations, define preconditions, idempotency, concurrency, partial
   failure, acknowledgment, retry, and long-running-operation semantics.
5. For events, classify the fact and delivery contract using
   [`event-delivery.md`](references/event-delivery.md). Emit from committed
   truth and give consumers a persisted recovery position when loss matters.
6. Centralize repeated boundary guarantees such as authentication,
   authorization, validation, response envelopes, provider error mapping, and
   privacy-safe activity logging.
   Activity metadata inherits the source's privacy obligations. Consume the
   data owner's [`privacy lifecycle`](../data-and-compatibility/references/privacy-lifecycle.md)
   for logging, telemetry, and delayed writes on sensitive paths.
7. Define additive and breaking evolution from each consumer's perspective and
   the required mixed-version, duplicate, gap, reorder, and replay scenarios.
   `verification-and-operations` owns adversarial execution and evidence.
8. Publish the smallest contract that supports the required behavior; keep
   storage and provider representations private.

Use [`consumer-contract.md`](references/consumer-contract.md) for the review
shape. Use [`event-delivery.md`](references/event-delivery.md) whenever a
notification, stream, webhook, or message is involved.

Before stopping work or changing the requested workflow, apply
[`precedence-and-exceptions.md`](../../references/precedence-and-exceptions.md)
and name the exact rule.

The contract is complete when every consumer can interpret identity, order,
absence, failure, and retry consistently; committed truth is recoverable after
lost notifications; and compatibility is proven against actual supported
versions.
