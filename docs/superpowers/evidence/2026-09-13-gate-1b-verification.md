# Gate 1B Verification Evidence

**Date:** 2026-09-13  
**Scope:** Bazi and astrology Context-Aware Mapping Registry contracts and development validator

## Boundary

- No production `bazi_mapping_registry_v1.yaml` or
  `astrology_mapping_registry_v1.yaml` was created.
- No real Primitive meaning, mapping rule, direction meaning, condition
  vocabulary, threshold, modifier effect, or interaction was introduced.
- Synthetic fixtures use `TEST_ONLY_` values in temporary directories.
- The distributable Skill contains no Python validator or calculation runtime.

## RED/GREEN record

### Public API and immutable happy path

- RED: the focused happy-path test failed with
  `public Mapping Registry loader is missing` (`1 failed`).
- GREEN: after adding immutable models, the public loader, and exports, the
  focused test passed (`1 passed`).

### Validation matrix

- RED: the first matrix run exited non-zero; the observed progress showed seven
  early cases passing followed by consecutive failures against the minimum
  loader.
- GREEN: after deterministic validation was implemented, the initial mapping
  matrix passed (`46 passed`).
- Prior runtime and Primitive loader regression group passed (`57 passed`).

### Skill contract

- RED: Skill package tests failed because the mapping schema and Skill links
  were absent (`2 failed, 16 passed`).
- GREEN: after adding the shared contract, non-production template, Skill route,
  stage gate, and methodology index, Skill package tests passed (`18 passed`).

### V2.2 status

- RED: integration tests failed because Gate 1B status and manifest state were
  absent (`2 failed, 8 passed`).
- GREEN: after consistent source-document and manifest updates, integration
  tests passed (`10 passed`).

### Score-model drift prevention

- Self-review found that `salience` used score-model bounds while the registry
  did not record `score_model_version`.
- RED: the focused happy path rejected the new field as unknown (`1 failed`).
- GREEN: after adding the exact version reference to models, loader, contract,
  template, design, and plan, focused coverage passed (`8 passed`).

## Pre-release regression

After all implementation and status changes present at this checkpoint:

```text
python3 -m pytest -q
212 passed in 19.71s
```

Final release commands are rerun after this evidence document is written so the
completion claim is based on a zero-exclusion, post-mutation verification.

## Remaining gates

Gate 1B establishes contracts only. Gate 1 and Phase D remain incomplete until
the project supplies real approved Primitive assets, both real Mapping Registry
assets, executable State Resolution values, deterministic calculation tables,
dimension and coverage policy, and Narrative Rules.
