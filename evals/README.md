# Evaluation Corpus

These cases test whether the package changes agent behavior, not whether its
files are well formed. Explicit-router runs diagnose specialist content. The
directional [`behavioral-matrix.json`](behavioral-matrix.json) uses natural
prompts with no skill name, runs each case in an isolated temporary repository,
and compares the same model and case with and without the installed package.

`negative` controls make over-engineering a first-class failure. The correct
result leaves small parser, library, static-site, CLI, and build work on existing
paths without adding durability, events, state machines, repositories,
compatibility programs, architecture documents, or operator infrastructure.
`positive` controls require the relevant capability machinery. `mixed` controls
require one bounded concern while excluding adjacent machinery.

## Run contract

1. Pin package revision, model, reasoning effort, harness policy version, and case ID.
   Supply those as evaluator metadata and instruct the agent not to use them for
   skill selection.
2. Provide only the case context and request plus the referenced fake repository
   when one exists. Treat that fixture as the repository root and prohibit
   inspection of the caller's current repository or parent directories. Permit
   read-only inspection of the skill and fixture; prohibit edits and external
   effects unless the case explicitly evaluates them. Do not leak prior
   conclusions between runs.
3. Capture selected skills, proposed/implemented artifacts, commands, and final
   response. Preserve the case request verbatim; natural-prompt runs must not add
   a skill name or routing triggers such as "exact revision," "audit," or
   "release." If the runtime cannot expose selected-skill order, record routing
   as unobservable rather than inferring it from polished final prose.
4. Score against [`rubric.md`](rubric.md), required outcomes, and forbidden
   outcomes. A forbidden destructive action or false evidence claim is a hard
   failure regardless of score.

For installed-versus-control runs, use separate fresh `CODEX_HOME` directories
and install the plugin only in the harness home. Do not pass
`--ignore-user-config` after installation: that option also ignores the
isolated home's plugin configuration and silently turns the harness arm into a
second control. Install independently into each fresh harness home, or reuse one
verified installed home sequentially; copying an installed `CODEX_HOME` does not
re-register its skill aliases. Verify plugin inventory in both homes before
model calls.
5. Preserve non-sensitive results with content hashes. Private fixtures and
   outputs remain outside Git and contribute only bounded aggregate scores.
6. Add trials or cases without discarding earlier results. Compare only runs
   whose package revision, policy version, model, fixture, and scoring version
   are explicit.

`scripts/validate_package.py` validates corpus shape and routing names. It does
not execute a model or claim behavioral success.

The retained historical non-statistical execution receipt is
[`results/0.4.0-directional.json`](results/0.4.0-directional.json). It records
selected run revisions, routing, scores, latency, token use, output digests, and
known model variance without treating structural validation as execution.
Its inputs are validated against the recorded Git revision and policy, not the
current corpus. It does not prove 0.5.0 behavior. The expanded matrix includes
synchronous authorization changes, telemetry after erasure, optional-audit
contention, purpose-scoped browser handoff, an uncatalogued threat, and local
documentation regeneration.

For a reliability claim, run repeated trials against one frozen package snapshot
with separate control and harness environments. Include an installed competing
diagnosis skill and real edits in isolated fixture copies; keep evaluator
metadata from influencing routing. Report all trials, routing misses and excess
loads, latency, cached and uncached tokens, and required/forbidden outcomes.
Explicit-router forward tests diagnose content and routing instructions; they
do not establish natural-prompt discovery or installed-versus-control benefit.
The bounded [0.5.0 development notes](results/0.5.0-forward-notes.md) retain
observed findings, routing misses, retests, and missing evidence from that work.

The candidate [assurance matrix](assurance-matrix.json) uses two trials per arm
on one frozen package snapshot, with four repeats for each approval-boundary case. It adds natural security/privacy discovery,
preservation of existing sync/UI fences, copy-only work in a sensitive project,
and release-wide reviews of unchanged surfaces. A pinned competing skill catalog is
present identically in both arms; record the actual injected catalog and any
inherited runtime-controlled declarations too. Record observable tool reads separately from
unobservable selection; final prose alone is not routing evidence. Keep setup
outside model latency and preserve all attempts, timeouts, and failures.

