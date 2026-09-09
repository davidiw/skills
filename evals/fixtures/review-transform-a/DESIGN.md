# Display adapter contract
The report adapter replaces [[ref:key]] tokens with labels from the supplied
verified mapping. All other characters remain unchanged, including punctuation,
quantities, associations, units and URLs. It is not a fact checker: an original
statement may be inaccurate. Labels may contain digits or punctuation. Unknown
references fail explicitly; ordinary unchanged text remains usable.
Field discovery supplies the names of direct root properties in both
input_schema and output_schema through service.display_fields. Nested schemas
and downstream summary construction are outside this adapter. Keep the existing
plain-text publication API and execution payloads unchanged.
