# P004 Dao-Shi Method and Neutral Relations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reconstruct the source-supported Dao-Shi method boundary and add the smallest candidate-only, school-neutral five-element control relation implementation without activating semantic behavior.

**Architecture:** Track A remains a Semantic Knowledge methodology candidate and records source-bound rule status; it never calculates chart facts. Track B is a separate candidate calculation policy and pure relation generator that emits only directed `five_element_controls` facts from chart stems. The generator is not wired into `ChartCalculationService`, Evidence Roots, Semantic Mechanisms, Mapping, or production activation.

**Tech Stack:** Python 3.9+, frozen dataclasses, PyYAML 6, pytest 8, candidate YAML contracts, Markdown governance reports.

## Global Constraints

- Preserve `conditional_limits_supported_high`; never infer `supports_low`.
- Keep `BMC-BZ-P004-DAO-SHI-V1` proposed, `NOT_READY`, `PENDING`, with null PO decision.
- Keep `ER-BZ-TEN-GOD-INTERACTION-V1` withdrawn and create no Evidence Root.
- Keep proposed and approved `PRIMARY_EVIDENCE` at zero and Mapping at zero.
- Do not change active Semantic or Presentation fingerprints.
- Do not use birth samples, golden outputs, calibration, holdout, strength scores, or invented exception precedence.

---

### Task 1: Source-bound methodology reconstruction

**Files:**
- Modify: `tests/test_semantic_knowledge_registry.py`
- Modify: `candidates/semantic-knowledge-v1/bazi_methodology_candidate_contract_v1.yaml`
- Modify: `candidates/semantic-knowledge-v1/bazi_methodology_candidate_registry_v1.yaml`
- Modify: `src/destiny_personality/semantic_knowledge.py`

**Interfaces:**
- Consumes: existing Source IDs `SK-BZ-YUANHAI-ZIPING-PROCESS-P004-V1` and `SK-BZ-SANMING-TONGHUI-DAO-SHI-P004-V1`.
- Produces: ten method-question records with `question`, `current_boundary`, `resolution_status`, `materiality`, `source_refs`, and `exact_locator`.

- [ ] Write failing tests proving coexistence is not an operative rule, every material rule is source-backed, unresolved material rules block readiness, direction never supports Low, and no Primitive state is asserted.
- [ ] Run `python3 -m pytest -q tests/test_semantic_knowledge_registry.py` and verify the new assertions fail because the current three-field decomposition cannot express the evidence boundary.
- [ ] Extend the Bazi candidate contract with allowed statuses `RESOLVED`, `PARTIALLY_RESOLVED`, `UNRESOLVED`, `CONFLICTING`, and `NOT_REQUIRED`; require source references and exact locators for every non-`UNRESOLVED` rule.
- [ ] Update the loader to validate the six-field records and reject `READY_FOR_PO_REVIEW` whenever a material item remains `UNRESOLVED`, `CONFLICTING`, or `PARTIALLY_RESOLVED`.
- [ ] Update the candidate from ten undifferentiated `UNRESOLVED` entries to the source-supported mixture while retaining `NOT_READY`.
- [ ] Re-run the focused tests and verify they pass.

### Task 2: Candidate neutral relation policy and generator

**Files:**
- Create: `candidates/calculation-v1/bazi_neutral_relation_contract_v1.yaml`
- Create: `src/destiny_personality/neutral_bazi_relations.py`
- Create: `tests/test_neutral_bazi_relations.py`

**Interfaces:**
- Consumes: `BaziChartFacts`, visible pillar stems, ordered hidden stems, and the versioned candidate policy.
- Produces: `load_neutral_bazi_relation_policy(root: Path) -> NeutralBaziRelationPolicy` and `derive_candidate_neutral_relations(facts: BaziChartFacts, policy: NeutralBaziRelationPolicy) -> tuple[BaziRelationFact, ...]`.

- [ ] Write failing tests for the five Wu-Xing control pairs, directed participant order, stable ordering, duplicate prevention, stable visible/hidden subject refs, fail-closed unknown stems, and absence of methodology/semantic fields.
- [ ] Run `python3 -m pytest -q tests/test_neutral_bazi_relations.py` and verify import/behavior failures.
- [ ] Add the exact candidate contract: relation ID `five_element_controls`, participant roles `[controller, controlled]`, visible ref `{pillar}.stem`, hidden ref `{pillar}.hidden_stem.{index}`, and an explicit prohibited-field list.
- [ ] Implement a small strict loader and pure generator. Do not modify `ChartCalculationService`, the deterministic codec, or existing relation payloads.
- [ ] Re-run the focused tests and verify deterministic green behavior.

### Task 3: Isolation and governance tests

**Files:**
- Modify: `tests/test_p004_po_gate_closure.py`
- Modify: `tests/test_semantic_evidence_roots.py`

**Interfaces:**
- Consumes: updated candidate and new candidate-only neutral relation contract.
- Produces: regression protection for zero Root/Mechanism/Mapping activation and unchanged permitted Root families.

- [ ] Write failing tests requiring the three new review reports and machine summary, while asserting `deterministic_facts.bazi.relations` is not yet in `permitted_canonical_source_refs`.
- [ ] Run focused tests and verify missing-report failures.
- [ ] Keep Root registry and active semantic assets unchanged; implement only the report-backed assertions required for the final state.
- [ ] Re-run focused tests and verify green.

### Task 4: Review packet and verification

**Files:**
- Create: `docs/reviews/c2-sm-p004-bazi-dao-shi-method-reconstruction-matrix.md`
- Create: `docs/reviews/c2-sm-p004-bazi-dao-shi-method-reconstruction-final-report.md`
- Create: `docs/reviews/c2-sm-p004-bazi-neutral-relation-fact-report.md`
- Create: `docs/reviews/c2-sm-p004-bazi-neutral-relation-fact-final-report.md`
- Create: `docs/reviews/c2-sm-p004-bazi-dao-shi-integration-readiness.md`

**Interfaces:**
- Consumes: Track A source findings and Track B candidate implementation evidence.
- Produces: `DAO_SHI_METHOD_NOT_READY`, relation fact `PARTIAL`, zero Root, zero PRIMARY_EVIDENCE, zero Mapping, and the next gate.

- [ ] Record exact locators, rule claims, conflicts, exceptions, rescue and strength dependencies without long quotations.
- [ ] Explain that the relation generator is deterministic candidate infrastructure but the canonical family is not emitted by a provider and Ten-God subject-ref conformance is not enforced.
- [ ] End the integration report with the required machine-readable summary.
- [ ] Run `python3 -m pytest -q`, `python3 scripts/verify_package.py`, fingerprint checks, and `git diff --check`.
- [ ] Commit the verified change on `codex/p004-dao-shi-reconstruction`; do not publish or merge without a separate publish instruction.

## Self-review

- Spec coverage: Track A source scope, ten questions, exceptions/rescue/strength, Track B direction/dedup/provenance boundary, no Root, no mechanism, no Mapping, reports, and verification are each assigned.
- Placeholder scan: no implementation step depends on an unspecified algorithm; unresolved method questions remain deliberately fail-closed.
- Type consistency: the generator returns the repository's existing immutable `BaziRelationFact`; no new active facts schema is claimed.
