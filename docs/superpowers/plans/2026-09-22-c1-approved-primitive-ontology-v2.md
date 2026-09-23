# C1 Approved Primitive Ontology v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Encode the approved C1 six-Primitive semantic boundaries and Multi-Context Promotion contract as isolated, unactivated candidate assets.

**Architecture:** Create an explicit v2 ontology containing only the approved six Primitive definitions, ownership boundaries, permitted contexts, and policy references. Put the shared Local-to-Global contract in a separate policy asset so it is not duplicated per Primitive. Validate both documents directly in tests; do not alter any loader, mapping registry, fingerprint input list, runtime bundle, or presentation asset.

**Tech Stack:** YAML candidate assets, Python 3, PyYAML, pytest.

## Global Constraints

- The active v0.3.x semantic bundle, presentation bundle, and runtime identity must remain byte-for-byte behaviorally unchanged.
- Primitive count is exactly six (`P001` through `P006`); no new psychological theory, mapping, or high-level semantic structure is allowed.
- Mapping registries are C2 work and must not be modified.
- A global candidate is never a resolved Primitive state.
- Candidate assets are not runtime inputs or semantic-fingerprint inputs.
- Stop after C1 implementation verification; C2 is not authorized by this plan.

---

### Task 1: Close C1 approval documentation

**Files:**
- Modify: `docs/reviews/c1-product-owner-decision-packet.md`
- Modify: `docs/reviews/c1-product-owner-approval-checklist.md`
- Modify: `docs/reviews/c1-primitive-semantic-review.md`
- Create: `docs/reviews/c1-product-owner-approval-record.md`

**Interfaces:**
- Consumes: Product Owner approval D1 Option A, D2 Option A, D3 Option A, D4 Multi-Context Promotion.
- Produces: immutable C1 decision record used as the sole source for v2 candidate asset content.

- [x] **Step 1: Record the approval status and decisions**

Update the three review artifacts to say `C1 APPROVED` and record D1–D4 choices without changing the original decision rationale.

- [x] **Step 2: Add the approval record**

Create a record containing the v0.3.9 baseline release and commit, six approved primitives, D1–D4, normative promotion rules, remaining C2 limitations, approval status, and `Primitive Ontology v2 Candidate Implementation` as the only next phase.

- [x] **Step 3: Check documentation references**

Run: `rg -n "AWAITING PRODUCT OWNER DECISION|not approved|APPROVED|Next Allowed Phase" docs/reviews/c1-*`

Expected: C1 documents record approval; no document authorizes C2 mapping work.

### Task 2: Add red static tests for candidate ontology and context policy

**Files:**
- Create: `tests/test_c1_primitive_ontology_v2.py`

**Interfaces:**
- Consumes: `candidates/core-profile-v2/primitive_ontology_v2.yaml` and `candidates/core-profile-v2/context_promotion_policy_v1.yaml`.
- Produces: direct schema and semantic-boundary assertions without importing runtime loaders.

- [x] **Step 1: Write failing asset tests**

Add tests that load the candidate YAML files and assert exactly six unique Primitive IDs, complete semantic fields, valid non-self neighbors, valid policy references, D1/D2/D3 ownership boundaries, and all seven required promotion scenarios.

- [x] **Step 2: Run the test to verify it fails**

Run: `python3 -m pytest -q tests/test_c1_primitive_ontology_v2.py`

Expected: FAIL because the v2 candidate assets do not yet exist.

### Task 3: Create isolated candidate assets

**Files:**
- Create: `candidates/core-profile-v2/primitive_ontology_v2.yaml`
- Create: `candidates/core-profile-v2/context_promotion_policy_v1.yaml`

**Interfaces:**
- Consumes: C1 cards and approved D1–D4 contract.
- Produces: an unactivated ontology asset with six semantic records and one shared promotion-policy reference.

- [x] **Step 1: Create the context promotion policy**

Encode explicit-global and multi-context candidate paths, source/root independence, representative contexts, minimum qualification, material counter-context blocking, contextual variation, and the global-mixed scope rule. The policy must state that it emits `global_candidate_evidence`, not state resolution.

- [x] **Step 2: Create the v2 ontology**

Encode all required semantic definitions for P001–P006; keep approved ownership boundaries explicit and point every eligible Primitive to `context_promotion_policy_v1`.

- [x] **Step 3: Run focused tests to verify green**

Run: `python3 -m pytest -q tests/test_c1_primitive_ontology_v2.py`

Expected: PASS.

### Task 4: Verify candidate isolation and record C1 implementation evidence

**Files:**
- Create: `docs/reviews/c1-primitive-ontology-v2-implementation-verification.md`

**Interfaces:**
- Consumes: candidate assets and focused/full verification outputs.
- Produces: an evidence-backed C1 implementation verification report; no runtime code change.

- [x] **Step 1: Capture frozen runtime identities before and after asset creation**

Run a Python one-liner that imports the existing builder and prints semantic fingerprint, presentation fingerprint, and runtime version. Repeat after candidate asset creation.

- [x] **Step 2: Verify forbidden surface remains unchanged**

Run: `git -C release/qia-zhi-yi-suan diff --name-only -- src/destiny_personality candidates/core-profile-v1 destiny-personality/configs`

Expected: any pre-existing dirty changes are reported but no changes from this task are written in that release worktree; compare only the root candidate v2 additions and C1 docs.

- [x] **Step 3: Run full verification**

Run: `python3 -m pytest -q` and `python3 scripts/verify_package.py`.

Expected: both exit 0.

- [x] **Step 4: Write C1 implementation verification report**

Record exact test and package-verification output, fingerprints, runtime identity, C1 decisions encoded, no new Primitives, no mapping change, no activation, and C2 readiness limited to a subsequent mapping-review gate.
