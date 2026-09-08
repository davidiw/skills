# Authoring Harness instructions

Use when editing discovery, skills, agent-facing policy or their references. This
is repository development guidance, not installed runtime policy. DESIGN.md owns
the package authority map; repository/platform validators own accepted formats.

- Start with the demonstrated missed decision and its existing owner. Keep one
  canonical rule; reuse an exact contract reference instead of loading another
  workflow. A useful external method may fill a gap without becoming a skill.
- Put the actual triggering task in discovery metadata; a condition hidden in a
  specialist cannot select the router. Include a nearby negative control.
- Keep common decisions in the entry point and uncommon methods behind precise
  conditional links. Avoid duplicating the same rule, evidence or report across
  router, specialist and reference. No fixed document/word quota replaces judgment.
- Make each required checkpoint observable before dependent actions. A completion
  claim needs a check at the relevant seam; a skill-body read only proves loading.
- Use this package's agents/openai.yaml invocation contract and official format
  validators. External runtimes' slash commands and invocation flags are not
  authoritative here. Plugin/skill utilities may supply formats and commands;
  they do not select engineering scope, acceptance criteria or review topology.
- Reuse mechanical checks: validate_package.py rejects a second implicit specialist,
  broken runtime links, package escapes and unregistered named policies. Exercise
  a deliberate invalid mutation when strengthening one of those checks. Natural
  cases establish routing/behavior; string matching does not establish judgment.

For a bounded change, report the decision, focused check and material limit once.
Detailed blockers and pending scope remain explicit. Keep external-source hashes
and rationale in development provenance, not the installed hot path. Never claim
that a shorter instruction or fewer reads prove better end-to-end behavior.
