# Cedar brand direction — proposal for review

Status: proposed, not accepted design authority. DESIGN.md remains authoritative;
production HTML, CSS and JavaScript are unchanged.

## Review

Cedar serves adults maintaining ordinary routines. Its accepted promise is clear
self-reflection and useful next actions. The app already expresses this through
“Your weekly reflection,” a concrete notes action, readable system type and quiet
green controls. Retain that foundation.

The current campaign is an unapproved exploration. “Win your health,” “performance
revolution” and “Dominate today” introduce competition and implied transformation
without explaining health journaling. In the real 390 × 844 normal-state render,
its solid purple panel and serif type also create an abrupt change from the app's
white surface and green system type. Both panels fit at this viewport; the issue
is identity and meaning, not demonstrated overflow. The campaign says “neon,” but
the rendered design does not actually establish a neon visual system.

## One direction: calm attention to everyday routines

Cedar should feel observant, grounded and practical. Its recognizable idea is
making room to notice one's routine and choose a next step. This extends the
accepted identity without adding a competitive persona, diagnosis or a promise
of better health. Comprehension and preference remain hypotheses, not findings
from user research.

| Element | Shared identity | During a health task | Campaign introduction |
| --- | --- | --- | --- |
| Color | Deep green text and actions, white and pale green surfaces | White reading area; green reserved for useful emphasis | A larger pale green field with deep green headline; restrained contrast |
| Type | Readable system sans serif; clear sentence case | Familiar heading sizes and legible body copy | Larger headline and more open spacing using the same family |
| Form | Soft corners, simple borders, uncluttered space | Notes and the next action take priority | More generous composition; optional quiet lines suggesting journal pages, away from text |
| Voice | Concrete, respectful, nonjudgmental | Brief prompts and explicit action labels | A warmer invitation that names the product and explains its use |

Existing colors such as #163832, #f6f8f5 and #174f4a are useful starting points,
not newly mandated universal tokens. Preserve visible focus and familiar controls.
Let recognition come from green, typography and the language of reflection;
the campaign can be more spacious and expressive without copying the app card.
Avoid trophies, streak imagery, clinical symbols and dramatic transformation
imagery that would suggest another product promise.

## Concrete wording

Keep the application wording:

- Heading: “Your weekly reflection”
- Prompt: “What helped your routine this week?”
- Action: “Review your notes”

Replace the campaign exploration with this proposed introduction:

- Product descriptor: “Cedar · Health journaling”
- Headline: “Make room for reflection.”
- Body: “Keep notes on your everyday routines. Look back on your week and consider what to do next.”
- Action: “Review your notes,” only when connected to that existing task.

Use “notes,” “routine” and “reflection” consistently. Invite observation rather
than judge performance; describe actions rather than health outcomes. Task copy
should not repeat the campaign slogan or interrupt a review with persuasion.
Do not invent reassuring save, recovery or success messages without corresponding
behavior. The current app.js is empty and the buttons have no handlers, so the
proposed CTA is a semantic recommendation, not a verified working journey.
No new route, onboarding flow or capability is proposed.

## Bounded follow-through after approval

The proposed identity decision is to align the campaign with Cedar's accepted
reflective identity using the shared visual roles and wording above. A later
implementation would replace the campaign's inline purple/serif treatment and
copy in index.html, with scoped presentation in style.css as needed. Retain app
task semantics and existing states. Replace the fixture-style page heading
“Cedar: one product?” with “Cedar” if this comparison becomes a product surface.
Record an approved direction in DESIGN.md only after it is accepted.

Before claiming an implemented improvement, inspect narrow and wide renders,
text wrapping at enlarged text sizes, keyboard focus and contrast. Verify CTA
behavior separately if wiring is authorized. A useful comprehension check would
ask whether a newcomer can identify health journaling from the campaign and
recognize the same product on entering the weekly reflection.

## Evidence and limits

- Ran `node test.js`: passed. Existing checks assert the two section IDs only.
- Rendered the unchanged real page offline using `python3 render.py --width 390 --height 844 --state normal --output renders/narrow.png` and opened the image.
- This review covers the displayed normal state at that viewport. No usability,
  accessibility conformance, working navigation or proposed visual result is claimed.
- No production or accepted-design files were edited; this document and the
  current-page render are review artifacts.
