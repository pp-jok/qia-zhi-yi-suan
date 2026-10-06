# Semantic Bridge Governance and P006 Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add enforceable Semantic Bridge governance, adjudicate the P006 pilot without semantic inflation, and open a non-runtime ontology-v3 candidate after the pilot fails.

**Architecture:** Reuse the current Claim → Semantic Mechanism → PRIMARY_EVIDENCE → Mapping chain. Add one candidate policy asset and validation functions in the existing Semantic Mechanism module, correct candidate resolver scope handling, and keep the package-owned formal release bundle empty. Research and ontology-discovery results remain versioned candidate/governance assets.

**Tech Stack:** Python 3.9+, PyYAML, pytest, Markdown review records, YAML policy assets, setuptools.

## Global Constraints

- Preserve v0.4.1 reports, matrices, corpora, and closure decisions as historical truth under the direct-construct policy.
- Do not admit symbolic analogy, capability/role, temperament-only, or outcome-only wording as PRIMARY_EVIDENCE.
- High and Low evidence are independent; absence is never opposite evidence.
- Local work evidence cannot become a global Primitive state without promotion authority.
- Fact, traditional method, traditional claim, Semantic Bridge, PRIMARY_EVIDENCE, Mapping, and Primitive state remain separate layers.
- Do not add a new scoring system, renderer inference, or large Bridge subsystem.
- P006 is the only reopened current Primitive.
- Formal runtime remains six `unknown` unless the full Bridge → Method → Fact → Root → PE → Mapping chain passes.
- If formal activation remains zero, release v0.4.2; reserve v0.5.0 for a formal non-zero Primitive.

---

### Task 1: Define Semantic Bridge policy acceptance tests

**Files:**
- Create: `tests/test_semantic_bridge_governance.py`
- Inspect: `src/destiny_personality/semantic_mechanisms.py`
- Inspect: `tests/test_semantic_mechanism_contract.py`

**Interfaces:**
- Consumes: existing `SemanticMechanismFinding` and semantic-mechanism validation API.
- Produces: executable requirements for `load_semantic_bridge_policy`, `validate_semantic_bridge_candidate`, and approved PRIMARY_EVIDENCE enforcement.

- [ ] **Step 1: Write failing policy and admission tests**

Create fixtures for a valid direct bridge and behavioural bridge. Assert that both pass all ten gates; capability, temperament, outcome, and symbolic classes return blocking codes; missing source behaviour, wrong subject, absent ownership rationale, unresolved alternatives, and empirical-psychology claims fail closed.

- [ ] **Step 2: Write failing PRIMARY_EVIDENCE integration tests**

Assert that an approved `PRIMARY_EVIDENCE` mechanism without a Bridge audit is rejected, a semantically valid but method-blocked bridge cannot become approved PE, and a `RULE_GATE` remains valid without Bridge fields.

- [ ] **Step 3: Verify RED**

Run: `python3 -m pytest tests/test_semantic_bridge_governance.py -q`

Expected: import/file failures because the policy and validator do not exist.

- [ ] **Step 4: Commit RED contract**

```bash
git add tests/test_semantic_bridge_governance.py
git commit -m "test: define semantic bridge governance contract"
```

### Task 2: Implement the minimal Bridge policy and validator

**Files:**
- Create: `candidates/semantic-core-v1/semantic_bridge_policy_v1.yaml`
- Modify: `src/destiny_personality/semantic_mechanisms.py`
- Modify: `candidates/semantic-mechanisms-v1/semantic_mechanism_contract_v1.yaml`
- Test: `tests/test_semantic_bridge_governance.py`
- Test: `tests/test_semantic_mechanism_contract.py`

**Interfaces:**
- Produces: `SemanticBridgePolicy`, `load_semantic_bridge_policy(project_root: Path)`, and `validate_semantic_bridge_candidate(bridge, policy) -> Tuple[SemanticMechanismFinding, ...]`.
- Produces: approved PE validation requiring `semantic_bridge` and reproducible method status.

- [ ] **Step 1: Add the policy asset**

Encode the six classes, two admissible classes, four rejected classes, exact ten gate names, directions `supported_high`/`supported_low`, local-first context rule, `traditional_system_semantic_translation` scientific boundary, and no score.

- [ ] **Step 2: Add strict loading and validation**

Load exact schema `semantic-bridge-policy-v1`. Reject malformed policy fields. Validate identity, source behaviour, person/native subject, process meaning, ownership/direction rationale, contexts, alternatives and exclusions, counterevidence, scientific boundary, and all gate values.

- [ ] **Step 3: Bind approved PRIMARY_EVIDENCE**

