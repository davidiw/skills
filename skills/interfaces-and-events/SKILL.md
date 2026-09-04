---
name: interfaces-and-events
description: Define or evolve public or independently consumed contracts across a process, client, provider, message, event, or trust boundary. Use for APIs, commands, queries, long-running responses, pagination, idempotency, errors, delivery, and consumer compatibility; not for private functions or internal adapter interfaces owned by one composition root.
---

# Interfaces and Events

Treat an interface as a durable consumer agreement, not a serialization detail.

## Workflow

1. Inventory producers, consumers, authoritative data, trust boundary, and
   independently deployed versions. Include workers, old clients, tools, and
   recovery processes rather than only the primary UI.
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
7. Define additive and breaking evolution from each consumer's perspective.
   Run mixed-version and duplicate/gap/reorder tests where applicable.
8. Publish the smallest contract that supports the required behavior; keep
   storage and provider representations private.

Use [`consumer-contract.md`](references/consumer-contract.md) for the review
shape. Use [`event-delivery.md`](references/event-delivery.md) whenever a
notification, stream, webhook, or message is involved.

The contract is complete when every consumer can interpret identity, order,
absence, failure, and retry consistently; committed truth is recoverable after
lost notifications; and compatibility is proven against actual supported
versions.
