# Bazi Deterministic Tables Template — Non-Production

This abbreviated authoring aid **must not be loaded as runtime configuration**,
copied into `configs/`, renamed to `bazi_deterministic_tables_v1.yaml`, or used
to pass `CALCULATION_CONFIG_CHECKED`.

```yaml
schema_version: bazi-deterministic-tables-v1
table_version: <PROJECT_OWNED_TABLE_VERSION>
methodology_version: <ACCEPTED_BAZI_METHODOLOGY_VERSION>
vocabulary_version: <ACCEPTED_VOCABULARY_VERSION>
tables:
  hidden_stems:
    - rule_id: <PROJECT_OWNED_RULE_ID>
      inputs:
        <BAZI_VOCABULARY_CATEGORY>: [<CANONICAL_ID>]
      outputs:
        <BAZI_VOCABULARY_CATEGORY>: [<CANONICAL_ID>]
      limitations: []
  ten_gods: [<PROJECT_OWNED_RULES>]
  relations: [<PROJECT_OWNED_RULES>]
```

Every placeholder is intentionally invalid and requires project-owner review.
