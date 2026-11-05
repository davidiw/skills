# Bench and Production Qualification

Inventory available hardware and its revision and population, instruments and
loads, calibration status, probe grounding and bandwidth, supply limits, and
operator skills before choosing a measurement. Establish a safe load setup and
whether equipment can resolve the expected signal; record limitations. Review
schematics, assembly, polarity, continuity, shorts and relevant static checks
before power. A bench script must not silently energize unknown hardware. Apply
the existing explicit flash and power authorization and operator preflight; if an
action is not authorized, surface that boundary before executing it.

For first power, preflight a current-limited supply and power the board without
expensive loads first. Check rail levels and current, power, reset and enable
states, and possible backfeeding across connected supplies and interfaces. If a
rail could damage a module, use suitable dummy loads and a meter plus scope to
check steady state and startup, shutdown and load transients before attaching it.
Do not infer transient safety from a meter reading alone.

Design experiments around the claimed operating range and failure mechanisms.
Change one factor at a time when practical; otherwise document interactions and
why the design is necessary. Name the criterion, conditions, repetitions and
measurement method before each experiment. Trace each qualification control to
its named experiment. Record board revision and population, jumpers, firmware,
profile and toolchain, equipment and setup, observed conditions and results so
another operator can reproduce them. Identify genuinely unavailable module strap
combinations as unsupported rather than guessing their behavior. Mark unrun
measurements **NOT MEASURED** and preserve the distinction between measured and
pending results. Use the domain owner's methodology for camera endurance, drops
and latency, and distinguish board/harness signal integrity from panel/protocol
limitations in the conclusions.

Use measured behavior and the design owner's constraints to propose a minimum
production circuit, including whether regulated rails or native GPIO can replace
prototype circuitry. A prototype fabrication step can precede runtime performance
measurement when circuit, connector and process safety are established. Before a
production release, qualify the operating corners, environmental exposure,
assembly, yield, reliability and compliance relevant to the intended product;
state outstanding work rather than inventing universal certifications or sample
quantities. Record the rationale and evidence for each simplification.
