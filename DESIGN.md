# Engineering Harness Design

## Objective

Provide one coherent, framework-neutral package that helps coding agents make
consequential application changes safely while leaving simple work simple.

The internal reasoning order is:

```text
authority -> lifetime -> contracts -> composition -> data evolution
          -> enforcement -> exact evidence -> authorized operation
```

The public workflow is only `bootstrap`, `adopt`, `change`, or `harden`.
Specialist selection and `minimal`, `bounded`, `consequential`, or
`stabilization` classification are internal routing details.

## Authority map

Each kind of package fact has one normative source. Other files are consumers,
generated views, examples, or tests.

| Concern | Normative source | Consumers or derived artifacts |
| --- | --- | --- |
| Package architecture and this authority map | `DESIGN.md` | `README.md` overview |
| Repository-local execution and publication rules | `AGENTS.md` | Agent sessions in this repository |
| Public workflow | `plugins/engineering-harness/skills/using-engineering-harness/SKILL.md` | README examples and plugin prompts |
| Internal classes, scope-expansion approval, and specialist routing | `plugins/engineering-harness/references/change-classification.md` | Router skill and eval expectations |
| Invariant statement, activation condition, timing, default rung, and single owner skill | `plugins/engineering-harness/references/invariants.json` | Generated invariant Markdown, profiles, skills, and validators |
| Enforcement timing and rung semantics | `plugins/engineering-harness/references/enforcement-ladder.md` | Invariant assignments, profiles, and validators |
| Capability vocabulary and capability-to-invariant activation | `plugins/engineering-harness/references/capability-activation.json` | Profiles, schema, discovery, and validators |
| Profile shape | `plugins/engineering-harness/references/project-profile.schema.json` | Profile validator and templates |
| A project's accepted capability and enforcement decisions | That project's `engineering-harness.json` | Drift checks and change routing |
| Discovery detectors and confidence | `plugins/engineering-harness/scripts/profile_repository.py` | Proposed profile discovery section |
| Security/privacy review evidence, open-world findings, and coverage | `plugins/engineering-harness/references/assurance-review.md` | Security and privacy assurance skills |
| Skill name and discovery description | Each `SKILL.md` frontmatter | Plugin discovery |
| Skill UI presentation and invocation policy | That skill's `agents/openai.yaml` when present | Codex UI and invocation behavior |
| Marketplace identity, runtime plugin source, and install policy | `.agents/plugins/marketplace.json` | Codex marketplace discovery |
| Eval scenario and expected routing | `evals/cases.json` | Corpus validator and runs |
| Directional natural-prompt selection | `evals/behavioral-matrix.json` | Behavioral runs and receipts |
| Eval scoring | `evals/rubric.md` | Evaluation runs |
| Generated invariant rendering | `scripts/render_invariants.py` | `plugins/engineering-harness/references/engineering-invariants.md` |
| Package structural validation entrypoint | `scripts/validate_package.py` | Delegated validators and unit tests |
| Profile cross-source semantic validation | `plugins/engineering-harness/scripts/validate_profile.py` | Profile discovery, package validation, and unit tests |
| Package version | `plugins/engineering-harness/.codex-plugin/plugin.json` | Profiles, receipts, and changelog checks |
| Release history and migration notes | `CHANGELOG.md` | Adopters and reviewers |
| Design provenance | `SOURCES.md` | README summary |
| Instruction precedence, exceptions, and authorization reuse | `plugins/engineering-harness/references/precedence-and-exceptions.md` | Router and specialist pointers |

Templates are non-normative starting points. Fixtures are isolated repository
facts for their eval case. Neither can override the authorities above.

## Install boundary

The marketplace installs only `plugins/engineering-harness/`. That directory owns
runtime skills, references, templates, the manifest, license, and the profile
scanner/validator consumed by adoption. Runtime file links stay within it.
Repository rules, architecture/provenance, generators, package validators, tests,
evaluation fixtures, expected outcomes, and evidence stay outside the install
source. Legacy root `.codex-plugin/`, `skills/`, `references/`, and `templates/`
are forbidden so the runtime remains the sole policy owner. Root `scripts/`
continues to own repository generators and validators. The package validator
checks both boundaries, including nested corpus folders and symlinks; installation checks compare the unmodified cache with the
runtime source. Historical receipts retain their original layouts and hashes.

## Skill boundaries

The router plus twelve specialists remain separate because they answer different
questions:

