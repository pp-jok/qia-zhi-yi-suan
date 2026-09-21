# Canonical Fact Vocabulary Verification Evidence

**Date:** 2026-09-14

- Public API RED: `1 failed` because
  `load_canonical_fact_vocabulary` was absent.
- Happy-path GREEN: `1 passed` with immutable ordered models.
- Validation-matrix RED: `20 failed, 2 passed`, exposing unclassified missing,
  type, version, unknown-field, and ambiguity failures.
- Complete loader GREEN: `22 passed`.
- Skill and status RED: `2 failed` because the contract resources and status
  declaration were absent.
- Focused loader, Skill, and integration suite: `59 passed`.
- Full suite before evidence recording: `296 passed`.
- Official Skill validation: `Skill is valid!`.
- Python syntax, manifest JSON, frozen-byte comparison, and production
  inventory checks passed.
- Skill binary scan returned no Python, bytecode, shared-library, or DLL files.
- Isolated Wheel build, install, public vocabulary-loader import, and existing
  CLI checks passed: `package verification passed`.

The contract defines ten normalization categories and deterministic alias
ambiguity rules without supplying any real Bazi, astrology, node, or alias
value. No `canonical_fact_vocabulary_v1.yaml` was added to production.
`CALCULATION_CONFIG_CHECKED` remains closed pending approved vocabulary,
lookup-table, node, boundary, and comparison assets.
