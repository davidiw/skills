# Engineering Harness

Engineering Harness is an owned Codex plugin for consequential application
work. It combines architecture, durable execution, interface evolution,
local-first data, verification, and operations without imposing those concerns
on every change.

The package has no runtime dependency on the projects listed in
[`SOURCES.md`](SOURCES.md). Their ideas were independently synthesized and are
pinned only for provenance and later review.

[`DESIGN.md`](DESIGN.md) records the package boundaries and deliberate 0.1
omissions so later iterations do not mistake restraint for unfinished work.

## Entry points

Use `$using-engineering-harness` when a change needs an explicit risk and skill
preflight. The router is manual. `$architecture-hardening` is discoverable only
from an explicit request to harden, simplify, grill, or audit a demonstrated
hotspot; its own workflow excludes ordinary review. The remaining specialists
are independently discoverable when their narrow conditions apply:

| Skill | Owns |
| --- | --- |
| `architecture-foundations` | Authority, quality scenarios, ownership, module boundaries, and composition |
| `durable-workflows` | Accepted work that must survive the caller, including retries, replay, coalescing, and cancellation |
| `interfaces-and-events` | Contracts crossing modules, processes, clients, or providers |
| `application-composition` | Shared semantics across UI, API, workers, assistants, providers, and hardware adapters |
| `data-and-compatibility` | Identity, replicated representations, migrations, mixed versions, and deletion semantics |
| `architecture-hardening` | Explicit hotspot hardening and bounded post-review adversarial audit |
| `verification-and-operations` | Evidence, exact revisions, generated/physical proof, operator interfaces, and external actions |

Repository-specific instructions remain authoritative. This package points to
existing design documents, trackers, commands, and checks instead of creating
parallel systems.

## Constitution

[`references/invariants.json`](references/invariants.json) is the
machine-readable invariant catalog. Its generated rendering is
[`references/engineering-invariants.md`](references/engineering-invariants.md).
A repository activates only the relevant rules and records their current
enforcement rung in an `engineering-harness.json` profile.
[`capability-activation.json`](references/capability-activation.json) makes the
minimum capability-to-invariant mapping executable rather than optional prose.
The schema and examples live under [`references/`](references/) and
[`templates/`](templates/).

## Development

The package uses Python 3 standard-library tooling only:

```bash
python3 scripts/validate_package.py
python3 scripts/render_invariants.py --check
```

The evaluation corpus in [`evals/cases.json`](evals/cases.json) tests routing,
required decisions, evidence, and prohibited overreach. Structural validation
does not substitute for running those scenarios through target models.

The initial package is intentionally unlicensed (`UNLICENSED`) until its public
distribution terms are selected.
