# Candidate CI contract

This repository uses local CI. Before opening or updating a pull request, run
all applicable gates against the final candidate source and retain results bound
to that source. A PCB change requires `make board-ci` (native ERC, DRC, parity,
route checks, tests and export verification). Firmware changes require
`make firmware-ci`. No hosted CI is configured or required in this repository.

The fixture records prior results only; it does not contain runnable sources or
the toolchain. A result for a different revision is historical evidence, not a
pass for the current candidate.
