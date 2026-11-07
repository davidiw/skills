# JLCPCB sourcing and actual-job review

Use only for a JLCPCB build. Verify current service rules, inventory and prices
against primary JLC/manufacturer sources when they affect the decision. Keep
part-specific offsets, quotes and accepted deviations in the project, not in
this reusable reference.

## Cost and assembly choices

Compare total assembled batch cost for the intended quantities: fabrication,
parts, setup/stencil, placement, per-type Extended charges, mixed SMT/THT or
second-side service, separately supplied accessories, shipping and tax where
known. Slightly more PCB area can be cheaper overall if it enables an eligible
single-side assembly process. Check the entire installed mechanical envelope.
Do not equate front-mounted component bodies with an SMT-only assembly if headers
still need through-hole soldering.

Prefer Basic or otherwise fee-favorable parts when electrically and mechanically
qualified. Verify exact MPN, package suffix, LCSC identity and usable assembly
stock; a catalog entry or EasyEDA footprint is not a stock reservation. Treat
Preferred/Extended promotions and quantity thresholds as current service facts,
not permanent exceptions. Compare a proposed substitute's tolerance, startup,
logic, leakage, thermal limits, footprint and availability before changing CAD.
Avoid a costly regulator, translator or switch without a concrete requirement;
remove one only after checking the requirement it served.

Reconcile each fitted MPN against orderable assembly quantity for the actual batch,
including required placement loss and minimums; physical stock can include
reserved or otherwise unavailable parts. Group the BOM into stocked Basic or
otherwise fee-free parts, stocked Extended parts with a concrete justification,
shortages or unknowns needing an ETA/global-sourcing inquiry, and confirmed
consignment only after the procurement route is established. Zero or negative
availability does not establish
end-of-life or mandatory consignment. Exclude obvious placeholder prices from cost
claims, and distinguish a prototype-only not-recommended-for-new-designs (NRND)
choice from a production approved-vendor list (AVL).

For MLCC substitutions, evaluate effective capacitance at the relevant DC bias and
temperature, tolerance, ESR, regulator stability and inrush where applicable. A
defensible modeled prototype choice can proceed with its assumptions and gaps
stated; do not require production lot qualification before every prototype.
Production acceptance needs the evidence appropriate to its actual operating and
manufacturing range.

Record a live captured quote separately from a modeled estimate. Include date,
currency, quantities, fitted sides and known exclusions. Unselected cart items,
partial fee displays or stale screenshots do not establish a final checkout total.
Do not promise a target cost by omitting necessary assembly labor or accessories.

## Match the actual job

Use the [manufacturing handoff](manufacturing-handoff.md) for the general check.
For JLC, compare exported BOM/CPL references with the selected parts and actual
placement preview. Account for intentional DNPs and manual-service references.
Loose shunt caps, cables and operator accessories need their own explicit supply
and installation plan; their header's BOM row does not include them automatically.
Tell the developer which unpopulated pads are configuration links and how they
will operate them with the available tools.

JLC's CPL names are `Designator`, `Mid X`, `Mid Y`, `Layer`, and `Rotation`;
confirm the currently accepted format, units and angle convention. Fit origins
against numbered pads when useful, then inspect the actual part model and lands.
Preserve an observed part-specific correction in the generator and return final
angles, not merely "rotate another 180 degrees" when prior manual edits may
already exist. Recheck the new preview and confirm process compatibility.

Read the selected stack identifier and actual drill/diameter option. If the order
option excludes a drill present in the files, change the option or obtain JLC's
specific acceptance; do not enlarge holes blindly and damage annular rings or
clearances. Request the intended impedance target, tolerance and report/coupon
where required, recording any fabricator-adjusted geometry. Confirm fine-pitch
finish, paste apertures, stencil thickness, mask registration and via treatment
where actual component drawings or artwork expose a conflict. Do not automatically
require ENIG or a stepped stencil for every prototype.

When required by the actual job, obtain the manufacturer's current impedance-
control worksheet/template, complete it for the routed structures and selected
stackup, and include it with the fabrication submission. Retain the completed
document with the matching board files; a calculator result or order checkbox
does not replace a requested worksheet.

Public component APIs and an exported preview can support review without live
account access. State the limits of those observations. Keep private cart access
tokens, account details and supplier correspondence out of public artifacts.
An order or job edit is a separate action from producing files.

Primary starting points (consult the relevant current page rather than copying
prices or process limits into the skill):

- [BOM/CPL requirements](https://jlcpcb.com/help/article/how-to-generate-the-bom-and-centroid-file-from-kicad)
- [Centroid file and rotation](https://jlcpcb.com/help/article/pick-place-file-for-pcb-assembly)
- [Assembly rotation FAQ](https://jlcpcb.com/help/article/pcb-assembly-faqs-part-2)
- [Assembly capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities)
- [Assembly pricing](https://jlcpcb.com/help/article/pcb-assembly-price)
- [Controlled-impedance stackups](https://jlcpcb.com/impedance)
