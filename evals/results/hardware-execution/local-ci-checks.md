# Local CI publication guidance: local pre-publication checks

Tested source commit: `23032a5d7214a484366c6eaa43b00df66a24297a`.
Before pushing the candidate to PR #15:

- `python3 -m unittest discover -s tests`: **147 passed**.
- `python3 scripts/validate_package.py`: **passed**.
- Official skill-creator `quick_validate.py` for Hardware Engineering and
  Verification and Operations: **both passed**.
- `git diff --check`: **passed**. No standalone official plugin-validator
  command is available in the installed Codex CLI.

One fresh read-only direct-skill probe received only the synthetic local-CI
fixture and the Hardware Engineering skill. It selected both applicable local
board and firmware gates on the final candidate, treated the other revision's
passes as historical, and did not invent a hosted workflow or billing gate. It
performed no checks or publication in the planning fixture. The tested fixture
aggregate SHA-256 is
`7510e38e833fa3095e1f808953b94093126ab079be7ec64e329ed9297a88bed8`, over
sorted relative paths followed by NUL, file bytes and NUL. Hardware execution
guidance and the fixture were unchanged between that probe and tested source
`23032a5`; the subsequent general verification guidance was not separately
forward-tested by that probe.

These are local checks of the skills package and a single direct-skill probe;
they do not establish installed natural discovery, control-arm performance,
current hardware-board results, a hosted check, or physical qualification. The
subsequent receipt-only commit records this evidence without changing tested
runtime instructions, fixtures or tests.
