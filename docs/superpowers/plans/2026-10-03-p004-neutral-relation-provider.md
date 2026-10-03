# P004 Neutral Bazi Relation Provider Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Emit governed, versioned neutral Bazi control relations from an explicitly selected candidate provider while enforcing joinable Ten-God subject references.

**Architecture:** Add rule provenance to the existing relation fact, then compose the existing Bazi calculator behind a candidate-only provider decorator. Keep the default calculation service and all semantic activation registries unchanged.

**Tech Stack:** Python 3.9+, frozen dataclasses, protocols, PyYAML, pytest.

## Global Constraints

- Keep Semantic Core and Semantic Knowledge active assets frozen.
- Do not create or approve Evidence Roots, PRIMARY_EVIDENCE, Mapping, golden, or calibration assets.
- Do not implement Dao-Shi strength, rescue, exception, qualification, or primitive direction.
- The provider must require explicit caller injection and remain absent from default CLI/runtime construction.
- Follow red-green-refactor for every behaviour change.

---

### Task 1: Versioned relation transport and validation

**Files:**
- Modify: `src/destiny_personality/calculation/models.py`
- Modify: `src/destiny_personality/deterministic_facts_codec.py`
- Modify: `src/destiny_personality/calculation/validation/bazi.py`
- Modify: `tests/test_neutral_bazi_relations.py`
- Modify: `tests/test_calculation_contract_validation.py`

**Interfaces:**
- Produces: `BaziRelationFact.rule_version: str` with compatibility default `unversioned`.
- Produces: deterministic-facts JSON relation member `rule_version`.

- [ ] **Step 1: Write failing provenance tests**

Add assertions that candidate relations use `wuxing-control-v1`, that the codec
round-trips the field, and that the Bazi contract rejects an empty rule version.

```python
assert relation.rule_version == "wuxing-control-v1"
assert payload["bazi"]["relations"][0]["rule_version"] == "wuxing-control-v1"
with pytest.raises(CalculationError) as caught:
    service.calculate(...replace(relation, rule_version="")...)
assert caught.value.field == "relations.0.rule_version"
```

- [ ] **Step 2: Run tests and verify RED**

Run:
`PYTHONPATH=src python3 -m pytest tests/test_neutral_bazi_relations.py tests/test_calculation_contract_validation.py -q`

Expected: failures because `rule_version` is absent.

- [ ] **Step 3: Implement minimal transport**

Add the dataclass field, serialize/decode it, set it in neutral derivation, and
validate it with `validate_nonempty_string`.

```python
@dataclass(frozen=True)
class BaziRelationFact:
    relation_type: str
    participant_refs: Tuple[str, ...]
    source_pillars: Tuple[PillarPosition, ...]
    rule_version: str = "unversioned"
```

- [ ] **Step 4: Run focused tests and verify GREEN**

Run the command from Step 2. Expected: all selected tests pass.

### Task 2: Candidate provider and Ten-God join conformance

**Files:**
- Create: `src/destiny_personality/candidate_bazi_provider.py`
- Modify: `src/destiny_personality/neutral_bazi_relations.py`
- Create: `tests/test_candidate_bazi_provider.py`
- Modify: `candidates/calculation-v1/bazi_neutral_relation_contract_v1.yaml`

**Interfaces:**
- Consumes: `derive_candidate_neutral_relations(facts, policy)`.
- Produces: `CandidateNeutralRelationBaziCalculator(delegate, policy)` implementing `calculate(birth_input, normalized_time, methodology) -> BaziChartFacts`.
- Produces: `validate_ten_god_subject_refs(facts, policy) -> None`.

- [ ] **Step 1: Write provider integration tests**

Cover visible and hidden references, explicit service injection, deterministic
provenance, unrelated-relation preservation, duplicate governed-relation
rejection, `UNKNOWN` source-kind rejection, bad reference rejection, and
source-pillar mismatch rejection.

