# Canonical Fact Vocabulary Template — Non-Production

This authoring aid **must not be loaded as runtime configuration**, copied into
`configs/`, renamed to the production filename, or used to pass
`CALCULATION_CONFIG_CHECKED`. Every angle-bracket token requires an explicit
project-owned value and approval.

```yaml
schema_version: canonical-fact-vocabulary-v1
vocabulary_version: <PROJECT_OWNED_VOCABULARY_VERSION>
methodology_versions:
  bazi: bazi-core-v1.0
  astrology: western-tropical-v1.0
categories:
  <EACH_REQUIRED_CATEGORY>:
    entries:
      - canonical_id: <PROJECT_OWNED_CANONICAL_ID>
        aliases: []
```

The abbreviated example is intentionally incomplete and contains invalid
placeholders. Production requires all ten categories and every approved
canonical identifier and alias.

