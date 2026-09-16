# Fact Comparison Policy Contract

## Production asset

The project-owned asset is `fact_comparison_policy_v1.yaml`. Its root contains
exactly `schema_version`, `policy_version`, `methodology_versions`,
`vocabulary_version`, `fact_schema_version`, `triggers`,
`logical_categories`, `boundary_margins`, `canonical_precision`, `tolerances`,
and `representation_equivalences`. The schema is
`fact-comparison-policy-v1`, the fact schema is `deterministic-facts-v1`, and
all referenced versions must match accepted inputs.

`triggers` declares exactly the structural cases `warning`, `uncertainty`,
`boundary_sensitivity`, `historical_time_ambiguity`, and `policy_anomaly`.
Every logical category has a unique `category_id` and `comparison_mode` of
either `exact` or `numeric`. Every numeric category must have exactly one
non-negative finite `margin`, non-negative integer `decimal_places`, and
non-negative finite `absolute_tolerance` in the corresponding lists. An
`exact` category cannot appear in those numeric-policy lists.

Each representation-equivalence row names a declared logical category, an
accepted vocabulary category and canonical ID, and a non-empty unique list of
`equivalent_values`. Equivalence is mechanical and may never repair or merge
substantively different facts.

## Validation and errors

Missing assets, fields, required triggers, or numeric coverage are
`CONFIG_GAP`; malformed YAML is `CONFIG_PARSE_ERROR`; wrong types are
`CONFIG_TYPE_ERROR`; incompatible versions are `CONFIG_VERSION_MISMATCH`; and
unknown fields, duplicates, invalid ranges, modes, or references are
`CONFIG_VALUE_ERROR`.

## Product boundary

This contract supplies no logical category IDs, margins, precision, tolerances,
or equivalences. The executing agent must not estimate them or learn them from
candidate tool disagreement.
