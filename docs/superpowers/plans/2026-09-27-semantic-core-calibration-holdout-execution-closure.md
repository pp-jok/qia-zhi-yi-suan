# Semantic Core Calibration and Holdout Execution Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute repository calibration and holdout fixtures against approved Mapping inputs, then admit only integrity-validated evaluation artifacts to the authority registry.

**Architecture:** Add a narrow fixture/evaluation module that owns fixture parsing, normalization, dataset independence checks, and Mapping-to-Primitive execution. Keep `mapping_v2` as the orchestration and artifact boundary, and make `promotion_authority` independently revalidate the artifact contract before persistence or promotion use.

**Tech Stack:** Python 3.9+, PyYAML, pytest, existing Mapping v2 and Primitive Resolver.

## Global Constraints

- Preserve all semantic assets and active fingerprints unchanged.
- Existing fixture schema `candidate-core-profile-calibration-facts-v1` remains valid.
- Repository zero state remains `blocked_by_gate`; synthetic approved Mapping inputs are test-only.
- Holdout executes independently and cannot mutate Mapping, policy, proposals, or runtime.
- Registration accepts only passing, self-consistent machine artifact contracts.

---

### Task 1: Fixture contract and dataset integrity

**Files:**
- Create: `src/destiny_personality/mapping_evaluation.py`
- Create: `tests/test_mapping_evaluation_execution.py`

- [ ] Write failing tests for valid v1 loading, invalid schema rejection, duplicate IDs, content fingerprint stability, and cross-set content overlap.
- [ ] Implement immutable normalized fixture records with canonical input tokens, optional expected states/context expectations, per-fixture hashes, and deterministic dataset hashes.
- [ ] Implement design/holdout discovery with path, ID, and content-disjointness validation; fail closed for invalid files.
- [ ] Run fixture tests.

### Task 2: Real Mapping-to-Primitive evaluation

**Files:**
- Modify: `src/destiny_personality/mapping_v2.py`
- Modify: `tests/test_mapping_evaluation_execution.py`

- [ ] Write failing synthetic cases for deterministic pass, unknown, mixed, context differentiation, expectation failure, and structural/observed collapse.
- [ ] Execute each normalized fixture by matching `canonical_fact_requirements` against fixture tokens and calling `resolve_primitive_states`.
- [ ] Derive execution metrics only from actual outcomes; preserve `blocked_by_gate` for empty approved bundles.
- [ ] Run execution tests.

### Task 3: Attested artifact and authority validation

**Files:**
- Modify: `src/destiny_personality/mapping_v2.py`
- Modify: `src/destiny_personality/promotion_authority.py`
- Modify: `tests/test_semantic_promotion_authority.py`

- [ ] Write failing tests for deterministic input hashes, data changes, forged artifacts, unknown runners, duplicate artifacts, and promotion rejection of an invalid registry record.
- [ ] Add dataset, mapping-bundle, evaluation-input, and artifact fingerprints to evaluated artifacts.
- [ ] Recompute and validate artifact integrity before registry persistence and authority resolution.
- [ ] Run authority and promotion tests.

### Task 4: Repository CLI and closure evidence

**Files:**
- Modify: `src/destiny_personality/cli.py`
- Modify: `tests/test_master_semantic_core.py`
- Create: `docs/reviews/semantic-core-final-calibration-holdout-closure.md`
- Modify: `docs/reviews/master-semantic-core-engineering-completion.md`
- Modify: `docs/reviews/semantic-core-final-trust-audit-closure.md`

- [ ] Write failing CLI tests proving repository fixture execution is reported while the zero state remains blocked and unregistrable.
- [ ] Wire runners through discovered fixtures and leave `--register` as the sole official registry write path.
- [ ] Record final scope, integrity model, active-fingerprint non-change, and asset zero state in closure documents.
- [ ] Run focused tests, full suite in bounded groups if required by the local execution limit, then package verification.
