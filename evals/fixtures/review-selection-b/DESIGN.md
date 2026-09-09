# Preparation contract
The inventory preparation gate covers amend_path (path.id) and amend_body
(body.target_id). Selectors and values are immutable through preparation.
A command must affirmatively identify the actual target. The accepted command
format is Update followed by one JSON-quoted verified label and a period; the
quoted text is data, including when a record's name contains command-like words.
A plain name is unique only with a complete unfiltered catalog snapshot.
Exact and filtered pages cannot prove global name uniqueness, even when complete
for that query. A backend-assigned unique slot_code allows the verified qualified
label name / slot_code without a full catalog read. Preserve valid preparation
with either proof; this gate does not authorize new read scopes or perform writes.
