# C2 Mapping Review Issue Taxonomy

## Review boundary

This taxonomy audits the active `core-profile-v1` mapping registries against the approved C1 v2 ontology and context-promotion policy. It is review vocabulary only. It does not authorize a mapping change, runtime change, or new semantic asset.

## Severity

| Severity | Meaning |
|---|---|
| critical | A current path can bypass approved scope/state safeguards, consume a non-canonical source, leak time-sensitive data, double-count the same fact as independent evidence, or directly assign a known wrong semantic owner. |
| major | A rule's semantic meaning, direction, evidence root, scope, exclusion, modifier role, or ownership cannot be justified against C1; it must not be carried into v2 unchanged. |
| minor | Documentation, naming, or audit clarity is incomplete but does not independently change semantic interpretation. |

## Codes

| Code | Meaning | Default severity |
|---|---|---|
| NON_CANONICAL_SOURCE | Rule consumes provider prose, natural-language interpretation, LLM output, or renderer prose instead of chart facts. | critical |
| OVERGENERALIZED_MAPPING | Symbol or generic aspect condition maps to a Primitive without sufficient fact condition, semantic rationale, modifier, or exclusion boundary. | major |
| SEMANTIC_OWNER_VIOLATION | Rule is assigned to a Primitive that conflicts with, or cannot be distinguished from, C1 semantic ownership. | major; critical if known wrong owner |
| DIRECTION_UNSUPPORTED | High or low direction has no explicit rule-level semantic rationale. | major |
| STRENGTH_UNSUPPORTED | Strength is fixed or asserted without an evidence-strength basis. | major |
| SINGLE_FACT_DOMINANCE_RISK | One activated rule can resolve a Primitive globally without an approved global-evidence path. | major |
| DOUBLE_COUNTING | Exact, same-root, or semantic duplication can multiply one fact's influence. | critical for false independent evidence; otherwise major |
| EVIDENCE_ROOT_AMBIGUOUS | A candidate has fact references but lacks a stable canonical root identity for audit and promotion independence. | major |
| CONTEXT_SCOPE_INVALID | Context is missing, not in taxonomy, or incompatible with the Primitive. | major |
| CONTEXT_PROMOTION_BYPASS | Local mapping evidence reaches global Primitive State Resolution without C1 policy qualification. | critical |
| MISSING_MODIFIER | A conditional signal is treated as primary evidence with no declared modifier/contextualizer role. | major |
| MISSING_EXCLUSION | A rule has no explicit non-application condition where C1 requires one. | major |
| TIME_SCOPE_LEAK | Time-sensitive fact is available in stable-only or unknown-time mode. | critical |
| TIME_SCOPE_UNDECLARED | A rule may consume hour/angle/house facts but has no auditable time-sensitivity declaration. | major |
| ASPECT_VALENCE_OVERSIMPLIFICATION | Aspect type is used as an intrinsic high/low personality direction rather than interaction, tension, or expression mode. | major |
| RULE_DENSITY_BIAS | Rule count is treated as evidence strength or one Primitive is structurally overrepresented. | major |
| MAPPING_COLLAPSE | Heterogeneous facts repeatedly collapse into a few attractive Primitive directions. | major |
| POSITIVE_BIAS | Direction distribution is systematically high/positive without an explicit reason. | major |
| NO_MAPPING_REQUIRED | A fact family lacks a defensible Primitive mapping and should remain unused. | major |
| CROSS_SYSTEM_VALIDATION_PREMATURE | Runtime labels two systems as validation without all C2 validation requirements. | major |

## Review method

- `canonical source` means a deterministic chart-fact field or a deterministic derivative of it. It does not itself prove semantic adequacy.
- A missing rule-level canonical fact reference is `EVIDENCE_ROOT_AMBIGUOUS`, not `NON_CANONICAL_SOURCE`, when the runtime demonstrably derives the fact from deterministic chart facts.
- A source can be semantically unproven without being a proven wrong owner. Such cases are dispositioned `rewrite`, `re-scope`, `no-mapping`, or `needs_product_decision` rather than claimed as a false factual assertion.
- Findings are counted by affected rule or independently auditable cross-rule cluster. The same rule may have more than one finding.
