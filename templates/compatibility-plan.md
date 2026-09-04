# Compatibility Plan

## Change

{Persistent, wire, event, storage, worker, generated-artifact, or operator
contract being changed.}

## Consumer profiles

| Consumer/profile | Reads | Writes | Coexistence | Evidence | Removal gate |
| --- | --- | --- | --- | --- | --- |
| {deployed identity} | {range} | {format} | {duration} | {fixture/receipt} | {release/telemetry} |

## Transition

- Authority before transition: {owner}
- Authority after transition: {owner}
- Durable state and interruption points: {states}
- Validation: {bounded structural checks}
- Rollback: {compatible binary or operation}
- Unsupported states: {fail-closed behavior}

## Rollout

{Writer order, reader order, telemetry, rollback trigger, and adapter cleanup.}
