# Manufacturing handoff

Use for fabrication/assembly exports, quote preparation, actual-job review, or an
order-readiness question. Apply the existing [artifact evidence contract](../../verification-and-operations/references/artifact-and-physical-proof.md);
hardware-specific checks below do not create another evidence hierarchy or grant
purchase authority.

## Select the intended build

Separate an engineering-file review, a prototype intended to resolve named
questions, and a production run. Identify which acceptance criteria apply now.
Unmeasured refresh rate or sleep current can be the purpose of a prototype. An
unresolved potentially damaging pin mapping, rail connection, footprint, or
unachievable power sequence needs resolution or safe test accommodation before
that circuit is fabricated or exposed to the affected device. Explain the exact
risk, corrective action and remaining experiment; a generic HOLD is insufficient.

Order eligibility concerns the named design and actual job. Qualification concerns
the measured assembly. Production acceptance additionally covers the intended
operating range, users, manufacturing variation, reliability and applicable
product requirements. Reuse accepted prototype deviations within their conditions;
new contrary evidence can reopen them. A clean DRC is not an operating guarantee.

## Bind design to delivered files

Use the repository's existing generation and check commands. For the affected
scope, confirm native schematic/netlist/PCB parity, relevant electrical and layout
checks, exact fitted population and test configurations. Fail a checker when its
required inputs are absent, tool execution fails, or required results are missing;
exercise the relevant negative case before trusting a repaired success path.

Export Gerbers, drills, assembly BOM and placement data from the same design and
population. Check exact reference-set agreement, intended DNPs, through-hole
service parts, polarity, side, coordinate origin and units. Inspect copper, mask,
paste and drill views at critical footprints, rather than relying on a body render.
Record actual tool versions and source/generator/output identities through the
existing artifact mechanism; preserve current review evidence when unchanged.

Read the assembler's actual placement preview and job settings when available.
Compare numbered lands, lead geometry, pin 1, polarity and mating orientation with
native pads and manufacturer drawings. A public footprint fit is preliminary;
it does not establish the assembler's private pickup centroid or zero angle.
A rotated body label alone does not prove a placement error; distinguish the
component model's registration from actual electrical lead/pad orientation.
When the job is inaccessible, state exactly which claims remain unverified and
use supplied exports or screenshots. Do not imply account access from a cart URL.

Compare actual fabrication selections with the exported board: stackup, layer
order, thickness, copper, minimum drills, finish, mask/via process, controlled
impedance structures and test/report options where relevant. A selected tolerance
alone does not establish the intended impedance target. Keep raw calculator inputs
and output separate from fabricator acceptance and measured coupons. Report the
actual run, launches, reference planes and transitions a model does and does not
cover. Request fabricator review of concrete process conflicts; do not invent a
service or guarantee that the assembler does not offer.

## Complete the correction and handback

For a demonstrated export or placement fault, correct its authoritative producer
or documented library transform, regenerate affected files, and run the focused
regression. Encode any assembler-specific angle/XY transformation with its part
identity and evidence. A library zero-angle change must not inadvertently rotate
the native footprint-to-body offset. Unknown transforms remain explicit; a
blanket correction for every IC is not evidence.

Name what changed: electrical design, copper, drills, fitted population, XY,
rotation, or documentation. Identify which artifacts the developer must replace
and which existing job inputs still match. If only CPL rotations changed, say so
and do not demand a new PCB upload solely for regenerated timestamps. If geometry
or population changed, provide the newly matched file set and invalidate the
affected older preview. Inspect the corrected preview before calling the live
placement fixed; generating a CSV does not modify an assembler's job.

Deliver concrete files, results and the smallest remaining action list. Separate
automated passes, prototype-order eligibility, physical qualification and
production acceptance. Distinguish eligibility from authorization to upload,
purchase, fabricate or publish; reuse the user's existing action authority.
For JLCPCB, use [the assembler-specific reference](jlcpcb.md).

Before assigning owner work, finish the research and preparation available to the
agent. Ask for specific photos, dimensions, documents or measured results, naming
the decision enabled, when the answer is needed and work that can continue. Match
bench instructions to the identified board revision, fitted population and available
instruments; an order or fabricated board is not proof it matches the latest PR.
Prepare exact connections, limits and a result format before asking the owner to
execute a powered experiment. Keep supplier inquiries ready to send and distinct
from permission to send them; final quotes and submissions must name the intended
build rather than an obsolete reference outline.
