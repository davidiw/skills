# Compact-first milestone guidance checks

Base: `29990c0`; unreleased 0.11.0 refinement. The narrow change follows the
owner's current envelope/cost/schedule priorities, requires a tangible next
deliverable, closes completed milestones, and prepares specific physical/external
owner tasks. Additional paid builds need a named learning purpose. No new
framework, invariant, activation or mandatory review campaign is introduced.

Before publication:

- `python3 -m unittest discover -s tests`: **147 passed**.
- `python3 scripts/validate_package.py`: **passed**.
- Official skill-creator `quick_validate.py` for Hardware Engineering: **passed**.
- `git diff --check`: **passed**.

No independent behavioral probe was added for this small guidance refinement;
prior probes retain their original scope. Tests/format validation do not prove
compact fit, faster execution or hardware correctness. No standalone official
plugin-validator command is available in the installed CLI.

Tested content SHA-256:

- `plugins/engineering-harness/skills/hardware-engineering/references/pcb-execution.md`: `e0ebbc78b62efb2561fbacf31f6ad03b97129afecbf4eeceb9d4db9c71bce671`
- `plugins/engineering-harness/skills/hardware-engineering/references/manufacturing-handoff.md`: `df8579125d8ff2368c7190210d1d0f07358bd62a50d60d28d856d4b2e5d3fdca`
- `CHANGELOG.md`: `b9b4f127824adbd52a6440ebc4269d49ea2d4c465d557f741c64bf2ea07a106f`

PR is ready for review/integration; release/tagging/installation and Mera adoption
remain separate actions. v0.11.0 is not released and Mera retains v0.10.0.
