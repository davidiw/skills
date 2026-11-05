---
name: hardware-qualification
description: Plan and assess first power-up, physical measurements, hardware experiments, and evidence for a minimum production circuit. Use for bench qualification and physical performance or reliability questions; not for circuit design alone or a claim that unmeasured hardware passed.
---

# Hardware Qualification

Own the physical experiment and its interpretation, including first power-up and
qualification of a proposed minimum production circuit. The hardware design owner
retains circuit and manufacturing decisions. Apply relevant
[invariants](../../references/invariants.json) and
[precedence](../../references/precedence-and-exceptions.md); consume verification
and operations' [artifact and physical proof](../verification-and-operations/references/artifact-and-physical-proof.md),
[evidence contract](../verification-and-operations/references/evidence-contract.md),
and, for actions, [operator interface](../verification-and-operations/references/operator-interface.md).
Those references own evidence classes and authorization, not this skill.

1. Identify the intended claim, operating conditions and available board,
   equipment and operator skills. Ask early about material goal or equipment
   tradeoffs while continuing independent design and preparation. Implement
   routine choices already accepted; do not repeatedly reopen settled selections.
2. Plan first power and a reproducible experiment matrix using
   [bench and production](references/bench-and-production.md). Run available
   static checks before energizing; reuse existing explicit flash and power
   authorization, and surface a missing action boundary where necessary.
3. Record configurations and observations, distinguish measured results from
   pending work, and trace each qualification control to an experiment. Use the
   relevant domain owner's performance methodology for camera latency, drops and
   endurance where applicable. Separate board and harness signal-integrity limits
   from panel or protocol limits.
4. Use evidence to propose a minimum production circuit and identify remaining
   operating-corner, environment, assembly, yield, reliability and applicable
   compliance qualification. A prototype may be fabricated before runtime
   performance measurement when circuit, connector and process safety are already
   established. Do not claim production release or physical proof for pending tests.
