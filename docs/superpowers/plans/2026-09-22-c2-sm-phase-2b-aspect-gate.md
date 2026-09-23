# C2-SM Phase 2B Aspect Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one proposed, non-directional astrology aspect `RULE_GATE` Semantic Mechanism candidate for the P004 review question.

**Architecture:** Candidate YAML remains exclusively under `candidates/semantic-mechanisms-v1/`. The existing validator is hardened to enforce every contract-required field plus allowed role, review status, and origin. The candidate is loaded and audited but has no approval, mapping, or runtime path.

**Tech Stack:** Python 3.9+, PyYAML, pytest.

## Global Constraints

- Create exactly one `proposed` `RULE_GATE` candidate and zero Mapping v2 candidates.
- Candidate may qualify an aspect fact for review only; it must not claim a P004 state, direction, magnitude, or score.
- Keep active runtime and semantic/presentation fingerprints unchanged.
- Missing contract fields, invalid role/status, and prohibited origins produce blocking audit findings.

---

### Task 1: Write failing mechanism-admission tests

**Files:**
- Modify: `tests/test_semantic_mechanism_contract.py`

**Interfaces:**
- `load_semantic_mechanism_candidates(root: Path) -> Tuple[Mapping[str, object], ...]`
- `validate_semantic_mechanism_candidate(candidate, approved_root_ids) -> Tuple[SemanticMechanismFinding, ...]`

- [x] Add a test that loads exactly `SMC-AS-ASPECT-ELIGIBILITY-GATE-P004-V1`, validates it against `ER-AS-ASPECT-INSTANCE-V1`, and expects no findings.
- [x] Replace the zero-candidate audit assertion with `{candidate_count: 1, error_count: 0, warning_count: 0, admission_eligible_count: 1}`.
- [x] Add parameterized tests using `_candidate()` that expect error codes `SEMANTIC_MECHANISM_CONTRACT_FIELD_REQUIRED`, `SEMANTIC_MECHANISM_INVALID_ROLE`, `SEMANTIC_MECHANISM_INVALID_REVIEW_STATUS`, and `SEMANTIC_MECHANISM_PROHIBITED_ORIGIN` for a missing `candidate_id`, `evidence_role: UNKNOWN`, `review_status: unreviewed`, and `origin: legacy_output`.
- [x] Run `python3 -m pytest -q tests/test_semantic_mechanism_contract.py` and confirm RED because the candidate file and stricter validation do not exist.

### Task 2: Harden candidate validation

**Files:**
- Modify: `candidates/semantic-mechanisms-v1/semantic_mechanism_contract_v1.yaml`
- Modify: `src/destiny_personality/semantic_mechanisms.py`
- Test: `tests/test_semantic_mechanism_contract.py`

**Interfaces:**
- `validate_semantic_mechanism_candidate` loads the contract requirements through a private helper and returns blocking findings rather than raising for candidate-content defects.

- [x] Add `review_status` to `required_candidate_fields`.
- [x] Implement `_candidate_contract_rules(root)` returning required fields, allowed roles, allowed review statuses, and prohibited origins from the contract.
- [x] Extend validation to append the four Task 1 findings for missing/non-empty required fields, invalid role, invalid review status, and prohibited origin. Preserve `GOLDEN_SAMPLE_SEMANTIC_LEAK` for `golden_sample`.
- [x] Update callers so loaded candidate validation receives the contract root, while direct unit tests can use the default project contract root.
- [x] Run the focused contract and legacy/golden tests and confirm GREEN.

### Task 3: Add the proposed aspect eligibility gate

**Files:**
- Create: `candidates/semantic-mechanisms-v1/mechanism_candidates/SMC-AS-ASPECT-ELIGIBILITY-GATE-P004-V1.yaml`

**Candidate content:**

```yaml
candidate_id: SMC-AS-ASPECT-ELIGIBILITY-GATE-P004-V1
review_status: proposed
source_system: astrology
source_fact_classes: [deterministic_facts.astrology.aspects]
evidence_root_refs: [ER-AS-ASPECT-INSTANCE-V1]
proposed_mechanism: An identified astrology aspect instance may enter later P004 evidence review only as a non-primary rule gate; it cannot establish P004 direction, magnitude, or Primitive state.
target_primitive_questions: [When and how is concrete action started and advanced?]
evidence_role: RULE_GATE
asserts_primitive_state: false
origin: approved_evidence_root
legacy_similarity:
  same_source_conditions: false
  same_target_primitive: false
  same_direction: false
```

- [x] Create the candidate with exactly this candidate-only content.
- [x] Run focused C2-SM tests and confirm the audit reports one eligible proposed candidate with no errors/warnings.

### Task 4: Record review and verify isolation

**Files:**
- Modify: `docs/domain/c2-semantic-mechanism-governance-v1.md`
- Modify: `docs/domain/c2-semantic-mechanism-review-v1.md`
- Create: `docs/reviews/c2-sm-phase-2b-aspect-gate-verification.md`

- [x] Record candidate status `proposed`, approved mechanism count `0`, Mapping v2 `0`, and runtime activation `none`.
- [x] Run `python3 -m pytest -q --disable-warnings`, `python3 scripts/verify_package.py`, and the candidate/root audit script using `PYTHONPATH=src`.
- [x] Record test counts, active fingerprints, candidate fingerprint, audit report, and the next gate: separate mechanism decision; no Mapping v2 authorization.
