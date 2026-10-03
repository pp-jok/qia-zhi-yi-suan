# Bazi Neutral Relation Canonical Adoption Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `five_element_controls` a provider-independent canonical Bazi fact family without activating a production provider or changing any P004 semantic state.

**Architecture:** Package three machine-readable canonical contracts for hidden-stem order, subject references, and relation identity. The explicit candidate provider normalizes provider output to those contracts, while the calculation and qualified-facts boundaries independently fail closed on noncanonical order, unknown rule versions, unresolved subjects, and false control claims.

**Tech Stack:** Python 3.9+, frozen dataclasses, PyYAML, pytest, setuptools package data.

## Global Constraints

- Preserve `BMC-BZ-P004-DAO-SHI-V1: NOT_READY`.
- Preserve zero Evidence Roots, zero PRIMARY_EVIDENCE, zero Mapping, and no production activation.
- Do not add strength, rescue, exception, operative, Dao-Shi, personality, Primitive, or direction semantics.
- Keep default Bazi provider/output behaviour unchanged; empty relations remain valid.
- Keep the active Semantic and Presentation fingerprints unchanged.
- Use project-owned offline rules only; no runtime network, LLM, user birth data, golden profiles, calibration, or holdout inputs.

---

### Task 1: Canonical identity contracts and loader

**Files:**
- Create: `src/destiny_personality/canonical_assets/calculation-v1/bazi_hidden_stem_order_v1.yaml`
- Create: `src/destiny_personality/canonical_assets/calculation-v1/bazi_subject_ref_contract_v1.yaml`
- Create: `src/destiny_personality/canonical_assets/calculation-v1/bazi_relation_canonical_contract_v1.yaml`
- Create: `src/destiny_personality/canonical_bazi_relations.py`
- Create: `tests/test_bazi_relation_canonical_contract.py`
- Modify: `pyproject.toml`

**Interfaces:**
- Produces: `canonical_bazi_relation_asset_root() -> Path`.
- Produces: `load_canonical_bazi_relation_policy(root: Optional[Path] = None) -> CanonicalBaziRelationPolicy`.
- Produces: `canonical_relation_identity(relation) -> Tuple[str, Tuple[str, ...], str]`.
- Produces: `canonical_relation_policy_fingerprint(root: Optional[Path] = None) -> str`.

- [ ] **Step 1: Write failing contract tests**

Require all twelve branches, exact ordered tuples, four pillars, visible/hidden
templates, source-kind mapping, valid/invalid examples, one approved relation
type/version, explicit identity/provenance fields, semantic exclusions, and a
stable three-file fingerprint.

```python
policy = load_canonical_bazi_relation_policy()
assert policy.hidden_stems["辰"] == ("戊", "乙", "癸")
assert policy.identity_fields == (
    "relation_type", "participant_refs", "rule_version"
)
assert policy.provenance_fields == ("source_pillars",)
assert policy.approved_rule_versions == {"five_element_controls": "wuxing-control-v1"}
```

- [ ] **Step 2: Run RED**

Run: `PYTHONPATH=src python3 -m pytest tests/test_bazi_relation_canonical_contract.py -q`

Expected: import/asset failures because the canonical contract does not exist.

- [ ] **Step 3: Implement strict loader and packaged assets**

Define identity-only hidden-stem ordering without strength labels. Put the
stem-to-element and control cycle in the canonical relation contract. Reject
unknown/missing keys, incomplete branches/stems, unapproved versions, and any
semantic prohibited-field gap.

- [ ] **Step 4: Run GREEN**

Run the command from Step 2. Expected: all contract tests pass.

### Task 2: Cross-provider canonicalization and explicit relation identity

**Files:**
- Modify: `src/destiny_personality/neutral_bazi_relations.py`
- Modify: `src/destiny_personality/candidate_bazi_provider.py`
- Modify: `tests/test_candidate_bazi_provider.py`
- Modify: `tests/test_neutral_bazi_relations.py`

**Interfaces:**
- Consumes: `CanonicalBaziRelationPolicy`.
- Produces: `canonicalize_bazi_subjects(facts, policy) -> BaziChartFacts`.
- Produces: `derive_canonical_neutral_relations(facts, policy) -> Tuple[BaziRelationFact, ...]`.
- Preserves: `derive_candidate_neutral_relations` as a compatibility alias.

- [ ] **Step 1: Write failing provider-independence tests**

Create providers that return the same branch/stems in canonical and reversed
orders. Require identical normalized hidden stems, remapped Ten-God refs,
relation identities, directions, and deterministic serialized dictionaries.

```python
canonical = provider_for(("戊", "乙", "癸"), "month.hidden_stem.0")
reversed_order = provider_for(("癸", "乙", "戊"), "month.hidden_stem.2")
assert normalize(canonical) == normalize(reversed_order)
```

Require wrong stem membership, missing pillar data, duplicate provenance, and
unresolvable hidden refs to fail closed.

- [ ] **Step 2: Run RED**

Run:
`PYTHONPATH=src python3 -m pytest tests/test_candidate_bazi_provider.py tests/test_neutral_bazi_relations.py -q`

Expected: provider-independence assertions fail because tuple order currently
defines index identity.

- [ ] **Step 3: Implement normalization and explicit identity**

