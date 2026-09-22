# Core Portrait Semantic Presentation v0.3.5

## Boundary

Candidate Core Profile remains a `primitive_only` preview. This release does
not enable production inference, chart calculation, relation dynamics, or an
unbounded narrative route.

## Layer contract

- The semantic bundle fingerprint is `256ba053b174a054226301f1b493e0e0c8f9f50e9f2976a72b8045dbf6ed6131`.
- The presentation bundle is fingerprinted independently and is stored on each
  rendered Core Portrait.
- Primitive presentation declares separate `high_expression` and
  `low_expression`; user text resolves direction before rendering.
- Presentation changes are not semantic evidence and cannot alter normalized
  candidate profiles.

## Runtime contract

`build-core-profile` consumes `deterministic-chart-facts-v1` JSON produced by
an already qualified external capability. It does not parse birth input or
calculate a chart. `NormalizedBirthTime.fact_mode` solely determines fact
scope: `stable_only` rejects hour pillar, ascendant, MC, houses, and
house-placed facts.

## Verification

The package verifier reads the actual project distribution name from
`pyproject.toml`, installs a freshly built wheel with force-reinstall, and
exercises the installed CLI. CI runs that verifier separately on Python 3.11.
