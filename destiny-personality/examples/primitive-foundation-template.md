# Primitive Foundation Template — Non-Production

This document is an authoring aid. It **must not be loaded as runtime configuration**,
copied into `configs/`, renamed to a production filename, or used to pass
`SEMANTIC_CONFIG_CHECKED`. Every angle-bracket token requires an explicit
project-owned value and approval.

## Ontology shape

```yaml
schema_version: primitive-ontology-v1
ontology_version: <PROJECT_OWNED_ONTOLOGY_VERSION>
primitives:
  - primitive_id: <PROJECT_OWNED_PRIMITIVE_ID>
    canonical_name: <PROJECT_OWNED_NAME>
    definition: <PROJECT_OWNED_DEFINITION>
    high_expression: <PROJECT_OWNED_HIGH_EXPRESSION>
    low_expression: <PROJECT_OWNED_LOW_EXPRESSION>
    aliases: []
    limitations: []
```

## State-policy shape

```yaml
schema_version: primitive-state-resolution-v1
resolution_version: <PROJECT_OWNED_RESOLUTION_VERSION>
ontology_version: <MATCH_APPROVED_ONTOLOGY_VERSION>
score_model_version: "2.2"
states: [supported_high, supported_low, mixed, unknown]
invariants:
  no_evidence_state: unknown
  low_requires_explicit_reverse_evidence: true
  unknown_is_not_low: true
  preserve_system_salience: true
  cross_system_validation_changes_trait_salience: false
  tension_reduces_trait_salience: false
rules:
  - rule_id: <PROJECT_OWNED_RULE_ID>
    target_state: <SUPPORTED_WIRE_STATE>
    priority: <PROJECT_OWNED_NON_NEGATIVE_INTEGER>
    description: <PROJECT_OWNED_RULE_DESCRIPTION>
    requires_explicit_reverse_evidence: <PROJECT_OWNED_BOOLEAN>
    evidence_requirements:
      <PROJECT_OWNED_KEY>: <PROJECT_OWNED_VALUE>
    thresholds: {}
    limitations: []
```

The examples deliberately contain invalid placeholder tokens. They are not
semantic defaults. A production bundle remains absent until every Primitive,
rule, threshold, reference, and limitation is reviewed and versioned.
