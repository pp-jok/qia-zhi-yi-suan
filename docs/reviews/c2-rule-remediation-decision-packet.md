# C2-R Rule Remediation Decision Packet

## Status

**RULE-LEVEL PRODUCT OWNER DECISIONS: APPROVED.** All fourteen legacy rules are approved `NO_MAPPING / NO_PORT` on 2026-09-22. This disposition applies to the legacy rule formulation, not to permanent eligibility of its canonical source facts. It does not implement any mapping change or create Mapping v2.

```text
legacy_rule_eligibility = rejected
canonical_fact_future_mapping_eligibility = undecided
```

## Bazi rules

### BZ-C2B-01

- **Current:** 比肩/劫财 + 食神/伤官 → P001 high in decision/work.
- **Problem:** action/output content does not prove P001 judgement ownership; root is unknown; direct global promotion bypass exists.
- **Recommended disposition:** `NO_MAPPING`.
- **Proposed replacement:** retain canonical Ten-God facts for audit only; emit no Primitive Evidence.
- **Semantic impact:** removes unproven P001/P004 conflation.
- **Evidence impact:** `UNKNOWN_ROOT` remains audit-visible and ineligible for aggregation, promotion, and validation.
- **Context impact:** no decision/work Primitive evidence is emitted.
- **Risk:** P001 has no proposed Bazi primary rule.
- **Product Owner Decision:** **APPROVED — NO LEGACY MIGRATION (NO_MAPPING / NO_PORT).**

### BZ-C2B-02

- **Current:** 印 + 官杀 → P002 high in pressure/work.
- **Problem:** identical structure/rule family is also used for P006; it does not prove predictability preference.
- **Recommended disposition:** `NO_MAPPING`.
- **Proposed replacement:** retain source facts for audit only; no Primitive Evidence.
- **Semantic impact:** preserves the P002/P006 ownership boundary.
- **Evidence impact:** prevents DC-01 same-root multiplication.
- **Context impact:** no pressure/work P002 evidence is emitted.
- **Risk:** P002 has no proposed Bazi high rule.
- **Product Owner Decision:** **APPROVED — NO LEGACY MIGRATION (NO_MAPPING / NO_PORT).**

### BZ-C2B-03

- **Current:** 食伤 + 财, with 印/官 counterweight → P002 low in change/work.
- **Problem:** source condition does not prove reverse predictability preference; counterweight is not an exclusion or root identity.
- **Recommended disposition:** `NO_MAPPING`.
- **Proposed replacement:** retain facts and counterweight for audit only; no Primitive Evidence.
- **Semantic impact:** prevents an unsupported low direction.
- **Evidence impact:** prevents DC-02 exact duplication with BZ-C2B-05.
- **Context impact:** no change/work P002 evidence is emitted.
- **Risk:** P002 has no proposed Bazi low rule.
- **Product Owner Decision:** **APPROVED — NO LEGACY MIGRATION (NO_MAPPING / NO_PORT).**

### BZ-C2B-04

- **Current:** broad Ten-God presence → P003 high in relationship.
- **Problem:** a relationship label and broad symbol presence do not prove relational attunement or response.
- **Recommended disposition:** `NO_MAPPING`.
- **Proposed replacement:** retain canonical facts for audit only; no relationship Primitive Evidence.
- **Semantic impact:** avoids inventing P003 from relationship context alone.
- **Evidence impact:** unknown root remains fail-closed.
- **Context impact:** no relationship-global or local P003 evidence is emitted.
- **Risk:** P003 has no proposed Bazi primary rule.
- **Product Owner Decision:** **APPROVED — NO LEGACY MIGRATION (NO_MAPPING / NO_PORT).**

### BZ-C2B-05

- **Current:** 食伤 + 财 → P004 high in work/action.
- **Problem:** action context does not prove action initiation or execution momentum; it duplicates BZ-C2B-03 source family.
- **Recommended disposition:** `NO_MAPPING`.
- **Proposed replacement:** retain source facts for audit only; no Primitive Evidence.
- **Semantic impact:** avoids treating output/wealth symbolism as P004 by default.
- **Evidence impact:** prevents DC-02 exact duplication.
- **Context impact:** no work/action P004 evidence is emitted.
- **Risk:** P004 has no proposed Bazi primary rule.
- **Product Owner Decision:** **APPROVED — NO LEGACY MIGRATION (NO_MAPPING / NO_PORT).**

### BZ-C2B-06

- **Current:** 印 + 官杀 → P005 high in pressure.
- **Problem:** pressure, constraint, and structure are not affect-regulation mechanisms under D5.
- **Recommended disposition:** `NO_MAPPING`.
- **Proposed replacement:** retain source facts for audit only; no P005 Primary Evidence or contextualizer is emitted.
- **Semantic impact:** enforces `emotion-related != emotion-regulation`.
- **Evidence impact:** prevents DC-01 same-root multiplication.
- **Context impact:** no pressure P005 evidence is emitted.
- **Risk:** P005 Primary Evidence remains zero, which D5 permits.
- **Product Owner Decision:** **APPROVED — NO LEGACY MIGRATION (NO_MAPPING / NO_PORT).**

### BZ-C2B-07

- **Current:** 印 + 官杀 → P006 high in work/decision.
- **Problem:** source does not distinguish organization method from P002 predictability preference.
- **Recommended disposition:** `NO_MAPPING`.
- **Proposed replacement:** retain source facts for audit only; no Primitive Evidence.
- **Semantic impact:** protects P002/P006 ownership separation.
- **Evidence impact:** prevents DC-01 same-root multiplication.
- **Context impact:** no work/decision P006 evidence is emitted.
- **Risk:** P006 has no proposed Bazi primary rule.
- **Product Owner Decision:** **APPROVED — NO LEGACY MIGRATION (NO_MAPPING / NO_PORT).**

