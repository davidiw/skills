# PCB execution

Use for a new integrated board or substantial placement/routing work. A settled
local schematic, footprint or CPL correction retains its focused checks; it does
not need a pilot project, new toolchain or full layout campaign. This method
applies the existing evidence and bounded-execution rules to PCB dependencies.

## Prove the actual pipeline early

Before board-wide routing, exercise the repository's registered candidate and
export path using its pinned CI toolchain on the smallest useful connected native
design or current vertical slice. Reuse valid existing proof when that path and
toolchain are unchanged. Include the relevant ERC/DRC/parity checks and a small
export whose required files can actually be parsed. A standalone helper passing
does not prove the registered CI contract, schema or exporter works. If repairing
a checker, exercise its missing/invalid-input rejection as well as success.

Run the pinned version first when native API, keepout enforcement or output
conventions differ. Record local-version results separately; do not change the
accepted pipeline merely to accommodate a different workstation version.
Independent schematic work can continue while a tooling problem is isolated.
Keep exact commands, versions, adapters and known tool limitations in the owning
repository's runbook rather than hard-coding them into this skill.

Follow the repository's actual CI location and publication policy; CI need not
mean a hosted workflow. Where the owner requires local CI before opening or
updating a PR, run all applicable local gates on the final source before that
publication and retain revision-bound results. State which gates apply and which
remain unrun; do not report unknown platform checks as passing or treat a hosted
service or its billing as a blocker when that repository does not use it.

## Integrate electrical blocks before depending on them

For delegated circuit blocks, agree numbered pins/nets, rail and logic domains,
exact part/footprint identities, and the relevant source drawing or datasheet.
Keep shared GPIO allocation, net naming and power sequencing with the integration
owner. Check the returned native block against that contract before downstream
placement or routing; a narrative completion claim is not an integration check.
Reuse the handback's valid evidence instead of repeating its research. Missing
evidence stays explicit while independent work continues.

## Place and route in dependency order

Honor the authorized envelope. When the user asks for a working baseline and
defers optimization, use practical placement space and postpone compaction or
minor BOM savings until the connected baseline exists.

Place connector escapes, local bypass/bulk capacitors, switching loops, and
critical ground/return vias before general signal routing. Respect component
keepouts as well as board rule areas, including via annuli, drills and acoustic
ports. Reserve continuous reference copper for the high-speed routes and route
their constrained launches/pairs before filling the remaining routing space.
Delegate against these fixed boundaries rather than allowing independent blocks
to consume each other's escape or return paths.

Later stitching supplements those local returns. It is not the first attempt to
connect every ground pad after signal routing has enclosed it. After local
repairs, refill and check actual connectivity and reference coverage. Remove
existing copper only after establishing it is unnecessary; an unlocked or
autorouted ground connection may still be the only return for a pad.

## Bound tool failures and accept real output

Before an unfamiliar or failing router/adapter run, choose a task-relative time
or pass budget and a stopping condition. Use a small reproducer and a bounded
correction attempt. When the budget is spent or the same failure repeats without
new evidence, stop the repair loop, retain the failure, and choose a supported
fallback within the accepted scope: a working pinned tool, native editing/API,
or a smaller remaining route problem. Report a concrete blocker if no defensible
fallback exists. Broader upstream-tool development needs its own justified scope;
do not silently make it the main board-design task.

Require fresh, nonempty, parseable router output before import. A zero exit code
or a log saying completed is insufficient. Preserve the source before import;
then use native fill, DRC, unconnected and parity checks to judge the result.
Separate intended net connections from dangling leftovers rather than trusting
the router's completion percentage.

After placement or routing revisions, check that critical local bypass, feedback
and switching-return paths remain local in the final native board.

Use focused checks at circuit/layout milestones. Once the board is coherent,
run the required full acceptance path before polishing the final renders and
packaging exports. Reuse unaffected evidence after a correction and refresh the
affected checks and matching outputs. Apply the existing
[manufacturing handoff](manufacturing-handoff.md) for readiness and authorization.
