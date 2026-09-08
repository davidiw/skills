**Make Today’s existing Weekly Reflection entry resumable.** Keep it below immediate work, retain History for completed activity, and add no destination.

The current flow saves answers as users type, but Today’s link creates a new draft every time. Reopening a saved ID restores progress correctly. The missing piece is discoverable entry.

Proposed contract:

| State | Entry and recovery behavior |
| --- | --- |
| No unfinished reflection | Keep the existing start entry. |
| One draft | Show **“Continue Weekly Reflection · Question 2 of 3”**, with its saved date. Open that record at its saved question, preserving answers. |
| Failed completion | Show **“Weekly Reflection · Completion failed”** with a Continue link. Reopen saved answers and the existing **Try again** action; do not retry automatically. |
| Multiple unfinished records | Show a compact **“Unfinished reflections (N)”** disclosure at the same entry, with dated, state-labelled links. Include older records; do not silently select or discard one. Keep starting a new reflection an explicit secondary action. |
| Completed | Remove it from unfinished entries; retain its existing completion view and History entry. |
| Missing record | Keep the existing “unavailable in this browser” message and Back to Today link. |

Within the flow, show **“Answers saved in this browser. Continue from Today.”** after successful saving. Bind newly created reflections to their ID in the URL so refresh preserves the same record.

This preserves local storage, existing records, destination priorities, and completion semantics. It introduces no expiry, cross-device recovery, or weekly scheduling rule—the current `week()` function actually records a calendar date.

I verified the current flow in local Chromium at 1000×800 using synthetic records: interruption/re-entry created another draft; ID-based resume restored progress; failed retry preserved answers; successful retry completed the record. Improved discoverability remains a hypothesis, without user research.

**Production is unchanged.** [DESIGN.md](source/DESIGN.md) explicitly leaves entry/recovery undecided. The behavior above is the concrete contract proposed for acceptance before implementation.
