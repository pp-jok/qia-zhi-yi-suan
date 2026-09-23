# C2-SM Phase 2A Evidence Roots Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Admit two candidate-only, project-owned Evidence Root definitions for deterministic Bazi Ten-God and astrology aspect fact instances, without creating semantic mechanisms, mappings, or runtime behavior.

**Architecture:** Extend the C2-SM registry loader so every root is validated against the root contract before it can be used. Store two approved fact-identity definitions in the candidate-only registry. The loader returns only approved IDs to existing mechanism validation and supplies an audit summary; it has no dependency from the active runtime.

**Tech Stack:** Python 3.9+, dataclasses, PyYAML, pytest, candidate YAML contracts.

## Global Constraints

- Root records describe canonical fact-instance identity only; they must not contain personality direction or Primitive state claims.
- This phase creates exactly two Evidence Roots and zero Semantic Mechanism candidates.
- Do not modify active mappings, profile runtime, active semantic/presentation fingerprint functions, calibration, Signature, C3, or package data.
- Roots with missing contract fields, duplicate IDs, unknown review statuses, or prohibited provenance origins must fail closed.
- The active semantic fingerprint must remain `256ba053b174a054226301f1b493e0e0c8f9f50e9f2976a72b8045dbf6ed6131` and the active presentation fingerprint must remain `2f1d3866638074485351ada0c6a9aaa9bd1acd916f65973ca2b319a75b99b91d`.

---

### Task 1: Add failing Evidence Root admission tests

**Files:**
- Modify: `tests/test_semantic_evidence_roots.py`

**Interfaces:**
- Consumes: `load_evidence_root_registry(root: Path) -> tuple[Mapping[str, object], ...]`, `load_approved_evidence_root_ids(root: Path) -> frozenset[str]`, `build_evidence_root_audit_report(roots) -> Mapping[str, int]`.
- Produces: executable proof for valid approved roots, malformed entries, duplicate IDs, unknown review statuses, and Golden-Sample provenance.

- [x] **Step 1: Write the failing registry admission test**

```python
def test_registry_loads_the_two_approved_fact_identity_roots() -> None:
    roots = load_evidence_root_registry(_candidate_root())

    assert {root["evidence_root_id"] for root in roots} == {
        "ER-BZ-TEN-GOD-INSTANCE-V1",
        "ER-AS-ASPECT-INSTANCE-V1",
    }
    assert load_approved_evidence_root_ids(_candidate_root()) == {
        "ER-BZ-TEN-GOD-INSTANCE-V1",
        "ER-AS-ASPECT-INSTANCE-V1",
    }
```

- [x] **Step 2: Write failing contract-rejection tests**

```python
@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    [
        (lambda root: root.pop("scope"), "CONFIG_GAP"),
        (lambda root: root.__setitem__("review_status", "unreviewed"), "CONFIG_VALUE_ERROR"),
        (lambda root: root["provenance"].__setitem__("origin", "golden_sample"), "CONFIG_VALUE_ERROR"),
    ],
)
def test_registry_rejects_invalid_root_entries(mutation, expected_code, tmp_path):
    registry = _registry_with_root(tmp_path)
    mutation(registry["roots"][0])
    _write_registry(tmp_path, registry)

    with pytest.raises(ConfigError) as error:
        load_evidence_root_registry(tmp_path)
    assert error.value.code == expected_code
```

- [x] **Step 3: Write the duplicate-ID and audit tests**

```python
def test_registry_rejects_duplicate_root_ids(tmp_path) -> None:
    registry = _registry_with_root(tmp_path)
    registry["roots"].append(copy.deepcopy(registry["roots"][0]))
    _write_registry(tmp_path, registry)

    with pytest.raises(ConfigError) as error:
        load_evidence_root_registry(tmp_path)
    assert error.value.code == "CONFIG_VALUE_ERROR"


def test_root_audit_reports_two_approved_and_zero_other_roots() -> None:
    report = build_evidence_root_audit_report(load_evidence_root_registry(_candidate_root()))

    assert report == {"root_count": 2, "approved_count": 2, "non_approved_count": 0}
```

