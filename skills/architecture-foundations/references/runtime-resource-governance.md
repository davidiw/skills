# Runtime Resource Governance

Use this workflow when RAM, DMA-capable buffers, hardware peripherals, sockets,
task stacks, descriptors, or another finite runtime pool can prevent required
work from progressing. Apply it to synchronous and durable activities alike.

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
phases. Verify protected progress, stop latency, cleanup completion, one retry,
and restart recovery. Measure sustained pressure and fragmentation separately
from failed allocation. Host fakes prove policy; device, firmware, or physical
claims remain separate evidence owned by `verification-and-operations`.

## Completion check

Do not compress this workflow to generic reserve-and-reclaim advice. A design,
plan, or review is incomplete until it reports every resource-contract field
for each contending activity and names all five mechanisms separately. Mark a
field `unknown` or `undecided` when repository evidence does not establish it;
do not silently omit it. State which evidence is automated and which physical
evidence remains pending.
