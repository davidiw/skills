# Current deterministic receipt-maintenance qualification

The local receipt fixture accepts complete LF or CRLF JSONL reports, including
literal U+0085, U+2028, and U+2029 in JSON strings, and preserves the SHA-256
digest of the original report bytes. It rejects duplicate decoded member names
at every object depth, blank records, malformed input, and bare-CR record
separators.

Run `python3 receipt_acceptance.py REPO_ROOT` from a scratch directory with the
reviewer-owned acceptance artifact, then run `python3 -m unittest` in the
fixture. This qualification describes the current source only; retained result
receipts and historical outcomes remain unchanged.
