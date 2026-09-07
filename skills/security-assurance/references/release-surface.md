# Release-Surface Security Assurance

Start from the candidate system and deployment shape, not the last diff. Record
the snapshot, intended launch boundary, principals, assets, trust assumptions,
and environments that can actually be inspected. Discover surfaces from route
registrations, gateway/proxy configuration, middleware, jobs, infrastructure,
dependency manifests, and operator tools. Reconcile documentation with code.

## Inventory before investigation

Account for each applicable surface below. These are discovery prompts, not
requirements to invent components the system does not have.

| Surface | Questions to carry into the coverage matrix |
| --- | --- |
| Authentication and sessions | Where are tokens/sessions issued, exchanged, refreshed, stored, revoked, or expired? |
| Authorization and object ownership | Which principals can reach each object/tenant, and where is ownership enforced? |
| Admin, support, impersonation | Which privilege transitions, debug endpoints, and support tools bypass ordinary paths? |
| OAuth and provider callbacks | How are state, audience, purpose, account binding, replay, and redirects validated? |
| Uploads, media, exports | Which parsers, storage permissions, content handling, and disclosure paths are exposed? |
| Webhooks | How are origin, signature, replay, and effect authority established? |
| AI and tool execution | Which untrusted inputs can select actions, parameters, credentials, or destinations? |
| Outbound fetch and file access | Can inputs reach internal network services or escape a storage/path boundary? |
| Input parsing and injection | Where does input enter queries, templates, commands, interpreters, or deserializers? |
| Browser boundaries | Which cookies, origins, redirects, CSRF/CORS/CSP controls, and embedding assumptions apply? |
| Secrets and IAM | Which runtime/deployment identities have access, and how are secrets provisioned and revoked? |
| Abuse and cost amplification | Which rates, quotas, uploads, fanout, provider calls, and expensive operations are bounded? |
| Workers and jobs | Who can admit/replay work, with what authority and resource limits? |
| Backup and restore | Which privileged paths can restore data, credentials, or obsolete authority? |
| Legacy and shadow surfaces | Which deprecated routes, alternate hosts, test/admin handlers, and bypass adapters remain reachable? |
| Dependencies and supply chain | Which manifests, lockfiles, build actions, artifacts, and privileged dependencies enter the release? |

Create one row per concrete surface with source location, reachability/principal,
owner, trust boundary, threat hypothesis, planned proof, and coverage status.
Mark absent surfaces not applicable with evidence; mark unknown deployment/IAM
facts unavailable. A route's absence from documentation does not prove it absent
from the release.

## Ownership and delegation

These rows identify attack surfaces; they do not transfer every underlying
analysis to security assurance. Security owns the threat hypothesis and security
consequence. Deep capacity/resource analysis stays with architecture foundations,
recovery with the relevant durable/data owner, and operational/deployment proof
with verification and operations. Economic-abuse analysis needs a named domain
owner for workload, cost, and acceptable-loss assumptions.

When a row requires that depth, record the owner, bounded question, needed evidence,
and handoff status. Delegate within the authorized campaign when a suitable
context is available; otherwise leave that coverage pending. Reconcile the
returned evidence at the security boundary without absorbing the entire owner's
workflow into this review. An inventory discovery does not authorize remediation
or expansion of implementation scope.

## Challenge and reconcile

Prioritize high-impact reachable paths, privilege transitions, and alternate
routes that bypass common controls. Trace selected hypotheses through the actual
enforcement owner, including concurrent changes and recovery. Use synthetic
checks where possible; live probes require the user's existing target/scope
authorization. A repository review alone cannot prove deployed IAM, edge
configuration, or current dependency advisories; identify the missing evidence
and use appropriate authoritative sources when those claims are requested.

Update the matrix as new surfaces appear. Return findings plus every row's final
disposition, remaining evidence, and release implications under the shared
[`assurance review contract`](../../../references/assurance-review.md). Neither a
quiet scanner nor findings confined to the latest diff closes the inventory.
