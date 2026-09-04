# Event Delivery

First classify the event:

- **Domain fact:** a committed material change that consumers may process.
- **Durable delivery item:** a persisted message or outbox entry with replay and
  acknowledgment semantics.
- **Wake hint:** an expendable notification telling a consumer to consult
  durable truth.
- **Operation progress:** non-material lifecycle information.
- **Operation terminal:** success, failure, cancellation, or supersession.
- **Environment state:** connectivity, authentication, or capability change.

Do not let a wake hint become the only record of a fact. A durable consumer
needs an inbox/outbox, sequence, cursor, watermark, or another persisted way to
recover after loss.

Specify:

1. transaction boundary between fact and emission;
2. delivery guarantee and retention;
3. identity, sequence, and partitioning;
4. duplicate, gap, reorder, replay, and late-arrival behavior;
5. acknowledgment and poison-message behavior;
6. which publication class invalidates which reads;
7. reconnect and catch-up behavior;
8. bounded fan-out and coalescing.

The essential fault test drops the live notification and proves the consumer
still converges from persisted truth.