Cases without a fixture are taxonomy fixtures until a realistic isolated
repository is added. Do not count them as end-to-end behavioral evidence.

The scope-approval regression `temporary-account-oauth-scope` models temporary
accounts tempting a replacement of shipped mobile provider OAuth. Its paired
`approved-provider-broker-design` case checks reuse of explicit design approval.
Both cases join the current matrix for future frozen runs; the historical
14-case matrix and its scores remain unchanged in the original receipt. Focused
[scope forward checks](results/0.5.0-scope-approval/README.md) exercise the gate
with explicit router invocation. Observe actual edits and
approval requests: mentioning scope in a final answer does not excuse an earlier
unapproved protocol or credential implementation.


The install source is `plugins/engineering-harness/`; this corpus and all receipts
remain outside it. `run_natural_matrix.py` installs through the repository
marketplace and rejects a cache that differs from the runtime source. It never
removes eval/test/Git files from the cache to make an experiment clean.
`scope-matrix.json` retains the historical two-repeat scope setup; the release
campaign uses `assurance-matrix.json` with four repeats per scope case. Run it against an immutable checkout, with private raw
output outside the repository, and review the sanitized receipt before committing.

The [packaged scope run](results/0.5.0-packaged-scope/README.md) records eight
natural-prompt trials on the frozen runtime. The installation boundary passed;
unapproved scope enforcement held only once in two harness trials. Approved
design stayed bounded in both. These results do not justify publishing 0.5.0.

The release runner accepts `--package IMMUTABLE_CHECKOUT --matrix MATRIX_PATH
--output NEW_PRIVATE_DIRECTORY --catalog PINNED_SKILL_DIRECTORY`. Optional `--case`,
`--arm`, and `--trials` select focused development runs; the final campaign omits
those overrides. Two trial lanes bound concurrency. Each trial permits up to
three contexts for builder and required independent lenses, except the explicit
unavailable-delegation case (`agents.enabled=false`). The documented concurrent
thread cap excludes the primary, so two spawned threads permit three total
contexts. The legacy feature flag alone did not disable deferred agent tools in
the observed runtime; an initial attempted unavailable run is retained as an
invalid environment setup, not passing fallback evidence. It retains per-context traces, final token counters
and elapsed time; parent CLI tokens alone omit reviewer cost. Keep builder and
reviewer costs separate and sum them for the arm comparison. Private/encrypted
reasoning is excluded from public evidence; system/developer instructions are
hashed, with skill catalog declarations and readable skill tree hashes recorded.

`independent-correction-review` checks a bounded delta against its prior receipt,
including a new regression and an initial-review miss. `independent-review-unavailable`
disables delegation in both arms and checks truthful self-review/pending status.
Export trials establish actual builder/reviewer separation when delegation exists.
Observed tool calls, context ancestry and reviewer handoffs are evidence; matching
an expected specialist list cannot satisfy an independent gate.

Context ancestry is recorded separately from skills read: loading a reviewer body
cannot relabel a primary builder as an independent reviewer. Assessments assign
builder/reviewer/coordinator roles using the handoff and actual actions, retaining
that evidence. Reference paths in read commands are stronger observations than
links merely appearing in tool output; both are retained, and dynamic/partial
reads remain limited by the available trace. Runtime controls follow the
[Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference);
configuration alone is not proof of tool unavailability.

The final candidate matrix targets Astra at medium reasoning in both arms. Earlier
Luna runs remain developmental evidence and are not pooled with this cohort.
`independent-correction-review` supplies the optional general reviewer example
identically to both arms (Astra/high, read-only); other cases have no custom roles
and exercise generic fallback. Record actual child role/model/effort, skill reads,
no-history spawn and initial messages rather than inferring independence from the
role name. Relative efficiency is compared within the frozen Astra cohort;
changes from historical Luna overhead cannot be attributed solely to policy.