## Astrology rules

### AS-C2B-01

- **Current:** Sun–Mars aspect/placement → P001 high in decision/work.
- **Problem:** action/assertion is not judgement ownership; aspect cannot supply Primitive direction.
- **Recommended disposition:** `NO_MAPPING`.
- **Proposed replacement:** retain deterministic aspect facts for audit only; no Primitive Evidence.
- **Semantic impact:** removes D3 P001/P004 conflation.
- **Evidence impact:** prevents DC-04 exact overlap with AS-C2B-05; unknown root remains fail-closed.
- **Context impact:** no decision/work P001 evidence is emitted.
- **Risk:** P001 has no proposed astrology primary rule.
- **Product Owner Decision:** **APPROVED — NO LEGACY MIGRATION (NO_MAPPING / NO_PORT).**

### AS-C2B-02

- **Current:** Saturn–Sun aspect/placement → P002 high in pressure.
- **Problem:** structure symbolism does not prove stability need; aspect cannot determine high direction.
- **Recommended disposition:** `NO_MAPPING`.
- **Proposed replacement:** retain deterministic facts for audit only; no Primitive Evidence.
- **Semantic impact:** protects P002/P006 ownership separation.
- **Evidence impact:** unknown root remains fail-closed.
- **Context impact:** no pressure P002 evidence is emitted.
- **Risk:** P002 has no proposed astrology high rule.
- **Product Owner Decision:** **APPROVED — NO LEGACY MIGRATION (NO_MAPPING / NO_PORT).**

### AS-C2B-03

- **Current:** Uranus–Sun aspect/placement → P002 low in change.
- **Problem:** generic interaction does not prove low predictability preference; aspect cannot determine low direction.
- **Recommended disposition:** `NO_MAPPING`.
- **Proposed replacement:** retain deterministic facts for audit only; no Primitive Evidence.
- **Semantic impact:** prevents unsupported reverse-direction inference.
- **Evidence impact:** unknown root remains fail-closed.
- **Context impact:** no change P002 evidence is emitted.
- **Risk:** P002 has no proposed astrology low rule.
- **Product Owner Decision:** **APPROVED — NO LEGACY MIGRATION (NO_MAPPING / NO_PORT).**

### AS-C2B-04

- **Current:** Moon–Venus aspect/placement → P003 high in relationship.
- **Problem:** affection/emotionality does not prove relational attunement; aspect cannot determine high direction.
- **Recommended disposition:** `NO_MAPPING`.
- **Proposed replacement:** retain deterministic facts for audit only; no Primitive Evidence.
- **Semantic impact:** preserves P003 as relationship responsiveness, not emotional symbolism.
- **Evidence impact:** unknown root remains fail-closed.
- **Context impact:** no relationship P003 evidence is emitted.
- **Risk:** P003 has no proposed astrology primary rule.
- **Product Owner Decision:** **APPROVED — NO LEGACY MIGRATION (NO_MAPPING / NO_PORT).**

### AS-C2B-05

- **Current:** Mars–Sun aspect/placement → P004 high in work/action.
- **Problem:** action/energy symbolism does not independently prove initiation; aspect cannot determine high direction.
- **Recommended disposition:** `NO_MAPPING`.
- **Proposed replacement:** retain deterministic facts for audit only; no Primitive Evidence.
- **Semantic impact:** does not replace P001 mapping with P004 automatically.
- **Evidence impact:** prevents DC-04 exact overlap with AS-C2B-01.
- **Context impact:** no work/action P004 evidence is emitted.
- **Risk:** P004 has no proposed astrology primary rule.
- **Product Owner Decision:** **APPROVED — NO LEGACY MIGRATION (NO_MAPPING / NO_PORT).**

### AS-C2B-06

- **Current:** Moon–Mercury aspect/placement → P005 high in pressure/relationship.
- **Problem:** emotion plus cognition does not prove affective regulation; aspect cannot determine high direction.
- **Recommended disposition:** `NO_MAPPING`.
- **Proposed replacement:** retain deterministic facts for audit only; no P005 Primary Evidence or contextualizer.
- **Semantic impact:** enforces D5 P005 eligibility.
- **Evidence impact:** unknown root remains fail-closed.
- **Context impact:** no pressure/relationship P005 evidence is emitted.
- **Risk:** P005 Primary Evidence remains zero, which is permitted.
- **Product Owner Decision:** **APPROVED — NO LEGACY MIGRATION (NO_MAPPING / NO_PORT).**

### AS-C2B-07

- **Current:** Mercury–Saturn aspect/placement → P006 high in work/decision.
- **Problem:** cognition/communication expression does not prove organization method; aspect cannot determine high direction.
- **Recommended disposition:** `NO_MAPPING`.
- **Proposed replacement:** retain deterministic facts for audit only; no Primitive Evidence.
- **Semantic impact:** preserves P006/P002 separation.
- **Evidence impact:** unknown root remains fail-closed.
- **Context impact:** no work/decision P006 evidence is emitted.
- **Risk:** P006 has no proposed astrology primary rule.
- **Product Owner Decision:** **APPROVED — NO LEGACY MIGRATION (NO_MAPPING / NO_PORT).**

## Approval boundary

All approved dispositions close legacy migration only. C2 Legacy Mapping Review is closed; C2 Fresh Mapping Design is authorized. Mapping v2 creation, runtime activation, fingerprint changes, and C3 work remain prohibited.
