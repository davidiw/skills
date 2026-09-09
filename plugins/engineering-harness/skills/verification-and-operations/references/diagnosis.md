# Targeted diagnosis

Use when the reported symptom has an unresolved cause. An obvious local correction
with a settled cause needs only its focused check. This method supports the
selected implementation owner; it does not require another specialist body.

1. State the user's symptom and inspect the actual path and relevant existing
   evidence. Distinguish observations from candidate explanations. Source
   inspection may be needed to find a reproducible seam; do not block it behind
   a requirement to have already reproduced an inaccessible failure.
2. Seek a discriminating signal at that seam: an existing test, small fixture,
   captured trace, targeted measurement or authorized local probe. Verify it can
   detect the reported failure, not just finish successfully. Narrow timing or
   inputs where useful, preserving the real failure mechanism.
3. Test plausible explanations with predictions and targeted probes; vary one
   relevant factor where practical. Use as many hypotheses as the ambiguity
   warrants, not a fixed quota. Reuse repository performance acceptance rules; a
   diagnostic speedup alone is not a qualified optimization.
4. Fix within the accepted owner and scope. When practical, show the same focused
   check fail before and pass after; check affected seams and remove temporary
   instrumentation. An unavailable environment or missing failure signal remains
   an explicit evidence limit, not a fabricated reproduction or an automatic
   prohibition on useful read-only investigation.

Keep output to the symptom, distinguishing evidence, correction and remaining
limit. Required gates and expansion approval remain with the router. If diagnosis
reveals a shared architecture or testing gap, record it for a separately scoped
system slice; do not automatically start a redesign or broad campaign.
