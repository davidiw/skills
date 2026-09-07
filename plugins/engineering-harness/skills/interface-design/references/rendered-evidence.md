# Evidence for experience claims

Rendered experience is evidence for experience claims. Source structure alone
does not establish visual hierarchy, usability, responsive quality, or interaction
clarity. Distinguish a rendered observation from a hypothesis about comprehension,
preference, or task success; those outcomes may require human evidence.

| Work or claim | Proportionate evidence |
| --- | --- |
| Tiny label or settled semantic-name correction | Source and a relevant focused check can suffice. |
| Minor spacing/alignment correction | One representative before/after render when claiming a visual improvement. |
| Responsive layout | Representative narrow/wide rendering and the content or text-scale transition affected. |
| Material interaction/flow | Actual navigation sequence and relevant normal, waiting, empty, partial, stale, failed, retry, disabled or success states. Select reachable states. |
| Accessibility | Applicable semantics, focus/input behavior, and rendered/platform checks; screenshots alone are insufficient. |

For ordinary bounded work, inspect the relevant rendering, identify the state and
viewport in the short handback, and state limits. **No artifact hashes, formal
receipt, or evidence directory is required merely because work changes UI.**
Use existing screenshots/traces when current and sufficient; do not duplicate them.

For retained evaluations, release gates, or repository-required evidence, use the
existing evidence contract: exact snapshot/diff, fixture, state, viewport/text
scale/input, artifact/trace, observed result, and unreviewed limits. Hash retained
artifacts only where that contract requires integrity or reproducibility. Required
review receipts remain required; this proportionality does not waive an existing gate.

Verify screenshot freshness against the route, source, theme, assets and variant.
Historical renders can establish a past defect, not current correctness. Mocks or
generated images support a proposal; they do not prove the implementation. When
rendering is unavailable, continue source inspection or authorized bounded work,
label visual conclusions unverified, and leave required visual gates pending.

Prefer synthetic, representative content and local tools. Never obtain real health
data or perform live provider effects merely to produce a visual example. Batch
relevant observations, correct demonstrated problems, and confirm affected states.
Broaden only for a concrete unresolved concern; a time budget cannot make a failed
gate pass. Do not claim accessibility conformance from a screenshot or automated score.
