# Photo Analysis Rules

- The server already has a durable-job repository and worker runtime.
- Protected media storage owns uploaded photo bytes.
- The photo-analysis service owns canonical analysis semantics.
- The client route may submit work and render status but must not own durable
  execution.
- Focused fault tests use fake media and providers. Do not perform deployment,
  migration, or live-provider actions.
