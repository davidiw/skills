# JLC sourcing guidance: bounded checks

Tested source: unreleased Hardware Engineering 0.11.0, skills PR #15 commit
`e4daa1f`. `python3 -m unittest discover -s tests` passed 147 tests;
`python3 scripts/validate_package.py`, the official skill-creator
`quick_validate.py` for Hardware Engineering, and `git diff --check` passed.
These validate package structure and fixture mechanics, not model judgment.
No standalone official plugin-validator command was available.

A fresh reviewer received only the hardware skill and an isolated synthetic
fixture, without expected outcomes or builder reasoning. It identified the
orderable-versus-physical-stock distinction, calculated batch plus loss, retained
the justified Extended reset part, and put unavailable parts into sourcing
follow-up without assuming consignment. It rejected the placeholder price and
the low-effective-capacitance MLCC, and treated the second Basic capacitor as a
conditional modeled prototype candidate with inrush and physical verification
pending. It made no edits, supplier contact or other external action.

The six-file fixture aggregate SHA-256 is
`7972830bad82f194f73ca84693789dbb5baff22d8f6561e180c8049cd78866b2`, using
sorted relative paths followed by NUL, file bytes and NUL. Individual file
hashes matched the reviewer's original run. The reviewer initially reported
`17fa54790f0bda077e52c74e763803ab0af9e347407a9ae1787f61c38234c8d1` while
incorrectly describing its separators as NUL; it used literal backslash-zero
bytes. The reviewer reran the NUL algorithm and confirmed the hash above.

This is one direct-skill, read-only probe of synthetic data. It does not establish
natural skill discovery, comparative performance against a control, live JLC
stock, a quote, supplier acceptance or physical component qualification.
