# Today contract and command-boundary correction

Evaluated source: **45af888e65fce5cef7f969c4979352e60e364b91**.
The changes address two review findings without changing runtime routing or skills.

Today previously said weekly averages belonged in the matching metric, settling
its supposed UX decision in advance. Its accepted contract now leaves historical
metric placement unspecified while preserving current metrics, inline scheduled
actions, routes and relative product priority. The rubric remains outcome-based;
there is no reward for unnecessary skill loading.

The previous pilot enabled unrestricted command networking to permit Chromium IPC
while a real authentication file existed in the trial home. Browser DNS flags and
prompt instructions did not fence other commands. That was a material boundary
weakness already present in the prior reviewed snapshot: **an initial-review miss**,
not a newly introduced defect or an excuse to relabel the old environment.

## Corrected boundary

The experience matrix now requires the existing Codex permission profile plus its
managed proxy with no allowed destinations. Commands have default-denied file reads,
with minimal runtime paths, fixture/temp access, and explicit skill/browser reads.
The isolated credential file and other trial records are outside those grants.
Tool environments do not inherit service credentials, and web search is disabled
separately. Codex's authenticated model transport remains outside the command
sandbox; this is not a claim that every client capability is governed by it.

Every trial must pass preflight **before real auth is copied**:

- Synthetic auth, a symlink to it, and an outside-file canary cannot be read.
- Direct HTTP/raw TCP cannot reach a live local sink; proxy HTTP receives 403.
- Local IPC works and Chromium produces an actual screenshot.

All six preflights passed with zero sink connections. No unrestricted fallback is
available, and the runner rejects the old matrix toggle. Unsupported hosts fail
setup and leave evaluation pending. Tests cover profile settings, missing/unsafe
matrix boundaries, and failure before credential copy. The isolated auth copies
were removed after all six executions. The settings tested before install remained
unchanged after execution; plugin registration added unrelated configuration, so
preflight and final whole-config hashes are recorded separately.

These probes establish the exercised command boundary, not exhaustive protocol,
kernel, native-tool, or deployment isolation. The current host uses CLI 0.153.4.
The same boundary applies to both arms. Raw preflight outputs, source/fixture
snapshots and native traces remain retained; [receipt.json](receipt.json) contains
integrity references, outcomes, runtime/input/artifact hashes, diffs and counters.
The retained inventory was pinned on completion and reconciled with the existing
cost-attribution tool; it is not an external execution attestation.

## Focused natural rerun

Six executions: Today, brand, and typo, each once in control and Harness, using
`gpt-6-astra` / medium, fresh homes and unmodified marketplace-installed runtime.
**All six meet the selected required outcomes; no listed forbidden outcome was
observed.** No timeout, setup failure, or incomplete native context occurred.

| Case | What the rerun establishes |
| --- | --- |
| Today | Both agents choose the existing summary after reasoning about another card displacing scheduled actions; compute the average; preserve routes/priority; open actual renders. Harness reads only the router. The fixture contradiction is fixed, but reliable UX-specialist activation is still not established. |
| Brand | Both propose identity, visual intent and voice against accepted design using rendering, without production edits. Harness selects Brand and Language and targeted references. |
| Typo | Both make the local correction without specialist fanout or scope/receipt documents. Rendering remains a bounded fixture-authority requirement. |

All six resulting Node check suites also passed when rerun by the parent. This does
not close the **unrerun accessible-name evidence gap** in the original cohort or
establish complete same-snapshot ten-case equivalence. Original receipts/reports
remain unchanged and describe the older, weaker boundary. This three-case subset
also does not demonstrate a unique Harness quality advantage or broad efficiency.

Native context/integrity reconciliation passed. Both arms used three primary
contexts. Total input was 287,075 Harness / 274,974 control; uncached input
34,659 / 43,422; output 3,404 / 3,041. Per-trial wall times and setup commands are
retained separately. Boundary preflight time is setup cost, not included in the
model-trial wall field; these changed-fixture/environment results are not a direct
before/after efficiency comparison with the original cohort.

Validation on the evaluated source: 93 unit tests, package validator, official
plugin validator, all 13 skill validators, and diff whitespace checks pass. A fresh
independent security/evidence review found no implementation blocker before the
natural rerun. No merge, release, or installed-plugin update is included.
