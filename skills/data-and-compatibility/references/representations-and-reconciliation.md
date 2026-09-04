# Representations and Reconciliation

Use distinct names and types for:

- source observation from a provider or device;
- canonical accepted state;
- derived state with algorithm version and input fingerprint;
- projection optimized for a reader;
- cache that may disappear;
- transport request/response;
- persisted record;
- operation, checkpoint, cursor, and watermark.

For each representation, record owner, identity, freshness rule, rebuild path,
and whether absence has meaning. A projection cursor proves processed input,
not necessarily domain completeness; a watermark must name the granular
derivation or source window it covers.

Reconciliation defines:

1. authority and tie-breaking;
2. duplicate and same-identity collapse;
3. late and out-of-order observations;
4. cursor advancement only after the corresponding bounded commit;
5. partial failure and replay;
6. tombstone retention and resurrection prevention;
7. stale account or tenant fencing;
8. deterministic validation that prevents repeatedly rescanning undefined
   history.

Test a missed wake, duplicate input, partial page, stale cursor, authority
switch, and rebuild from canonical state.
