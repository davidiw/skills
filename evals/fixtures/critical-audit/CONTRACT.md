# Revocation contract
Credential revocation must progress during optional analytics outage. The audit
adapter writes optional security activity metadata and may wait on a row lock or
an exhausted connection pool. Other instances of the same audit adapter may hold
a lock on the account row needed by revoke_credentials. No external retained-audit
requirement applies in this fixture. The established database owner can revoke
without using that analytics path. Account state and revocation are sensitive.
