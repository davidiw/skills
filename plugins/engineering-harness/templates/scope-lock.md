# Scope Lock

## Objective

{One observable outcome.}

## Acceptance criteria

- {Criterion with a pass/fail signal.}

## In scope

- {Owning execution path or module.}

## Non-goals

- {Adjacent behavior that remains unchanged.}

## Scope expansion decision

Complete before consequential production edits under the
[Scope expansion gate](../references/change-classification.md#scope-expansion-gate).
Repeat the decision for each requested behavior/owner; do not combine a supported
local change and a pending shared boundary into one approved row.

- **Accepted owner/contract:** {Existing owner and accepted contract, with its source.}
- **Already supported?:** {Yes/no with accepted-contract evidence before choosing
  a solution. An excluded behavior is pending unless its concrete expansion was
  explicitly approved; the feature request alone is not that approval.}
- **Expansion status:** {none / approved / pending — choose one.}
- **Proposed expansion:** {New shared responsibility or changed contract. For
  `none`, explain how the accepted contract remains unchanged.}
- **Approval source/limits:** {Concrete proposal plus the user's explicit
  affirmative response, or the user's direct scope approval; record its exact
  limits. For `pending`, state the decision still needed; for `none`, mark not
  applicable.}
- **Blocked boundary:** {For `pending`, name the boundary whose implementation is
  blocked and the independent authorized work that can continue; otherwise none.}

## Active invariants

| Invariant | Owner | Current rung | Required evidence |
| --- | --- | --- | --- |
| {id} | {path} | {rung} | {command or observation} |

## Test lanes

- {Focused command and artifact.}

## Stop condition

{Ambiguity, missing authority, unsafe migration state, unavailable physical
evidence, or another condition that requires an owner decision.}
