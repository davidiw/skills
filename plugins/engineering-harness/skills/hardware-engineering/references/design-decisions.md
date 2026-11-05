# Hardware design decisions

Start with the actual experiment or product, its operating conditions, budget,
quantity, available operator equipment, and complete assembly envelope. Identify
the decision, its constraints and consequences, and the evidence that would change
it. Compare alternatives where the tradeoff matters; do not manufacture options
for a settled or trivial choice. Every experimental feature should answer a named
question. Separate configuration controls, current measurement links, and debug
resets: they have different purposes and failure modes.

Evaluate small switches, buttons, and solder links alongside tall jumpers where
appropriate. Account for operator access, pinch and headroom, service frequency,
assembly labor, parts, and the real total assembly cost, not component price alone.

Use exact supplier and manufacturer evidence for the chosen parts and revisions.
For power and logic interfaces examine nominal and minimum operating values,
absolute limits, tolerances, voltage drop, transients, logic thresholds, and
unpowered I/O behavior as relevant. Confirm that startup, shutdown, and sequencing
are achievable in the actual circuit, including external connections. Resolve
potentially damaging unknowns or accommodate them safely in hardware before
exposing a device; unknown performance may instead be a bounded experiment.

Calculate available margin against the guaranteed input range after supply
tolerance, cable/trace/switch loss and relevant load conditions. A nominal supply
equal to a device's minimum leaves no guaranteed positive margin. Controller-family
capability does not establish the delivered module's factory straps, interface
mode or initialization. Reconcile exact-module schematics, drawings and code;
record conflicts and request only the missing facts that cannot be derived.

A documented prototype procedure can require an equipped operator to calibrate and
scope the actual waveform before connecting a panel. That does not establish
production tolerance, recovery, or safe handling by the intended user. For production,
design and verify those conditions for the actual use and variations.
