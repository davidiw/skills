# Engineering Harness

Engineering Harness is an owned Codex plugin for making consequential software
changes without imposing distributed-system ceremony on ordinary work. It helps
an agent locate authority, reason about lifetime and contracts, preserve data
and compatibility, and produce evidence appropriate to the actual risk.

It is not a framework, architecture replacement, issue tracker, deployment
system, mandatory document set, or durable-runtime vendor. Repository-specific
instructions and accepted product decisions remain authoritative.

## Four workflows

Use `$using-engineering-harness` and state one of four intents. The router loads
specialist guidance internally; users do not select specialist skills.

### Bootstrap

Use for a new repository or major new subsystem. The harness establishes the
smallest useful authority map, quality scenarios, capability profile, boundary
checks, and verification path. A small project should remain small.

### Adopt

Use for an existing repository. From the Engineering Harness checkout, generate
an evidence-backed proposal:

```bash
python3 scripts/profile_repository.py TARGET_REPOSITORY \
  --output TARGET_REPOSITORY/engineering-harness.json
```

The proposal records confidence and relative evidence paths. Review uncertain
signals, assign real repository enforcement owners, record any approved scoped
exceptions, and change its status to `accepted`. Check later drift with:

```bash
python3 scripts/profile_repository.py TARGET_REPOSITORY \
  --check TARGET_REPOSITORY/engineering-harness.json
```

Discovery proposes; it does not overrule repository decisions or prove a
capability absent. See
[`references/profile-discovery.md`](references/profile-discovery.md).

### Change

Use for normal implementation, fixes, migrations, and refactors. Internal risk
classification activates only the relevant invariants and specialist guidance.
Minimal work stays on the repository's normal focused path; consequential work
adds only the contracts and evidence its execution path requires.

### Harden

Use when incidents, recurring fixes, competing owners, or repeated coordination
guards demonstrate architecture divergence. Hardening consolidates ownership,
repairs the root cause, and prevents recurrence. It is not routine review or a
repository-wide cleanup. Adversarial proof and exact-revision review belong to
verification and operations.

The normative workflow is in
[`skills/using-engineering-harness/SKILL.md`](skills/using-engineering-harness/SKILL.md).

## Capabilities and invariants

[`references/invariants.json`](references/invariants.json) defines the invariant
catalog, each invariant's single normative owner skill, its consumers, and its
enforcement timing. The generated readable view is
[`references/engineering-invariants.md`](references/engineering-invariants.md).

A version-controlled `engineering-harness.json` records project capabilities,
active enforcement, exceptions, discovery evidence, and the harness policy
version. [`references/capability-activation.json`](references/capability-activation.json)
maps capabilities to minimum active invariants.

Cheap deterministic checks normally accompany a declared foundational
boundary. Behavioral, performance, fault, physical, and operational evidence
scales with capability and risk. The harness rejects both missing protection and
speculative infrastructure.

Explicit user intent and repository-authoritative decisions take precedence
over generic recommendations unless an applicable safety constraint prohibits
the action. Conflicts and exceptions are reported rather than silently
rewritten. See
[`references/precedence-and-exceptions.md`](references/precedence-and-exceptions.md).

## Internal skills

The router progressively loads seven internal specialists:

| Skill | Normative responsibility |
| --- | --- |
| `architecture-foundations` | Authority, quality scenarios, ownership, boundaries, and composition |
| `durable-workflows` | Work lifetime, admission, replay, coalescing, fencing, and bounded units |
| `interfaces-and-events` | Independently consumed contracts, event truth, delivery, and boundary types |
| `application-composition` | Shared semantics across runtimes, adapters, UI ownership, and useful paint |
| `data-and-compatibility` | Representations, identity, deletion, migration, repair, and mixed versions |
| `architecture-hardening` | Divergence discovery, consolidation, root-cause repair, and recurrence prevention |
| `verification-and-operations` | Adversarial evidence, fault injection, physical proof, exact revisions, and operations |

These skills meet at execution-path seams but do not share normative ownership
of an invariant. The package authority map is in [`DESIGN.md`](DESIGN.md).

## Design provenance

The package independently synthesizes external engineering workflows and
lessons from repositories we operate. External work contributed harness,
progressive-disclosure, architecture, interface, and hardening techniques. Our
repositories contributed empirical durability, local-first, account, event,
physical-proof, AI-action, compatibility, and operational failure modes.

There is no runtime dependency on those projects and no claim that a skill maps
one-to-one to an upstream source. Exact reviewed revisions, licenses, adopted
influences, and rejected assumptions are in [`SOURCES.md`](SOURCES.md).

## Validation and versioning

The package uses Python 3 standard-library tooling:

```bash
python3 -m unittest discover -s tests
python3 scripts/validate_package.py
python3 scripts/render_invariants.py --check
python3 scripts/validate_profile.py engineering-harness.json
python3 scripts/profile_repository.py . --check engineering-harness.json
```

Structural validation does not claim that model evaluations ran. The behavioral
corpus in [`evals/cases.json`](evals/cases.json) contains both positive controls
and explicit over-engineering failures.

The current policy version lives in [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json).
Release behavior and migration requirements are defined in
[`references/versioning.md`](references/versioning.md) and recorded in
[`CHANGELOG.md`](CHANGELOG.md).

The package remains unlicensed (`UNLICENSED`) until public distribution terms
are selected.