In `validate_semantic_mechanism_candidate`, require an approved PE to contain a Bridge audit with no errors and `traditional_method_status: reproducible`. Keep all current non-PE assets valid.

- [ ] **Step 4: Verify GREEN and regressions**

Run: `python3 -m pytest tests/test_semantic_bridge_governance.py tests/test_semantic_mechanism_contract.py tests/test_master_semantic_core.py -q`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add candidates/semantic-core-v1/semantic_bridge_policy_v1.yaml candidates/semantic-mechanisms-v1/semantic_mechanism_contract_v1.yaml src/destiny_personality/semantic_mechanisms.py tests/test_semantic_bridge_governance.py
git commit -m "feat: govern semantic bridge admission"
```

### Task 3: Correct single-direction and local-context resolution

**Files:**
- Modify: `tests/test_semantic_core_nonzero_pipeline.py`
- Modify: `src/destiny_personality/semantic_pipeline.py`

**Interfaces:**
- Consumes: Mapping dictionaries with `proposed_direction.state`, `contexts`, optional `global_eligible`, and optional `semantic_bridge_refs`.
- Produces: local `context_states`, global `context_differentiated` when promotion is absent, and retained `bridge_refs`.

- [ ] **Step 1: Add RED resolver tests**

Assert:

```python
single_global_high -> supported_high
single_work_high -> context_differentiated with work=supported_high
single_work_high_without_low -> remains valid local high
no_mapping -> no low inference
local_high_with_global_eligible_false -> not global
semantic_bridge_refs -> retained in primitive and provenance
```

- [ ] **Step 2: Verify RED**

Run: `python3 -m pytest tests/test_semantic_core_nonzero_pipeline.py -q -k 'single_direction or local_bridge or bridge_ref'`

Expected: FAIL because current resolver promotes one local mapping to a top-level High state and drops Bridge refs.

- [ ] **Step 3: Implement minimal scope correction**

Resolve top-level direction only from mappings with no local contexts or explicit `global_eligible: true`. If only local mappings exist, emit `context_differentiated`. Preserve direction independence and declared Bridge provenance.

- [ ] **Step 4: Verify GREEN and full semantic pipeline file**

Run: `python3 -m pytest tests/test_semantic_core_nonzero_pipeline.py tests/test_master_semantic_core.py -q`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/destiny_personality/semantic_pipeline.py tests/test_semantic_core_nonzero_pipeline.py
git commit -m "fix: preserve local scope and one-sided evidence"
```

### Task 4: Adjudicate the P006 Bridge pilot

**Files:**
- Create: `docs/reviews/p006-semantic-bridge-pilot-matrix.md`
- Create: `docs/reviews/p006-semantic-bridge-pilot-final-report.md`
- Create: `tests/test_p006_semantic_bridge_pilot.py`

**Interfaces:**
- Consumes: v0.4.1 P006 reports, exact Bazi passages, Ptolemy III.13, and the Bridge policy.
- Produces: Exit C decision with zero PE and Mapping.

- [ ] **Step 1: Write RED document-contract tests**

Require the matrix columns Candidate, Source, Exact context, Source meaning,
Bridge class, P006 ownership, Direction, Context, Alternative interpretations,
and Result. Require independent High/Low outcomes, all six candidate phrases,
ten-gate rationale, and exact zero activation counts.

- [ ] **Step 2: Write the matrix from exact contexts**

Classify `处事有方`, `治事无规`, `布置有方`, `able to direct business`,
`systematic workers`, and `prone to change their minds`. Record capability,
negative capability, temperament, compound-list ambiguity, unresolved method,
and P002/discipline/occupation alternatives.

- [ ] **Step 3: Write the final report**

Include all sections mandated by the execution specification and conclude:

`P006_BEHAVIORAL_BRIDGE_FAIL_CAPABILITY_OR_TEMPERAMENT_ONLY`

Record Bridge High/Low failure independently, Method not entered for
activation, Fact/Root/PE/Mapping counts zero, resolver `unknown`, and the
ontology-review trigger.

- [ ] **Step 4: Verify GREEN**

