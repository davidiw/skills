# Existing operation contract
A pending import is admitted once per account/target. Queue.admit_unique persists
intent in production and validates the existing account/grant fence at execution.
Wakes must not reset operation backoff or change authorization, grants, collection,
retention, disclosure, or erasure. The fixture queue is a deterministic fake.
