---
name: application-composition
description: Align product behavior across UI, API, workers, assistants, providers, and hardware adapters. Use for shared-domain parity, screen/controller ownership, useful-paint loading, local-first interaction, AI action boundaries, or platform capability composition; not for visual-only styling.
---

# Application Composition

Compose one product from different runtimes without duplicating semantics or
making presentation the durable owner.

## Workflow

1. Name the canonical product behavior and deterministic policy owner. Map how
   each UI, API, worker, assistant, provider, or hardware surface reaches it.
2. Separate domain command/result, transport object, persistence record,
   provider observation, and view state. Adapters translate; they do not
   reinterpret policy.
3. Put assembly in an explicit composition root. Platform and provider
   capabilities enter through narrow interfaces and report unsupported behavior
   honestly.
4. For interactive surfaces, draw the useful-paint graph: data required for a
   correct first interaction, independent enrichment, and work that can defer.
   Render authoritative local or server state without waiting for unrelated
   refreshes.
5. Keep route/screen state transient. Durable drafts, sync, imports, retries,
   provider polling, AI jobs, and replay belong to controllers, repositories,
   schedulers, or workers that survive the route as required.
6. For AI-mediated behavior, use typed bounded actions and the same canonical
   service as direct product UI. Preserve manual input and provenance; the
   assistant may explain or propose but not maintain a private implementation
   of product policy.
7. Test semantic parity at the domain result, stale publication during route or
   account changes, optional-enrichment failure, and overlapping reload/mutation.
8. Extract only where ownership is currently preventing correctness, testing,
   bounded execution, or independent failure.

Read [`interactive-surfaces.md`](references/interactive-surfaces.md) for UI and
loading work. Read [`adapters-and-ai.md`](references/adapters-and-ai.md) when
providers, hardware, or assistants participate.

The composition is complete when all surfaces reach one semantic owner,
platform differences are isolated, useful content does not depend on optional
work, and stale or unsupported adapters cannot publish misleading state.
