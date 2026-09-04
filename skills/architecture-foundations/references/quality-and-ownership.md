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

An ownership gap is resolved in the design before implementation proceeds.
