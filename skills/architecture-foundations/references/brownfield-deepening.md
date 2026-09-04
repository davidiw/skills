# Brownfield Deepening

Start from demonstrated friction rather than a repository-wide cleanup list.

1. Inspect recent change frequency, repeated fixes, incident paths, and files
   edited for several unrelated reasons.
2. Trace the same domain concept across callers, UI, prompts, transport,
   persistence, background work, and tests. Record duplicate semantics and
   alternative mutation paths.
3. Identify where current ownership forces generation tokens, hidden
   coordination, stale-result guards, or cross-layer special cases.
4. Attempt deletion: remove an alternate path, redundant representation, or
   obsolete compatibility branch in a fixture before proposing an abstraction.
5. Characterize the current behavior at its owning seam, including one fault
   path, before extracting it.
6. Move one vertical slice and add one boundary check. Reassess before moving
   the next slice.

Do not rank debt by line count. A large composition file can be stable; a small
adapter with two authorities can be dangerous. Rank by violated invariant,
execution frequency, consequence, and the amount of coordination a normal
change currently requires.
