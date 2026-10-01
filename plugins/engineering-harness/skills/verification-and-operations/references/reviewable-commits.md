# Reviewable Commit History

## PR delivery

When the user or repository authorizes PR delivery, including a standing user
preference, submit a PR for implementation work. Honor explicit exceptions such
as local-only work, no commits, no PR, or a separately selected integration path.
Read-only investigation or review does not require an invented change or PR.

Once the first coherent commit is reviewable, push it and open the PR before
expensive verification. Run fast, relevant checks first when practical. Include
the scope, known limitations, and completed, pending or blocked checks so a
coordinator can give feedback while further verification runs. Use a draft when
the implementation itself is incomplete; pending tests alone do not require a
draft. Update the same PR as the work progresses and include its URL in the final
handback. If publication fails, report the concrete blocker and retain the branch
for retry rather than claiming submission.

Treat expensive tests as opportunistic for early PR feedback: their completion
does not gate opening the PR. Required verification and review still gate final
acceptance, integration and release. Bind each result to the tested revision and
never describe pending, blocked or local-only checks as passing CI. PR submission
does not authorize merge, deployment, artifact publication or release changes.

## Final history review

Before final review or integration, inspect the complete diff against the branch
base and the final commit sequence. Remove unintended, exploratory, unrelated or
formatting-only changes. Each commit should express one coherent behavior or
contract, include its associated checks/evidence, leave the repository consistent,
and be independently understandable and, where practical, revertible.

Order prerequisites before consumers. Squash fixups into the behavior they correct;
split materially independent changes. Use messages describing resulting behavior
and rationale. Avoid both per-file micro-commits and an opaque multi-owner squash.
Keep independently important behavior changes and meaningful review information
visible; history should explain the result without requiring development chat.

Do not rewrite shared/published commits without authorization. Clean unpublished
feature work when repository policy permits; otherwise preserve history and use
the normal repository integration policy. Reuse explicit restructuring approval.
After rewriting, run relevant checks on the final history and bind final review
and evidence to its **new exact revision**. Review the whole branch diff, meaningful
commit sequence and cross-commit compatibility/migration assumptions. A later
finding belongs in its owning commit when practical, followed by affected checks
and delta review. Commit cleanup never authorizes merge, tag or publication.
