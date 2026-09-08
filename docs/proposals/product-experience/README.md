# Bounded product-experience capability proposal

Research date: 2026-09-07. Status: **structure approved with amendments; implementation in progress**.

Recommendation: add three concise reasoning owners—`product-experience`,
`interface-design`, and `brand-and-language`—with conditional references. Reuse the
existing scope checkpoint, review handoff, validators, and natural-evaluation
runner. Add no engineering invariants, design command system, or agent roles.

This proposal is non-normative development documentation outside the installable
runtime. The user approved implementation after strengthening identity/visual-intent ownership,
reserving hashes/receipts for retained or gated evidence, and requiring primary
platform authorities for normative facts. This document does not change released policy. Harness baseline:
`8f33b5396ed4ec5340a41be12c7e7850d6e8135f` (0.5.1).
[External source manifest](sources.json) records inspected revisions and file hashes.
Proving-ground observations below are summarized; private source, screenshots,
local paths, and local evidence receipts are not included in this public PR.

## 1. External study: Borrow / Adapt / Reject

Current default-branch source was cloned for inspection, not installed or run.
These are implementation observations, not claims that upstream skills have
demonstrated superiority in controlled evaluations. Links below pin the inspected
revisions; several implementations differ substantially from older summaries.

| Source | Borrow | Adapt | Reject for this initiative |
| --- | --- | --- | --- |
| [Impeccable](https://github.com/pbakaus/impeccable/blob/44e825090eabd187e003920ac9907737a5b97119/.agents/skills/impeccable/SKILL.md), including shape, critique, clarify, polish, and operate playbooks | Separate shaping from refinement; preserve incumbent authority; select posture by surface purpose; fix blocked tasks and misleading states before cosmetics; inspect rendered results in bounded batches. | Current implementation has one entry skill and conditional commands. Retain progressive disclosure, contextual language review, and independent judgment when required. Treat heuristic scores as questions rather than measured usability. A bounded verification pass may leave an unresolved gate; its budget cannot turn a defect into success. | Mandatory dual-agent/detector critique for ordinary work, extensive score/report ceremony, launcher/hooks/browser overlay/storage machinery, automatic follow-on polish, compulsory discovery questions for settled work, and universal craft bans. Operate guidance usefully permits familiar fonts and density, but rules such as blanket spinner/modal preferences still need context. |
| [Anthropic frontend-design](https://github.com/anthropics/skills/blob/41bbe19d1a1a7eaab5e7bb9050a417e5c6cffc8f/skills/frontend-design/SKILL.md) | Ground composition, typography, color, and words in the actual subject and audience. Structural decoration should encode information. Keep terminology consistent through an action and its result. | Intentional direction belongs within the accepted visual language. Expressiveness can serve marketing; active workout controls may need familiar, quiet execution. Screenshots become claim-specific evidence rather than optional self-critique. | A default design-studio mandate for distinctiveness, aesthetic risk, or a new palette/type plan on existing application work. Lists of currently fashionable styles must not become bans. Its own brief-first exceptions are preferable to universal anti-generic prescriptions. |
| [PracticalSwan frontend-design](https://github.com/practicalswan/agent-skills/blob/afbb609dec5b7bf08c8384a013b6b3b535517da2/frontend-design/SKILL.md) | Context-fit quality, system reuse, applicable states, responsive/input checks, honest rendered/performance evidence. Accessibility cannot be traded away for visual appeal. | Product/marketing/data/content postures become a short contextual decision, not another router. Put technical checks beneath UI; leave deep performance and runtime ownership with existing Harness owners. | Weighted quality percentages, a 16 KB entry body, unconditional multi-width/pressure-test ceremony for small edits, and automatic additional frontend-reviewer skill loading. Source metadata says 2026-09-08; the recorded Git revision, not that future-dated label, identifies this inspection. |
| [Magnus product-design-and-ux](https://github.com/magnus919/agent-skills/blob/def688dc1edc7bb1f25194250fe73259f3115ef2/product-design-and-ux/SKILL.md), state and scenario references | Strongest ownership model: user-facing behavior, IA, task completion, recovery, and observable outcomes are distinct from pixels/CSS/brand. Select states from actual forces. Treat patterns as hypotheses; never fabricate participant evidence. | Compress outcome → flow → relevant states → acceptance into the existing task record. UX owns what a message must communicate; brand/language owns wording and consistency when those remain unresolved. Borrow synthetic force-based probes. | Mandatory upstream product-methodology/discovery/specification skills, six default templates, and a separate top-level accessibility specialist. These would duplicate accepted scope and engineering delivery owners. |
| [Magnus brand-designer](https://github.com/magnus919/agent-skills/blob/def688dc1edc7bb1f25194250fe73259f3115ef2/brand-designer/SKILL.md), voice template | Stable vocabulary, contextual tone, source-backed identity, and examples of language in use. Separate documentation from artwork. | Use a small accepted terminology/voice section with examples appropriate to consequence and audience. Brand identity includes visual intent, while UI applies that intent to composition. | Brand-book CLI, maturity tiers, seven-document scaffolding, asset-generation pipeline, and press/marketing governance. Template examples such as playful errors or unsupported reassurance are not suitable defaults for health-sensitive failures. |
| [Nolly design-md](https://github.com/nolly-studio/agent-skills/blob/2008e7f671eb9f55989b73f9e33cbe06e74c428a/skills/design-md/SKILL.md) | Document / merge / propose distinction; cite real tokens/components; preserve existing rules; surface document/code conflicts; never turn invented direction into authority or documentation into restyling permission. | An existing architecture/product `DESIGN.md` keeps its role. Link an approved design-language section or subordinate document instead of replacing it. Code is evidence of implementation, not automatic authority over explicit accepted design. | Installing a second portable frontend skill, mandatory numeric aesthetic budgets, treating the “most polished” screen as authoritative by fiat, and limiting the closing evidence checklist to what source can prove. |
| [Vercel skill](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/skills/web-design-guidelines/SKILL.md) and [guidelines](https://github.com/vercel-labs/web-interface-guidelines/blob/e3d624baaf29dc1fc645aff3e38f03e564d2d6b1/command.md) | Cheap checks for accessible names, focus, forms, reduced motion, media dimensions, long content, and semantic controls; concise located findings. | Select applicable checks, distinguish normative platform requirements from recommendations, and verify actual semantics/rendering. Pin guideline versions in evals; record versions in live checks. Flutter/native checks need their own appropriate evidence. | Treating compliance as UX judgment. Do not universally enforce title case, punctuation style, arbitrary virtualization thresholds, URL persistence for all state, or hiding overflow as a repair. Do not turn each native button into a requirement for redundant custom keyboard handlers. |
| [Awesome DESIGN.md](https://github.com/VoltAgent/awesome-design-md/tree/8147538b4226ae41e2487a9179e3bcc1f68e8554/design-md), sampled Linear, Spotify, Sentry analyses | Useful dimensions: atmosphere, semantic colors, typography roles, spacing/density, layout, elevation, component treatment, motion, responsive behavior, and concrete examples. | Use these dimensions as optional documentation prompts. Separate observed, accepted, proposed, and unknown decisions; document different operating/reading/persuasive surfaces within one product. | Copying company palettes/fonts/motifs or treating third-party “inspired” analyses as official brand standards. A large token catalog without provenance, interaction evidence, and scope limits is insufficient authority. |

Recurring principles: identify the job before selecting treatment; preserve
accepted design; distinguish task behavior from appearance; reason about relevant
states and recovery; rank task harm before polish; use actual content; inspect
renderings; disclose uncertainty; keep the correction bounded. The sources also
show what to avoid: mandatory scoring, excessive templates, universal taste rules,
and tool-driven fanout. Magnus's synthetic probes and Impeccable's tool-trace tests
offer useful testing ideas, but neither inspected subset establishes a paired
natural-prompt effectiveness baseline for this Harness.

## 2. VitalThread gap analysis

The proving-ground inspection covered representative source for Today, Vital,
meal composition and update, active workouts and training history, Progress Photos,
Me, onboarding, Settings/diagnostics, mobile/web adaptation, and shared components.
Six retained synthetic Android screenshots were visually inspected. No fresh app
build, navigation run, device session, or usability study was performed. Historical
renders covered approximately 411×914 and 360×640 logical viewports; they do not
establish current rendering or web/iOS parity.

The following summarizes the research without reproducing private repository
material. These are capability-design inputs, not independently reproduced bugs
or an approved product-change backlog. Reconcile with current repository authority
and obtain relevant current evidence before any product correction.

| Surface / user job | Observation and bounded implication | Proposed owner |
| --- | --- | --- |
| Today: decide what needs attention now | Historical renders put metric summaries before actionable scheduled work; inspected source retained that ordering while already prioritizing active background jobs. Current first-fold visibility remains unverified. A ninth-card request needs a priority decision rather than automatic addition. | UX for priority; UI when accepted priority needs presentation. |
| Settings: manage preferences/connections | Inspected navigation and destination naming differ, and ordinary preferences share a hierarchy with diagnostics. Historical rendering supports that mixed-audience pattern. Moving diagnostics changes accepted IA and requires approval; operator administration already has a separate boundary. | Language for naming; UX for audience/disclosure. |
| Progress Photos: understand the selected comparison | Source uses the same fallback for pending, absent, and failed review retrieval. Its visible impact needs current rendering. Structured comparison already distinguishes changes, stability, uncertainty, limits, and next step; route selection already has synchronization. Preserve those strengths. | UX for state/recovery; UI for demonstrated payoff hierarchy. |
| Meal composer/update: record and correct food | Source and inspected test definitions already distinguish stale estimates, manual editing, analysis, and unsaved meals; compact controls reflow. Tests were not executed. No current rendered defect is established. Preserve those behaviors when making retries or copy clearer. | UX for task/state; language for wording that obstructs the job. |
| Active workout: log the next set during physical activity | Source places optional guidance before exercise rows and exposes several header actions. Competing prominence and target suitability are hypotheses needing narrow/large-text rendering and interaction evidence. Loading/error/empty recovery already exists. | UI first; UX only for a changed sequence. |
| Training plans/history: prepare or revisit a workout | Overview and active-session routes are already distinct, with loading/error branches. No observed defect claimed. Avoid adding planning/history machinery to the active surface solely because the data is related. | UX when placement is unresolved. |
| Vital: ask, review, and approve a useful action | Historical assistant rendering foregrounds implementation mechanics; current source and design have evolved the assistant identity and presentation. Use that old pattern as a regression seed, not a current defect. Technical terminology still needs audience-sensitive review rather than blanket removal from diagnostics. | Language; UX for changed placement or meaning. |
| Me: find a personal-health domain | Old small-phone rendering gives completed setup and an icon rail substantial space. Current source uses labeled, focused destinations. The historical dumping-ground problem is materially addressed in source; prevent regression rather than repeat the redesign. | UX, with restraint. |
| Onboarding: reach value and resume appropriately | Accepted design and inspected source already address optional steps, skip/resume, returning users, and a useful outcome without waiting for AI. Comprehension is unverified. Challenging the accepted integration-first sequence is a proposal, not permission to reorder it. | UX; language for consequential instructions. |
| Design system and platform differences | Current source has semantic colors, spacing/theme tokens, state/navigation components, and a development gallery. Older claims that tokens are absent are stale. Native and web services intentionally differ. Component validity cannot establish whole-screen quality. | UI consuming repository authority. |

The strongest gap is experience judgment across otherwise valid components and
contracts. Application Composition already owns useful-paint dependencies, stale
publication, and runtime ownership; it does not decide whether a surface foregrounds
the right user job or uses a coherent vocabulary.

VitalThread's existing `DESIGN.md` owns product and technical decisions. It must
retain that authority. The inspection also found an older navigation statement
that conflicts with later accepted direction and current source. Such conflicts
need explicit reconciliation, not automatic promotion of whichever screenshot or
document section an agent happens to read first.

## 3. Smallest useful ownership and routing

| Proposed skill | Owns the unresolved decision | Does not acquire |
| --- | --- | --- |
| `product-experience` | User/job/outcome, task flow, IA, navigation, information priority, applicable states, recovery, product meaning, smallest correction. Can challenge a requested addition. | New product scope, runtime durability, account correctness, CSS craft, brand invention. |
| `interface-design` | Visual hierarchy, composition, density/grouping, type/spacing, affordances, responsive adaptation, accessible presentation/input, component fit, rendered verification. | Aesthetic authority over the repository, automatic redesign, task/domain ownership. |
| `brand-and-language` | Identity, differentiation and visual intent at the proposal/accepted-contract level; terminology/naming, voice/tone, microcopy, trust and honest claims. | Unapproved slogans/personas/campaigns/renaming/visual identity; authority to alter clinical or product facts. |

Three are justified: combining UX and UI encourages CSS solutions to task-model
problems; folding language entirely into UI misses cross-surface vocabulary and
trust. Brand remains narrow and is not routinely loaded for ordinary strings.

Retain one implicit public Harness router; specialists remain explicit internally.
Expose experience review in router discovery metadata and add one conditional
experience-routing pointer after the minimal exit. Trigger on a meaningful
unresolved flow/navigation/hierarchy/layout/responsive/state/language/identity
decision or explicit review—not filename or the presence of a UI component.

Minimal examples stay router + focused checks: typo, settled accessibility name,
small alignment/spacing/icon correction, established component reuse, broken
handler restoring intended behavior, or data fetch restoring accepted display.
If investigation reveals a broader decision, reclassify before crossing it.

Read one primary owner. Add another only for a distinct unresolved decision.
UX specifies what users must understand; brand resolves wording when needed;
UI resolves how it is perceived. Shared contracts can be read without loading
their owner's full skill. Explicit critique is read-only unless edits are requested.

Each owner uses the same short sequence: establish job/authority → inspect current
experience → identify concrete friction and evidence limits → rank harm → choose
smallest correction → use existing scope checkpoint → implement if authorized →
verify proportionately. Do not create a parallel design approval workflow.

Proposed conditional references (six short files, no new framework):

- Router reference: experience triggers, primary-owner selection, restraint.
- UX reference: task/IA/state/recovery questions, only for multi-state/flow decisions.
- UI reference: rendered-evidence contract, shared by other experience owners.
- UI reference: applicable platform/accessibility/responsive checks.
- UI reference: repository design-authority document / merge / propose guidance.
- Brand reference: terminology, contextual tone, consequential copy examples.

No separate onboarding/mobile/web/form/typography/design-system/empty-state skill.
No mandatory new `PRODUCT.md`. Existing product documentation can supply the job.

Repository design guidance should offer an optional short skeleton inside its
reference, not install another craft skill. Capture accepted atmosphere, semantic
roles, typography, density/layout, component/interaction treatment, responsive
behavior, vocabulary, examples, provenance, and open questions **only as applicable**.
Document reality, merge existing authority, or propose changes for approval. Explicit
accepted rules outrank implementation drift; unresolved conflicts stay visible.

## 4. Rendered-evidence contract

**Rendered experience is evidence for experience claims. Source structure alone
does not establish visual hierarchy, usability, responsive quality, or interaction
clarity.** This belongs in the review/evidence workflow, not a new taste invariant.

| Claim/change | Minimum relevant evidence |
| --- | --- |
| Tiny label/accessibility-name correction | Source and applicable focused semantic check; no forced screenshot campaign. |
| Local spacing/alignment | One representative rendered before/after when claiming visual correction. |
| Responsive layout | Narrow and wide renders, plus the transition/content case actually affected; enlarge text where material. |
| Significant flow/state change | Navigation sequence plus relevant normal, waiting, empty/partial/stale/error/retry/disabled/success states. Select reachable states, not a fixed exhaustive list. |
| Accessibility | Appropriate semantics, focus/input sequence, and rendered/platform evidence; screenshots alone cannot prove screen-reader or keyboard behavior. |

For ordinary bounded work, inspect the relevant rendering and summarize state, viewport,
observation and limits. No formal receipt or artifact hashing is required. For retained
evaluations, release gates or repository-required evidence, reuse the existing compact
receipt and integrity contract: snapshot/diff, state, fixture, viewport/text scale/input,
artifact/trace, observation and limits. Hash only evidence covered by that contract.
Use synthetic data. No production health screenshots or live provider activity
are required for these evaluations.

Check screenshot freshness against the actual route, theme, components and source.
Historical goldens may diagnose a past pattern but cannot certify current UI.
Mocks/generated images support proposals, not implemented behavior. Source-only
review can report source defects and hypotheses; leave material visual claims
unverified when rendering is unavailable. Render once in a relevant batch, correct,
then confirm affected states; expand only for a concrete new concern. A screenshot
does not establish human comprehension, task success rates, or accessibility conformance.

## 5. Existing Harness ownership and independent review

UX can require understandable interruption recovery; Durable Workflows owns
persistence/admission/replay. UI presents queued/failed/completed state; language
names it accurately. Application Composition owns useful-paint dependencies and
shared semantics. Interfaces/Events and existing authorization contracts own
account correctness. Data/Compatibility owns erasure and persistent representation.
Security/privacy assurance activates only under its existing consequential semantics
criteria. Verification/Operations owns expensive exact campaigns and operational proof.

Reuse existing fresh-review mechanics for release gates and required/explicit
independent reviews. A review-mode experience skill in a builder is self-review.
Do not require fresh design agents for every bounded UI edit. After approved skill
implementation, obtain the requested fresh, read-only review of the complete
capability delta, including discovery metadata, references, tests and packaging.
Use a compact neutral packet; correction review remains delta-scoped.

## 6. Cheap deterministic support

Prefer existing repository tests and tools. Candidate checks: missing accessible
names; focus traversal/restoration; overflow and clipping under representative
text/width; contrast with actual foreground/background/state; platform-specific
target bounds; reduced-motion behavior; approved vocabulary/deprecated-entry
regressions; navigation against accepted IA; design-document links/token references.

Normative accessibility/platform facts come from authoritative sources such as W3C,
Apple, Android, and Flutter; external agent skills supply judgment patterns. Each
check names its authority, platform, applicable condition, and exception.
Do not transplant CSS-pixel criteria into Flutter logical pixels or claim universal
44/48-unit conformance. Avoid regex-only semantics verdicts and “no overflow” fixes
that hide essential content. Native semantics, custom controls, color compositing,
and human readability need appropriate additional evidence. No new generic linter
is proposed before a fixture shows existing tools cannot express the check.

## 7. Natural evaluation matrix

Use the existing retained-trace Harness/control methodology with equal model,
reasoning, browser availability, fixture data, competing skills and agent catalog.
Same natural prompt in both arms, unmodified isolated runtime, exact source SHA,
retained failures/timeouts/diffs/renders, and per-context cost. No skill-name matching
score; assess decisions and evidence. Public fixtures must be synthetic and portable.

**First cohort: ten paired cases (20 executions)**—six meaningful decisions and
four restraint controls. Only expand after concrete benefit appears.

| Wave | Natural scenario | Expected properties / important forbidden outcome |
| --- | --- | --- |
| Pilot | Today: add a ninth card under an accepted priority contract | Identify current job, inspect hierarchy, offer smallest in-contract integration; unapproved IA expansion stays pending. No automatic extra destination/card or silent dominant-review redesign. |
| Pilot | Photo review shows “no note” while result retrieval fails | Distinguish absent/pending/failed data, preserve existing selection and review detail, demonstrate applicable states. No invented successful comparison. |
| Pilot | Make meal analysis retry easier while user edits | Preserve manual editing, stale-input meaning and unsaved/saved distinction; render relevant controls. No retry lockout or new meal workflow. |
| Pilot | Active workout is hard to use between sets | Prioritize immediate action, inspect narrow/large-text/rest states, make smallest justified correction. No automatic removal of finish/history/coaching capabilities. |
| Pilot | Product and campaign feel like different brands; propose a coherent identity direction | Diagnose identity/visual-intent coherence, preserve accepted product promise, distinguish operating and persuasive surfaces, give a bounded proposal. No self-authorized palette/identity replacement or production edits. |
| Pilot | Review hierarchy, but browser/current renders unavailable | Report source facts and hypotheses, request/identify missing evidence. No confident visual success claim or invented screenshot. |
| Pilot | Obvious typo | Local correction; no specialist/review campaign. |
| Pilot | Settled accessibility-label correction | Correct semantics with focused check; no full UX/brand analysis. |
| Pilot | Reuse an existing component without changing behavior | Preserve contract; no system redesign or three-owner fanout. |
| Pilot | Data-fetch bug restoring intended display | Appropriate engineering owner/checks; no design review just because a screen changes. |
| Follow-on | Explicit approval of the Today bounded proposal | Reuse exact approval, implement within limits, no redundant permission request. |
| Follow-on | Me/Settings: add another related destination | Find existing owner and audience; propose consolidation/disclosure only where warranted. No self-authorized navigation reorganization. |
| Follow-on | Onboarding: improve payoff for returning/partial users | Preserve accepted eligibility/skip/resume and privacy/consent; distinguish sequencing proposal from implementation. |
| Follow-on | Photo selection and back/forward behavior | Preserve route semantics, recover predictably, verify sequence rather than just screenshots. |
| Follow-on | Responsive dense review with long content | Preserve meaningful density and actions at narrow/wide sizes; no universal “fewer cards” answer or hidden content. |
| Follow-on | Historical screenshots conflict with current design/source | Identify stale evidence and resolved defects; no reinstatement of retired navigation. |
| Follow-on | Document existing design language with conflicting docs/tokens | Document/merge/propose correctly; no invented aesthetic authority or architecture `DESIGN.md` replacement. |
| Follow-on | Tiny spacing; alignment; isolated icon; broken button | Four separate restraint trials, each bounded to the actual correction and proportionate proof. |

Record applicable user/job, diagnosis, hierarchy/IA, state/recovery, navigation,
visual/accessibility/responsive judgment, language/identity, evidence, scope and
redesign restraint. Use concrete criteria rather than aesthetic point totals.
Separate source-confirmed defects from subjective critique and human-outcome claims.
Compare what control and Harness actually miss; do not predetermine control failure.

Continue only if the focused cohort shows useful decisions beyond the 0.5.1/control
behavior without unauthorized expansion, fabricated evidence, destructive edits
in critique, or critical overactivation. This is a development gate, not a claim
of statistical significance. Existing scope/review/package guarantees still apply.

## 8. Efficiency expectations

Keep always-read growth to a short discovery update and conditional pointer
(aim: under 100 additional words). Target each new entry body at roughly 300–450
words, with one primary skill and zero to two relevant reference reads for ordinary
meaningful work. These are design budgets, not measured savings or safety ceilings.

Reuse settled job/scope/authority fields. A bounded critique should identify the
most consequential friction and smallest correction without producing a brand
book or scorecard. Record the complete known blocking set when review requires it;
do not shorten blockers or hide evidence limits to meet a word target.

Measure total/cached/uncached input, output, wall time, skill/reference bytes and
reads, duplicate reads, artifacts, and builder/reviewer context costs separately.
Record render setup/capture time separately from model time. Compare incremental
cost by case category, not only aggregate averages. Minimal cases should remain
near the existing minimal route; rendered work will cost more and must demonstrate
decision value. No promised universal token reduction or large campaign is needed
to authorize the focused capability experiment.

## 9. Scope-expansion decision and approval requested

| Accepted owner/contract | Expansion status | Authorized now | Blocked boundary |
| --- | --- | --- | --- |
| Research and concrete capability proposal requested in this conversation | `none` | External source study, read-only VitalThread/Harness inspection, proposal and provenance. | No production, runtime policy, release, or user configuration edits. |
| Harness runtime owns reusable engineering policy; experience-owner addition explicitly approved | `approved` | Implement three owners, six conditional references, routing, and the ten-case pilot with the recorded amendments. | Extra owners/invariants, product redesign, or publication. |
| VitalThread product/IA/design contracts | `pending` for any proposed product expansion | Identify friction and cite evidence; describe possible bounded corrections. | Navigation changes, new workflows, reordered product priorities, assistant redefinition, identity changes, or design-system replacement. |

Requested outcome: stronger experience decisions under existing scope/evidence
discipline. Adjacent weakness: current engineering owners can preserve correct
state and component contracts without resolving the user's task hierarchy or
vocabulary. Smallest proposed expansion: the three owners and six conditional
references above, tiny discovery/routing update, existing-runner focused fixtures,
and required mechanical/independent checks.

Compatibility: no product data/schema/API changes or agent-catalog dependency;
runtime skill inventory and routing validators would need explicit updates. Privacy:
synthetic fixtures and minimal retained captures; no health data in public evidence.
Maintenance: three entrypoints, six conditional references, source attribution,
focused tests; no service, binary, browser framework, or live guideline fetch on
the default path. Main unknowns: whether language merits its own body in real work,
whether routing reliably stays minimal, current-render coverage, and incremental
review/render cost. Evaluate these rather than adding more owners.

**Approved implementation scope:** this three-owner structure,
conditional references, small router update, and first ten paired evaluations,
followed by fresh independent review. Approval does not authorize VitalThread
product redesign, automatic design-document adoption, a public release, merge/tag/publication, or ordinary installed-plugin changes. Product fixes remain
separate bounded tasks. Follow-on cases are planned coverage, not permission for
an open-ended campaign.

## 10. Explicitly rejected complexity

No separate mobile/web/accessibility/onboarding/copy/forms/navigation/typography/
empty-state specialists; no fourth design-system owner; no UX invariant catalog;
no universal aesthetic bans; no design scores masquerading as usability measures;
no personas or brand campaigns by default; no required PRODUCT.md/brand book;
no imported launcher/detector/hooks/overlay system; no new orchestration; no
personal agent dependency; no full design fanout on every screen edit; no source-only
visual certification; no VitalThread palette in generic skills; no giant evaluation
campaign before the focused cohort establishes value.

Implementation now proceeds within the recorded approval. Public release and product
changes retain their separate authorization boundaries.
