# Calculation Configuration Framework Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete every remaining calculation-configuration contract,
aggregate validator, fingerprint, CLI, and Skill gate that can be implemented
without inventing project-owned values.

**Architecture:** Four focused immutable configuration assets reference the
accepted vocabulary and runtime methodologies. One ordered bundle loader and
stable two-pass CLI compose them. Production values remain absent.

**Tech Stack:** Python 3.9, frozen dataclasses, PyYAML, hashlib, argparse,
pytest, Markdown, JSON.

## Global Constraints

- Operate only in this project and temporary validation directories.
- Never invent or import domain values from conventions or external sources.
- All fixtures use `TEST_ONLY_` values.
- Templates never enter production `configs/`.
- Preserve existing public APIs, error precedence, frozen bytes, and Skill runtime independence.
- Every implementation follows RED, observed failure, minimal GREEN, refactor.

---

### Task 1: Bazi deterministic table contract

**Files:** Create `bazi_table_models.py`, `bazi_table_loader.py`,
`tests/test_bazi_deterministic_tables.py`, Skill schema and template.

- [x] Define and test immutable versioned sections for `hidden_stems`,
  `ten_gods`, and `relations`, with unique rule IDs and vocabulary references.
- [x] Validate exact keys, non-empty rows, declarative conditions/results,
  methodology/vocabulary versions, and precise configuration errors.
- [x] Route the non-production contract after canonical vocabulary.

### Task 2: Astrology dignity table contract

**Files:** Create `astrology_table_models.py`, `astrology_table_loader.py`,
`tests/test_astrology_dignity_table.py`, Skill schema and template.

- [x] Define and test immutable body/sign/dignity reference rows and unique keys.
- [x] Validate exact versions, vocabulary references, duplicates, and error paths.
- [x] Route after the Bazi deterministic tables without supplying dignity values.

### Task 3: True North Node policy contract

**Files:** Create `node_policy_models.py`, `node_policy_loader.py`,
`tests/test_astrology_node_policy.py`, Skill schema and template.

- [x] Define explicit canonical fact ID, inclusion, phase, aspect, dignity,
  weight, and time-sensitivity fields.
- [x] Require every decision to be explicit and vocabulary-referenced; validate
  versions, exact keys, enums/types, and contradictions.
- [x] Route after the dignity table; no default node behavior is permitted.

### Task 4: Fact comparison policy contract

**Files:** Create `comparison_policy_models.py`, `comparison_policy_loader.py`,
`tests/test_fact_comparison_policy.py`, Skill schema and template.

- [x] Define triggers, logical categories, boundary margins, decimal precision,
  field tolerances, and representation equivalences as immutable records.
- [x] Validate exact versions, uniqueness, non-negative finite numbers,
  vocabulary references, and complete trigger/category coverage declarations.
- [x] Route before capability discovery and independent comparison.

### Task 5: Aggregate bundle, fingerprint, and CLI

**Files:** Create `calculation_bundle.py`, `calculation_fingerprint.py`, focused
tests; modify `cli.py`, `__init__.py`, and `verify_package.py`.

- [x] Test and implement exact ordered loading from vocabulary through comparison.
- [x] Test and implement raw-byte SHA-256 for four baseline plus five candidate
  assets and canonical bundle digest.
- [x] Add `validate-calculation-contracts` with two stable passes, deterministic
  JSON versions/counts/fingerprint, and unchanged failure behavior.
- [x] Verify the installed Wheel exposes every public loader and CLI route.

### Task 6: Skill, status, and final audit

**Files:** Modify Skill router, stage gates, methodology index, manifest, four
authoritative status documents, tests, and create final evidence.

- [x] Verify every contract/template link, ordered gate, exact error mapping,
  absent production asset, and no executable dependency.
- [x] Set individual contract statuses to `implemented` without marking
  calculation completeness, Gate 1, or downstream phases complete.
- [x] Run all focused tests and full pytest; run official Skill validation,
  syntax/JSON/frozen/inventory/binary checks, and isolated Wheel verification.
- [x] Record remaining project-owned assets as the only blockers and rerun the
  entire final verification after the last mutation.
