# C2 Astrology Mapping Review

## Scope and inventory

Review target: `candidates/core-profile-v1/astrology_mapping_registry_v1.yaml`. Semantic baseline: C1-approved `primitive_ontology_v2.yaml` and `context_promotion_policy_v1.yaml`.

```text
Astrology mapping rule count: 7
Canonical-source finding: 0 NON_CANONICAL_SOURCE
Time-scope leak: 0 observed in stable-only / unknown-time fact contract
Context-promotion bypass: 7 rules
```

Each rule consumes deterministic placements and a deterministic aspect predicate; it does not consume provider prose or renderer text. The registry's angle, house, and dignity fields are optional modifier collection only. They are read only when an ascendant exists, and stable-only fact validation rejects ascendant, house, MC, and cusp data. Therefore no observed `TIME_SCOPE_LEAK` exists. However, no rule emits a stable `canonical_fact_ref` or `evidence_root`, so C1 source-independence cannot be audited.

## Review-card legend

- **Assurance:** `capability_reported`, based on deterministic placements/aspects and fact mode.
- **Strength label:** `strong` at orb ≤3 and `moderate` at orb ≤8 under the current weighting asset; this is a technical salience band, not an approved semantic direction rule.
- **Aspect caveat:** the registry models expression mode and tension, but every listed aspect type can still trigger the same high/low Primitive direction. That is reviewed as valence oversimplification, not as a claim that difficult aspects are intrinsically negative.

### AS-C2B-01

- **Source / assurance:** deterministic Sun/Mars placement plus Sun–Mars aspect (conjunction, sextile, square, trine, or opposition; orb ≤8); optional dignity and angular/house modifier; `capability_reported`.
- **Primitive / C1 question:** P001 — “How is judgement formed and to whom do its standards belong?”
- **Direction / strength / context:** high; strong or moderate by orb; `decision`, `work`.
- **Modifiers / exclusions / counter-conditions:** optional dignity/angle/house modifiers; no explicit exclusion or counter-condition.
- **Required facts / provenance:** placements, aspect type/orb, optional dignity/house facts; flattened references only, no stable evidence root.
- **Semantic rationale:** absent. Sun/Mars activation or action expression does not establish internal judgement standards and risks C1 D1 P001/P004 conflation.
- **Risk flags:** `SEMANTIC_OWNER_VIOLATION` (P001/P004 risk), `OVERGENERALIZED_MAPPING`, `ASPECT_VALENCE_OVERSIMPLIFICATION`, `DIRECTION_UNSUPPORTED`, `EVIDENCE_ROOT_AMBIGUOUS`, `MISSING_EXCLUSION`, `SINGLE_FACT_DOMINANCE_RISK` (major), `CONTEXT_PROMOTION_BYPASS` (critical).
- **Review status:** `rewrite`.

### AS-C2B-02

- **Source / assurance:** deterministic Saturn placement plus Saturn–Sun aspect (all five configured aspect types; orb ≤8); `capability_reported`.
- **Primitive / C1 question:** P002 — “How much predictability and stability is preferred?”
- **Direction / strength / context:** high; strong or moderate by orb; `pressure`.
- **Modifiers / exclusions / counter-conditions:** no rule modifier, exclusion, or counter-condition.
- **Required facts / provenance:** placement and aspect facts; no canonical root identity.
- **Semantic rationale:** absent. Saturn-related structure may be organizational method rather than preference for predictability; C1 D2 requires separation from P006.
- **Risk flags:** `SEMANTIC_OWNER_VIOLATION` (P002/P006 risk), `OVERGENERALIZED_MAPPING`, `ASPECT_VALENCE_OVERSIMPLIFICATION`, `DIRECTION_UNSUPPORTED`, `EVIDENCE_ROOT_AMBIGUOUS`, `MISSING_MODIFIER`, `MISSING_EXCLUSION`, `SINGLE_FACT_DOMINANCE_RISK` (major), `CONTEXT_PROMOTION_BYPASS` (critical).
- **Review status:** `rewrite`.

### AS-C2B-03

- **Source / assurance:** deterministic Uranus placement plus Uranus–Sun aspect (all five configured types; orb ≤8); `capability_reported`.
- **Primitive / C1 question:** P002 — “How much predictability and stability is preferred?”
- **Direction / strength / context:** low; strong or moderate by orb; `change`.
- **Modifiers / exclusions / counter-conditions:** no rule modifier, exclusion, or counter-condition.
- **Required facts / provenance:** placement and aspect facts; no canonical root identity.
- **Semantic rationale:** absent. A generic aspect interaction cannot by itself prove low predictability preference; explicit reverse semantics are required rather than absence of stability.
- **Risk flags:** `OVERGENERALIZED_MAPPING`, `ASPECT_VALENCE_OVERSIMPLIFICATION`, `DIRECTION_UNSUPPORTED`, `EVIDENCE_ROOT_AMBIGUOUS`, `MISSING_MODIFIER`, `MISSING_EXCLUSION`, `SINGLE_FACT_DOMINANCE_RISK` (major), `CONTEXT_PROMOTION_BYPASS` (critical).
- **Review status:** `rewrite`.

### AS-C2B-04

