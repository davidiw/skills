# Interactive Surfaces

## Useful-paint graph

Classify each dependency:

- **Core:** needed for a correct first useful interaction.
- **Independent:** useful enrichment that can load and fail on its own.
- **Deferred:** background refresh, analysis, or maintenance not needed to
  render authoritative current state.
- **Durable:** accepted work observed by the surface but owned elsewhere.

Measure data-ready and render delay separately. Treat app suspension or a later
frame callback separately from active computation.

## Ownership test

A screen or route may:

- read and render state;
- own focus, selection, animation, and unsaved transient gestures;
- collect intent and submit bounded commands;
- observe durable operation state.

Move ownership when it must survive route replacement, arbitrate writers,
retry, synchronize, poll a provider, checkpoint progress, or fence stale
authority. Moving generation counters unchanged into another file is not a
simplification; remove the competing lifecycle that made them necessary.

Large files are investigation signals, not violations. Demonstrate mixed
ownership or recurring coordination before extracting a boundary.
