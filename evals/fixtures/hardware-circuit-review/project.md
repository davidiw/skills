# Candidate and scope

This prototype has one 1,800 mAh lithium-ion battery. USB may be unplugged
while the retained V3V3 rail powers the processor from the battery. The design
intends to recharge a substantially depleted cell without user intervention.
PROG2 selects the USB input current allowance; the processor may change it after
USB startup. The board also includes a fuel gauge, a PDM microphone and an I2S
speaker amplifier. The latest recorded full-project ERC completed with zero
violations; no physical board is available.

The `native/` directory holds relevant KiCad schematic sheets, a filtered
exported netlist and a two-footprint PCB placement extract from the same prior
candidate. The netlist preserves the original pin electrical types. The PCB
extract omits other components and all tracks and zones; use it for the two
retained footprints' placement, not full-board connectivity or DRC. Sheet
fragments are not a standalone full project. The receipt is historical and
cannot validate subsequent edits.
