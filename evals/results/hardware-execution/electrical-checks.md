# Electrical-review guidance: bounded checks

Candidate: unreleased Hardware Engineering 0.11.0 on top of skills PR #15 at
`85a970b`. The fixture extracts a prior native/netlist snapshot from
`davidiw/mera-hardware` commit `2520213`, not the current board. The review-fixture
aggregate SHA-256 is
`f833a5ffb985a9e53146706b297c3171423350f4844d69db8ad0bf277998ec92`.
The hash is computed over sorted relative paths, each followed by NUL, file bytes
and NUL. The two-footprint PCB extract is not a complete native board.

## Automated checks

- `python3 -m unittest discover -s tests`: **147 passed**.
- `python3 scripts/validate_package.py`: **passed**.
- Official skill-creator `quick_validate.py` on Hardware Engineering: **passed**.
- Local KiCad/pcbnew 10.0.7 loaded the two-footprint native PCB extract.
- The fixture test checks actual component identities, relevant netlist nodes,
  active-device passive roles and the zero-finding historical ERC receipt.
  It also shows the local placement check fails at 63.19 mm and passes for a
  nearby nonoverlapping fixture position. These are fixture assertions, not a
  claim that the full board or an agent's output passed native ERC/DRC.
- The available Codex CLI exposes no standalone official plugin-validator
  command; no official plugin integration/install check was performed.

## Fresh direct-skill probes

Neither probe received the case's expected outcomes or a prior reviewer
conclusion. These test the requested skill's content under explicit loading;
they are not installed-versus-control, natural-discovery or reliability trials.

| Probe | Result |
|---|---|
| Read-only electrical review | Fresh `reviewer` context inspected the local KiCad sheets, netlist, PCB extract, historical ERC and manufacturer facts. It identified the six-hour charger timer versus 100 mA / 1,800 mAh conflict, the PG-to-unpowered-USB path, the remote bypass, and the passive-only active symbols. It did not claim physical measurements or new ERC/DRC. The fixture hash matched before/after. |
| Bounded local edit | A separate fresh `worker` context received a disposable copy and the unmodified natural request. It moved only C106 from `(25.5, 68)` to `(6.4, 7.25, 180°)` and ran the fixture check, which passed at 2.61 mm center spacing. The only file difference was that footprint placement. It stated that routes and full-board clearance were not checked. |

The reviewed circuit fixture intentionally supplies a concise offline extract of
manufacturer facts and a scoped mechanism question. It does not establish
performance with a complete datasheet, an installed competing skill catalog, a
fresh production PCB, or a control arm. No model trial, physical test, or
supplier interaction is implied by the structural validation alone.