- [x] **Step 4: Run the focused tests and confirm RED**

Run: `python3 -m pytest -q tests/test_semantic_evidence_roots.py`

Expected: FAIL because `load_evidence_root_registry` and `build_evidence_root_audit_report` do not exist, and the Registry is empty.

---

### Task 2: Implement fail-closed Root Registry validation

**Files:**
- Modify: `candidates/semantic-mechanisms-v1/semantic_evidence_root_contract_v1.yaml`
- Modify: `src/destiny_personality/semantic_mechanisms.py`
- Test: `tests/test_semantic_evidence_roots.py`

**Interfaces:**
- `load_evidence_root_registry(root: Path) -> Tuple[Mapping[str, object], ...]`
- `build_evidence_root_audit_report(roots: Collection[Mapping[str, object]]) -> Mapping[str, int]`
- `load_approved_evidence_root_ids(root: Path) -> frozenset[str]` delegates to the validated registry.

- [x] **Step 1: Extend the root contract**

Add these fields to `semantic_evidence_root_contract_v1.yaml`:

```yaml
allowed_review_statuses: [proposed, approved, rejected, deferred]
prohibited_origins: [golden_sample, legacy_output, desired_personality, renderer_wording]
required_root_fields:
  - evidence_root_id
  - system
  - source_type
  - source_ref
  - version
  - scope
  - approved_use
  - prohibited_use
  - provenance
  - review_status
  - product_owner_decision_ref
```

- [x] **Step 2: Implement the minimal validator and loader**

```python
def load_evidence_root_registry(root: Path) -> Tuple[Mapping[str, object], ...]:
    registry = _load_mapping(Path(root), EVIDENCE_ROOT_REGISTRY_FILE)
    _require_equal(registry, "schema_version", EVIDENCE_ROOT_REGISTRY_SCHEMA_VERSION,
                   EVIDENCE_ROOT_REGISTRY_FILE)
    roots = _require_list(registry, "roots", EVIDENCE_ROOT_REGISTRY_FILE)
    seen_ids = set()
    for index, entry in enumerate(roots):
        _validate_evidence_root(entry, index, seen_ids)
    return tuple(roots)


def build_evidence_root_audit_report(
    roots: Collection[Mapping[str, object]],
) -> Mapping[str, int]:
    approved_count = sum(root["review_status"] == "approved" for root in roots)
    return {
        "root_count": len(roots),
        "approved_count": approved_count,
        "non_approved_count": len(roots) - approved_count,
    }
```

`_validate_evidence_root` must require each named contract field, reject non-mapping entries, non-empty string violations, duplicate `evidence_root_id`, review statuses outside the contract list, empty `scope`/`approved_use`/`prohibited_use` mappings or lists, a non-mapping `provenance`, and prohibited `provenance.origin` values. Raise `ConfigError` with `CONFIG_GAP`, `CONFIG_TYPE_ERROR`, or `CONFIG_VALUE_ERROR` and the registry file/field.

- [x] **Step 3: Rework approved-ID loading to use the validated registry**

```python
def load_approved_evidence_root_ids(root: Path) -> frozenset[str]:
    return frozenset(
        entry["evidence_root_id"]
        for entry in load_evidence_root_registry(root)
        if entry["review_status"] == "approved"
    )
```

- [x] **Step 4: Run focused tests and confirm GREEN**

Run: `python3 -m pytest -q tests/test_semantic_evidence_roots.py`

Expected: PASS after Task 3 populates the two valid root entries.

---

### Task 3: Admit two fact-identity Root definitions

**Files:**
- Modify: `candidates/semantic-mechanisms-v1/semantic_evidence_root_registry_v1.yaml`
- Test: `tests/test_semantic_evidence_roots.py`

**Interfaces:**
- Produces two validated registry mappings consumed by `load_evidence_root_registry`.
- Produces exactly two IDs in `load_approved_evidence_root_ids`.

