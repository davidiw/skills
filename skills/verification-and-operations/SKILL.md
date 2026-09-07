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
4. Bind executed evidence to an identifiable source snapshot, command/harness, timestamp,
   environment and device where relevant, discovered/completed/skipped counts,
   result, and artifact or transcript digest when a gate requires one. Local
   checks may name a commit plus worktree patch/content digests; a clean exact
   revision is required when repository integration or release policy says so.
   Zero discovered tests and skipped required tests are failures when the
   command is a test suite, not for a generator freshness check.
5. Keep secrets and private content out of commands, logs, prompts, receipts,
   screenshots, and artifacts. Record bounded allowlisted metadata.
6. Record action scopes and apply the authorization and reuse semantics in
   [`precedence-and-exceptions.md`](../../references/precedence-and-exceptions.md).
7. For shared or irreversible writes, preflight current state, show the exact
   target and revision, use compare-and-set or lease protection, bound the
   action, and preserve a recovery artifact.
8. After source, dependency, or generated output changes, refresh evidence for
   affected claims at the smallest sufficient scope. A metadata-only commit
   does not invalidate unchanged content evidence; bind release gates to their
   required revision.

For consequential alterations to trust/authorization or privacy-lifecycle semantics, use
the relevant `security-assurance` and/or `privacy-assurance` reviewer under
[`assurance-review.md`](../../references/assurance-review.md). These reviewers
may discover material defects outside the invariant catalog. They own threat
review; this skill owns evidence and release-gate semantics. Do not load this
skill solely to invoke a focused assurance reviewer.

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