Run: `python3 -m pytest tests/test_p006_semantic_bridge_pilot.py -q`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add docs/reviews/p006-semantic-bridge-pilot-* tests/test_p006_semantic_bridge_pilot.py
git commit -m "docs: adjudicate P006 semantic bridge pilot"
```

### Task 5: Complete ontology compatibility review and v3 pilot

**Files:**
- Create: `docs/reviews/core-primitive-ontology-compatibility-review.md`
- Create: `candidates/core-profile-v3/primitive_ontology_v3.yaml`
- Create: `docs/reviews/core-primitive-ontology-v3-pilot.md`
- Create: `tests/test_primitive_ontology_v3_candidate.py`

**Interfaces:**
- Consumes: six v2 Primitive definitions and completed independent research.
- Produces: isolated candidate ontology `candidate-primitive-ontology-v3` with pilot `TP001` and no runtime authority.

- [ ] **Step 1: Add RED candidate-isolation tests**

Require exact P001-P006 compatibility rows, explicit systematic-mismatch
decision, unchanged v2 fingerprint/content, candidate-only v3 activation, one
pilot `TP001`, clear High/Low process variation, exclusions, source-discovery
refs, and zero PE/Mapping/runtime refs.

- [ ] **Step 2: Write the compatibility review**

Assess modern abstraction, tradition-native nearby constructs, semantic
distance, Bridge feasibility, and compatibility for all six. Preserve their
product value while identifying systematic knowledge-object mismatch for the
five repeatedly starved axes.

- [ ] **Step 3: Add the v3 pilot asset**

Define `TP001 Task Continuity Process`: sustained/revised/interrupted/carried-
through handling of an undertaken matter. Exclude achievement, diligence
morality, action-start speed, organizational method, and outcome. Keep it
candidate-only and method-blocked.

- [ ] **Step 4: Verify GREEN**

Run: `python3 -m pytest tests/test_primitive_ontology_v3_candidate.py tests/test_c1_primitive_ontology_v2.py tests/test_release_primitive_coverage.py -q`

Expected: PASS with v2 release authority unchanged.

- [ ] **Step 5: Commit**

```bash
git add docs/reviews/core-primitive-ontology-* candidates/core-profile-v3 tests/test_primitive_ontology_v3_candidate.py
git commit -m "docs: open evidence-discovered ontology v3 pilot"
```

### Task 6: Final governance, machine summary, and v0.4.2 metadata

**Files:**
- Create: `docs/reviews/semantic-bridge-governance-final-report.md`
- Create: `docs/reviews/semantic-bridge-governance-five-role-review.md`
- Create: `docs/reviews/semantic-bridge-governance-final-v1.yaml`
- Create: `docs/release/v0.4.2-release-readiness.md`
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `pyproject.toml`
- Modify: `src/destiny_personality/__init__.py`
- Modify: `tests/test_verify_package_script.py`

**Interfaces:**
- Produces: final classification and machine-readable summary with bridge,
  single-direction, P006, ontology, formal activation, release, and CI fields.

- [ ] **Step 1: Add RED metadata and summary tests**

Require version 0.4.2, the exact summary schema, P006 zero counts and unknown,
ontology review triggered/systematic mismatch, formal non-unknown count zero,
and release classification from the design.

- [ ] **Step 2: Write final governance records**

Complete Semantic, Traditional Method, Ontology, Architecture, and Product
reviews. Record evidence inspected, findings, fixes, blockers, and verdict.

- [ ] **Step 3: Update version and release narrative**

State that v0.4.2 adds governance and a candidate ontology, not formal
personality capability. Keep v0.5.0 reserved.

- [ ] **Step 4: Verify focused release tests**

Run: `python3 -m pytest tests/test_semantic_bridge_governance.py tests/test_p006_semantic_bridge_pilot.py tests/test_primitive_ontology_v3_candidate.py tests/test_verify_package_script.py -q`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add docs/reviews/semantic-bridge-governance-* docs/release/v0.4.2-release-readiness.md README.md CHANGELOG.md pyproject.toml src/destiny_personality/__init__.py tests/test_verify_package_script.py
git commit -m "release: close semantic bridge pilot at v0.4.2"
```

### Task 7: Verify, review, merge, and publish

**Files:**
- Modify only to fix verified defects.

**Interfaces:**
- Consumes: completed branch.
- Produces: merged main and v0.4.2 GitHub release if every gate is green.

- [ ] **Step 1: Run full verification**

Run:

```bash
python3 -m pytest -q
python3 scripts/verify_package.py
python3 -m build
git diff --check
```

- [ ] **Step 2: Perform final whole-branch and five-role review**

Resolve every Critical or Important finding, rerun affected tests, and confirm
the formal bundle still contains zero Mapping records.

- [ ] **Step 3: Fetch latest main and verify integration**

Require a clean worktree, inspect the full base-to-head diff, integrate only if
main advanced, and rerun the full suite after integration.

- [ ] **Step 4: Push and require CI**

Require Python 3.9, 3.11, 3.12, and package-verification jobs to pass.

- [ ] **Step 5: Merge and publish**

Merge without squashing the audited implementation commits, verify merged main,
tag `v0.4.2`, and publish a release that explicitly discloses zero formal
activation and the candidate-only ontology-v3 pilot.
