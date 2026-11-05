# Hardware skill checks — 2026-11-04

Source candidate `2ced9d263530fe40183f95dddaea28edd79b9d0e`, unreleased policy
0.10.0. The [receipt](checks.json) retains the check results,
source identities, fixture/output file hashes and validation limits. This is a
bounded development check, not a stable-release qualification campaign.

## Executed checks

- Full repository unit suite: **141 passed**.
- Package validator: **passed**.
- Official skill-creator validation of both new skills: **passed**.
- Codex CLI 0.166.0 temporary plugin installation: **passed**; exactly one runtime
  was installed, with all runtime file hashes matching the source. The temporary
  installation was removed; the user's installed plugin was not changed. A
  separate official plugin-validator command was not available in this CLI;
  actual CLI installation and the repository package validator were exercised.

An independent fresh read-only reviewer inspected all 39 initially changed files
at `1872267778aa609ee426214c77b8d8c23948db68`, verified the neutral packet's
file hashes, and personally reran the package validator and three hardware
fixture tests. No blocker was found. One P3 identified `hardware-narrow-cpl`'s
`bounded` expectation as inconsistent with its minimal route. The one-line
correction at `2ced9d263530fe40183f95dddaea28edd79b9d0e` received a delta review:
**closed, no known findings**. The reviewer did not review the forward probes
or independently rerun unrelated validation families.

## Direct-router forward probes

Three fresh worker contexts received only the explicit runtime router path,
their isolated target fixture and its natural task. They had no builder-history
fork, other fixtures, grading outcomes or network/vendor/equipment permissions.
Source-router invocation was explicit; these are content/proportionality probes,
not evidence of installed natural discovery. File comparisons were performed
afterward against the original fixtures.

| Probe | Observed outcome | File comparison |
|---|---|---|
| Placement generator | Corrected U1 from 90° to 180°, regenerated CPL, reported the independent 0.30/0.25-mm job mismatch and exact handoff | Only generator and CPL changed; geometry, BOM and job snapshot identical |
| Preapproved local CPL edit | Changed the requested field, disclosed that future generation could overwrite it, kept the requested boundary | Only CPL changed |
| Read-only bench plan | Identified missing duty-cycle/threshold/instrument facts, described prospective current/transient/runtime measurements and labeled them NOT MEASURED | No fixture files changed |

The generator probe's existing aggregate check still failed on the separate
job-drill mismatch, as reported by the worker and reproduced afterward. That is
not recorded as a passing whole-board check. All data are synthetic, and no live
job or hardware was used.

## Installed natural campaign limitation

The existing runner requested four cases with both control/harness arms on frozen
source `1872267778aa609ee426214c77b8d8c23948db68`. The initial eight setups
stopped on an incorrect Chromium executable path. After correcting that external
setting, all eight retry setups stopped at protected sandbox preflight: bwrap
could not execute the current Codex native binary. The runner stopped before
copying real authentication or starting model trials. Both attempts were retained
privately; no sandbox restriction was relaxed to obtain a result.

**Zero model executions completed in that campaign.** Natural discovery,
installed/control benefit and whole-cohort reliability remain **NOT MEASURED**.
The successful temporary installation above establishes package loading only.
The three direct-router probes establish their stated bounded outcomes only.
