# Temporary identity contract
Readings and health activity metadata exist only while the temporary identity is
active. Erasure ends consent and removes both. There is no separate retained-audit
requirement. A telemetry callback can be buffered before expiry and flushed after
it. The production store supports an atomic lifecycle predicate on writes.
