# C2 Mapping Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to complete this review task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Audit every current Bazi and astrology mapping rule against the approved C1 v2 Primitive boundaries without changing runtime, mapping assets, fingerprints, or activation state.

**Architecture:** Treat `candidates/core-profile-v2` as the semantic baseline and the active `core-profile-v1` registries as read-only review targets. Produce independent Bazi and astrology inventories before a cross-system alignment review. Record all findings as review cards, issue reports, and a Product Owner decision packet.

**Tech Stack:** Markdown review records, YAML asset inspection, Python 3, pytest.

## Global Constraints

- C2 is review only: do not create mapping v2 assets or change v1 registries, runtime, loader, fingerprints, or activation.
- No Signature, Dynamic, Shadow/Mature, Fate Theme, or Archetype work is allowed.
- Each current rule must be reviewed; Bazi and astrology must remain separate until the cross-system review.
- C1 v2 ontology and context-promotion policy are the only semantic boundary sources.
- Stop at the C2 Product Owner Gate.

---

### Task 1: Freeze baseline and inventory all active mapping rules

**Files:**
- Modify: `docs/reviews/c1-product-owner-approval-record.md`
- Create: `docs/reviews/c2-issue-taxonomy.md`

- [x] Record C1 closed status and C2 review-only authorization.
- [x] Count all Bazi and astrology rules from the active candidate registries.
- [x] Record the issue taxonomy, severity rules, and review method.

### Task 2: Perform independent Bazi and astrology rule reviews

**Files:**
- Create: `docs/reviews/c2-bazi-mapping-review.md`
- Create: `docs/reviews/c2-astrology-mapping-review.md`
- Create: `docs/reviews/c2-mapping-semantic-ownership-report.md`
- Create: `docs/reviews/c2-mapping-double-counting-report.md`

- [x] Create a complete card for each Bazi rule.
- [x] Create a complete card for each astrology rule.
- [x] Record semantic ownership, direction, strength, context, source, exclusion, modifier, time-scope, and evidence-root findings.
- [x] Record duplication and fact-dominance analysis without proposing executable changes.

### Task 3: Perform cross-system alignment review and prepare C2 decisions

**Files:**
- Create: `docs/reviews/c2-cross-system-alignment-review.md`
- Create: `docs/reviews/c2-product-owner-approval-checklist.md`
- Create: `docs/reviews/c2-product-owner-decision-packet.md`

- [x] Produce the Primitive × Source System coverage matrix and positive-bias/collapse analysis.
- [x] Review alignment as validation, complement, contextualization, tension, correction, unresolved, or non-comparable; never as a vote.
- [x] List decisions needed for every non-keep disposition; do not implement any disposition.

### Task 4: Verify review-only isolation

**Files:**
- Modify: `docs/reviews/c2-*.md`

- [x] Capture semantic and presentation fingerprints plus runtime identity.
- [x] Confirm no non-document runtime reference or mapping asset changed during C2 review.
- [x] Run `python3 -m pytest -q --disable-warnings` and `python3 scripts/verify_package.py`.
- [x] Record exact results and stop at C2 Product Owner Gate.
