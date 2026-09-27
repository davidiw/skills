# Quality Scenarios and Ownership

## Observable scenario

Use this compact form:

```text
Stimulus:
Operating condition:
Expected response:
Measured bound:
Evidence source:
```

Examples of measurable bounds include time to useful content, maximum
uninterrupted database work, duplicate external requests after replay,
recovery point after process death, and mixed-version behavior. Avoid labels
such as "fast," "robust," or "scalable" without an observable outcome.

## Ownership map

For each material concept, record:

| Concept | Authoritative owner | Writers | Readers | Representations | Recovery or rebuild |
| --- | --- | --- | --- | --- | --- |

Then test four questions:

1. Can two writers accept conflicting commands without one arbitration policy?
2. Can a reader mistake a cache, projection, provider observation, or transport
   object for authoritative state?
3. Can an external effect occur without a committed fact that explains it?
4. Can the owner be located from repository wayfinding and enforced dependency
   direction?

For resource-bearing concepts, extend the existing map with **Owned / Borrowed /
Transferred**, the transfer boundary (if any), permitted destructive operations,
and what must remain usable after close. Owning a wrapper or subscription does
not imply owning the underlying resource. A transfer identifies when the old
owner loses authority and the new owner gains it. Ordinary value/parser work
needs no resource table.

An ownership gap is resolved in the design before implementation proceeds.

## Domain meaning before structure

When competing terms imply different behavior, locate the repository's accepted
vocabulary and contracts. Trace a concrete example and counterexample through
the code: who acts, what changes, which state is authoritative, and what a reader
can observe. Distinguish an overloaded label from two genuinely different facts.

Record accepted meaning, implementation evidence and unresolved proposals
separately. A contradiction is a finding to resolve, not permission to rewrite
either authority. Clarifying terminology does not approve a new lifecycle or
owner. Present alternatives and their behavioral consequences when meaning is
unsettled; preserve that boundary while continuing independent authorized work.

Update an existing glossary/design decision only for accepted conclusions within
scope. No particular filename, new glossary, ADR series or renamed API is required.
Use an architecture decision record only when a consequential trade-off needs
durable rationale under repository convention. Ordinary naming fixes stay local.
