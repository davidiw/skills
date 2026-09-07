---
name: interface-design
description: Resolve visual hierarchy, composition, density, affordance, responsive layout, and accessible presentation. Use for meaningful interface changes or rendered UI review; not every UI file edit or a settled label correction.
---

# Interface Design

Own how an accepted task and visual intent become a clear, usable interface.
Valid components are necessary evidence of consistency, not proof of hierarchy.

1. Identify the surface's job and accepted visual authority. Inspect relevant
   tokens, components, neighboring surfaces, and available current rendering.
   Missing DESIGN.md does not make an established interface greenfield. When
   documenting, merging, or resolving design authority, read
   [repository design language](references/design-authority.md).
2. Judge what actually draws attention: composition, grouping, density, spacing,
   typography, alignment, affordance, action prominence, and state presentation.
   Distinguish a local craft problem from an unresolved task or identity decision.
   Respect the usage situation: operational, reading, persuasive, or expressive.
   Familiar controls, dense information, and expressive typography each need context.
3. Choose the smallest authorized correction within accepted intent. Preserve
   effective components and semantics; avoid automatic redesign or creating tokens
   for isolated exceptions. Product/IA changes return to product-experience;
   proposed identity/visual-intent changes belong to brand-and-language and the
   existing approval gate, not an implicit CSS decision.
4. For meaningful visual or interaction claims, read and apply
   [rendered evidence](references/rendered-evidence.md). Check the affected content,
   state and viewport ranges rather than polishing only a convenient screenshot.
   When accessibility, input, or responsive constraints matter, read
   [platform checks](references/platform-checks.md); standards come from primary
   platform authorities, not external agent-skill checklists.
5. Correct demonstrated defects in a bounded batch and confirm the affected
   states. Report what was observed, the correction, and any material unverified
   claim. A source-only review cannot certify visual success; a screenshot cannot
   establish keyboard behavior or human task success.

Do not turn taste into universal rules about cards, gradients, modals, minimalism,
fonts, or CTA counts. Brand-and-language owns accepted identity intent; this owner
applies it to concrete composition without silently changing it. Engineering
[invariants](../../references/invariants.json) remain with their owners; load exact
contracts only when unresolved. Apply [precedence](../../references/precedence-and-exceptions.md)
for conflicts. Read-only review leaves production unchanged, and independent gates
retain the existing context-separation requirements.
