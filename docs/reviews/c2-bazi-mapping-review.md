# C2 Bazi Mapping Review

## Scope and inventory

Review target: `candidates/core-profile-v1/bazi_mapping_registry_v1.yaml`. Semantic baseline: C1-approved `primitive_ontology_v2.yaml` and `context_promotion_policy_v1.yaml`.

```text
Bazi mapping rule count: 7
Canonical-source finding: 0 NON_CANONICAL_SOURCE
Time-scope leak: 0 observed in stable-only fact contract
Time-scope declaration gap: 7 rules
Context-promotion bypass: 7 rules
```

All seven rules consume deterministic `bazi.ten_gods` plus a deterministic day-master/month-environment derivative in the current runtime. They are therefore not raw-provider or prose mappings. None has a rule-level `canonical_fact_ref` or `evidence_root`; runtime fact references are flattened after matching and cannot establish C1 source independence.

## Review-card legend

- **Source fact / scope:** deterministic fact family and the exact current predicate, not an inferred metaphysical interpretation.
- **Assurance:** `capability_reported`; day-master environment is required, while hour-pillar participation is not declared separately.
- **Strength label:** `moderate`, from the active Bazi weighting policy; it is a runtime label, not an approved C2 evidence-strength rationale.
- **Review status:** `requires_product_decision` means the rule cannot pass unchanged to a future mapping v2.

### BZ-C2B-01

- **Source / assurance:** `bazi.ten_gods` (比肩/劫财 and 食神/伤官), visible or hidden stems, at least two pillars; requires deterministic day-master environment; `capability_reported`.
- **Primitive / C1 question:** P001 — “How is judgement formed and to whom do its standards belong?”
- **Direction / strength / context:** high; moderate; `decision`, `work`.
- **Modifiers / exclusions / counter-conditions:** environment contextualizer; no explicit exclusion; no explicit counter-condition.
- **Required facts / provenance:** Ten-God facts, source kind, source pillars, and environment table; flattened fact references only, no canonical fact root.
- **Semantic rationale:** absent. The condition includes action/output symbolism but does not distinguish internal judgement standards from action initiation.
- **Risk flags:** `SEMANTIC_OWNER_VIOLATION` (P001/P004 risk, major), `DIRECTION_UNSUPPORTED` (major), `EVIDENCE_ROOT_AMBIGUOUS` (major), `MISSING_EXCLUSION` (major), `TIME_SCOPE_UNDECLARED` (major), `SINGLE_FACT_DOMINANCE_RISK` (major), `CONTEXT_PROMOTION_BYPASS` (critical).
- **Review status:** `rewrite`.

### BZ-C2B-02

- **Source / assurance:** `bazi.ten_gods` (正印/偏印 and 正官/七杀), visible or hidden stems, two pillars, required environment; `capability_reported`.
- **Primitive / C1 question:** P002 — “How much predictability and stability is preferred?”
- **Direction / strength / context:** high; moderate; `pressure`, `work`.
- **Modifiers / exclusions / counter-conditions:** environment contextualizer; no explicit exclusion or counter-condition.
- **Required facts / provenance:** Ten-God evidence, pillars, source kinds, environment table; no stable canonical root identity.
- **Semantic rationale:** absent. The condition may describe rule/structure and must not be treated as predictability preference without a preference-specific bridge.
- **Risk flags:** `SEMANTIC_OWNER_VIOLATION` (P002/P006 risk, major), `DIRECTION_UNSUPPORTED`, `EVIDENCE_ROOT_AMBIGUOUS`, `MISSING_EXCLUSION`, `TIME_SCOPE_UNDECLARED`, `SINGLE_FACT_DOMINANCE_RISK` (all major), `CONTEXT_PROMOTION_BYPASS` (critical).
- **Review status:** `rewrite`.

### BZ-C2B-03

- **Source / assurance:** `bazi.ten_gods` (食神/伤官 and 正财/偏财), visible or hidden stems, two pillars, required environment; `capability_reported`.
- **Primitive / C1 question:** P002 — “How much predictability and stability is preferred?”
- **Direction / strength / context:** low; moderate; `change`, `work`.
- **Modifiers / exclusions / counter-conditions:** environment contextualizer; explicit 印/官 counterweight contextualizer; no explicit exclusion.
- **Required facts / provenance:** Ten-God evidence, pillar/source-kind facts, environment and counterweight facts; no `evidence_root`.
- **Semantic rationale:** absent. Explicit reverse evidence exists, but the source condition is not a stated preference for change; absence of stability is not sufficient for low.
- **Risk flags:** `SEMANTIC_OWNER_VIOLATION` (P002/P004-adaptation risk, major), `DIRECTION_UNSUPPORTED`, `EVIDENCE_ROOT_AMBIGUOUS`, `MISSING_EXCLUSION`, `TIME_SCOPE_UNDECLARED`, `SINGLE_FACT_DOMINANCE_RISK` (major), `CONTEXT_PROMOTION_BYPASS` (critical).
- **Review status:** `rewrite`.

### BZ-C2B-04

