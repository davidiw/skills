# Artifact and Physical Proof

## Evidence classes

- **Modeled:** a design, calculation, or static assertion.
- **Simulated:** behavior observed in a simulator or synthetic environment.
- **Host-validated:** real code against fakes, fixtures, or emulators.
- **Provider-validated:** observed against the real external service.
- **Device-validated:** observed on named hardware and software versions.
- **Physically validated:** fit, power, thermal, motion, timing, or another
  real-world property directly measured.
- **Production-observed:** bounded telemetry from the deployed environment.

Name the class. Never upgrade one class into another by wording.

## Generated artifacts

Record authoritative source, generator and version, exact command, input
revision, output digest, and freshness check. Publication uses immutable
versioned artifacts; a mutable alias may move atomically only after the target
is valid.

Generated files are stale when their authoritative source or generator changes,
even if a superficial comparison still passes. Tests must deliberately alter
the source or output and prove the freshness check fails.

Hardware or provider capabilities are explicit. A fake proves consumer behavior
for supported/unsupported results; only real evidence proves the device,
provider, physical, power, privacy-indicator, or lifecycle claim.
