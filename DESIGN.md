# Engineering Harness Design

## Objective

Provide one coherent, framework-neutral package that helps coding agents make
consequential application changes safely while leaving simple work simple.

The ordering is:

```text
authority -> lifetime -> contracts -> composition -> data evolution
          -> enforcement -> exact evidence -> authorized operation
```

Repository instructions and product decisions remain authoritative. The
package supplies workflows and schemas, not a replacement architecture or work
tracker.

## Package decisions

### One plugin, eight entries

The initial proposal's router plus seven specialists survived review because
the specialists have independent trigger branches:

- architecture ownership can change without durable work;
- durable work can exist behind a private interface;
- public contracts can evolve without persistence;
- application parity and useful-paint ownership are composition concerns;
- data compatibility spans representations and deployed consumers;
- hardening is an explicit intervention, not routine review;
- evidence and external operations have their own authority boundary.

The router disables implicit invocation in `agents/openai.yaml` so preflight is
intentional. Hardening remains model-discoverable when the user explicitly asks
to harden, simplify, grill, or audit a concrete hotspot, or repository policy
mandates an audit for the current high-risk diff; its body excludes ordinary
review. This lets the router reach every specialist without bypassing invocation
policy while keeping normal work out of adversarial audit.

### Twenty conditional invariants

The proposed 18 invariants remain, with wording generalized beyond
VitalThread. Two evidence-backed gaps were added:

1. implementation, integration, metadata, deployment, installation, migration,
   repair, and publication are separately authorized actions;
2. claims bind to exact artifacts and truthful evidence classes, so generated,
   simulated, host, device, physical, and production observations cannot stand
   in for one another.

The count is not a target. `references/invariants.json` is authoritative and a
project activates only relevant entries. The minimal profile demonstrates that
most of the catalog can remain inactive.

`references/capability-activation.json` defines the minimum invariants implied
by declared capabilities and sensitive-data handling. Profile validation fails
when a required capability is unassessed or an activated invariant has no
enforcement owner. Repositories may activate additional invariants.

### Proportionality before completeness

Cross-repository review showed that VitalThread's full durability and release
model would be wasteful for a static website, deterministic CLI, in-memory
tutoring prototype, or conventional single-module build. Change classification
therefore happens before specialist loading. The harness must receive a failing
evaluation when it invents persistence, jobs, events, abstraction, or release
machinery for a simple case.

### General contracts before adapters

DBOS, cloud queues, mobile schedulers, PostgreSQL outboxes, SQLite journals,
provider APIs, Flutter controllers, and hardware ports are possible adapters.
None defines the package's generic contract. A skill first specifies authority,
lifetime, failure, and evidence, then selects the smallest repository-supported
adapter.

### Evidence is a product of execution

The package separates implementation, automated evidence, physical/external
evidence, and release eligibility. A file path or harness definition is not a
pass. Receipts bind exact revision, environment, result counts, and immutable
artifacts. This comes from repeated false confidence caused by stale reviews,
zero-test runs, generated device scripts, and simulated hardware checks.

## Deliberate omissions in 0.1

- No marketplace entry or installation side effect. The repository is staged
  first; installation and distribution are separate decisions.
- No automatic upstream updater. `SOURCES.md` pins reviews, but an update tool
  needs defined comparison and approval semantics before it can modify skills.
- No generic language-tooling directory. Dart, TypeScript, C++, Android, CAD,
  and static-site repositories share principles but not enough commands to
  justify placeholder adapters.
- No vendor runtime dependency and no generated repository framework.
- No broad code-review replacement. Existing repository review, test, and
  operator paths remain canonical.

## Evaluation strategy

Structural validation checks manifests, frontmatter, invocation policy, links,
profiles, generated invariant documentation, source pins, and corpus shape.
Behavioral evaluation tests routing, required outcomes, and forbidden
overreach against the same model with and without the package.

Initial forward tests prioritize three discriminating cases:

1. a tiny CLI that should activate no specialist;
2. durable photo analysis that must survive its caller;
3. a hardware capability unavailable on one model, where host proof must not be
   reported as physical proof.

Expand cases and trials without discarding earlier results. Compare only runs
whose package revision, model, case, and rubric version are explicit.
