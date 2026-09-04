# Consumer Contract

## Inventory

| Consumer | Version/lifecycle | Reads | Writes | Retry behavior | Compatibility window |
| --- | --- | --- | --- | --- | --- |

## Required decisions

- authoritative owner and canonical schema;
- command versus query intent;
- identifiers and collision domain;
- time representation, timezone attribution, and ordering ties;
- units, precision, range, and normalization;
- required, optional, null, absent, and redacted meanings;
- pagination stability and snapshot expectations;
- authentication, authorization, and account/tenant scope;
- idempotency key, preconditions, conflict response, and replay;
- error codes, retryability, and safe diagnostic fields;
- long-running admission and status lookup;
- version negotiation, coexistence duration, deprecation, and rollback.

Contract fixtures should exercise the real boundary wrapper and serialization,
not a separately recreated schema.
