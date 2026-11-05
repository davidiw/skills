# EDA and mechanics

Treat native CAD and the netlist as authoritative design sources. Use the official
KiCad CLI for relevant ERC, DRC, parity checks, and exports supported by the
project's toolchain. Inspect exported fabrication and assembly views visually as
well as checking automated results. Use supported APIs for transformations; when
necessary, pin a pcbnew adapter to the applicable version and verify its output.
A known component rotation correction needs the relevant focused checks, not an
automatic redesign or independent review.

Derive connector pin 1, contact face and orientation, staggered lands, bend
allowance, and footprint details from the actual part and mating-part drawings.
Record drawing revision and viewpoint; do not infer orientation from an appealing
render. Preserve accepted choices unless contrary evidence changes the decision.

PDF, DWG, and image extraction can supply dimensions or geometry, but record
warnings, scale, coordinate origin, transforms, and provenance; check extracted
features against the source. Model the complete assembly in FreeCAD or the
project's mechanical CAD, including mating parts, fasteners, access, and clearances.
Physical measurements and observed builds outrank catalog dimensions and renders;
distinguish specified, modeled, automatically checked, and physically proven facts.

Use SPICE with suitable models for the circuit question, checking the model's
validity and missing operating modes. Use a fabricator calculator or appropriate
field solver for impedance, retaining the exact stackup, geometry, inputs and raw
result. Simulation can inform a design but does not prove actual waveforms, tolerance,
thermal behavior, or physical fit; those claims need their appropriate evidence.

Start with the [official KiCad CLI documentation](https://docs.kicad.org/10.0/en/cli/cli.html)
for the installed release and inspect available commands before scripting them.
Netlist and geometry checks should inspect actual native connections, routed
tracks, vias and filled reference copper, not just net names, nominal rules or
the existence of one ground polygon. Match, for example, a claimed reference
plane check to coverage beneath the real routed segment.
