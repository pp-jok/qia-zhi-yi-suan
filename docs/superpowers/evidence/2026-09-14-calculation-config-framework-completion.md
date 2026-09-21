# Calculation Configuration Framework Completion Evidence

**Date:** 2026-09-14  
**Scope:** Current project only; no external domain values imported or inferred

## Delivered

- Immutable strict loaders for the Bazi deterministic tables, astrology dignity
  table, True North Node policy, and fact comparison policy.
- Ordered Calculation Contract Bundle loading vocabulary, Bazi tables, dignity,
  node policy, and comparison policy.
- Raw-byte SHA-256 fingerprints for four baseline plus five candidate files,
  with one canonical nine-file bundle digest.
- `validate-calculation-contracts` with two complete validate-and-fingerprint
  passes and empty-stdout deterministic failure behavior.
- Skill contracts, non-production templates, gate routing, methodology index,
  manifest statuses, public APIs, and isolated package verification.

All test fixtures use `TEST_ONLY_` values. No candidate was copied to
`destiny-personality/configs/`, and the Skill contains no Python, binary,
third-party calculator, or fixed executable dependency.

## Verification record

- Focused contract, CLI, bundle, and integration tests passed.
- Full suite: `369 passed`.
- Python syntax compilation passed with its cache redirected to `/tmp`.
- `manifest.json` parsed successfully.
- Official Skill validation: `Skill is valid!`.
- Skill production inventory contains exactly the four frozen baseline YAML
  files.
- Isolated Wheel build, install, public import, `validate-config`, missing
  calculation-candidate behavior, and missing semantic-candidate behavior:
  `package verification passed`.

## Remaining owner-controlled blockers

`CALCULATION_CONFIG_CHECKED` remains closed until the project supplies, reviews,
approves, and promotes exact versions of:

1. `canonical_fact_vocabulary_v1.yaml`
2. `bazi_deterministic_tables_v1.yaml`
3. `astrology_dignity_table_v1.yaml`
4. `astrology_node_policy_v1.yaml`
5. `fact_comparison_policy_v1.yaml`

`SEMANTIC_CONFIG_CHECKED` and Gate 1 remain closed until the project supplies
and approves:

1. `primitive_ontology_v1.yaml`
2. `primitive_state_resolution_v1.yaml`
3. `bazi_mapping_registry_v1.yaml`
4. `astrology_mapping_registry_v1.yaml`
5. `dimension_coverage_policy_v1.yaml`
6. `narrative_rules_v1.yaml`

These are business assets, not missing framework code. Phase D, Phase E, and a
production release also require their approved fingerprints and project-owned
evaluation/release evidence. The reference validator must not generate,
repair, promote, or approve those assets.
