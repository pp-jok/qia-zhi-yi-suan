# Canonical Fact Vocabulary Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a versioned, immutable contract for project-approved canonical
fact identifiers and aliases without supplying production vocabulary values.

**Architecture:** A standalone loader validates one candidate YAML against the
accepted runtime methodology versions. The Skill owns the human-readable
contract and non-production template; Python remains development-only.

**Tech Stack:** Python 3.9, frozen dataclasses, PyYAML, pytest, Markdown, JSON.

## Global Constraints

- Read and write only this project and temporary test locations.
- Do not create real Bazi, astrology, node, or alias values.
- All test values start with `TEST_ONLY_` where language permits.
- Do not add `canonical_fact_vocabulary_v1.yaml` to production `configs/`.
- Preserve existing APIs, frozen YAML bytes, error precedence, and Skill boundaries.
- Use TDD for code and Skill routing.

---

### Task 1: Happy-path model and loader

**Files:**
- Create: `tests/test_canonical_fact_vocabulary.py`
- Create: `src/destiny_personality/vocabulary_models.py`
- Create: `src/destiny_personality/vocabulary_loader.py`
- Modify: `src/destiny_personality/__init__.py`

**Interfaces:**
- Consumes: `Path` plus accepted `RuntimeConfig`.
- Produces: `load_canonical_fact_vocabulary(config_dir, runtime_config) -> CanonicalFactVocabularyConfig`.
- Model: `VocabularyEntry(canonical_id, aliases)`, `VocabularyCategory(category_id, entries)`, and `CanonicalFactVocabularyConfig(schema_version, vocabulary_version, bazi_methodology_version, astrology_methodology_version, categories)` as frozen dataclasses with tuples.

- [x] Write a failing public-API test using ten categories and only
  `TEST_ONLY_` identifiers; assert order, tuple conversion, versions, and
  immutability.
- [x] Run the test and confirm failure because the public loader is absent.
- [x] Implement the three frozen models and exact filename/schema/category
  constants.
- [x] Implement YAML loading, root validation, version matching, category and
  entry parsing, then export the API.
- [x] Run the happy-path test and confirm it passes.

### Task 2: Validation matrix

**Files:**
- Modify: `tests/test_canonical_fact_vocabulary.py`
- Modify: `src/destiny_personality/vocabulary_loader.py`

**Interfaces:**
- Consumes: malformed or inconsistent candidate vocabulary documents.
- Produces: deterministic `ConfigError(code, file, field)` failures.

- [x] Add failing tests for missing file/field, malformed YAML, non-mapping
  root, non-string keys, unknown root/category/entry fields, wrong schema,
  wrong methodology versions, missing/empty categories and entries, wrong
  scalar/list types, empty identifiers/aliases, duplicate canonical IDs, and
  canonical/alias collisions after trim plus casefold.
- [x] Run the module and confirm every new assertion fails for the intended
  missing validation.
- [x] Add only the validation needed for those cases, preserving the first
  failure and exact field paths.
- [x] Run the complete module and confirm it passes.

### Task 3: Skill contract and routing

**Files:**
- Modify: `tests/test_skill_package.py`
- Create: `destiny-personality/schemas/canonical-fact-vocabulary.md`
- Create: `destiny-personality/examples/canonical-fact-vocabulary-template.md`
- Modify: `destiny-personality/SKILL.md`
- Modify: `destiny-personality/checklists/stage-gates.md`
- Modify: `destiny-personality/references/methodology-index.md`

**Interfaces:**
- Consumes: candidate vocabulary supplied within the authorized project scope.
- Produces: an ordered `CALCULATION_CONFIG_CHECKED` sub-gate before lookup tables.

- [x] Add failing Skill tests for all fields, ten categories, error mapping,
  alias ambiguity, node non-goals, non-production template rules, router links,
  ordered placement, and absent production YAML.
- [x] Add the schema and template, then route vocabulary validation before
  lookup tables without adding a CLI or Python dependency to the Skill.
- [x] Run Skill tests and official validation.

### Task 4: Status and release verification

**Files:**
- Modify: `tests/test_v2_2_config_integration.py`
- Modify: `destiny_personality_skill_docs_v2_2/manifest.json`
- Modify: `destiny_personality_skill_docs_v2_2/00_README_V2_2.md`
- Modify: `destiny_personality_skill_docs_v2_2/10_CODEX_IMPLEMENTATION_PLAN_V2_2.md`
- Modify: `destiny_personality_skill_docs_v2_2/11_ACCEPTANCE_CRITERIA_V2_2.md`
- Modify: `destiny_personality_skill_docs_v2_2/12_SKILL_EXECUTION_ARCHITECTURE_V2_2.md`
- Create: `docs/superpowers/evidence/2026-09-14-canonical-fact-vocabulary.md`

**Interfaces:**
- Consumes: verified contract implementation.
- Produces: `calculation_vocabulary_contract_status: implemented` without claiming calculation completeness.

- [x] Add a failing integration test for consistent status and absent
  production vocabulary.
- [x] Update the manifest and four authoritative documents with the exact
  verified status and remaining lookup/node/boundary/comparison gaps.
- [x] Run full pytest, official Skill validation, Python syntax, manifest,
  frozen-byte comparison, Skill binary scan, production inventory, and isolated
  Wheel build-install-run verification.
- [x] Record exact evidence, mark this plan complete, and rerun every final
  check after the last file mutation.