- [x] **Step 1: Add the Bazi Ten-God identity root**

```yaml
- evidence_root_id: ER-BZ-TEN-GOD-INSTANCE-V1
  system: bazi
  source_type: canonical_fact_instance
  source_ref: deterministic_facts.bazi.ten_gods
  version: deterministic-chart-facts-v1
  scope:
    identity_fields: [subject_ref, ten_god, source_pillars, source_kind]
  approved_use: [fact_instance_identification, candidate_mechanism_evidence_reference]
  prohibited_use: [direct_primitive_state_assertion, mapping_rule_creation]
  provenance:
    origin: project_owned_deterministic_facts
    methodology_ref: bazi-core-v1.0
  review_status: approved
  product_owner_decision_ref: PO-DELEGATED-C2-SM-PHASE-2A-2026-09-22
```

- [x] **Step 2: Add the astrology aspect identity root**

```yaml
- evidence_root_id: ER-AS-ASPECT-INSTANCE-V1
  system: astrology
  source_type: canonical_fact_instance
  source_ref: deterministic_facts.astrology.aspects
  version: deterministic-chart-facts-v1
  scope:
    identity_fields: [body_a, body_b, aspect_type, orb]
  approved_use: [fact_instance_identification, candidate_mechanism_evidence_reference]
  prohibited_use: [direct_primitive_state_assertion, mapping_rule_creation]
  provenance:
    origin: project_owned_deterministic_facts
    methodology_ref: western-tropical-v1.0
  review_status: approved
  product_owner_decision_ref: PO-DELEGATED-C2-SM-PHASE-2A-2026-09-22
```

- [x] **Step 3: Verify no mechanism candidate was added**

Run: `find candidates/semantic-mechanisms-v1/mechanism_candidates -type f -name '*.yaml' 2>/dev/null`

Expected: no output; the directory is intentionally absent.

---

### Task 4: Update governance records and verify isolation

**Files:**
- Modify: `docs/domain/c2-semantic-mechanism-governance-v1.md`
- Modify: `docs/domain/c2-semantic-evidence-root-review-v1.md`
- Modify: `docs/domain/c2-semantic-mechanism-review-v1.md`
- Modify: `docs/reviews/c2-sm-infrastructure-verification.md`
- Create: `docs/reviews/c2-sm-phase-2a-evidence-root-verification.md`

**Interfaces:**
- Consumes validated root registry and fingerprint commands.
- Produces the Phase 2A review record and a clear next gate.

- [x] **Step 1: Record the approved root identities and their non-semantic boundary**

Set Evidence Root count to 2, Approved Evidence Root count to 2, Semantic Mechanism count to 0, and state that approval is limited to fact identity and candidate mechanism reference.

- [x] **Step 2: Record the validation evidence**

Include focused test output, full-suite output, package verification, active semantic/presentation fingerprints, candidate-mechanism fingerprint, and the Root audit report. State that the candidate fingerprint is allowed to change while the active fingerprints must not.

- [x] **Step 3: Run final verification**

Run:

```text
python3 -m pytest -q tests/test_semantic_mechanism_contract.py tests/test_semantic_evidence_roots.py tests/test_semantic_mechanism_legacy_guard.py tests/test_semantic_mechanism_golden_leak.py tests/test_semantic_mechanism_activation_isolation.py
python3 -m pytest -q --disable-warnings
python3 scripts/verify_package.py
PYTHONPATH=src python3 -c "from pathlib import Path; from destiny_personality.semantic_mechanisms import load_evidence_root_registry, build_evidence_root_audit_report; r=load_evidence_root_registry(Path('candidates/semantic-mechanisms-v1')); print(build_evidence_root_audit_report(r))"
```

Expected: all tests and package verification pass; Root audit is `{root_count: 2, approved_count: 2, non_approved_count: 0}`; active fingerprints remain frozen; zero mechanism candidates remain.