- **Source / assurance:** deterministic Moon/Venus placements plus Moon–Venus aspect (all five configured types; orb ≤8); `capability_reported`.
- **Primitive / C1 question:** P003 — “How are relationship interactions handled and responded to?”
- **Direction / strength / context:** high; strong or moderate by orb; `relationship`.
- **Modifiers / exclusions / counter-conditions:** no rule modifier, exclusion, or counter-condition.
- **Required facts / provenance:** placement and aspect facts; no canonical root identity.
- **Semantic rationale:** relationship context is plausible but no rule distinguishes response/coordination from affiliation, affect, or social preference.
- **Risk flags:** `OVERGENERALIZED_MAPPING`, `ASPECT_VALENCE_OVERSIMPLIFICATION`, `DIRECTION_UNSUPPORTED`, `EVIDENCE_ROOT_AMBIGUOUS`, `MISSING_MODIFIER`, `MISSING_EXCLUSION`, `SINGLE_FACT_DOMINANCE_RISK` (major), `CONTEXT_PROMOTION_BYPASS` (critical).
- **Review status:** `re-scope` or `rewrite`.

### AS-C2B-05

- **Source / assurance:** deterministic Mars placement plus Mars–Sun aspect (all five configured types; orb ≤8); `capability_reported`.
- **Primitive / C1 question:** P004 — “When and how is concrete action started and advanced?”
- **Direction / strength / context:** high; strong or moderate by orb; `work`, `action`.
- **Modifiers / exclusions / counter-conditions:** no rule modifier, exclusion, or counter-condition.
- **Required facts / provenance:** placement and aspect facts; no canonical root identity.
- **Semantic rationale:** action owner is more plausible than P001, but the rule does not distinguish initiation/advancement from energy, conflict, or expression style.
- **Risk flags:** `OVERGENERALIZED_MAPPING`, `ASPECT_VALENCE_OVERSIMPLIFICATION`, `DIRECTION_UNSUPPORTED`, `EVIDENCE_ROOT_AMBIGUOUS`, `MISSING_MODIFIER`, `MISSING_EXCLUSION`, `SINGLE_FACT_DOMINANCE_RISK` (major), `CONTEXT_PROMOTION_BYPASS` (critical).
- **Review status:** `rewrite`.

### AS-C2B-06

- **Source / assurance:** deterministic Moon placement plus Moon–Mercury aspect (all five configured types; orb ≤8); `capability_reported`.
- **Primitive / C1 question:** P005 — “How is affect preferentially held or processed?”
- **Direction / strength / context:** high; strong or moderate by orb; `pressure`, `relationship`.
- **Modifiers / exclusions / counter-conditions:** no rule modifier, exclusion, or counter-condition.
- **Required facts / provenance:** placement and aspect facts; no canonical root identity.
- **Semantic rationale:** no explicit bridge establishes affect regulation rather than affect expression, communication style, or relationship response.
- **Risk flags:** `OVERGENERALIZED_MAPPING`, `ASPECT_VALENCE_OVERSIMPLIFICATION`, `DIRECTION_UNSUPPORTED`, `EVIDENCE_ROOT_AMBIGUOUS`, `MISSING_MODIFIER`, `MISSING_EXCLUSION`, `SINGLE_FACT_DOMINANCE_RISK` (major), `CONTEXT_PROMOTION_BYPASS` (critical).
- **Review status:** `re-scope` or `no-mapping`.

### AS-C2B-07

- **Source / assurance:** deterministic Mercury placement plus Mercury–Saturn aspect (all five configured types; orb ≤8); `capability_reported`.
- **Primitive / C1 question:** P006 — “How are activities and tasks arranged and organized?”
- **Direction / strength / context:** high; strong or moderate by orb; `work`, `decision`.
- **Modifiers / exclusions / counter-conditions:** no rule modifier, exclusion, or counter-condition.
- **Required facts / provenance:** placement and aspect facts; no canonical root identity.
- **Semantic rationale:** organization is plausible, but the rule does not separate task arrangement from C1 P002 predictability preference or from cognitive style.
- **Risk flags:** `SEMANTIC_OWNER_VIOLATION` (P006/P002 risk), `OVERGENERALIZED_MAPPING`, `ASPECT_VALENCE_OVERSIMPLIFICATION`, `DIRECTION_UNSUPPORTED`, `EVIDENCE_ROOT_AMBIGUOUS`, `MISSING_MODIFIER`, `MISSING_EXCLUSION`, `SINGLE_FACT_DOMINANCE_RISK` (major), `CONTEXT_PROMOTION_BYPASS` (critical).
- **Review status:** `rewrite`.

## Astrology contradiction, density, aspect, and positive-bias analysis

- **Contradiction:** AS-C2B-02 (P002 high, pressure) and AS-C2B-03 (P002 low, change) are distinct local contexts. They must remain contextual variation unless qualified global-scope evidence independently establishes a state.
- **Aspect semantics:** no rule labels a square, opposition, or conjunction as intrinsically bad/good. The problem is instead that all five types are equally permitted to cause the same high/low direction, while tension is only a presentation modifier.
- **Fact dominance:** each triggered rule can produce a candidate that active runtime resolves globally. Orb strength does not establish C1 context coverage or source independence.
- **Rule density:** P002 is the only Primitive with both directions; every other covered Primitive has only a high rule. P001–P006 otherwise each have one rule.
- **Positive bias:** six high rules and one low rule. This requires approval review; no balancing change is implied.
