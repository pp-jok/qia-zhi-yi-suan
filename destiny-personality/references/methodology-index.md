# Methodology and Configuration Index

Load only the assets needed by the current gate.

## Calculation baseline

- `configs/bazi_methodology_v1.yaml`: frozen Bazi method decisions, version `bazi-core-v1.0`.
- `configs/astrology_methodology_v1.yaml`: frozen Western tropical method decisions, version `western-tropical-v1.0`.
- `schemas/birth-input.md`: normalized user input and `stable_only` rules.
- `schemas/capability-descriptor.md`: present capability discovery record; discovery remains separate from qualification.
- `schemas/compatibility-evidence.md`: present exact-setting evidence contract.
- `schemas/calculation-envelope.md`: present invocation provenance contract.
- `schemas/deterministic-facts.md`: present normalized deterministic fact schema.
- `schemas/fact-comparison.md`: present independent comparison contract.
- `references/capability-protocol.md`: present discovery, qualification, execution-scoped authorization, invocation, and retry protocol.
- `checklists/capability-preflight.md`: present ordered capability preflight.
- `checklists/stage-gates.md`: calculation and semantic gate order.
- `schemas/canonical-fact-vocabulary.md`: Canonical Fact Vocabulary contract is present for the ten normalization categories.
- `examples/canonical-fact-vocabulary-template.md`: non-production authoring aid; never load it as configuration.
- `schemas/bazi-deterministic-tables.md`: present exact-section and vocabulary-reference contract for Bazi lookup candidates.
- `schemas/astrology-dignity-table.md`: present body/sign/dignity reference-row contract.
- `schemas/astrology-node-policy.md`: present explicit True North Node decision contract with no defaults.
- `schemas/fact-comparison-policy.md`: present trigger, logical-category, margin, precision, tolerance, and equivalence contract.

All calculation configuration contracts are present, but production values remain absent. The production canonical vocabulary and exact versioned project-owned `hidden-stem`, `Ten-God`, `Bazi-relation`, and `astrology-dignity` lookup rows remain absent. The frozen project also lacks an approved True North Node output policy and canonical fact identifier, exact boundary-distance margins, and versioned comparison tolerances. These are `CONFIG_GAP` conditions at `CALCULATION_CONFIG_CHECKED`; do not substitute common tables, choose a node convention, invent aliases or margins, or derive tolerances from external knowledge.

Strict production remains closed at `CALCULATION_CONFIG_CHECKED`. A
`controlled_inference` portrait follows a separate business-test path:
controlled business testing may proceed after the four baseline assets pass and
a qualified external calculation capability supplies a valid, provenance-backed
fact basis. Missing advanced assets are `CONFIG_LIMITATION` only when every
dependent fact or interpretation is omitted and disclosed; they never become
strict approval.

## Semantic baseline

- `configs/score_model_v2_2.yaml`: frozen separation of salience, stability, cross-system relation, and synthesis priority.
- `configs/primitive_relation_graph_v1.yaml`: opaque relation entries only; do not interpret its `Pxxx` references without an ontology.
- `schemas/primitive-ontology.md`: present Gate 1A ontology structure and uniqueness contract.
- `schemas/primitive-state-resolution.md`: present Gate 1A state-policy and result contract.
- `examples/primitive-foundation-template.md`: non-production authoring aid; never load it as configuration.
- `schemas/context-aware-mapping-registry.md`: present Gate 1B shared structure, isolation, and cross-reference contract for Bazi and astrology registries.
- `examples/mapping-registry-template.md`: non-production authoring aid; never copy or load it as configuration.
- `schemas/dimension-coverage-policy.md`: present Gate 1C twelve-dimension, provisional-threshold, and partial-policy contract.
- `examples/dimension-coverage-template.md`: non-production authoring aid; never load it as configuration.
- `schemas/narrative-rules.md`: present Gate 1D versioned no-new-claims rendering contract.
- `examples/narrative-rules-template.md`: non-production aid with no prose defaults.

Gate 1A contracts are present. Gate 1B contracts are present, but production Primitive assets are absent and production Mapping Registry assets are absent. The semantic baseline is not complete. Required missing values and assets include a project-approved versioned `Primitive Ontology`, project-approved Primitive State resolution rules, real Bazi and astrology Mapping Registry values, 12-dimension definitions and coverage rules, a frozen provisional coverage threshold with partial policy, and `Narrative Rules`. Their definitions, aliases, cross-references, thresholds, and business values remain project-owned semantic gaps.

Return `CONFIG_GAP` at `SEMANTIC_CONFIG_CHECKED` when any required semantic asset is absent or cross-references are invalid. A valid complete registry with no applicable case rule may later produce `coverage_warning`; a missing registry may not.

That semantic `CONFIG_GAP` applies to `strict`. In `controlled_inference`, the
agent does not claim `SEMANTIC_CONFIG_CHECKED`; it may interpret anchored chart
facts without inventing Primitive IDs, Mapping rules, scores, or frozen-rule
approval. Safe omission is recorded as `CONFIG_LIMITATION`.

Golden, calibration expected, and boundary cases are build/release evidence. Never load their expected results during production execution.
