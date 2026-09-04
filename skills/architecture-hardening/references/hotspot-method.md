# Hotspot Method

## Evidence

Rank candidates by:

1. repeated user-visible or operational failure;
2. one logical change repeatedly touching unrelated owners;
3. duplicate semantic implementations or mutation paths;
4. coordination state required to prevent stale work;
5. inability to test the owning seam without broad setup;
6. consequence and frequency.

Churn is a lead, not a verdict. A large stable composition file ranks below a
small module with competing authorities.

## Simplification order

1. delete an unreachable or duplicate path;
2. unify behavior at the existing canonical owner;
3. narrow an interface and move translation outward;
4. extract a meaningful lifecycle or transaction owner;
5. introduce a new abstraction only after two valid callers expose the same
   shape.

## Fragility checkpoint

Stop and discuss when fixing the same invariant starts requiring another
durable representation, alternate command path, hidden coordinator, artificial
fixture, or compatibility for an unexplained state. Report:

- violated invariant and execution path;
- why the design resists a local correction;
- smallest product or architecture choices;
- data, compatibility, and migration consequences;
- recommendation and decision needed.

Do not silently widen the initiative while the choice is unresolved.
