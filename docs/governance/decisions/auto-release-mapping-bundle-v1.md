# Autonomous Decision: Active Release Mapping Bundle v1

- Outcome: `CLOSE_ZERO`
- Authority: `delegated_autonomous_executor`
- Mode: `AUTONOMOUS_COMPLETION`
- Asset: `ACTIVE-RELEASE-MAPPING-BUNDLE-V1`
- Asset fingerprint: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`

The v0.4.0 release activates an explicit empty Mapping bundle. No reviewed
PRIMARY_EVIDENCE or Mapping is available, so admitting a non-empty caller
record would violate the release boundary. The runtime must therefore resolve
all six Core primitives to `unknown` and reject any modified or non-empty
bundle. A future non-empty bundle requires a new schema, evidence chain,
decision, calibration/holdout record, and release.
