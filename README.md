# Engineering Harness

Engineering Harness is an owned Codex plugin for making consequential software
changes without imposing distributed-system ceremony on ordinary work. It helps
an agent locate authority, reason about lifetime and contracts, preserve data
and compatibility, and produce evidence appropriate to the actual risk.

It is not a framework, architecture replacement, issue tracker, deployment
system, mandatory document set, or durable-runtime vendor. Repository-specific
instructions and accepted product decisions remain authoritative.

The repository includes a Codex marketplace at
`.agents/plugins/marketplace.json`. Adding this repository as a marketplace
exposes the `plugins/engineering-harness/` runtime plugin for installation.

## Install

Install the immutable **0.5.0** stable release:

```bash
codex plugin marketplace add davidiw/skills --ref v0.5.0
codex plugin add engineering-harness@davidiw-skills
```

Use `--ref main` only for deliberate development/nightly testing. Evidence and
repository profiles name the harness policy version they used; stable tags are
immutable.

For local development, pass the checkout root containing
`.agents/plugins/marketplace.json`; the marketplace selects the runtime subdirectory:

```bash
codex plugin marketplace add /path/to/skills-checkout
codex plugin add engineering-harness@davidiw-skills
```

## Four workflows

Ordinary natural requests enter `change` through the public router
automatically. Invoke `$using-engineering-harness` when explicitly asking to
bootstrap, adopt, harden, or diagnose routing. The router loads specialist
guidance internally; users do not select specialist skills.

### Bootstrap

Use for a new repository or major new subsystem. The harness establishes the
smallest useful authority map, quality scenarios, capability profile, boundary
checks, and verification path. A small project should remain small.

### Adopt

Use for an existing repository. From the Engineering Harness checkout, generate
an evidence-backed proposal:

```bash
python3 plugins/engineering-harness/scripts/profile_repository.py TARGET_REPOSITORY \
  --output TARGET_REPOSITORY/engineering-harness.json
```

The proposal records confidence and relative evidence paths. Review uncertain
signals, assign real repository enforcement owners, record any approved scoped
exceptions, and change its status to `accepted`. Check later drift with:

```bash
python3 plugins/engineering-harness/scripts/profile_repository.py TARGET_REPOSITORY \
  --check TARGET_REPOSITORY/engineering-harness.json
```

Discovery proposes; it does not overrule repository decisions or prove a
capability absent. See
[`plugins/engineering-harness/references/profile-discovery.md`](plugins/engineering-harness/references/profile-discovery.md).

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

For a named flow or diff, security/privacy assurance stays on the changed path.
For pre-launch or external security/privacy readiness, the same reviewers use
release-wide inventory and coverage matrices, including unchanged and legacy
surfaces. Merely preserving an existing authorization fence or working in a
sensitive repository does not activate an independent assurance review.

The normative workflow is in
[`plugins/engineering-harness/skills/using-engineering-harness/SKILL.md`](plugins/engineering-harness/skills/using-engineering-harness/SKILL.md).

## Capabilities and invariants

[`plugins/engineering-harness/references/invariants.json`](plugins/engineering-harness/references/invariants.json) defines the invariant
catalog, each invariant's single normative owner skill, its consumers, and its
enforcement timing. The generated readable view is
[`plugins/engineering-harness/references/engineering-invariants.md`](plugins/engineering-harness/references/engineering-invariants.md).

A version-controlled `engineering-harness.json` records project capabilities,
active enforcement, exceptions, discovery evidence, and the harness policy
version. [`plugins/engineering-harness/references/capability-activation.json`](plugins/engineering-harness/references/capability-activation.json)
maps capabilities to minimum active invariants.

Cheap deterministic checks normally accompany a declared foundational
boundary. Behavioral, performance, fault, physical, and operational evidence
scales with capability and risk. The harness rejects both missing protection and
speculative infrastructure.

Explicit user intent and repository-authoritative decisions take precedence
over generic recommendations unless an applicable safety constraint prohibits
the action. Conflicts and exceptions are reported rather than silently
rewritten. See
[`plugins/engineering-harness/references/precedence-and-exceptions.md`](plugins/engineering-harness/references/precedence-and-exceptions.md).

## Internal skills

The router progressively loads nine internal specialists:

| Skill | Normative responsibility |
| --- | --- |
| `architecture-foundations` | Authority, quality scenarios, ownership, boundaries, and composition |
| `durable-workflows` | Work lifetime, admission, replay, coalescing, fencing, and bounded units |
| `interfaces-and-events` | Independently consumed contracts, event truth, delivery, and boundary types |
| `application-composition` | Shared semantics across runtimes, adapters, UI ownership, and useful paint |
| `data-and-compatibility` | Representations, identity, deletion, migration, repair, and mixed versions |
| `architecture-hardening` | Divergence discovery, consolidation, root-cause repair, and recurrence prevention |
| `verification-and-operations` | Evidence semantics, fault injection, physical proof, exact revisions, and operations |
| `security-assurance` | Authorization and trust threats, including defects outside the invariant catalog |
| `privacy-assurance` | Sensitive data use, derivation, retention, expiry, erasure, and delayed writers |

Implementation specialists own product invariants. Assurance reviewers consume
them and may identify additional evidenced security/privacy obligations. The package authority map is in [`DESIGN.md`](DESIGN.md).

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
python3 plugins/engineering-harness/scripts/validate_profile.py engineering-harness.json
python3 plugins/engineering-harness/scripts/profile_repository.py . --check engineering-harness.json
```

Structural validation does not claim that model evaluations ran. The behavioral
corpus in [`evals/cases.json`](evals/cases.json) contains both positive controls
and explicit over-engineering failures.

The current policy version lives in [`plugins/engineering-harness/.codex-plugin/plugin.json`](plugins/engineering-harness/.codex-plugin/plugin.json).
Release behavior and migration requirements are defined in
[`plugins/engineering-harness/references/versioning.md`](plugins/engineering-harness/references/versioning.md) and recorded in
[`CHANGELOG.md`](CHANGELOG.md).

Engineering Harness is available under the
[`BSD-3-Clause`](LICENSE) license.