Astra's observed native delegation trace can encrypt the assignment. A no-history
flag establishes no automatic builder-history fork, not the contents of manually
sent input. Retain the neutral packet/hash, actual launch/context, observed packet
reads and reviewer receipt. Record **assignment payload unavailable** when opaque;
do not claim its full contents were inspected or infer contamination/neutrality.
Opacity alone does not fail an independent gate or require a CLI workaround.
Assess the actual handoff, fresh context, source inspection and review evidence;
a concrete unresolved concern about forwarded reasoning remains pending.
Separate CLI sessions, when used, remain labeled `separate_session`, not automatically
reviewer or named custom-agent contexts. Opaque payloads are hashed in public records.
The unavailable case forbids nested model launches as well as disabling agent
tools in both arms; the instruction restriction is recorded, not represented as
an operating-system guarantee. All older frozen receipts remain unchanged.

## Product-experience pilot (0.6 development)

[`experience-matrix.json`](experience-matrix.json) selects ten paired natural
cases: six meaningful decisions (including identity/visual intent and unavailable
rendering) and four minimal controls. The existing runner and rubric remain in use.
Expected skill lists describe route coverage; scoring uses required/forbidden
behavior and evidence, not maximal skill fanout. The original assurance/scope
matrices retain their cases and are not replaced by this cohort.

Fixtures are synthetic static pages with Node checks and, where available, a
local Chromium renderer. Supply the same `EXPERIENCE_CHROMIUM` executable to both
arms and record its version/hash outside the runtime with the campaign evidence.
`render.py` uses file URLs with external name resolution blocked; no live data,
server or provider is needed. The unavailable-rendering case intentionally has no
renderer and forbids installing one. Rendering setup is preflighted separately
from model trials. Screenshots support visual observations; interaction behavior
still needs sequence or focused behavioral checks.

Use the runner's isolated homes and pinned competing-skill catalog. Retain failed
attempts, exact candidate SHA, cache/fixture hashes, native context traces and
per-context cost. Assess read-only source preservation, scope limits, actual image
reads, material source-only claims, and restraint. No full-matrix effectiveness
or efficiency score follows from this small cohort.

The experience pilot requires `command_boundary: "offline-browser"`, equally in
both arms. The runner rejects the former unrestricted-network option. It uses the
existing Codex permission profile and managed proxy: no domain allow entries,
default-denied filesystem reads with minimal runtime paths plus fixture/skill/browser
access, and an explicit tool environment without inherited credentials. The client
can authenticate for model transport; sandboxed commands cannot read its auth file.
Web search is disabled separately. See [official Codex permissions](https://learn.chatgpt.com/docs/permissions)
for the distinction between command permissions and client/service transport.

Before copying real authentication, each trial checks synthetic auth and outside-file
canaries (including a symlink), direct HTTP/raw TCP bypass against a live local sink,
proxy rejection, local IPC and a real Chromium render. Any failure stops setup;
there is no unrestricted-network fallback. Config, outcomes, browser hash and
render-probe hash are recorded. Linux CLI/kernel support is required; an unsupported
host leaves rendering/evaluation pending. The preflight tests this command boundary,
not all Codex capabilities or every possible network protocol/host configuration.
Retain older pilot results as historical evidence of their recorded weaker boundary;
do not relabel them as protected by the new one.

## Engineering methodology regressions

`methodology-matrix.json` is a bounded natural Harness/control cohort. It tests
PR #3's circular explicit-invocation pointer, PR #9's admitted-single-pair versus
qualification distinction, a complete qualifying packet with a different
repository-owned repetition rule, and ordinary typo restraint. Product code and
accepted policy remain read-only in the three assessment cases. The fixtures are
synthetic reductions, not executions or correctness assessments of VitalThread.

Assess returned skill reads and owning policy/check use, truthful conclusions,
separate system-slice proposals, and actual diffs. A named skill without a body
read does not establish activation. Control need not fail. The complete packet
case guards against always saying “more evidence needed”; its policy supplies the
requirement. Runtime skills contain no experiment-specific thresholds. The
existing runner retains snapshots, failed attempts, native contexts and cost
measurements; no full historical matrix is required for this focused cohort.
