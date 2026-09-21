# Candidate Promotion Gate Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reject incomplete or unreviewed candidate assets before any production promotion.

**Architecture:** Refactor the existing gate into small pure checks over a candidate root. The default path remains unchanged; an optional root supports isolated filesystem fixtures. The gate only emits blocker codes and never edits assets or enables production.

**Tech Stack:** Python 3.9, PyYAML, pytest.

## Global Constraints

- No candidate YAML is copied to `destiny-personality/configs/`.
- No review status changes automatically.
- No table values, mappings, directions, thresholds, or narrative semantics change.

---

### Task 1: Make the review and environment checks asset-aware

**Files:**
- Modify: `src/destiny_personality/core_profile_promotion.py`
- Modify: `tests/test_candidate_promotion_gate.py`

**Interfaces:**
- `validate_candidate_bundle_for_promotion(candidate_root: Optional[Path] = None) -> Tuple[str, ...]`
- A candidate root is review-ready only when every YAML file has `review_status: approved`.
- The environment table is structurally available only when it has all ten stems and all twelve month branches with non-empty values.

- [ ] **Step 1: Write failing isolated-root tests**

```python
assert "CANDIDATE_REVIEW_PENDING" in validate_candidate_bundle_for_promotion(bundle_root)
(bundle_root / "bazi_day_master_environment_v1.yaml").write_text("review_status: approved\nstem_elements: {}\nmonth_branch_seasons: {}\n")
assert "BAZI_DAY_MASTER_ENVIRONMENT_UNAVAILABLE" in validate_candidate_bundle_for_promotion(bundle_root)
```

- [ ] **Step 2: Verify RED**

Run: `python3 -m pytest tests/test_candidate_promotion_gate.py::test_candidate_promotion_gate_rejects_incomplete_environment_table -q`

- [ ] **Step 3: Add root selection and pure structure checks**

```python
def validate_candidate_bundle_for_promotion(candidate_root: Optional[Path] = None) -> Tuple[str, ...]:
    root = candidate_root or _default_candidate_root()
    assets = {path.name: yaml.safe_load(path.read_text(encoding="utf-8")) for path in root.glob("*.yaml")}
    ...
```

- [ ] **Step 4: Verify GREEN**

Run: `python3 -m pytest tests/test_candidate_promotion_gate.py -q`

### Task 2: Validate Bazi and astrology gate field completeness

**Files:**
- Modify: `src/destiny_personality/core_profile_promotion.py`
- Modify: `tests/test_candidate_promotion_gate.py`

**Interfaces:**
- Every Bazi rule must explicitly include both source kinds, `minimum_distinct_pillars >= 2`, and `requires_day_master_environment: true`.
- At least one astrology rule must provide a non-empty dignity modifier list and a non-empty angular-body plus house-context pair.

- [ ] **Step 1: Write failing fixture mutations**

```python
bazi["rules"][0].pop("allowed_source_kinds")
assert "BAZI_VISIBLE_HIDDEN_PROVENANCE_UNAVAILABLE" in validate_candidate_bundle_for_promotion(bundle_root)
astrology["rules"][0].pop("house_context_any")
assert "ASTROLOGY_ANGLE_HOUSE_BRANCH_UNIMPLEMENTED" in validate_candidate_bundle_for_promotion(bundle_root)
```

- [ ] **Step 2: Verify RED**

Run: `python3 -m pytest tests/test_candidate_promotion_gate.py::test_candidate_promotion_gate_requires_complete_modifier_fields -q`

- [ ] **Step 3: Replace presence-only predicates with structural predicates**

```python
def _bazi_provenance_is_complete(rules: object) -> bool: ...
def _astrology_modifiers_are_complete(rules: object) -> bool: ...
```

- [ ] **Step 4: Verify candidate and full regression**

Run: `python3 -m pytest tests/test_candidate_promotion_gate.py tests/test_candidate_core_assets.py -q`
Run: `python3 -m pytest -q`
