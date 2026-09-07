# Runtime Resource Governance

Use this workflow when scarce resources or optional effects can prevent required
work from progressing. Apply it to synchronous and durable activities alike.
For RAM, DMA-capable buffers, peripherals, sockets, task stacks, and finite
pools, use the resource contract and five mechanisms below. For locks, database
connections, transactions, and serialized queues, use the contention contract;
apply both only when both mechanisms affect the path.

## Critical effects and serialized contention

Name the primary action, whether it is safety/correctness-critical, and each
side effect's required or optional status. An optional telemetry or audit effect
cannot determine success or delay a critical action such as credential
revocation through a shared lock, connection, transaction, or queue.

For each demonstrated contention pair, record the lock/connection/transaction/
queue owner, acquisition order, hold or wait bound, critical progress bound,
and timeout/failure behavior. Trace indirect dependencies: moving an audit to a
background task does not isolate it if it still locks the row revocation needs.
Use omission, shedding, or an existing isolated bounded path for optional work.

If an audit is mandatory, define its durability, reserved capacity, atomicity,
failure, and recovery contract with the primary action. Repository policy must
decide what happens when it cannot be recorded; silently dropping mandatory
audit is not isolation. Avoid logging sensitive data beyond that contract.

Prove critical progress while the optional effect fails, stalls, holds a lock,
or exhausts its connections. Prove mandatory audit behavior separately when
applicable. A lock-only fix does not require memory reclamation, a restart
policy, or a new scheduler.

The correction is incomplete if it only moves the current request's audit after
commit. A second audit writer may already hold the row lock or connection the
critical transaction needs. Prove progress with that concurrent writer stalled,
as well as with this request's callback stalled. Removing this invocation's event
only removes that edge. Correct **all optional writers' participation** in the
critical domain, including already-running transactions and connection use. A
"direct" database method can still need the same locked row; its name is not
isolation evidence. Bound/revoke optional resource ownership through the existing
owner where supported, or leave that progress claim pending. State activation and
in-flight writer handling; do not assume stalled legacy writers vanish on rollout.
Returning success must also respect the response bound.

## Resource contract

Name each resource pool, its measurable capacity, and the reserve protected for
required control-plane progress. Every managed activity declares:

```text
Resource pools required:
Estimated or reserved amount:
Priority class:
Non-reclaimable phase:
Cooperative stop operation:
Maximum stop latency:
Cleanup completion evidence:
Restart or resume policy:
Durable or external-effect ambiguity:
```

One lifecycle owner admits, starts, stops, and confirms cleanup for each
activity. A composition root may assemble owners but does not become an
unaccounted second resource manager. Keep non-reclaimable phases short and
bounded. Optional work never consumes the protected control-plane reserve.

## Five distinct mechanisms

1. **Admission accounting** reserves expected demand before an activity starts
   and rejects, defers, or sheds optional work when capacity is unavailable.
2. **Pressure monitoring** observes free capacity, fragmentation, queueing, and
   stop latency so estimates and reservations can be corrected.
3. **Failed-allocation callbacks** report an emergency condition. They do not
   perform normal scheduling or complex cleanup from an unsafe context.
4. **Cooperative shedding** asks the owning lifecycle to stop reclaimable work,
   waits for bounded cleanup evidence, and then retries admission once.
5. **Restart recovery** restores a safe baseline only when bounded shedding
   cannot recover. It is the final fallback, not the primary policy.

Priority does not authorize arbitrary termination. Define which activity may
yield, which phase cannot, and what happens when the stop deadline expires.
Prevent thrashing with bounded retries or hysteresis rather than repeatedly
starting work that admission already predicts cannot finish.

## Proving the boundary

Start with one demonstrated contention pair before generalizing. Inject
allocation denial at admission and during reclaimable and non-reclaimable
phases. These are owner-focused failure fixtures, not by themselves an
independent fault campaign. Verify protected progress, stop latency, cleanup
completion, one retry, and restart recovery. Measure sustained pressure and
fragmentation separately from failed allocation. Host fakes prove policy;
executing or assessing device, firmware, or physical proof belongs to
`verification-and-operations` when the requested claim requires it.

## Completion check

For finite runtime pools, do not compress this workflow to generic
reserve-and-reclaim advice. A design, plan, or review is incomplete until it
reports every resource-contract field for each contending activity and names
all five mechanisms separately. For serialized contention, complete the
critical-effect and contention contract instead. Mark a
field `unknown` or `undecided` when repository evidence does not establish it;
do not silently omit it. State which evidence is automated and which physical
evidence remains pending.

## Critical progress against an incumbent optional writer

First record a before/after contention table: critical action, every optional
writer, each shared lock/connection/transaction/queue, and the exact ownership/path
change that removes their dependency. Omitting this invocation's callback does not
change another writer's lock or pool use. If that other path is unavailable, leave
its isolation unproven; do not replace the database with a contention-free fake.

When optional audit/telemetry can contend with a critical action, prove the
**other-writer case before claiming isolation**: stall an independent optional
writer while it holds the shared row/lock/connection/queue; only then begin the
critical action. Assert the critical commit completes within a bounded deadline
while the writer is still stalled. Release/join all test workers in cleanup.
The baseline model must reproduce blocking while the optional writer owns the
identified shared resource. The corrected model changes only the proposed
isolation and must pass while that writer remains held. Show the mapping to the
real owner contract; a stalled callback holding no needed resource is not this test.
A mock that merely verifies the current audit callback was not called proves
only omission, not contention isolation. Moving that callback after commit is
also insufficient. Use the existing database owner's independent critical path
or remove the optional contention dependency across all writers; do not invent a
new queue/framework. Do not change the critical row to an unrelated free lock in
a fake: preserve resource identity and model the actual proposed owner mechanism.
If audit is mandatory, its durability, reserved capacity and failure behavior
must be explicit before selecting the implementation.

For design-only requests, exercise the proposed isolation in a synthetic model
and label it design proof; do not modify production code or claim its deployed
behavior is verified. The proof still needs synchronization, a bounded deadline,
an independently held contention domain and deterministic worker cleanup.
