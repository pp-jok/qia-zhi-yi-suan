# Fact Comparison Policy Template — Non-Production

This abbreviated authoring aid **must not be loaded as runtime configuration**,
copied into `configs/`, or renamed to `fact_comparison_policy_v1.yaml`.

```yaml
schema_version: fact-comparison-policy-v1
policy_version: <PROJECT_OWNED_POLICY_VERSION>
methodology_versions:
  bazi: <ACCEPTED_BAZI_METHODOLOGY_VERSION>
  astrology: <ACCEPTED_ASTROLOGY_METHODOLOGY_VERSION>
vocabulary_version: <ACCEPTED_VOCABULARY_VERSION>
fact_schema_version: deterministic-facts-v1
triggers: [warning, uncertainty, boundary_sensitivity, historical_time_ambiguity, policy_anomaly]
logical_categories:
  - category_id: <PROJECT_OWNED_LOGICAL_CATEGORY>
    comparison_mode: <exact_OR_numeric>
boundary_margins: [<PROJECT_OWNED_NUMERIC_POLICIES>]
canonical_precision: [<PROJECT_OWNED_NUMERIC_POLICIES>]
tolerances: [<PROJECT_OWNED_NUMERIC_POLICIES>]
representation_equivalences: [<PROJECT_OWNED_EQUIVALENCES>]
```

All policy values remain intentionally unspecified.
