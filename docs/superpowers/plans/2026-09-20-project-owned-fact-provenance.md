# Project-Owned Fact Provenance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add versioned, auditable Bazi provenance and environment facts plus constrained astrology modifiers to the candidate Core Profile path.

**Architecture:** Extend calculation facts only with explicit provenance, derive the limited day-master environment from a project-owned YAML table, and keep astrology dignity/house data as modifiers after a major-aspect rule activates. Candidate mapping stays isolated; the promotion gate remains closed unless every declared requirement is present and tested.

**Tech Stack:** Python 3.9, frozen dataclasses, PyYAML, pytest.

## Global Constraints

- No external provider, internet table, or model-generated fact is used.
- `unknown` provenance never activates a Bazi candidate.
- Day-master environment is descriptive only: no strength, favorable-element, pattern, transit, or outcome inference.
- Dignity, angle, and house data never activate or reverse a Primitive; they only annotate an already aspect-activated astrology candidate.
- Candidate assets stay outside `destiny-personality/configs/` and never enter the default route.
- Any candidate semantic asset change requires a new Bundle fingerprint and Design Set run.

---

### Task 1: Add explicit Bazi fact provenance

**Files:**
- Modify: `src/destiny_personality/calculation/models.py`
- Modify: `src/destiny_personality/calculation/validation/bazi.py`
- Modify: `tests/test_bazi_provenance.py`
- Modify: `tests/conftest.py`

**Interfaces:**
- Produces `TenGodSourceKind` with `visible_stem`, `hidden_stem`, `unknown` and `TenGodFact.source_kind`.
- Existing generic fact validation accepts `unknown`; candidate mapping will reject it.

- [ ] **Step 1: Write the failing provenance test**

```python
def test_ten_god_source_kind_is_preserved_in_validated_facts(bazi_facts, runtime_config):
    facts = replace(
        bazi_facts,
        ten_gods=(TenGodFact("year.stem", "比肩", (PillarPosition.YEAR,), TenGodSourceKind.VISIBLE_STEM),),
    )
    validate_bazi_facts(facts, FactMode.TIME_SENSITIVE, runtime_config)
    assert facts.ten_gods[0].source_kind is TenGodSourceKind.VISIBLE_STEM
```

- [ ] **Step 2: Run the test and confirm RED**

Run: `python3 -m pytest tests/test_bazi_provenance.py::test_ten_god_source_kind_is_preserved_in_validated_facts -q`  
Expected: FAIL because the enum and constructor field do not exist.

- [ ] **Step 3: Implement the smallest immutable model extension**

```python
class TenGodSourceKind(str, Enum):
    VISIBLE_STEM = "visible_stem"
    HIDDEN_STEM = "hidden_stem"
    UNKNOWN = "unknown"

@dataclass(frozen=True)
class TenGodFact:
    subject_ref: str
    ten_god: str
    source_pillars: Tuple[PillarPosition, ...]
    source_kind: TenGodSourceKind = TenGodSourceKind.UNKNOWN
```

Validate `source_kind` is a `TenGodSourceKind`; update fixtures to use
`VISIBLE_STEM` when their evidence represents a visible stem.

- [ ] **Step 4: Verify GREEN**

Run: `python3 -m pytest tests/test_bazi_provenance.py tests/test_calculation_contract_validation.py -q`  
Expected: PASS.

### Task 2: Derive the limited day-master environment from a project table

**Files:**
- Create: `candidates/core-profile-v1/bazi_day_master_environment_v1.yaml`
- Create: `src/destiny_personality/day_master_environment.py`
- Modify: `src/destiny_personality/calculation/models.py`
- Create: `tests/test_day_master_environment.py`

**Interfaces:**
- Produces `DayMasterEnvironmentFact` and
  `derive_candidate_day_master_environment(BaziChartFacts) -> DayMasterEnvironmentFact`.
- Table maps all ten stems to five elements and all twelve month branches to one of four seasons.

- [ ] **Step 1: Write the failing derivation test**

```python
def test_derives_day_master_environment_from_day_stem_and_month_branch(bazi_facts):
    result = derive_candidate_day_master_environment(bazi_facts)
    assert result.day_master_stem == "庚"
    assert result.day_master_element == "metal"
    assert result.month_branch == "午"
    assert result.season == "summer"
    assert result.table_ref == "candidate-bazi-day-master-environment-v1"
```

- [ ] **Step 2: Run the test and confirm RED**

Run: `python3 -m pytest tests/test_day_master_environment.py::test_derives_day_master_environment_from_day_stem_and_month_branch -q`  
Expected: FAIL because the module and table are absent.

- [ ] **Step 3: Add the table and pure derivation function**

```python
def derive_candidate_day_master_environment(facts: BaziChartFacts) -> DayMasterEnvironmentFact:
    table = _load_table()
    return DayMasterEnvironmentFact(
        day_master_stem=facts.day_pillar.heavenly_stem,
        day_master_element=table["stem_elements"][facts.day_pillar.heavenly_stem],
        month_branch=facts.month_pillar.earthly_branch,
        season=table["month_branch_seasons"][facts.month_pillar.earthly_branch],
        source_pillars=(PillarPosition.DAY, PillarPosition.MONTH),
        table_ref=table["table_version"],
    )
```

