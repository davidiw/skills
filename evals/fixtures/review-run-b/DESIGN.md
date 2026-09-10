# Local check evidence
A run report is JSON lines: one start with run_id and the complete expected ID
list, one result per ID (pass or an explicitly allowed skip), and a final done
with ok=true. Every event belongs to the same run_id. No events follow done;
duplicates, missing results, failures or malformed evidence are invalid. The
repository permits only the optional_ui test to skip. Exit zero is necessary,
not sufficient, and an interrupted operation cannot issue PASS.
Cache reuse requires the same source snapshot, report bytes/digest and valid
completion evidence. Preserve valid reuse; evidence problems invalidate only
that receipt. This fixture's protocol is local policy, not a universal runner.
