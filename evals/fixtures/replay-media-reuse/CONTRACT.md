# Replay contract
The capture reference binds canonical versioned evidence to the pose, features,
events, media bytes, and each captured provenance value. `media_path` is a local
locator, not identity. `verify(reference, record, pose, features, events,
media_bytes)` checks both recorded evidence and the supplied payloads against
that reference. Replay must verify the bytes it returns, using one file read.
Labels, rep counts, and adjudication are separately revisioned and may change
without changing evidence identity. Missing media is an error. Inputs are JSON
serializable. Run `python3 -m unittest -v test_reuse` for the local check.
