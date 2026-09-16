# Dimension Coverage Policy Template — Non-Production

This document **must not be loaded as runtime configuration**, copied into
`configs/`, renamed to `dimension_coverage_policy_v1.yaml`, or used to pass a
gate. Every placeholder requires project approval.

```yaml
schema_version: dimension-coverage-policy-v1
policy_version: <PROJECT_OWNED_POLICY_VERSION>
ontology_version: <MATCH_APPROVED_ONTOLOGY_VERSION>
score_model_version: "2.2"
dimension_count: 12
dimensions:
  - dimension_id: <PROJECT_OWNED_DIMENSION_ID>
    canonical_name: <PROJECT_OWNED_DIMENSION_NAME>
    definition: <PROJECT_OWNED_DIMENSION_DEFINITION>
    primitive_refs: [<APPROVED_PRIMITIVE_ID>]
    limitations: []
coverage_policy:
  threshold_status: provisional
  coverage_metric: <PROJECT_OWNED_COVERAGE_METRIC>
  complete_threshold: <PROJECT_OWNED_COMPLETE_THRESHOLD>
  partial_threshold: <PROJECT_OWNED_PARTIAL_THRESHOLD>
  partial_portrait_allowed: true
  partial_status: partial
  warning_code: coverage_warning
  missing_config_code: CONFIG_GAP
  dimension_requirements:
    - dimension_id: <MATCH_PROJECT_OWNED_DIMENSION_ID>
      minimum_supported_primitives: <PROJECT_OWNED_POSITIVE_INTEGER>
```

The single shown record is deliberately incomplete: production requires twelve
approved dimensions and one requirement per dimension.