- **Source / assurance:** two broad Ten-God groups covering all configured Ten-God families, visible or hidden stems, two pillars, required environment; `capability_reported`.
- **Primitive / C1 question:** P003 — “How are relationship interactions handled and responded to?”
- **Direction / strength / context:** high; moderate; `relationship`.
- **Modifiers / exclusions / counter-conditions:** environment contextualizer; no explicit exclusion or counter-condition.
- **Required facts / provenance:** deterministic Ten-God/pillar/environment facts; no relationship-specific canonical fact reference or evidence root.
- **Semantic rationale:** absent. Broad category presence plus a relationship context label does not establish relational response or coordination.
- **Risk flags:** `OVERGENERALIZED_MAPPING`, `SEMANTIC_OWNER_VIOLATION`, `DIRECTION_UNSUPPORTED`, `EVIDENCE_ROOT_AMBIGUOUS`, `MISSING_EXCLUSION`, `TIME_SCOPE_UNDECLARED`, `SINGLE_FACT_DOMINANCE_RISK` (major), `CONTEXT_PROMOTION_BYPASS` (critical), `NO_MAPPING_REQUIRED` (major candidate).
- **Review status:** `no-mapping` pending Product Owner confirmation.

### BZ-C2B-05

- **Source / assurance:** `bazi.ten_gods` (食神/伤官 and 正财/偏财), visible or hidden stems, two pillars, required environment; `capability_reported`.
- **Primitive / C1 question:** P004 — “When and how is concrete action started and advanced?”
- **Direction / strength / context:** high; moderate; `work`, `action`.
- **Modifiers / exclusions / counter-conditions:** environment contextualizer; no explicit exclusion or counter-condition.
- **Required facts / provenance:** deterministic Ten-God/pillar/environment facts; no root identity.
- **Semantic rationale:** action context is present, but no rule explains why the fact pattern supports initiation rather than output, wealth, or work expression.
- **Risk flags:** `DIRECTION_UNSUPPORTED`, `EVIDENCE_ROOT_AMBIGUOUS`, `MISSING_EXCLUSION`, `TIME_SCOPE_UNDECLARED`, `SINGLE_FACT_DOMINANCE_RISK` (major), `CONTEXT_PROMOTION_BYPASS` (critical).
- **Review status:** `rewrite`.

### BZ-C2B-06

- **Source / assurance:** `bazi.ten_gods` (正印/偏印 and 正官/七杀), visible or hidden stems, two pillars, required environment; `capability_reported`.
- **Primitive / C1 question:** P005 — “How is affect preferentially held or processed?”
- **Direction / strength / context:** high; moderate; `pressure`.
- **Modifiers / exclusions / counter-conditions:** environment contextualizer; no explicit exclusion or counter-condition.
- **Required facts / provenance:** deterministic Ten-God/pillar/environment facts; no root identity.
- **Semantic rationale:** no bridge separates affect regulation from the same rule family used for P002/P006 structure and pressure signals.
- **Risk flags:** `SEMANTIC_OWNER_VIOLATION` (P005/P006 risk, major), `DIRECTION_UNSUPPORTED`, `EVIDENCE_ROOT_AMBIGUOUS`, `MISSING_EXCLUSION`, `TIME_SCOPE_UNDECLARED`, `SINGLE_FACT_DOMINANCE_RISK` (major), `CONTEXT_PROMOTION_BYPASS` (critical).
- **Review status:** `re-scope` or `no-mapping`.

### BZ-C2B-07

- **Source / assurance:** `bazi.ten_gods` (正印/偏印 and 正官/七杀), visible or hidden stems, two pillars, required environment; `capability_reported`.
- **Primitive / C1 question:** P006 — “How are activities and tasks arranged and organized?”
- **Direction / strength / context:** high; moderate; `work`, `decision`.
- **Modifiers / exclusions / counter-conditions:** environment contextualizer; no explicit exclusion or counter-condition.
- **Required facts / provenance:** deterministic Ten-God/pillar/environment facts; no root identity.
- **Semantic rationale:** no explicit bridge establishes organizational method rather than P002 predictability preference or P005 affect regulation.
- **Risk flags:** `SEMANTIC_OWNER_VIOLATION` (P006/P002 risk, major), `DIRECTION_UNSUPPORTED`, `EVIDENCE_ROOT_AMBIGUOUS`, `MISSING_EXCLUSION`, `TIME_SCOPE_UNDECLARED`, `SINGLE_FACT_DOMINANCE_RISK` (major), `CONTEXT_PROMOTION_BYPASS` (critical).
- **Review status:** `rewrite`.

## Bazi contradiction, density, and positive-bias analysis

- **Contradiction:** BZ-C2B-02 (P002 high: pressure/work) and BZ-C2B-03 (P002 low: change/work) overlap on `work`. Current runtime can convert this into global `mixed`; C1 requires scope, quality, modifier, and root analysis first. Finding: `CONTEXT_PROMOTION_BYPASS` critical.
- **Fact dominance:** every Bazi rule can emit one candidate that the current resolver may make global. The two-pillar threshold improves evidence quantity but does not meet C1 multi-context independence.
- **Rule density:** counts are P001 1, P002 2, P003 1, P004 1, P005 1, P006 1. P002 has the only bidirectional coverage; other Primitives have only high rules. Finding: `RULE_DENSITY_BIAS` major.
- **Positive bias:** six high rules and one low rule. This is a directional skew requiring Product Owner review; it is not proof that a 50/50 distribution is correct.
