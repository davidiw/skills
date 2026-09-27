# Parser contract

`parse_records` reads text from a stream supplied by its caller. The caller
retains lifecycle ownership of that stream. Parsed records are returned directly
and are used only within the current process.
