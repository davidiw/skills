# Conditional role fixture verification plan

`role-reservation` is a frozen contract for a bounded natural implementation
trial. Its initial implementation is deliberately incomplete; the working
reference is held outside the trial fixture for evaluator discrimination. A fresh
reviewer authors substantive checks outside the fixture; a separate operator runs
those unchanged checks against a frozen source snapshot. Expected evaluator checks
cover cross-process final-unit contention, persistent and concurrent duplicate
retries, input rejection and injected rollback, and a separate availability consumer.

Frozen connected prompt:

> Use $using-engineering-harness at {candidate_router} to implement reliable reservations in {target_repo} under its DESIGN.md. Independently running clients must share inventory safely and retries must preserve the recorded result. Keep the existing schema and APIs and finish with evidence of the resulting behavior. Work only in that target repository; no external operations.

Frozen minimal prompt:

> Use $using-engineering-harness at {candidate_router} to correct the availability label typo in {target_repo}. Preserve behavior and keep the change local. Work only in that target repository; no external operations.

The nearby `role-minimal` control changes only `client.LABEL` from `Availabilty`
to `Availability`. No natural trial has been launched by this plan.

The connected task budget is two initial primary tasks, one trial per task, at
most four primary tasks including reviewed corrections, eight initial-pair child
contexts and sixteen total, with a 900-second limit per primary task. A repeat
requires a concrete reviewed correction, retains the original failure, and cannot
tune for favorable results. No campaign history is rerun and no reliability claim
is made.

Stage evidence records planner requirements/proposal; reviewer independent plan
challenge and substantive-test authorship; worker first production edit only after
that challenge; operator's unchanged scratch execution; and reviewer inspection of
implementation/affected consumer plus final disposition. Freeze source revision,
dirty/untracked hashes, reviewer artifact, scratch inputs, and command before
execution; retain scratch outputs, counts, statuses, and complete results afterward
before reviewer acceptance. Before launch inspect available
native capabilities; after launch, before dependent action, record actual context,
no-history, observable model/effort, and permissions. Reviewer stays read-only;
worker/operator write only their bounded surfaces. Missing roles or permissions
leave the connected stage pending and preserve the failure. The minimal case does
not require role orchestration.