Normalize each declared pillar by its actual earthly branch, remap indexed
Ten-God and relation refs by stem identity, require one hidden-stem record for
every present pillar in the explicit provider, derive/deduplicate with
`canonical_relation_identity`, and sort by the canonical identity fields.

- [ ] **Step 4: Run GREEN**

Run the command from Step 2. Expected: all selected tests pass.

### Task 3: Canonical calculation and qualified-facts validation

**Files:**
- Modify: `src/destiny_personality/calculation/validation/bazi.py`
- Modify: `src/destiny_personality/deterministic_facts_codec.py`
- Modify: `tests/test_calculation_contract_validation.py`
- Modify: `tests/test_birth_input_contract.py`
- Create: `tests/test_bazi_relation_qualification_boundary.py`

**Interfaces:**
- Produces: `validate_canonical_bazi_relations(facts, policy) -> None`.
- Produces: stable error code `BAZI_RELATION_FACT_INVALID` for false canonical relations.
- Preserves: decoding legacy facts without `rule_version` as `unversioned` for noncanonical relation types.

- [ ] **Step 1: Write failing validation tests**

Require rejection of wrong hidden order, nonexistent refs, false element
control, unknown rule version, duplicate canonical identity, and source-pillar
mismatch. Require empty relation tuples and legacy noncanonical facts to remain
valid.

```python
false_relation = BaziRelationFact(
    "five_element_controls",
    ("year.stem", "month.stem"),
    (PillarPosition.YEAR, PillarPosition.MONTH),
    "wuxing-control-v1",
)
with pytest.raises(CalculationError) as caught:
    service.calculate(...facts whose year stem does not control month stem...)
assert caught.value.code == "BAZI_RELATION_FACT_INVALID"
```

Require `load_validated_deterministic_facts` to apply the same canonical checks
without changing fact-assurance derivation.

- [ ] **Step 2: Run RED**

Run:
`PYTHONPATH=src python3 -m pytest tests/test_calculation_contract_validation.py tests/test_bazi_relation_qualification_boundary.py tests/test_birth_input_contract.py -q`

Expected: false/unknown canonical relations are currently accepted.

- [ ] **Step 3: Implement semantic-free consistency validation**

Resolve each participant to its actual visible or canonical hidden stem, check
the approved version and element-control table, reject duplicate explicit
identity, and treat `source_pillars` only as validated provenance. Invoke this
from both the service Bazi validator and qualified-facts loader.

- [ ] **Step 4: Run GREEN**

Run the command from Step 2. Expected: all selected tests pass.

### Task 4: Candidate transition, adoption decision, and closure

**Files:**
- Modify: `candidates/calculation-v1/bazi_neutral_relation_contract_v1.yaml`
- Modify: `docs/reviews/c2-sm-p004-bazi-dao-shi-integration-readiness.md`
- Create: `docs/reviews/c2-sm-p004-bazi-hidden-stem-identity-audit.md`
- Create: `docs/reviews/c2-sm-p004-bazi-subject-ref-contract-review.md`
- Create: `docs/reviews/c2-sm-p004-bazi-relation-canonical-contract-review.md`
- Create: `docs/reviews/c2-sm-p004-bazi-neutral-relation-canonical-adoption.md`
- Create: `docs/reviews/c2-sm-p004-bazi-neutral-relation-canonical-adoption-final-report.md`
- Modify: `tests/test_p004_po_gate_closure.py`
- Modify: `tests/test_semantic_evidence_roots.py`

**Interfaces:**
- Produces: `deterministic_facts.bazi.relations: CANONICAL` only if Tasks 1–3 pass.
- Produces: `Evidence Root Proposal Readiness: READY` without creating a Root.
- Preserves: method `NOT_READY`, zero semantic assets, and default provider unchanged.

- [ ] **Step 1: Write failing governance tests**

Require all five reports, unambiguous method counts, candidate transition audit,
canonical family decision, reference-only provider authority, zero Root entries,
zero semantic/mapping changes, and next gate
`GENERIC_BAZI_RELATION_EVIDENCE_ROOT_PROPOSAL`.

- [ ] **Step 2: Run RED**

Run:
`PYTHONPATH=src python3 -m pytest tests/test_p004_po_gate_closure.py tests/test_semantic_evidence_roots.py -q`

Expected: missing reports and obsolete next-gate/count wording fail.

- [ ] **Step 3: Write transition assets and reports**

Mark the old candidate contract historical/superseded. Record why raw element
control is school-neutral, why the provider remains reference-only, why
canonical adoption does not make Dao-Shi ready, and why the Root is deferred to
the next independent gate.

- [ ] **Step 4: Run GREEN**

Run the command from Step 2. Expected: all selected tests pass.

- [ ] **Step 5: Run full verification**

```bash
PYTHONPATH=src python3 -m pytest -q
python3 scripts/verify_package.py
git diff --check
```

Verify the active fingerprints remain exactly:

```text
semantic: 256ba053b174a054226301f1b493e0e0c8f9f50e9f2976a72b8045dbf6ed6131
presentation: 2f1d3866638074485351ada0c6a9aaa9bd1acd916f65973ca2b319a75b99b91d
```

- [ ] **Step 6: Commit and update PR #2**

```bash
git add candidates docs pyproject.toml src tests
git commit -m "feat: adopt canonical Bazi relation identity"
git push origin codex/p004-dao-shi-reconstruction
```
