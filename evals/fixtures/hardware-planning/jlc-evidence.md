# Synthetic JLC assembly snapshot

A customer wants ten assembled experimental boards. `jlc-inventory.csv` lists
one row for each fitted part number. The orderable quantities, attrition and
placement minimums are service snapshots, not reservations. No supplier response
or consignment decision has been received. Prices are per piece; feeder, setup,
fabrication, assembly and shipping charges are not in the snapshot. No actual
order, inquiry or supplier message is authorized.

U1 implements a reset threshold, output type, timing and supply range needed by
the board. The current research has not established a compatible Basic item.
The MCU-X listing flags not recommended for new designs; the displayed price is
a placeholder with no supported quote. Prototype supply and the production
approved-vendor list are separate decisions.

The design has a regulated 5 V rail with an input capacitor C1. The converter
vendor's review condition for the intended load and startup is at least 8 µF
effective capacitance at 5 V and an ESR of 3–50 mΩ over -20 to +60 °C. Switching
and inrush estimates must be checked for any change. Two Basic candidates in the
same package have these synthetic first-pass models:

| Candidate | Nominal capacitance | Modeled effective C at 5 V | Modeled ESR | Other evidence |
|---|---:|---:|---:|---|
| CAP-A | 10 µF | 3.6 µF | 15 mΩ | Meets voltage rating; effective C is modeled across the target temperature range. |
| CAP-B | 22 µF | 9.2 µF | 10 mΩ | Meets voltage rating; effective C is modeled across the target temperature range. Inrush estimate and physical behavior remain unverified. |

These data are deliberately synthetic, are not manufacturer guarantees, and do
not qualify a production part. Assume both candidates have sufficient available
Basic stock for the batch; no other substitute is prequalified.
