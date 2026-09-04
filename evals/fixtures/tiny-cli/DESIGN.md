# Design

The CLI reads one local file, parses it through `src/parser`, and prints one
report. Optional fields are absent by default. Malformed recognized values use
the parser's existing validation error.
