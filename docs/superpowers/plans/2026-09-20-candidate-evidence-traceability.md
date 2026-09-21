# Candidate Evidence Traceability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every newly enabled candidate mapping auditable from its actual project-derived facts, without adding semantic conclusions or a production route.

**Architecture:** The candidate builder already requires a day-master environment for Bazi rules and a major aspect for eligible astrology rules. Preserve those gates, but serialize their concrete input values as stable fact references on the resulting `PrimitiveCandidate`. No scoring, direction, or activation condition changes.

**Tech Stack:** Python 3.9, frozen dataclasses, PyYAML, pytest.

## Global Constraints

- Candidate assets remain outside `destiny-personality/configs/`.
- No external table, provider, or inferred semantic value is introduced.
- Day-master environment remains descriptive only.
- Dignity, angle, and house remain modifiers and cannot activate or reverse a candidate.
- A major aspect remains mandatory before any astrology modifier is emitted.

---

### Task 1: Record concrete day-master environment evidence

**Files:**
- Modify: `src/destiny_personality/core_profile_builder.py`
- Modify: `tests/test_core_profile_builder.py`

**Interfaces:**
- Produces a Bazi fact reference in the exact form `bazi.day_master_environment:<stem>:<element>:<branch>:<season>:<table_version>`.

- [ ] **Step 1: Write a failing audit-reference test**

```python
assert (
    "bazi.day_master_environment:庚:metal:午:summer:candidate-bazi-day-master-environment-v1"
    in candidate.fact_refs
)
```

- [ ] **Step 2: Run the test to confirm RED**

Run: `python3 -m pytest tests/test_core_profile_builder.py::test_candidate_builder_records_concrete_day_master_environment_evidence -q`

- [ ] **Step 3: Emit the versioned concrete reference after the existing environment gate**

```python
environment_ref = (
    "bazi.day_master_environment:"
    f"{environment.day_master_stem}:{environment.day_master_element}:"
    f"{environment.month_branch}:{environment.season}:{environment.table_ref}",
)
```

- [ ] **Step 4: Run the focused test to confirm GREEN**

Run: `python3 -m pytest tests/test_core_profile_builder.py::test_candidate_builder_records_concrete_day_master_environment_evidence -q`

### Task 2: Record the actual aspect that activated an astrology candidate

**Files:**
- Modify: `src/destiny_personality/core_profile_builder.py`
- Modify: `tests/test_core_profile_builder.py`

**Interfaces:**
- Produces an aspect reference in the exact form `astrology.aspects:<body_a>:<aspect_type>:<body_b>:<orb>` only when that aspect satisfies the rule’s pair, type, and orb constraints.

- [ ] **Step 1: Write a failing audit-reference test**

```python
assert "astrology.aspects:Sun:trine:Mars:1" in candidate.fact_refs
```

- [ ] **Step 2: Run the test to confirm RED**

Run: `python3 -m pytest tests/test_core_profile_builder.py::test_candidate_builder_records_activating_major_aspect -q`

- [ ] **Step 3: Keep the matched aspects and append only their fact references**

```python
matching_aspects = tuple(
    aspect for aspect in facts.astrology.aspects if ...
)
has_required_aspect = not required_pair or bool(matching_aspects)
aspect_refs = tuple(
    f"astrology.aspects:{aspect.body_a}:{aspect.aspect_type}:{aspect.body_b}:{aspect.orb}"
    for aspect in matching_aspects
)
```

- [ ] **Step 4: Run focused and candidate-chain regression tests**

Run: `python3 -m pytest tests/test_core_profile_builder.py tests/test_candidate_pipeline.py tests/test_core_profile_validation.py -q`

### Task 3: Rebind the candidate calibration fingerprint and verify the package

**Files:**
- Modify only if the fingerprint changes: `candidates/core-profile-v1/core_profile_calibration_policy_v1.yaml`, `docs/domain/core-profile-calibration-review-v1.md`, `docs/domain/c4b-calibration-decision-record-v1.md`
- Verify: `tests/test_candidate_core_assets.py`, `tests/test_core_profile_calibration.py`, `tests/test_skill_package.py`

**Interfaces:**
- Code-only changes do not change the candidate YAML fingerprint. The existing policy fingerprint must remain current.

- [ ] **Step 1: Verify the semantic fingerprint policy still matches**

Run: `python3 -m pytest tests/test_candidate_core_assets.py tests/test_core_profile_calibration.py -q`

- [ ] **Step 2: Run full regression**

Run: `python3 -m pytest -q`

