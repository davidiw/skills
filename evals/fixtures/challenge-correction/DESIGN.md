# Display adapter contract
The report adapter replaces [[ref:key]] tokens with labels from the supplied
verified mapping. All other characters remain unchanged, including punctuation,
quantities, associations, units and URLs. It is not a fact checker: an original
statement may be inaccurate. Labels may contain digits or punctuation. Unknown
references fail explicitly; ordinary unchanged text remains usable.
Field discovery covers field names in both input_schema and output_schema.
The service uses discovery to suppress internal schema field names in display
summaries. Keep execution payloads and the existing plain-text API unchanged.
