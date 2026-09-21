# C4b Calibration Decision Record v1

**Stage:** C4b — Candidate numeric calibration
**Status:** candidate policy approved for the named D1 Bundle on 2026-09-18; no production approval

## Evidence reviewed

- D1 candidate-only Builder and isolated candidate assets.
- Eight anonymous Design Set fixtures under
  `tests/fixtures/core_profile_calibration/design_set/`.
- Determinism, source-isolation, unknown-time, and candidate-differentiation
  checks in the project test suite.

## Raw outcomes

1. All eight Design Set cases create distinct normalized candidate Profiles.
2. The `cross_system_tension` case retains `P002 = mixed` rather than collapsing
   the two source systems into one direction.
3. The `unknown_birth_time` case suppresses astrology candidates even when its
   fixture supplies an aspect pair.
4. The D1 Dynamic, Fate Theme, and Archetype policies are disabled; no such
   conclusion was produced.
5. The Pairwise Profile Similarity diagnostic preserves Primitive-state pair
   inputs but reports `CALIBRATION_POLICY_GAP` instead of an unapproved score.

## Frozen candidate decisions

- Semantic Bundle fingerprint:
  `5d3cd30fd19a871fcf3a76ae6698cd856b5e24f14e7a0aeb31185cbea0ebcac5`.
- All six Primitive salience weights and both source evidence-stability weights:
  `1.0`.
- `weighted_primitive_overlap`: `1.0`; unavailable Signature, Dynamic, and
  Fate components: `0.0`.
- Default Design Set contrast-pair maximum similarity: `0.75`; no D1
  exception.
- `unsupported_activation_frequency: 0`.

The Holdout Set remains inaccessible for tuning.
- The Holdout Set remains inaccessible for tuning.

## Gate B requirement

This approval applies only to the exact candidate Bundle and policy above. Any
candidate semantic asset change invalidates the fingerprint and returns the
policy to pending calibration before promotion, a default route, or Holdout
evaluation.
