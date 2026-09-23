# C2-M Fresh Mapping Model Design Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to complete this design task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close legacy-rule migration and define the fail-closed evidence, mechanism, and eligibility model required before any fresh Mapping v2 candidate can exist.

**Architecture:** Keep all fourteen legacy formulations rejected while retaining their canonical source facts as undecided. Document a role model and an evidence-identity model first, then independently inventory Bazi and astrology facts against each approved Primitive. Admit a mapping candidate only with a complete source → mechanism → semantic-question chain; otherwise record `NO_CURRENT_DEFENSIBLE_MAPPING`.

**Tech Stack:** Markdown design and review records, Python 3, pytest.

## Global Constraints

- All fourteen legacy rules are `NO_MAPPING / NO_PORT`; this does not permanently prohibit their canonical source facts.
- Do not create Mapping v2 assets, alter runtime, activate ontology v2, change fingerprints, or enter C3.
- Mapping emits contextual evidence only; any global candidate still requires C1 policy qualification.
- Aspects are not Primitive directions; dignity is modifier-only; house/angle facts are time-sensitive contextualizers or salience modifiers.
- No Primary Evidence exists without an explicit project-owned semantic mechanism.
- Stop at the C2 Fresh Mapping Product Owner Gate.

---

### Task 1: Close legacy migration decisions

**Files:**
- Modify: `docs/reviews/c2-rule-remediation-decision-packet.md`
- Modify: `docs/reviews/c2-rule-level-remediation-matrix.md`

- [x] Record all fourteen Product Owner decisions as approved non-migration and distinguish legacy-rule rejection from future canonical-fact eligibility.

### Task 2: Define fresh mapping eligibility

**Files:**
- Create: `docs/design/c2-mapping-evidence-role-model.md`
- Create: `docs/design/c2-semantic-mechanism-candidates.md`

- [x] Define exactly six evidence roles and their eligibility constraints.
- [x] Define Canonical Fact → Evidence Root → Semantic Mechanism → Evidence Instance identity and fail-closed rules.
- [x] Independently assess Bazi and astrology facts without reintroducing legacy source/target/direction formulations.

### Task 3: Publish feasibility and candidate proposal

**Files:**
- Create: `docs/reviews/c2-fresh-mapping-feasibility-matrix.md`
- Create: `docs/reviews/c2-fresh-mapping-candidate-proposal.md`
- Create: `docs/reviews/c2-fresh-mapping-design-verification.md`

- [x] State per-Primitive, per-system feasibility with no coverage quota.
- [x] Publish only admissible candidates; record zero candidates if none meet the contract.
- [x] Verify legacy-reintroduction rule, frozen runtime identities, full tests, and package verification.
