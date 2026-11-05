# Engineering Harness 0.10.0 — bounded release qualification

Policy version: **0.10.0**. The six-case campaign used frozen source
`6fa21342024d42b55fb6187887b1edde9ee428c3`; the targeted media case used
`713c0b8e8861bb07231837268d03a0e7e812aee7`. Runtime policy and runner files
are byte-identical between those snapshots. Model: `gpt-6-astra`, medium
reasoning, one trial per case/arm; Codex CLI 0.166.0. Both control and installed
harness arms used fresh isolated homes and an empty additional skill catalog.
Platform-provided declarations remain recorded in the private traces.

The [original observations](release-observations.json) and
[targeted media observations](release-media-observations.json) retain immutable
source/input/output identities and observed body reads separately from this
acceptance judgment. Raw transcripts remain private; public digests alone are
not replayable evidence.

## Results and limits

All **14 executions completed** without timeouts, incomplete usage flags or runner
errors. This is an execution count, not a claim that every initial result met
every acceptance criterion. The first replay result left a material proof gap;
the targeted case below closes it while preserving the earlier limitation.

| Scenario | Observed harness outcome |
|---|---|
| Camera borrowing | Analysis closes its subscription while preview retains and finally closes the same camera; scratch lifecycle/re-entry checks pass |
| Replay evidence identity | Versioned canonical JSON binds content hashes and provenance; supported serialization and mutations work; annotations remain separately editable. Initial verification was manifest-only |
| Placement handoff | Generator and CPL corrected; geometry/BOM unchanged; separate drill-setting failure reported. Hardware reference was read; no hardware skill-body read is claimed for this case |
| Prototype readiness | Hardware Engineering and Hardware Qualification bodies read; performance left as an experiment and production acceptance kept separate |
| Minimal CPL correction | Router body read; only the requested field changed |
| Bench plan | Hardware Qualification body read; physical measurements honestly remain NOT MEASURED |
| Actual media reuse | Same-path file corruption rejected with original reference/manifest unchanged; replay verifies and returns the same single read; annotations still editable |

Successful tool outputs establish actual router and specialist-body reads,
including Data and Compatibility in the original replay case. Expected skill
lists are available owners, not mandatory fanout. Control outcomes and their
exact identities remain in the observation files; no statistical improvement,
efficiency benefit or general reliability claim is made from these single trials.

## Referenced-byte proof and independent review

The initial replay checks authenticated the evidence manifest and separately
compared pose/features/events digests. Their media input was a locator/placeholder;
they did **not** verify actual referenced media bytes. Independent review retained
this as **R1-E1**, preventing release acceptance.

The additional fixture supplies an actual consuming path. Both completed model
outputs now hash bytes at capture, load media once at replay, verify raw payload
and media digests against the retained reference/evidence, and return those same
verified bytes. Independent scratch probes, without any reference repair applied,
exercise intact acceptance, same-path byte replacement, raw payload/provenance
mutation, unchanged evidence/reference after rejection, annotation revisions,
exactly one read and missing-file failure. Both outputs pass.

The same fresh read-only reviewer retained its prior source/security review,
verified both actual output hashes, personally ran six tests per targeted output
and the independent probe, and closed **R1-E1 and R1**. Closure packet SHA-256:
`9eba5978ed4faff0c842682181b2323e98c02080cd2b3f7c851f6ed1836a22de`.
The prior manifest-only result is not relabeled as raw-content verification.

## Integration and publication checks

The final candidate runs the complete repository unit suite, package/profile/link
and generated-invariant checks, all 15 official skill validators, and official
CLI local installation/inventory with installed/source byte-hash agreement.
The current CLI exposes no separate plugin-validator command; actual official
CLI loading is the available platform format check. Exact final-source results
are retained in the release handoff before merge/tag publication.

Protected preflight verifies credential/outside/symlink read denials, direct
network denial, proxy rejection, local IPC and browser rendering. It now admits
only the exact native executable and hashes actual installed skill/reference
resources before copying authentication. Earlier `/tmp` visibility failures are
retained as failed setup evidence, not successful model trials.

This qualification establishes bounded synthetic outcomes and artifact integrity.
It does not establish producer authenticity, physical-device behavior, statistical
reliability, or authorization for vendor orders or equipment operation. Stable
publication is separately authorized by the user; immutable tags must match the
plugin manifest and tested runtime. Historical receipts retain their own scope.
