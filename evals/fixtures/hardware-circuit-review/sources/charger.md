# Charger facts, from the exact manufacturer's data sheet

Microchip, MCP73871 data sheet DS20002090F (2022),
[manufacturer PDF](https://ww1.microchip.com/downloads/en/DeviceDoc/MCP73871-Data-Sheet-DS20002090F.pdf):

- Product Identification System, page 33: option 2CA specifies 4.20 V
  termination voltage and a six-hour safety timer.
- Section 3.14, page 16: TE low enables the timer; TE high disables it.
- Section 4.8, page 19: charge-current regulation IREG in mA is 1000 divided
  by RPROG1 in kΩ. The input power limit and available system power also constrain
  charging current. PROG2 sets USB input current selection; it is not RPROG1.
- Section 5.2.4, page 22: PG sinks current, has a diode path to VIN and must
  not be pulled above VIN.
- Section 4.8 and its timer flow: timer expiration can terminate a charge cycle;
  cycling CE resets the timer. Thermal regulation and system loads can further
  reduce battery current.

These are abbreviated paraphrases for this offline fixture. The authoritative
source remains the linked manufacturer's data sheet.
