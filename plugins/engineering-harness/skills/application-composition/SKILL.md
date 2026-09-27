---
name: application-composition
description: Align product behavior across UI, API, workers, assistants, providers, and hardware adapters. Use for shared-domain parity, screen/controller ownership, useful-paint loading, local-first interaction, AI action boundaries, or platform capability composition; not for visual-only styling.
---

# Application Composition

Own shared product semantics and UI/runtime composition. Use accepted owners;
consult relevant [invariants](../../references/invariants.json) only when needed.

1. Trace each affected surface to the canonical deterministic policy owner.
   Distinguish domain results, transport/storage forms and view state.
2. Keep assembly in a composition root; adapters translate rather than redefine
   policy. Unsupported platform capabilities remain explicit. When an adapter
   wraps an external owner, trace acquisition, teardown and subsequent reuse or
   re-entry under the declared owned/borrowed/transferred contract. At the
   composition seam, prove borrowed owners remain usable after wrapper close or
   pause; for transfer, prove the old owner can no longer act.
3. For UI/loading, read [interactive surfaces](references/interactive-surfaces.md).
   Separate useful first interaction from independent enrichment; route state is
   transient, while accepted durable work remains with its existing owner.
4. For providers/hardware/assistants, read [adapters and AI](references/adapters-and-ai.md).
   AI uses the same typed, bounded action service as direct UI; preserve manual
   input and provenance. It does not gain execution authority from a suggestion.
5. Test semantic parity, optional failure, overlapping reload/mutation and stale
   route/account publication at the owning seam. Using an existing canonical
   account fence does not itself require security/privacy assurance.

For shared scarce pools, consume [resource governance](../architecture-foundations/references/runtime-resource-governance.md)
without transferring lifecycle ownership into presentation. Extract only where
ownership blocks correctness, testing or independent failure. Done means one
semantic owner, useful content independent of optional work, and no stale or
misleading publication. Apply [precedence](../../references/precedence-and-exceptions.md)
for workflow conflicts.
