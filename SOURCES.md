# Design Provenance

This file records design provenance, not one-to-one skill derivation. The
package is an independent synthesis: no upstream skill text, template, or code
is copied. Repository pins make reviewed influence repeatable; they are not
runtime dependencies and do not silently update local behavior.

## Source layers

1. **Harness doctrine:** repository context, deterministic tools, and feedback
   loops that improve after recurring failures.
2. **Reusable workflows:** architecture, lifecycle, interface, hardening, and
   progressive-disclosure techniques.
3. **Empirical projects:** observed failure modes and enforcement that survived
   real application, hardware, provider, and release work.
4. **Optional adapters:** vendor-specific implementations considered only after
   the generic contract is established.

## External sources

Reviewed on 2026-09-04.

| Source | Reviewed revision | License | Adopted influence | Deliberately not adopted |
| --- | --- | --- | --- | --- |
| [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/) | Published article, no repository revision | Site terms | Early mechanical boundaries, repository wayfinding, and harness improvement after repeated failures | Repository-specific autonomy and merge policy as universal defaults |
| [OpenAI Cookbook](https://github.com/openai/openai-cookbook) | `a78f3f37bd23637aac2b3f1e8b1251cf5bb9e1a7` | MIT | Small sources of truth, feedback artifacts, and postmortems that improve the harness | Any optional file layout as a mandatory Codex protocol |
| [Addy Osmani agent-skills](https://github.com/addyosmani/agent-skills) | `1c760d643497e9da289300e5eb2f5aca861503f7` | MIT | Progressive disclosure, explicit triggers, reversible slices, and anti-rationalization checks | A large lifecycle catalog or universal numeric thresholds |
| [mblode agent-skills](https://github.com/mblode/agent-skills) | `f7d7a28b942bf00299ceb39e8bb2767767ed8f78` | MIT | Design/Deepen/Harden framing, surface budgets, deletion-first analysis, and guardrails that prove they bite | Framework-specific TypeScript/Next.js assumptions and maturity claims; the reviewed README contained merge-conflict markers |
| [Magnus Hedemark agent-skills](https://github.com/magnus919/agent-skills) | `de968dfdfb5ac92336a4915dad4bb56a27fe0207` | MIT | Observable quality scenarios, distributed failure semantics, consumer contracts, and compatibility analysis | The full specialist routing graph or breadth as evidence of equal maturity |
| [Tech Leads Club agent-skills](https://github.com/tech-leads-club/agent-skills) | `fc886b77e54db38b621f08472434cbb73ef35008` | Infrastructure MIT; first-party skill content generally CC-BY-4.0 | Registry validation, integrity metadata, and modularity vocabulary | Unverified security/maturity claims, mandatory deployment independence, or copied CC-BY text |
| [DBOS agent-skills](https://github.com/dbos-inc/agent-skills) | `f39687cb282334e6b14d3e9f79ebca4a5f9b93e8` | MIT | A concrete optional durable-runtime adapter and separation of core instructions from references | Treating one vendor as the definition of durable execution |

## Empirical repositories

These local repositories supplied examples and counterexamples. Their licenses
are not relied upon because no text or implementation is reused.

| Repository | Reviewed revision | Evidence incorporated |
| --- | --- | --- |
| VitalThread (`workout.codex`) | `c67719688b34ec6509d26e579df4a3d51bfa1ef9` | Local-first storage contention, durable work, event classes, account fencing, compatibility profiles, exact-revision evidence, and guarded operations |
| MERA Hardware (`davidiw/mera-hardware`) | `a0cf1be5502c17c3afd4cce742078e9f762fa9fb` | Capability honesty, SDK consumer boundaries, ports and fakes, single-writer media ownership, immutable artifacts, and physical-proof separation |
| `aichestrator` | `dbd724df26e52b78339ba711e25bb4b02b55b581` | Typed AI actions, discussion-versus-execution authority, provider adapters, approvals, and durable task recovery |
| `protectai` | `5434a15b40159c134e6f303eb801b8e937ec582a` | Central boundary wrappers for authentication, permissions, errors, envelopes, and privacy-safe activity logging |
| `smartypants` | `36baf6165f615567a13ca9ff6cd3d1c560a785af` | Small-project restraint, deterministic policy ownership, and explicit deferral of unnecessary infrastructure |
| `robot-tank` | `9b8d375032ead19b8f9fbbd86f18cc9485434a33` | Source-versus-generated artifact authority and the boundary between automated and physical fit evidence |
| `workout.website` | `b0b653bdaa7ccbf45218604f5a969a437b60037d` | A proportional static-site path with rendered-contract tests rather than distributed-system machinery |
| `fermata` | `d31bdf94d6b0a6a826f5ef6214dd76bbcb319d9f` | A conventional build path where explicit Gradle configuration is sufficient and extra harness layers would be waste |

## Updating sources

Review upstream changes deliberately. Record the new revision, material idea,
local decision, license impact, and affected evaluation before changing a
skill. A source update never changes installed behavior by itself.

## Product-experience study (0.6 development)

[Borrow / Adapt / Reject](docs/proposals/product-experience/README.md) records the
Impeccable, Anthropic, PracticalSwan, Magnus, Nolly, Vercel and DESIGN.md studies.
[Source manifest](docs/proposals/product-experience/sources.json) pins revisions
and inspected-file hashes. Runtime guidance is an original synthesis, not copied
skill bodies or product aesthetics. These sources inform judgment patterns;
normative accessibility/platform facts instead use W3C, Apple, Android and Flutter
primary documentation linked from the runtime platform-check reference.
