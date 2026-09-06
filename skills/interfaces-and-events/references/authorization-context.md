# Mutable Authorization Context

Apply `authority-context-fencing` to synchronous reads and exports as well as
durable work. Account identity is only one part of authority.

At the operation owner, bind the principal/account, requested operation and
purpose, required capability, applicable consent, and lifecycle/expiry. Name
which values can change and which owner decides whether use is still allowed.
Use the existing authorization service and fencing mechanism where possible.

A credential, browser handoff token, provider grant, or OS permission proves
only its stated scope. Capability availability does not establish product
authorization. A handoff credential remains bound to its intended audience,
purpose, principal, lifetime, and replay policy; it cannot become an ordinary
product session through an implicit fallback or shared cookie path.

Revalidate at sensitive reads and externally visible effects, after waits or
callbacks that can invalidate the decision, and at each staged export boundary.
Fence the effect against the validated context using an atomic precondition,
version check, or the repository's equivalent. Repeated checks with an unguarded
check/use gap do not establish fencing. For a provider call that cannot be
atomic with local authorization, state the revocation linearization point and
residual exposure; stop future stages and suppress stale results. Already
disclosed bytes cannot be recalled.

Test account switch, permission loss, consent withdrawal, expiry, and deletion
between the check and use and between stages. A denied read must not leak via
its response, cache, telemetry, temporary file, or error body. Select the
smallest relevant cases; immutable public data does not need account machinery.