| Skill | Question it owns |
| --- | --- |
| `architecture-foundations` | Who owns the fact and what is the system shape? |
| `durable-workflows` | What must remain true when work outlives its caller? |
| `interfaces-and-events` | What can an independently evolving consumer rely on? |
| `application-composition` | How do runtimes and presentation reach canonical behavior? |
| `data-and-compatibility` | How do representations and deployed consumers evolve safely? |
| `architecture-hardening` | Where has ownership diverged, and how is the root cause consolidated? |
| `verification-and-operations` | What evidence proves the claim, and which external action is authorized? |
| `security-assurance` | Can the changed path violate trust or authorization, including threats absent from the catalog? |
| `privacy-assurance` | Does sensitive data retain its purpose, lifecycle, and erasure obligations through every changed representation? |
| `product-experience` | What job, flow, information priority and recovery make sense to the user? |
| `interface-design` | Does the rendered interface express accepted intent clearly and accessibly? |
| `brand-and-language` | What identity/visual intent is proposed or accepted, and how is it expressed in naming and language? |

Experience owners add judgment without owning new engineering invariants.
[Experience routing](plugins/engineering-harness/references/experience-routing.md)
selects one unresolved decision; the existing scope checkpoint governs expansion.
Brand and Language owns identity/visual intent at the proposal and accepted-contract
level; Interface Design applies that intent in composition. Project-specific taste
stays in repository design authority. Normative accessibility/platform facts come
from primary platform sources. [Rendered evidence](plugins/engineering-harness/skills/interface-design/references/rendered-evidence.md)
is proportional: ordinary bounded work needs relevant observations, while retained
or gated evidence uses the existing integrity/receipt contract.

Every invariant names exactly one normative owner skill. A consuming skill may
apply that invariant at its seam but does not reinterpret it. Architecture
hardening owns discovery and repair of divergence; verification and operations
owns evidence semantics, bounded architecture audits, fault campaigns, and
release gates. Security and privacy assurance own threat review, including
evidenced defects outside the catalog; implementation owners retain authority
over product behavior. Each assurance reviewer has changed-path and release-wide
modes. Release modes begin with attack-surface or data-lifecycle inventories,
then reconcile evidence and uncovered rows beyond the latest diff. The
`open-world-assurance` entry records a review-policy obligation; additional
workflow instructions remain in their owning references rather than becoming
catalog entries.

## Execution roles and skill policy

Custom-agent roles select execution context, model/reasoning and permissions for
a narrow mandate. They do not own engineering policy. The runtime's independent
handoff prefers a configured general reviewer and otherwise uses a fresh generic
context; it never requires a user's agent inventory. Applicable review skills load
inside that context. Optional role examples live at repository-level
`examples/agents/`, outside the install boundary. Skills retain scope, invariants,
assurance methods, evidence and review-convergence semantics.

## Proportional activation

Profiles activate invariants implied by actual capabilities plus additional
repository choices. Discovery proposes a profile from bounded evidence; a human
or repository-authorized agent reviews it before acceptance. The normative
discovery and drift rules are in
[`profile-discovery.md`](plugins/engineering-harness/references/profile-discovery.md). Enforcement timing
and exception requirements are defined by
[`enforcement-ladder.md`](plugins/engineering-harness/references/enforcement-ladder.md) and
[`precedence-and-exceptions.md`](plugins/engineering-harness/references/precedence-and-exceptions.md).

## Precedence and authorization

[`precedence-and-exceptions.md`](plugins/engineering-harness/references/precedence-and-exceptions.md) is the
normative policy for safety precedence, repository decisions, scoped invariant
exceptions, workflow-changing disclosures, and reuse of multi-stage authority.

## General contracts before adapters

Workflow engines, queues, mobile schedulers, transactional outboxes, SQLite
journals, provider APIs, UI controllers, and hardware ports are possible
adapters. None defines the generic contract. A skill first establishes
authority, lifetime, failure, and evidence, then selects the smallest
repository-supported implementation.

## Evaluation strategy

Structural validation checks manifests, frontmatter, invocation policy, all
relative links, profiles, generated documentation, source pins, version
alignment, public-path hygiene, and corpus shape. Behavioral evaluation tests
routing, required outcomes, and prohibited overreach against isolated fixtures.

Over-engineering is a first-class failure. Negative controls cover a parser,
library, static site, and CLI where the correct result omits durable runtimes,
events, state machines, repositories, compatibility programs, architecture
documents, and extra operational infrastructure. Positive controls retain
durability, replication, compatibility, UI ownership, providers, constrained
runtime resources, and physical proof.

Runs remain comparable only when model, case, fixture, rubric, package revision,
and harness policy version are explicit. Structural validation never claims a
behavioral run occurred.

## Deliberate omissions

- No automatic upstream updater.
- No generic language-tooling layer.
- No vendor runtime dependency or generated repository framework.
- No replacement for repository-specific review, test, issue, or operator paths.
- No claim that heuristic profile discovery proves capability absence.

## Engineering methodology discovery

Repository-specific methodology stays in canonical repository policy/specs and
commands. Profile `sources` registers those policies; existing invariant
`enforcement` entries name their owner, rung and artifacts. Verification and
Operations owns claim qualification and the promotion workflow. The profile
helper audits registrations without running commands or inferring acceptance.
No second methodology catalog or threshold copy is maintained in the plugin.
