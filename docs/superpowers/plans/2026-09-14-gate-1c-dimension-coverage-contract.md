# Gate 1C Dimension Coverage Policy Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans`. This workspace is not a Git repository, so test checkpoints replace commits.

**Goal:** Add a distributable twelve-dimension coverage-policy contract and standalone immutable development validator without adding production semantic values.

**Architecture:** One asset atomically binds exactly twelve dimension definitions to one versioned provisional coverage and partial-portrait policy. The public loader consumes accepted Primitive and runtime configs, validates references, and does not calculate case coverage.

**Tech Stack:** Markdown, YAML, Python 3.9+, frozen dataclasses, PyYAML, pytest.

## Global Constraints

- Stay inside the current project; do not read unrelated project data.
- Do not add the production asset or real domain values.
- Keep the Skill free of Python and bundled calculation software.
- Preserve existing loaders and four frozen production YAML files.
- Use test-first RED-GREEN and `TEST_ONLY_` fixtures.
- Keep Gate 1 and downstream phases incomplete.

### Task 1: Public model and happy path

**Files:** create `tests/test_dimension_coverage_policy.py`,
`src/destiny_personality/dimension_models.py`, and
`src/destiny_personality/dimension_loader.py`; modify package `__init__.py`.

- [ ] Write a fixture with twelve `D##` records and a complete requirement for
  each, then assert the public loader returns immutable models and preserves
  dimension order.
- [ ] Run the focused test and observe failure because the API is missing.
- [ ] Implement only the models, parsing, accepted-version checks, and happy
  path required by the test.
- [ ] Re-run and require `1 passed`.

Public interface:

```python
load_dimension_coverage_policy(
    config_dir,
    primitive_foundation,
    runtime_config,
) -> DimensionCoveragePolicyConfig
```

### Task 2: Validation matrix

**Files:** modify the new test and loader files.

- [ ] Add failing tests for missing/parse/type errors; exact keys; exact count;
  ID/name uniqueness; unknown/duplicate Primitive references; exact versions;
  fixed policy wire values; finite ordered thresholds; requirement completeness,
  uniqueness, local references, and bounds.
- [ ] Run the suite and observe RED.
- [ ] Implement direct deterministic validation with precise dot paths.
- [ ] Run the new suite and prior runtime, Primitive, and Mapping suites; require
  zero failures.

### Task 3: Skill contract and routing

**Files:** create `destiny-personality/schemas/dimension-coverage-policy.md` and
`destiny-personality/examples/dimension-coverage-template.md`; modify Skill,
stage-gates, methodology-index, and `tests/test_skill_package.py`.

- [ ] Add failing tests requiring both links, all fields and fixed wire values,
  the exact five error codes, the no-partial-before-semantic-gate rule, and
  absence of `dimension_coverage_policy_v1.yaml` from production configs.
- [ ] Run focused tests and observe RED.
- [ ] Add the contract, template, and routing without semantic values.
- [ ] Re-run and require GREEN.

### Task 4: Status and release

**Files:** modify the four authoritative V2.2 status documents, manifest, and
integration tests; create Gate 1C evidence.

- [ ] Add a failing status test for `gate_1c_status: implemented`, the exact
  2026-09-14 verification sentence, and explicit remaining gaps.
- [ ] Update status without adding the absent asset to manifest documents.
- [ ] Run integration tests and require GREEN.
- [ ] Run full pytest, official Skill validation, JSON validation, frozen asset
  check, syntax compile, forbidden-file scan, production inventory, and package
  build/install/run verification.
- [ ] Re-run full pytest after the final file mutation before claiming completion.