```python
provider = CandidateNeutralRelationBaziCalculator(delegate, policy)
service = ChartCalculationService(normalizer, provider, astrology)
result = service.calculate(birth_input, runtime_config)
assert any(
    relation.relation_type == "five_element_controls"
    and relation.rule_version == "wuxing-control-v1"
    for relation in result.bazi.relations
)
```

- [ ] **Step 2: Run provider tests and verify RED**

Run: `PYTHONPATH=src python3 -m pytest tests/test_candidate_bazi_provider.py -q`

Expected: collection failure because the provider module is absent.

- [ ] **Step 3: Implement the provider decorator**

Use `dataclasses.replace`, validate each Ten-God reference against the governed
subject catalogue, reject a pre-existing `five_element_controls` relation, and
append generated relations in deterministic order.

```python
class CandidateNeutralRelationBaziCalculator:
    def calculate(self, birth_input, normalized_time, methodology):
        facts = self._delegate.calculate(birth_input, normalized_time, methodology)
        validate_ten_god_subject_refs(facts, self._policy)
        generated = derive_candidate_neutral_relations(facts, self._policy)
        return replace(facts, relations=tuple(facts.relations) + generated)
```

Update candidate status to `candidate_provider_available_not_activated` without
changing `review_status: candidate_only` or `activation_status: inactive`.

- [ ] **Step 4: Run provider and calculation tests and verify GREEN**

Run:
`PYTHONPATH=src python3 -m pytest tests/test_candidate_bazi_provider.py tests/test_neutral_bazi_relations.py tests/test_calculation_service.py tests/test_calculation_contract_validation.py tests/test_bazi_provenance.py -q`

Expected: all selected tests pass.

### Task 3: Governance closure and full verification

**Files:**
- Modify: `candidates/semantic-knowledge-v1/bazi_methodology_candidate_registry_v1.yaml`
- Create: `docs/reviews/c2-sm-p004-bazi-neutral-relation-provider-final-report.md`
- Modify: `docs/reviews/c2-sm-p004-bazi-dao-shi-integration-readiness.md`
- Modify: `tests/test_p004_po_gate_closure.py`
- Modify: `tests/test_semantic_evidence_roots.py`

**Interfaces:**
- Produces: auditable status `CANDIDATE_PROVIDER_AVAILABLE_NOT_ACTIVATED`.
- Preserves: zero Evidence Root, PRIMARY_EVIDENCE, Mapping, and production activation.

- [ ] **Step 1: Write failing governance assertions**

Require the provider report, candidate-emitted status, unchanged Dao-Shi method
status, unchanged active fingerprints, and continued rejection of
`deterministic_facts.bazi.relations` as an approved Root.

- [ ] **Step 2: Run governance tests and verify RED**

Run:
`PYTHONPATH=src python3 -m pytest tests/test_p004_po_gate_closure.py tests/test_semantic_evidence_roots.py tests/test_semantic_knowledge_registry.py -q`

Expected: failures until status assets and report are updated.

- [ ] **Step 3: Update candidate governance documents**

Record provider availability, successful join conformance, and the next gate as
`EVIDENCE_ROOT_PROPOSAL_REVIEW`. State explicitly that the method remains
`NOT_READY` and no Root is created in this change.

- [ ] **Step 4: Run governance tests and verify GREEN**

Run the command from Step 2. Expected: all selected tests pass.

- [ ] **Step 5: Run final verification**

Run:

```bash
PYTHONPATH=src python3 -m pytest -q
python3 scripts/verify_package.py
git diff --check
```

Verify exact fingerprints:

```text
semantic: 256ba053b174a054226301f1b493e0e0c8f9f50e9f2976a72b8045dbf6ed6131
presentation: 2f1d3866638074485351ada0c6a9aaa9bd1acd916f65973ca2b319a75b99b91d
```

- [ ] **Step 6: Commit the implementation**

```bash
git add candidates docs src tests
git commit -m "feat: emit candidate neutral Bazi relations"
```
