---
name: hardware-engineering
description: Resolve electrical, power, connector, PCB, mechanical CAD, and manufacturing design decisions for physical hardware. Use when designing or materially changing those interfaces or artifacts; not for generic firmware work, routine verification policy, or actual bench qualification.
---

# Hardware Engineering

Own design decisions at the electrical, mechanical, and manufacturing seams.
Generic firmware remains with its implementation owner; verification and operations
owns evidence semantics and gates, and hardware qualification owns actual bench
measurements. Apply the existing [invariants](../../references/invariants.json) and
[precedence](../../references/precedence-and-exceptions.md) rather than creating a
parallel policy.

1. Establish whether the design is an early experiment or intended for production,
   the question each experimental feature answers, and the budget, batch size,
   operator equipment, and assembly envelope. Identify accepted decisions and the
   evidence behind them. Reopen them when contrary evidence warrants it, not merely
   because alternatives exist.
2. Before costly routing or fabrication, resolve consequential architecture and
   interface tradeoffs in [design decisions](references/design-decisions.md). Scale
   analysis to the decision; there is no quota of alternatives. A known local fix
   should remain local unless evidence exposes a wider problem.
3. For schematic, PCB, source extraction, or mechanical fit work, apply
   [EDA and mechanics](references/eda-and-mechanics.md). Use authoritative native
   sources and actual component drawings; assess the complete assembly. Unknown
   performance can be tested, while potentially damaging power or connector
   unknowns need resolution or safe hardware accommodation before exposure.
   For a new board or substantial reroute, apply
   [PCB execution](references/pcb-execution.md) before board-wide routing.
4. When preparing fabrication or assembly deliverables, read
   [manufacturing handoff](references/manufacturing-handoff.md); for a JLCPCB-specific
   handoff, also read [JLCPCB](references/jlcpcb.md). Distinguish design intent,
   automated checks, and physical evidence using the existing evidence contract.
   Record material unknowns and hand off required measurements to hardware
   qualification; do not imply simulation, a render, or export checks prove a build.

Use risk-based judgment, not a generic safety checklist or a mandatory redesign or
independent review for each change. Respect the applicable repository gates.
