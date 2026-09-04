# Pure Library Fixture Rules

- `src/date_parser.py` owns date parsing.
- Preserve the existing value type and `ValueError` behavior.
- Use the existing table-driven unit test.
- The library has no persistence, network, background work, release workflow,
  or operational interface.
