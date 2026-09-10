# Current deterministic receipt-maintenance qualification

This maintenance follows PR #7 without changing its original scope, evaluated
snapshots, campaign records, or outcomes. The four-role workflow is separate.

The receipt parser rejects duplicate decoded JSON member names at every depth,
including escaped aliases. It splits JSONL on LF, accepts CRLF, and preserves
literal U+0085, U+2028 and U+2029 within JSON strings. Original report-byte digests
remain intact; bare CR separators, blank records and malformed input are rejected.

A configured independent reviewer authored the acceptance artifact; a separate
configured operator executed the unchanged bytes against frozen sources.
Run from the repository root:

```sh
python3 evals/receipt-maintenance/receipt_acceptance.py .
(cd evals/fixtures/review-run-b && python3 -m unittest)
```

| Frozen source | Tests | Passed | Failures | Errors | Skips |
| --- | ---: | ---: | ---: | ---: | ---: |
| PR #7 `83c6267293eb2fe0853ff4189c4c55a71641fc33` | 55 | 35 | 14 | 6 | 0 |
| Maintenance `00a8821bb31a52526a298537dba1a3958a988e16` | 55 | 55 | 0 | 0 | 0 |

The artifact includes 12 valid cases, 42 invalid cases, and one execution/digest/
snapshot/reuse boundary test. Its SHA-256 is
`caf3b85a1cfa4e5e2e0110904ea0d0778cf2534e562a250b0474ecc921452911`.
The corrected `receipts.py` SHA-256 is
`380168d094a5816736cd76e57e1aba7c227796178b7db7b9ee70ececdb293e71`.
The independent reviewer also executed all 55 checks successfully and found no
remaining source blocker in the four-file maintenance change.

Package, official plugin, and all 13 skill validators passed. The full suite ran
131 tests: 130 passed; one errored because the operator's unchanged workspace-write
sandbox disallowed the loopback socket bind in
`test_boundary_config_and_canary_cleanup`. That same environment failure was
reproduced on the unchanged main baseline. No permission was broadened, assertion
weakened, or failure hidden. Initial archive-based validation lacked historical
Git objects; corrected setup used identical source bytes with Git history and
retained the original failed runs. This is deterministic fixture requalification,
not a rerun of the historical campaigns or proof of autonomous Harness routing.
