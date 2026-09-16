# Context-Aware Mapping Registry Template — Non-Production

This document is an authoring aid. It **must not be loaded as runtime configuration**,
**must not be copied** into `configs/`, renamed to a production filename, or
used to pass `SEMANTIC_CONFIG_CHECKED`. Every angle-bracket token requires an
explicit project-owned value and approval.

## `bazi_mapping_registry_v1.yaml` shape

```yaml
schema_version: context-aware-mapping-registry-v1
registry_version: <PROJECT_OWNED_BAZI_REGISTRY_VERSION>
source_system: bazi
methodology_version: bazi-core-v1.0
fact_schema_version: deterministic-facts-v1
score_model_version: "2.2"
ontology_version: <MATCH_APPROVED_ONTOLOGY_VERSION>
rules:
  - rule_id: <PROJECT_OWNED_BAZI_RULE_ID>
    priority: <PROJECT_OWNED_NON_NEGATIVE_INTEGER>
    primary_condition:
      <PROJECT_OWNED_KEY>: <PROJECT_OWNED_VALUE>
    context:
      <PROJECT_OWNED_KEY>: <PROJECT_OWNED_VALUE>
    outputs:
      - primitive_id: <APPROVED_PRIMITIVE_ID>
        direction: <PROJECT_OWNED_DIRECTION>
        salience: <PROJECT_OWNED_SALIENCE>
        limitations: []
    modifiers: []
    limitations: []
interactions: []
```

## `astrology_mapping_registry_v1.yaml` shape

```yaml
schema_version: context-aware-mapping-registry-v1
registry_version: <PROJECT_OWNED_ASTROLOGY_REGISTRY_VERSION>
source_system: astrology
methodology_version: western-tropical-v1.0
fact_schema_version: deterministic-facts-v1
score_model_version: "2.2"
ontology_version: <MATCH_APPROVED_ONTOLOGY_VERSION>
rules:
  - rule_id: <PROJECT_OWNED_ASTROLOGY_RULE_ID>
    priority: <PROJECT_OWNED_NON_NEGATIVE_INTEGER>
    primary_condition:
      <PROJECT_OWNED_KEY>: <PROJECT_OWNED_VALUE>
    context:
      <PROJECT_OWNED_KEY>: <PROJECT_OWNED_VALUE>
    outputs:
      - primitive_id: <APPROVED_PRIMITIVE_ID>
        direction: <PROJECT_OWNED_DIRECTION>
        salience: <PROJECT_OWNED_SALIENCE>
        limitations: []
    modifiers: []
    limitations: []
interactions: []
```

The template contains no approved mapping semantics. A production bundle
remains absent until both registries and all referenced Primitive values have
been reviewed, versioned, and supplied as project assets.
