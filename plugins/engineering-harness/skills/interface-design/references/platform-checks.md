# Authoritative platform checks

Normative accessibility requirements and platform facts come from the applicable
primary authority. External agent skills supply judgment/workflow patterns, not
standards. Identify platform, criterion/version, applicability and exceptions before
making a conformance claim. Repository taste cannot waive an applicable requirement.

| Need | Primary source |
| --- | --- |
| Web accessibility requirements | [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/). Its [Understanding documents](https://www.w3.org/WAI/WCAG22/Understanding/) explain criteria; distinguish requirements from sufficient/advisory techniques. |
| Complex web widget patterns | [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/). Examples are implementation guidance, not automatic conformance. |
| Apple platform behavior and accessibility guidance | [Apple Human Interface Guidelines: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility). Use the relevant platform/control documentation. |
| Android accessibility and target behavior | [Android accessibility guidance](https://developer.android.com/guide/topics/ui/accessibility/apps). Distinguish recommendations and framework-enforced behavior. |
| Flutter semantics and testing | [Flutter accessibility testing](https://docs.flutter.dev/ui/accessibility/accessibility-testing), including Guideline API and platform semantics. |

Fetch only the relevant authoritative section when its facts are needed; use
repository-pinned authoritative excerpts when available. For frozen evaluations,
record the consulted version/excerpt; do not silently grade against moving guidance.
If unavailable, identify the unverified fact rather than inventing a numeric rule.

Useful checks include accessible names; semantic controls; keyboard reachability,
visible focus and restoration; actual hit targets; contrast against the rendered
background; reflow, zoom/text expansion and clipping; reduced-motion behavior;
state announcements; image dimensions/alternatives; and retained access to essential
actions. Reuse repository tests/tools, and verify flagged results in context.

CSS pixels, native points, Android dp, and Flutter logical pixels are not an
interchangeable universal minimum. Visible glyph size may differ from hit area.
Avoid hiding overflow or actions to make a screenshot pass, redundant keyboard
handlers on native controls, or regex-only accessibility verdicts. Cheap checks
support expert judgment; they cannot establish holistic usability or conformance.
