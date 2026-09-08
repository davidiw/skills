# Cedar brand direction: Make room for reflection

Proposal for review; not an amendment to DESIGN.md. Production files remain unchanged.

## What the current surface communicates

DESIGN.md establishes Cedar as health journaling for adults maintaining ordinary routines: clear self-reflection and useful next actions. The app supports that promise through a specific weekly question, a familiar notes action, readable system type, white space and quiet green controls.

The campaign is explicitly an unapproved exploration. “Become unstoppable,” “Win your health,” and “Dominate today” introduce competition and pressure; “performance revolution” obscures what Cedar actually does. Its purple field and serif typography introduce a separate visual identity. In the actual 390 × 844 render, the campaign becomes the dominant block even though the app appears first. The campaign claims neon energy in its copy, but the rendered design is a solid purple panel, not a neon treatment. Matching colors alone would leave the deeper promise mismatch unresolved.

## One identity, two levels of expression

**Make room for reflection.** Cedar gives ordinary routines a place to be noticed and considered. The shared character is attentive, grounded and clear. Success means understanding your notes and considering a useful next step, without performance rankings or health-outcome promises.

| Element | Shared visual intent | Campaign introduction | In-task application |
| --- | --- | --- | --- |
| Color | Cedar green, warm pale neutral and white | Use a broad pale green field with dark green text; green supplies recognition | White reading surfaces, quiet green actions and restrained borders |
| Type | Readable system sans serif with a consistent weight hierarchy | Larger headline, generous spacing and short supporting text | Compact hierarchy that puts the reflection prompt and action first |
| Shape | Soft corners and simple lines, drawing from the existing cards | A spacious composition of journal-like lines can suggest reflection | Familiar cards and controls; decoration stays outside the reading and action areas |
| Imagery | Everyday observation rather than athletic or clinical symbolism | Optional abstract journal motif; no fabricated metrics, testimonials or outcomes | No hero artwork competing with notes or task status |
| Interaction | Clear action labels and visible focus | Introduce the same notes/reflection activity | Preserve established destinations, state meanings and familiar behavior |

The campaign can feel inviting through scale, spacing and composition without giving the task screen a promotional tone. Existing CSS colors and shapes are useful starting points, not a requirement to make every surface identical. Remove the campaign’s purple/serif identity in a future approved implementation. Avoid neon effects, trophies, streak pressure and clinical imagery.

## Voice and proposed copy

Use plain, adult-to-adult language. Name the activity before adding emotion. Invite reflection without judging missed routines, promising improvement or implying diagnosis. Prefer “notice,” “reflect,” “notes” and “routine” over “win,” “dominate,” “optimize” or “transform.”

**Campaign**

- Headline: “Make room for reflection.”
- Supporting copy: “Cedar is a health journal for your everyday routines. Look back at your notes and reflect on what helped.”
- Action: “Review your notes.”

**Application**

- Heading: “Your weekly reflection”
- Prompt: “What helped your routine this week?”
- Action: “Review your notes”

Keeping the app’s current copy lets the campaign introduce the experience users actually encounter. The campaign action names that same activity. The current buttons have no implemented behavior and app.js is empty; this proposal does not claim a working journey or authorize a new destination. Future wiring requires a separately defined behavior.

## Approval and verification

Approve the shared identity, campaign visual treatment and copy as one direction before implementation. Keep DESIGN.md authoritative until that decision. A later bounded change would belong to the existing campaign markup and stylesheet; this review adds no routes or functionality.

Review a future implementation for immediate recognition across both surfaces, accurate understanding of health journaling, legible narrow-screen wrapping, text/control contrast and visible keyboard focus. During a reflection, the question and notes action should remain easier to find than promotional material.

Evidence: rendered the real current page offline at 390 × 844 in normal state and opened [current rendering](brand-current.png) for visual inspection. `node test.js` passed; its assertions only check the two section IDs, so they do not validate brand coherence, accessibility or working interactions. No proposed redesign has been rendered.
