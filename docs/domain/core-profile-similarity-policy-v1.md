# Core Profile Similarity Policy v1

**Stage:** C4 — Calibration Review
**Status:** C4b candidate policy frozen for the named D1 Bundle on 2026-09-18; no production approval

## Purpose

`Pairwise Profile Similarity Matrix` detects profile collapse without requiring
different prose. It compares normalized Core Profiles generated from separate
anonymous cases using the same approved Semantic Bundle.

## Required components

Each matrix cell contains values in `[0, 1]` for:

| Component | Candidate comparison |
| --- | --- |
| `weighted_primitive_overlap` | weighted Jaccard overlap of Primitive ID plus resolved direction, weighted only by approved salience and evidence stability |
| `signature_primitive_overlap` | overlap of Primitive membership in source-local Dominant Signatures, retaining source system |
| `dynamic_family_pole_overlap` | overlap of approved relation-family IDs and declared poles; empty sets are `not_applicable`, not 1.0 |
| `fate_theme_overlap` | overlap of approved Fate Theme basis references; absent themes are `not_applicable`, not evidence of sameness |

The matrix records component applicability and case pair. The overall score
combines only applicable components using versioned policy weights. It never
uses report sections, archetype names alone, or opaque unique-ID counts as a
substitute for structure.

## C4b candidate threshold policy

For Bundle fingerprint
`2e09e801b58fbd18cd5fa8b53a15041144cd6c1830b91d986473e476a161cfcd`:

- `weighted_primitive_overlap` has weight `1.0`, using equal Primitive and
  source evidence-stability weights of `1.0`.
- Signature, Dynamic, and Fate components have weight `0.0` because their D1
  policies are disabled; their cells remain `not_applicable`.
- The Design Set contrast-pair maximum is `0.75`; no D1 exceptions exist.

The matrix is candidate-only and cannot support production promotion by itself.
Any semantic asset change invalidates the fingerprint and returns evaluation to
`CALIBRATION_POLICY_GAP` until the candidate policy is recalibrated.