The YAML has `review_status: pending`, complete stem/branch mappings, and no
strength or favorable-element values.

- [ ] **Step 4: Verify GREEN**

Run: `python3 -m pytest tests/test_day_master_environment.py -q`  
Expected: PASS.

### Task 3: Enforce Bazi provenance/environment and constrained astrology modifiers

**Files:**
- Modify: `candidates/core-profile-v1/bazi_mapping_registry_v1.yaml`
- Modify: `candidates/core-profile-v1/astrology_mapping_registry_v1.yaml`
- Modify: `src/destiny_personality/core_profile_builder.py`
- Modify: `tests/test_core_profile_builder.py`

**Interfaces:**
- Bazi rules add `allowed_source_kinds` and require a derived environment.
- Astrology rules may add `dignity_modifier_any`, `angular_body_any`, and
  `house_context_any`; builder includes matching modifier references only after
  the major-aspect condition succeeds.

- [ ] **Step 1: Write failing rule-boundary tests**

```python
def test_unknown_ten_god_origin_cannot_activate_bazi_candidate(...):
    profile = build_candidate_core_profile(facts_with_unknown_origin, fact_assurance="capability_reported")
    assert profile.bazi_primitive_candidates == ()

def test_dignity_cannot_activate_astrology_candidate_without_major_aspect(...):
    profile = build_candidate_core_profile(facts_with_dignity_only, fact_assurance="capability_reported")
    assert profile.astrology_primitive_candidates == ()
```

- [ ] **Step 2: Run tests and confirm RED**

Run: `python3 -m pytest tests/test_core_profile_builder.py -q`  
Expected: FAIL because origin and modifier conditions are currently ignored.

- [ ] **Step 3: Implement scoped matching**

```python
origin_allowed = all(
    fact.source_kind.value in rule["allowed_source_kinds"]
    for fact in matching_facts
)
environment = derive_candidate_day_master_environment(facts.bazi)
if groups_match and origin_allowed and environment:
    ...

modifier_refs = _astrology_modifier_refs(rule, facts.astrology)
if has_required_major_aspect:
    candidate = PrimitiveCandidate(..., fact_refs=aspect_refs + modifier_refs)
```

`_astrology_modifier_refs` returns empty when no modifier matches and never
changes `direction`; it returns no candidate when the required major aspect is
absent.

- [ ] **Step 4: Verify GREEN**

Run: `python3 -m pytest tests/test_core_profile_builder.py tests/test_candidate_pipeline.py -q`  
Expected: PASS.

### Task 4: Rebind calibration and narrow the promotion gate

**Files:**
- Modify: `src/destiny_personality/core_profile_promotion.py`
- Modify: `tests/test_candidate_promotion_gate.py`
- Modify: `candidates/core-profile-v1/core_profile_calibration_policy_v1.yaml`
- Modify: `docs/domain/core-profile-calibration-review-v1.md`
- Modify: `docs/domain/c4b-calibration-decision-record-v1.md`
- Modify: `docs/domain/bazi-executable-mapping-review-v1.md`
- Modify: `docs/domain/astrology-executable-mapping-review-v1.md`

**Interfaces:**
- Promotion gate removes a blocker only when the corresponding candidate table,
  rule field, Builder behavior, and test are all present.
- Bundle fingerprint is recomputed from candidate YAML excluding its calibration policy.

- [ ] **Step 1: Write the failing promotion test**

```python
def test_candidate_promotion_gate_removes_implemented_fact_blockers():
    blockers = validate_candidate_bundle_for_promotion()
    assert "BAZI_DAY_MASTER_ENVIRONMENT_UNAVAILABLE" not in blockers
    assert "ASTROLOGY_DIGNITY_MODIFIER_UNIMPLEMENTED" not in blockers
```

- [ ] **Step 2: Run test and confirm RED**

Run: `python3 -m pytest tests/test_candidate_promotion_gate.py -q`  
Expected: FAIL because the gate still returns the old static blockers.

- [ ] **Step 3: Implement asset-aware gate and rebind policy**

```python
if not (candidate_root / "bazi_day_master_environment_v1.yaml").exists():
    blockers.append("BAZI_DAY_MASTER_ENVIRONMENT_UNAVAILABLE")
if not _astrology_modifier_fields_present(astrology):
    blockers.append("ASTROLOGY_DIGNITY_MODIFIER_UNIMPLEMENTED")
```

Update the exact `bundle_fingerprint` only after all candidate YAML changes;
run the Design Set and retain `0.75` only if its calibrated maximum remains at
or below that threshold.

- [ ] **Step 4: Verify candidate regression and package regression**

Run:

```bash
python3 -m pytest tests/test_candidate_core_assets.py tests/test_core_profile_builder.py tests/test_core_profile_calibration.py tests/test_candidate_pipeline.py tests/test_candidate_promotion_gate.py -q
python3 -m pytest tests/test_skill_package.py -q
```

Expected: PASS. The promotion gate remains non-empty until every requirement is
implemented; no file is copied to `destiny-personality/configs/`.
