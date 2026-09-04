---
name: verification-and-operations
description: Build or apply adversarial, fault, physical, exact-revision, and operational verification. Use for acceptance gates, high-risk audits, benchmarks, release evidence, generated artifacts, migrations, live repairs, deployment, installation, publication, or rollback; not for ordinary focused unit testing alone.
---

# Verification and Operations

Make claims reproducible and external actions explicit without replacing a
repository's existing command system.

Use the [invariant catalog](../../references/invariants.json) as normative.
Interpret only entries whose `owner_skill` names this skill; consume other
entries without redefining them.

## Workflow

1. Discover the repository's operator interface, toolchain pins, machine
   capability checks, release source, and authorization model. Extend that path
   instead of adding an orphan script or second deployment route.
2. Convert each release-relevant behavior into an acceptance contract with
   implementation, automated evidence, physical/external evidence, and
   release-gate status kept separate.
3. Own proof selection by risk and owning seam: deterministic policy tests, boundary
   fixtures, fault/replay tests, mixed-version tests, performance campaigns,
   generated-artifact checks, and physical observations only where needed.
   For constrained runtime resources, test the declared admission reserve,
   cooperative stop deadline, cleanup evidence, retry bound, and restart
   fallback from the authoritative
   [`runtime resource contract`](../architecture-foundations/references/runtime-resource-governance.md).
4. Bind executed evidence to clean exact revision, command/harness, timestamp,
   environment and device where relevant, discovered/completed/skipped counts,
   result, and immutable artifact or transcript digest. Zero discovered tests
   and skipped required tests are failures.
5. Keep secrets and private content out of commands, logs, prompts, receipts,
   screenshots, and artifacts. Record bounded allowlisted metadata.
6. Record action scopes and apply the authorization and reuse semantics in
   [`precedence-and-exceptions.md`](../../references/precedence-and-exceptions.md).
7. For shared or irreversible writes, preflight current state, show the exact
   target and revision, use compare-and-set or lease protection, bound the
   action, and preserve a recovery artifact.
8. After any commit, rebase, generated output change, or corrected blocker,
   invalidate stale evidence and review the new exact revision at the smallest
   sufficient scope.

Read [`evidence-contract.md`](references/evidence-contract.md) when building a
gate, [`operator-interface.md`](references/operator-interface.md) for commands
that mutate external state, and
[`artifact-and-physical-proof.md`](references/artifact-and-physical-proof.md)
for generated or real-world outputs. For a repository-mandated high-risk audit,
read [`adversarial-review.md`](references/adversarial-review.md). When evidence
must identify policy semantics across package releases, read
[`versioning.md`](../../references/versioning.md).

Before stopping work or changing the requested workflow, apply that precedence
policy and name the exact rule.

The operation is complete only when the requested action, exact target, result,
and remaining unproven evidence classes are explicit. Successful code or tests
never imply deployment or physical proof.
