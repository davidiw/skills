---
name: verification-and-operations
description: Build or apply adversarial, fault, physical, exact-revision, and operational verification. Use for engineering methodology, evidence standards, shared test/review infrastructure, acceptance gates, benchmarks, release evidence, generated artifacts, migrations and external operations; not for ordinary focused unit testing alone.
---

# Verification and Operations

Own exact evidence, independent campaigns and authorized external operations,
not ordinary focused unit tests. Use repository commands and relevant
[invariants](../../references/invariants.json); avoid a parallel operator system.

For an unresolved failure, use [diagnosis](references/diagnosis.md); for a generic
code review, use [change review](references/change-review.md). These methods may
be read directly without loading this skill.

1. For reusable methodology or performance acceptance, first read
   [methodology ownership](references/methodology.md) and locate its registered
   repository policy. Bind requested acceptance to source, toolchain, environment and authorized
   actions. Separate implementation, automated proof and physical/external proof.
2. Select proof at the actual failure seam: deterministic, replay/fault,
   mixed-version, performance or physical evidence as warranted. For constrained
   resources, test [resource governance](../architecture-foundations/references/runtime-resource-governance.md)
   including admission, incumbent-writer progress, cleanup and restart fallback.
3. Record the snapshot, command, counts, result and retained evidence under
   [evidence contract](references/evidence-contract.md). Skipped required tests or
   zero discovered tests cannot pass; generator freshness is a different claim.
4. For external mutations, read [operator interface](references/operator-interface.md):
   exact target, current preflight, bounded compare-and-set/lease action and
   recovery artifact. Reuse explicit action approval; no implementation result
   implies deployment, tagging, installation or publication authority.
5. Before final branch review/integration, apply [reviewable commits](references/reviewable-commits.md).
   Refresh affected evidence after changes and bind final gates to the required
   revision. Keep private payloads/secrets outside public artifacts.

For generated/physical output, read [artifact proof](references/artifact-and-physical-proof.md).
For a required independent high-risk audit, read [adversarial review](references/adversarial-review.md).
For release policy semantics, read [versioning](../../references/versioning.md).
Security/privacy review uses the [assurance handoff](../../references/assurance-handoff.md),
not another verification load solely to summon reviewers. Done means the exact
claim, target, result and unproven classes are explicit. Apply
[precedence](../../references/precedence-and-exceptions.md) for workflow conflicts.
