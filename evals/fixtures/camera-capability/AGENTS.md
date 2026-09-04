# Camera Fixture Rules

- Shared firmware consumes contracts from `firmware/components`.
- Hardware behavior belongs in `firmware/ports/<model>` and composition selects
  the model port.
- Model S3 supports the requested physical capability. Model P4 does not.
- Host fakes prove contract behavior. Device and physical evidence remain
  separate and pending until run on named hardware.
- Implementation does not authorize firmware installation or publication.
