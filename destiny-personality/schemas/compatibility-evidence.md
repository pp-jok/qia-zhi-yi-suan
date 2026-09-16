# Compatibility Evidence Contract

Create one evidence item for every applicable frozen methodology setting.

## Evidence item

Each item requires `config_ref`, `expected`, `candidate_setting`, `evidence_ref`, `status`, and `note`. `status` is `exact`, `unsupported`, `unverified`, or `not_applicable`.

Only `exact` passes an applicable setting. `not_applicable` requires a reason tied to the requested fact mode. Any `unsupported` or `unverified` item rejects that candidate.

## Accepted evidence

Use versioned operation metadata first, versioned official interface documentation second, stable response metadata third, and a reproducible non-sensitive probe only when it proves the specific setting. Tool popularity, reputation, generic accuracy claims, and model memory are not evidence.

## Example

```yaml
config_ref: astrology.core.zodiac
expected: tropical
candidate_setting: tropical
evidence_ref: fixture-operation-metadata:v1
status: exact
note: The versioned test fixture exposes the configured zodiac directly.
```

This example demonstrates record shape only and does not select a provider.

## Failure

Reject a conflicting or unproven candidate with reason `METHODOLOGY_VERSION_MISMATCH`. If discovered candidates exist but all are rejected this way, stop at `METHODOLOGY_VERIFIED` with that code. If no candidate exists for a required category, use `CAPABILITY_GAP`.
