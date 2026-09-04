# Design

Photo analysis is currently submitted by an authenticated user after media is
stored. The route polls an in-memory task and loses its handle when the route or
process closes. The existing server durable-job runtime can persist work and
execute bounded retries, but this domain has not defined its admission,
idempotency, status, or publication contract.

Cancellation, supersession, payload retention, and result-retention behavior
are open product decisions. Progress can expose truthful phases or measured
units only. Notifications, if added, are wake hints rather than authority.
