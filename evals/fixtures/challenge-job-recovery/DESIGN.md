# Shared render queue
job_store.py owns the existing SQLite queue and worker.py is its process-facing
consumer. Independently running workers share one database. Queue state and the
single accepted output survive process exit. The current allocator only takes
pending jobs; a stopped worker can leave a job running indefinitely.

The accepted recovery feature allows another worker to take a running job once
its lease deadline has been reached. Before that deadline another worker cannot
take it. Completion is permitted only by the current, unexpired claim; a displaced
or expired claimant must not change either job status or output. Worker names can
be reused after restart. Current claims must remain able to complete, and a done
job is not taken again. The completion decision and durable output are one store
operation. This is local state, not a claim of atomicity with external services.

Keep the existing schema, Lease fields, claim/finish APIs and worker entry points.
They already reserve a generation field for claim identity. Do not add a broker,
new queue, migration, public workflow or external effect. The storage algorithm
and validation predicate for recovery remain implementation decisions of this owner.
The caller supplies consistent numeric clock values and positive lease durations;
clock synchronization, malformed caller types, fairness and renewal are outside
this change. Test interruptions using separate worker processes and database
connections, including continuation by an earlier claimant.
