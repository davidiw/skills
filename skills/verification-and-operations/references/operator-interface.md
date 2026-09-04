# Operator Interface

Prefer one discoverable command registry with:

- `list` or equivalent command discovery;
- per-operation help;
- machine-capability doctor/preflight;
- dry-run or plan output for writes;
- exact target, source revision, and risk class;
- the action scopes authorized by the current instruction;
- bounded concurrency, locks, leases, or compare-and-set protection;
- structured result and recovery location;
- secret references rather than secret values.

Machine configuration may contain allowlisted tool paths, device IDs, and local
targets. Product URLs, credentials, tokens, signing material, and application
secrets remain in the owning credential system.

Adding a command requires an owner, help text, preflight, safe retry semantics,
test or dry-run fixture, and a reason it belongs in the existing interface. A
one-off script that mutates shared state still needs the same controls.

Apply external-action authorization from
[`precedence-and-exceptions.md`](../../../references/precedence-and-exceptions.md).
The command plan records the resulting scopes; it does not redefine them.
