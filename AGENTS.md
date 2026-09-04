# Engineering Harness Repository Rules

- `DESIGN.md` owns package architecture and the authority map.
- `references/invariants.json` owns invariant wording, activation conditions,
  enforcement timing, and normative skill ownership. Regenerate its Markdown
  view after changes.
- `references/capability-activation.json` owns capability vocabulary and
  activation. Repository profiles remain reviewed project decisions.
- The public entry point is `using-engineering-harness`; specialist skills are
  internal explicit-only references selected by that router.
- Changes to invariant meaning, activation, routing, profile interpretation, or
  evidence semantics require the version and migration treatment in
  `references/versioning.md`.
- Run `python3 -m unittest discover -s tests`,
  `python3 scripts/validate_package.py`, and the official plugin and skill
  validators before integration.
- Implementation, integration, tagging, marketplace installation, and public
  release are separate actions. Perform only the scopes the user named.
- Keep public artifacts free of private content, local absolute paths, and
  machine-specific configuration.
