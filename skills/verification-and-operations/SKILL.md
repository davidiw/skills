---
name: verification-and-operations
description: Build or apply exact-revision verification and guarded operational workflows. Use for acceptance gates, test matrices, benchmarks, release evidence, machine preflight, generated artifacts, physical validation, migrations, live repairs, deployment, installation, publication, or rollback; not for ordinary focused unit testing alone.
---

# Verification and Operations

Make claims reproducible and external actions explicit without replacing a
repository's existing command system.

## Workflow

1. Discover the repository's operator interface, toolchain pins, machine
   capability checks, release source, and authorization model. Extend that path
   instead of adding an orphan script or second deployment route.
2. Convert each release-relevant behavior into an acceptance contract with
   implementation, automated evidence, physical/external evidence, and
   release-gate status kept separate.
3. Select proof by risk and owning seam: deterministic policy tests, boundary
   fixtures, fault/replay tests, mixed-version tests, performance campaigns,
   generated-artifact checks, and physical observations only where needed.
4. Bind executed evidence to clean exact revision, command/harness, timestamp,
   environment and device where relevant, discovered/completed/skipped counts,
   result, and immutable artifact or transcript digest. Zero discovered tests
   and skipped required tests are failures.
5. Keep secrets and private content out of commands, logs, prompts, receipts,
   screenshots, and artifacts. Record bounded allowlisted metadata.
6. Separate plan from effect. Implementation, integration, release metadata,
   deployment, installation, migration, repair, publication, and rollback each
   require the authority defined by the repository or user.
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
for generated or real-world outputs.

The operation is complete only when the requested action, exact target, result,
and remaining unproven evidence classes are explicit. Successful code or tests
never imply deployment or physical proof.
