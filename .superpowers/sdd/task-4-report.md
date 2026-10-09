# Task 4 Report: Product Fixtures, Differentiation Matrix, and Demos

## Scope delivered

- Added a product-quality suite at `tests/test_interpretive_product_quality.py`.
- Added 12 qualification-bound fact pairs under
  `tests/fixtures/interpretive/v060/`.
- Generated five v0.6.0 standard reader demos through the production
  `build-interpretive-report` CLI.
- Added an actual-report topic × system coverage matrix and a differentiation /
  template-collapse review.
- Made no changes to production runtime, rules, report composition, or prior
  task artifacts.

## TDD evidence

### RED

Command:

```text
python3 -m pytest tests/test_interpretive_product_quality.py -q
```

Initial result:

```text
8 failed, 24 errors in 4.32s
```

The failures were the intended missing-product failures: no v0.6 fixture
directory, no five checked-in demos, and no coverage/differentiation documents.
After adding the 12 qualified pairs, the intermediate result was:

```text
6 failed, 26 passed in 6.83s
```

Those six failures were exactly the five absent CLI demos plus the absent
documentation gate.

### GREEN

Focused command after the complete implementation:

```text
python3 -m pytest tests/test_interpretive_product_quality.py -q
```

Result:

```text
32 passed in 5.88s
```

Full regression command:

```text
python3 -m pytest -q
```

Fresh final result:

```text
905 passed in 66.43s (0:01:06)
```

## Complete fixture inventory

1. `bazi-dominated`: 7 Bazi signals and 2 astrology signals; seven reader topics.
2. `astrology-dominated`: 1 Bazi signal and 10 astrology signals; eleven reader topics.
3. `cross-system-agreement`: output and solar-expression evidence converge in the expression section without inventing an exact-topic validation.
4. `cross-system-tension`: reflective Bazi expression and outward astrology expression form a formal tension.
5. `missing-time`: stable-only facts remove the Sun-house claim and expose the omission notice.
6. `practical-builder`: wealth, authority and earth-sign pacing.
7. `relational-connector`: peer, branch-relation and affiliative evidence.
8. `expressive-creator`: output and fire-sign expression evidence.
9. `structured-steward`: authority, relation and long-horizon structure evidence.
10. `reflective-scholar`: seal and water-sign reflective evidence.
11. `adaptive-explorer`: peer/output and air/mutable evidence.
12. `boundary-mentor`: authority, resources and relational-boundary evidence.

All 11 normal complete charts expose at least six reader topics and retain both
Bazi and astrology provenance. Across the matrix, all current v2 rule families
are exercised, including ten-god repetition and all seven core planets.

## Production CLI demos

The production CLI generated these artifacts in `docs/demos/v0.6.0/`:

- `bazi-dominated-standard.json`
- `astrology-dominated-standard.json`
- `agreement-standard.json`
- `tension-standard.json`
- `missing-time-standard.json`

Each was generated with `python3 -m destiny_personality.cli
build-interpretive-report ... --mode standard-interpretive-v1`. The product
suite regenerates every demo into a temporary directory through the same CLI
and asserts parsed JSON equality with the checked-in artifact.

## Product gates and self-review

- **Qualified boundary:** every pair loads through
  `load_qualified_deterministic_facts`; fact and qualification fingerprints are
  non-empty and bound.
- **Differentiation:** title-plus-content reader bodies are unique for all
  12 fixtures. The review does not count audit IDs or fingerprints as semantic
  differentiation.
- **Depth:** all normal complete charts have 7–12 reader-visible topics.
- **Dual-system contribution:** all normal complete charts include signal
  provenance from exactly `bazi` and `astrology`.
- **Required scenario semantics:** signal counts prove the two dominated cases;
  signal composition proves reader-level agreement; the synthesis packet proves
  the formal tension; metadata and missing signal prove time degradation.
- **Traceability:** each report retains rule-bundle, fact and qualification refs;
  every visible section has signal IDs and complete provenance.
- **Reader/audit separation:** the complete reader-visible surface (title,
  sections, limitations and boundary statement) is scanned for raw calculation
  paths. Raw paths remain only in signal provenance.
- **Agreement wording:** because the current audited rules have no same-topic,
  same-direction Bazi/astrology pair, the agreement demo is explicitly reviewed
  as reader-level convergence between creative output and solar expression. It
  is not mislabeled as formal synthesis validation.
- **Scope:** `git diff` review found no production-source modifications and no
  edits to Task 1–3 deliverables.
