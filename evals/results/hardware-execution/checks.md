# PCB execution guidance checks

Source candidate `ef33ede21b8b6fb62488b94e39e6603f9dccd82a`, unreleased policy0.11.0.
PCB execution reference SHA-256: `d58f4d13c72ae1174f63f92b0fc4326bb9ff6e2b8bc75f4bfec895467248856a`.
The later change corrects one changelog space and adds this development record;
the tested runtime instructions and fixtures are unchanged.

## Automated checks

- `python3 -m unittest discover -s tests`:145 tests passed.
- `python3 scripts/validate_package.py`:passed.
- Official skill-creator `quick_validate.py` on Hardware Engineering:passed.
- The existing hardware-matrix mutation test rejects removal of the new required
  baseline-execution case, as well as unknown cases and invalid boundaries.
- The available Codex CLI exposes no standalone plugin-validator command. No
  official plugin integration/install test was performed and no user installation
  was modified. Integration/release remains separately authorized.

## Bounded forward probes

Two fresh contexts received the source router path, their isolated synthetic
fixture, and a natural request. They received no builder history, grading outcomes
or other fixtures. These are direct-router content probes, not installed natural
skill-discovery or control/harness comparisons.

| Probe | Observed result | Parent verification |
|---|---|---|
| Baseline execution plan | Rejected the empty session despite exit0/COMPLETED; prioritized the registered pinned candidate/export path, native handback evidence, connector escapes/local returns and constrained routes; selected supported fallback after repeated unproductive repairs; preserved accepted components/outline | All fixture file hashes unchanged; no native execution or physical success claimed |
| Preapproved CPL-only correction | Changed U1 rotation90→180 without a new board/toolchain/architecture campaign | Exactly `cpl.csv` changed, and its text differs only in the requested rotation value |

The baseline fixture has no native CAD or runnable EDA toolchain. The plan's
commands and native checks are prospective. The minimal probe actually edited
only its isolated synthetic CSV. Neither probe qualifies a PCB, installed
routing/discovery, or an improvement in time/cost to complete a real board.

## Independent review

A separate, read-only context reviewed candidate `ef33ede21b8b6fb62488b94e39e6603f9dccd82a` after completing
the minimal probe. It authored none of the changed instructions or fixtures,
inspected scope/evidence/versioning boundaries and matrix mutation coverage,
and independently ran40 focused tests successfully. No blocking finding was
reported. Its one editorial finding, a missing changelog space, is corrected.
There was no broad natural campaign, native CAD run, equipment access, vendor
contact, manufacturing order, installation, tag or release.
