# Candidate semantic calibration v0.2.3

**Status:** candidate evidence record; not production authorization.

## Bound bundle

This run is bound to the exact semantic bundle fingerprint
`256ba053b174a054226301f1b493e0e0c8f9f50e9f2976a72b8045dbf6ed6131`.
It uses `candidate-builder-semantic-v3`, `candidate-state-resolver-v3`, and
`candidate-alignment-resolver-v3`.

The former v1 calibration policy is superseded, rather than rewritten, because
its bundle predates scoped context, counterweight-aware audit, and policy-driven
alignment behavior.

## Design-set result

| Check | Result |
| --- | --- |
| Anonymous design cases | 8 / 8 loaded |
| Normalized profiles | 8 / 8 unique |
| Maximum primitive similarity | 0.75 |
| Frozen threshold | 0.75 |
| Threshold failures | 0 |
| Signature / Dynamic / Fate activation | 0 |

The threshold was recorded after this frozen bundle run. Holdout fixtures were
not used to change mapping rules or the threshold.
