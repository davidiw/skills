# Reviewable Commit History

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
