# Adapters, Capabilities, and AI

## Platform and provider adapters

- Shared code consumes a product contract, not vendor DTOs.
- Composition selects the adapter; callers do not branch throughout the domain.
- Capabilities are explicit and runtime-validated where hardware or permission
  state can vary.
- Unsupported behavior returns a typed result and remains unclaimed in docs and
  evidence.
- A fake proves contract behavior; it does not prove provider, device, power,
  timing, privacy-indicator, or physical behavior.

## AI-mediated product behavior

Separate:

1. model observation or proposal;
2. typed action compilation and validation;
3. deterministic product policy;
4. authorized effect execution;
5. durable result and user-visible explanation.

The model does not own identity, authorization, aggregate invariants, retries,
or conflict resolution. Investigation-only language remains non-mutating until
the user or owning workflow authorizes execution. Compare AI and direct UI at
the canonical domain result, including manual data, attachments, timestamps,
provenance, corrections, and replay.
