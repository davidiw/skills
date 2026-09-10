# Independent reservation acceptance artifacts

These tests were authored by the configured independent reviewer and are kept
outside the task fixture. The operator executes their bytes unchanged against a
frozen source directory. They are acceptance evidence, not runtime Harness policy.

```sh
python3 evals/conditional-role-checks/reservation_acceptance.py FROZEN_TASK_ROOT
python3 evals/conditional-role-checks/reservation_hook_acceptance.py FROZEN_TASK_ROOT
```

The seven-test evaluator covers process contention, durable and concurrent retries,
validation/conflicts, rollback/visibility, and the availability consumer. Its
SHA-256 is `e1fec6ad0db0bec45d5ae98df57e4075638bcf5c5983d4381fecf92d2302e26f`.
The two-test addendum checks that hook-raised SQLite locking exceptions propagate
and roll back both reserved and insufficient outcomes. Its SHA-256 is
`233df9e33cfd5073b65154af345191d727c56ac28f7032fd9e6061b49d5a62bd`.

Do not copy these artifacts or the test-only reference into natural task inputs.
The fixture is deliberately incomplete; the external reference qualifies the tests.
The original seven-test run passed against an earlier reference, but the reviewer
later found the hook defect and authored the addendum, which failed twice there.
The corrected reference passed all nine unchanged checks. Preserve both results;
passing the reference does not establish a natural trial's implementation result.
