# Enforcement Ladder

Documentation is not enforcement. For each active invariant, record its current
rung and concrete owner or artifact.

| Rung | Meaning | Completion evidence |
| --- | --- | --- |
| `principle` | The behavior is documented | One authoritative statement and trigger |
| `owner` | The intended code or operational owner is named | Path, module, service, or command |
| `audit` | A bounded check can detect violations | Query, review rule, or report with a failure condition |
| `local_check` | A deterministic developer command rejects violations | Command and deliberately failing fixture |
| `ci_check` | The exact-revision gate executes the check | Required lane and immutable result |
| `runtime_guard` | The running system fails safely at the boundary | Typed failure, metric, and recovery path |
| `fault_test` | Failure, replay, race, or interruption is exercised | Deterministic adversarial fixture at the owning seam |

Timing depends on the invariant catalog:

- `ownership_declaration` names the owner when the behavior or representation
  is introduced;
- `boundary_introduction` normally installs a cheap deterministic check with a
  declared foundational boundary, before recurrence;
- `risk_proportional` adds behavioral, performance, fault, physical, and
  operational evidence only when capability and consequence justify it.

Higher is not automatically better. Runtime guards can harm availability and
fault tests can be expensive. Use the cheapest rung that makes the active risk
defensible. A foundational boundary below mechanical enforcement requires a
scoped repository-authorized exception, not an assumption that recurrence must
come first.

An acceptance report keeps four states separate:

1. implementation status;
2. automated-evidence status;
3. physical or external-evidence status;
4. release-gate status.

File existence, a test name, or a generated harness is not a passing result.
