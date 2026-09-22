# Repository-owned engineering methodology

Use for changes to evidence standards, shared testing infrastructure, review or
safety/compatibility policy, reusable Harness behavior, and performance acceptance.
Ordinary product fixes and focused unit tests do not require this workflow.

Read `engineering-harness.json` sources and relevant enforcement entries, then
inspect the canonical policy, command/help and necessary tests. Consult existing
`docs/agents/` pointers when present; a product design document alone need not
contain the testing contract. If registration is absent, search the repository's
specs/scripts and report the gap rather than assuming no policy exists.

For a demonstrated reusable lesson, reconcile one short record:

- canonical policy/owner and when it applies;
- existing profile `sources` pointer and relevant invariant's enforcement entry;
- actual enforcement rung and command/artifact that establishes it;
- deliberately failing check and behavioral eval/evidence, or an explicit TODO.

Use existing `sources` keys (arbitrary repository-specific names are supported)
and `enforcement` owner/artifacts. Name policy sources descriptively, e.g.
`performance_evidence` or `testing_policy`; do not copy their thresholds into
skills or invent an invariant merely to register a procedure. Reference the
canonical policy from the relevant existing enforcement entry. Keep one owner;
registration, a script's existence, and successful execution are different facts.

The installed profile helper can audit known policy locations and named seams:

```bash
python3 scripts/profile_repository.py /path/to/repository \
  --audit-methodology /path/to/repository/engineering-harness.json \
  --policy docs/your-policy.md
```

Run from the plugin root, substitute the actual path, or omit `--policy` for
standard policy locations. The audit reports missing registration, ownership,
references and circular explicit-invocation pointers; it never runs repository
commands. It is a bounded detector, not proof that all methodology was found.
Verify the owning check separately under the task's execution authorization.

For performance claims, read the owning acceptance rule before concluding:
**admitted sample → measured result → qualified optimization → integration/release**
are separate decisions. A clean pair can be promising without satisfying required
repetition, order, environment, provenance or success criteria. Preserve failures
and incomplete attempts. A full qualifying packet may pass: do not invent an
extra repetition or statistical requirement. Use the repository comparator and
its limits; a successful diagnostic command need not mean formal acceptance.

Keep product work and system learning in coherent slices. Finish or pause the
product slice with its evidence and outstanding gates. Propose adjacent system
work separately; a lesson does not authorize editing skills, changing acceptance
rules, or expanding the product PR. When system work is authorized, establish its
owner → registration → executable check → eval/evidence, recording gaps honestly.
Return to the product slice against its actual revision and existing acceptance
rules; a Harness update never upgrades old evidence or waives a pending gate.

For reusable execution coordination, the canonical generic workflow is the
[builder checkpoints](../../../references/change-classification.md), not a
parallel delegation policy. Keep architecture and unresolved authority with the
coordinator; reuse the existing task/review packet for executable checks and
assurance handoffs. A long command is a worker assignment when a capable worker is
available, and unavailable delegation remains an evidence limit rather than a
fictional launch.
