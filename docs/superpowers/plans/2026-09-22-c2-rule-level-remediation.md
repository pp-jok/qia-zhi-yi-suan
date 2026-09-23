# C2-R Rule-Level Remediation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to complete this review task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert approved C2 D1–D6 policy into auditable, fail-closed recommended dispositions for all fourteen existing mapping rules without creating mapping v2 assets or changing runtime.

**Architecture:** Preserve the current registries as review targets. Attach each rule to an evidence-root strategy, C1 ownership conclusion, context/direction/strength/aspect review, and one allowed disposition. Aggregate results by Primitive coverage and use a separate decision packet for Product Owner rule-level approval.

**Tech Stack:** Markdown review records, YAML asset inspection, Python 3, pytest.

## Global Constraints

- C2-R is remediation design only; mapping registries, runtime, activation, fingerprints, and advanced layers must remain unchanged.
- An unknown evidence root is audit-visible but aggregation, promotion, and validation ineligible.
- Mapping emits contextual evidence only; it cannot resolve global state.
- Aspect cannot supply Primitive direction.
- Lack of defensible mapping is preferred over speculative mapping.
- Stop at the C2 Rule-Level Product Owner Gate.

---

### Task 1: Record approved high-level policy

**Files:**
- Modify: `docs/reviews/c2-product-owner-decision-packet.md`
- Modify: `docs/reviews/c2-product-owner-approval-checklist.md`

- [x] Record D1–D6 as approved policy while preserving that rule-level dispositions remain unapproved.

### Task 2: Produce complete rule-level remediation evidence

**Files:**
- Create: `docs/reviews/c2-rule-level-remediation-matrix.md`
- Create: `docs/reviews/c2-evidence-root-matrix.md`

- [x] Review all fourteen rules against D1–D6 and assign only an allowed disposition.
- [x] Mark unknown current roots fail-closed and document no new independent root creation.
- [x] Recalculate proposed Primitive coverage without forcing any Primary Evidence count.

### Task 3: Prepare the rule-level approval packet and verify isolation

**Files:**
- Create: `docs/reviews/c2-rule-remediation-decision-packet.md`
- Create: `docs/reviews/c2-rule-level-remediation-verification.md`

- [x] Provide fourteen Product Owner-ready cards with current state, proposed replacement, impacts, and decision field.
- [x] Capture frozen identities, run the complete tests and package verifier, and stop at the rule-level gate.
