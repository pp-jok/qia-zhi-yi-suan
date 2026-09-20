# Template Collapse Policy v1

**Stage:** C4 — Calibration Review
**Status:** C4b candidate policy frozen for the named D1 Bundle on 2026-09-18; no production approval

## Required per-family metrics

For every approved Dynamic relation family, compute across a named test set:

```text
dynamic_family_frequency
evidence_supported_frequency
unsupported_activation_frequency
eligible_case_frequency
```

- `dynamic_family_frequency`: Profiles where the family appears.
- `evidence_supported_frequency`: appearances passing every Dynamic eligibility
  condition in the audit trail.
- `unsupported_activation_frequency`: appearances without complete eligibility
  evidence; the candidate target is zero.
- `eligible_case_frequency`: cases where the reviewed family could legitimately
  have been selected, whether or not it was selected.

Evaluation compares family frequency with eligible-case frequency and evidence
support. It must not cap selected named themes, because a valid family can recur
in a representative population. It must not single out legacy report motifs.

## Collapse conditions

Record `TEMPLATE_COLLAPSE_ERROR` when:

1. `unsupported_activation_frequency > 0`.
2. A Dynamic appears where its relation was not eligible.
3. A Dynamic, Fate Theme, or Archetype lacks required source references.
4. A weak-signal or ambiguous Holdout case gains a topic solely to meet a
   renderer-size target.

The initial candidate policy freezes `unsupported_activation_frequency: 0`.
All Dynamic-family frequency metrics are `not_applicable` while C3 retains an
intentionally empty relation-family set. Future values must be versioned and
justified from a new Design / Calibration run before Holdout access.
