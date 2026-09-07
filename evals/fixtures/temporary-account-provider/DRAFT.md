# Temporary-account provider proposal

A backend browser broker could allow provider callbacks without a permanent
mobile registry entry. It would issue a new short-lived provider-browser handoff
credential, correlate browser completion to temporary identity/expiry, and add
a server return endpoint. A mobile callback compatibility adapter could then
share the broker across all providers and permanent accounts.

Putting this behind `TEMP_PROVIDER_BROKER` would allow staged rollout. A follow-on
could replace native provider OAuth entirely. This is a proposal, with migration,
credential purpose/replay rules, and rollback still unresolved.
