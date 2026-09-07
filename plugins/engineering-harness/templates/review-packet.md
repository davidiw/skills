# Review Packet

Keep the launch receipt separate from the packet: record its final path/hash,
actual child identity, fresh-context/no-history evidence, role/launcher, model,
effort and sandbox. Record assignment visibility limitations; do not describe an
opaque payload as inspected. Do not put a self-referential checksum inside the packet.

## Neutral handoff from builder

- Exact source: {commit plus worktree diff/file hashes, with source locations}
- Comparison base: {full SHA; complete branch diff/commit sequence for integration}
- Requested outcome and acceptance criteria: {observable requirements}
- Scope and non-goals: {permitted surface and exclusions}
- Authoritative contracts: {relevant repository sources and approved limits}
- Already-executed evidence: {commands, results, snapshot and artifact locations}
- Permitted review actions: {read-only production inspection; bounded synthetic checks}
- Reviewer entry points and context: {exact skill paths, fresh reviewer role and
  actual no-history spawn setting; do not rediscover the router}
- Required review lenses/gates: {only those selected by policy/request}
- Prior review receipt: {for correction review; prior snapshot and coverage limits}
- Correction delta: {changed paths and directly affected seams; none on first pass}

Exclude builder reasoning, design justifications, expected findings and persuasive
conclusions. Use the [fresh-context handoff](../references/assurance-handoff.md).

## Reviewer handback

- Reviewed exact snapshot and evidence used: {commit/digests, commands and artifacts}
- Context status: {fresh independent context and separation evidence, or self-review}
- Complete currently known blockers: {each severity, confidence, path and evidence}
- Non-blocking follow-ups: {bounded observations}
- Explicitly unreviewed/unavailable areas: {coverage gaps and reasons}
- Correction findings: {new regression / unresolved blocker / initial-review miss;
  cite the prior snapshot and whether that area was previously covered}
- Gate disposition: {satisfied / pending with remaining obligation}

Delta review covers corrections, affected seams and introduced regressions. Reopen
unchanged scope only for expanded scope, invalidated assumptions or newly reachable
surfaces. A rewritten commit changes the exact revision; bind subsequent review
and evidence to that revision without claiming older receipts prove it.
