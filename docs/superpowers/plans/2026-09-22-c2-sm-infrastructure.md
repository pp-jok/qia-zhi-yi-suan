# C2-SM Semantic Mechanism Infrastructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a candidate-only Semantic Mechanism governance infrastructure that validates evidence roots and review safety without admitting any real mechanism or Mapping v2 rule.

**Architecture:** Store two empty-but-valid candidate contracts outside the active semantic bundle. A pure Python governance module loads those contracts, validates mechanism candidates, reports review findings, calculates a separate candidate-mechanism fingerprint, and blocks mapping-candidate consumption unless a mechanism is explicitly approved. It never alters the active semantic fingerprint or runtime path.

**Tech Stack:** Python 3.9+, dataclasses, PyYAML, pytest, candidate YAML contracts.

## Global Constraints

- C2-SM Phase 1 is infrastructure only: actual evidence roots, semantic mechanisms, and Mapping v2 candidates remain zero.
- Do not modify active mapping registries, profile runtime, active semantic/presentation fingerprint definitions, calibration, holdout, Signature, or C3.
- A mechanism requires approved evidence roots, an explicit Primitive question, and a non-directional mechanism statement.
- Golden Sample-derived mechanisms fail; material legacy equivalence produces a warning.
- Candidate-mechanism changes may change only the separate candidate-mechanism fingerprint.

---

### Task 1: Add failing governance tests

**Files:**
- Create: `tests/test_semantic_mechanism_contract.py`
- Create: `tests/test_semantic_evidence_roots.py`
- Create: `tests/test_semantic_mechanism_legacy_guard.py`
- Create: `tests/test_semantic_mechanism_golden_leak.py`
- Create: `tests/test_semantic_mechanism_activation_isolation.py`

**Interfaces:**
- Consumes: `load_semantic_mechanism_contracts(root)`, `validate_semantic_mechanism_candidate(candidate, approved_root_ids)`, `mapping_candidate_eligibility(candidate, approved_mechanism_ids)`, and `build_semantic_mechanism_candidate_fingerprint(root)`.
- Produces: failing proof that missing roots/questions, unapproved roots, direct state claims, Golden leakage, and unapproved consumption are rejected.

- [x] Write focused failing tests for the contract and empty-registry validity.
- [x] Run: `python3 -m pytest -q tests/test_semantic_mechanism_*.py`.
- [x] Expected: import failure because the governance module and candidate contracts do not exist.

### Task 2: Implement minimal candidate-only governance

**Files:**
- Create: `candidates/semantic-mechanisms-v1/semantic_mechanism_contract_v1.yaml`
- Create: `candidates/semantic-mechanisms-v1/semantic_evidence_root_contract_v1.yaml`
- Create: `candidates/semantic-mechanisms-v1/semantic_evidence_root_registry_v1.yaml`
- Create: `src/destiny_personality/semantic_mechanisms.py`

**Interfaces:**
- `load_semantic_mechanism_contracts(root: Path) -> SemanticMechanismContracts`
- `validate_semantic_mechanism_candidate(candidate: Mapping[str, object], approved_root_ids: Collection[str]) -> tuple[SemanticMechanismFinding, ...]`
- `mapping_candidate_eligibility(candidate: Mapping[str, object], approved_mechanism_ids: Collection[str]) -> tuple[SemanticMechanismFinding, ...]`
- `build_semantic_mechanism_candidate_fingerprint(root: Path) -> str`

- [x] Create empty valid contracts and a loader that rejects malformed contracts.
- [x] Implement candidate validation, audit findings, legacy/golden guards, and mapping consumption eligibility.
- [x] Implement a separate recursive candidate fingerprint.
- [x] Run focused tests and confirm they pass.

### Task 3: Document governance and verify isolation

**Files:**
- Create: `docs/domain/c2-semantic-mechanism-governance-v1.md`
- Create: `docs/domain/c2-semantic-evidence-root-review-v1.md`
- Create: `docs/domain/c2-semantic-mechanism-review-v1.md`
- Create: `docs/reviews/c2-sm-infrastructure-verification.md`
- Modify: `docs/domain/c2-fresh-mapping-product-owner-decision-v1.md`

- [x] Record C2-SM authorization and Phase 1 scope.
- [x] Document review workflow, zero-state validity, and product-owner approval boundary.
- [x] Capture active fingerprints, run full tests and package verification, and record results.
