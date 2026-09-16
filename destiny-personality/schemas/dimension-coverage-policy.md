# Dimension Coverage Policy Contract

The project-owned production asset is `dimension_coverage_policy_v1.yaml`. Its
root contains exactly `schema_version`, `policy_version`, `ontology_version`,
`score_model_version`, `dimension_count`, `dimensions`, and `coverage_policy`.
The schema is `dimension-coverage-policy-v1`; referenced versions must match
accepted assets; `dimension_count` is exactly `12`; and `dimensions` contains
exactly twelve records.

Each dimension contains exactly `dimension_id`, `canonical_name`, `definition`,
`primitive_refs`, and `limitations`. IDs are unique `D##` values. Names are
non-empty and globally unique after trim and case-fold. `primitive_refs` is a
non-empty, duplicate-free list resolved against the accepted ontology.
`limitations` is an explicit string list and may be empty.

## Coverage policy

`coverage_policy` contains exactly:

- `threshold_status`: `provisional`;
- `coverage_metric`: a non-empty project-owned identifier;
- `complete_threshold`: a finite number in `[0, 1]`;
- `partial_threshold`: a finite number in `[0, complete_threshold)`;
- `partial_portrait_allowed`: `true`;
- `partial_status`: `partial`;
- `warning_code`: `coverage_warning`;
- `missing_config_code`: `CONFIG_GAP`;
- `dimension_requirements`: exactly one entry for each dimension.

Each requirement contains exactly `dimension_id` and
`minimum_supported_primitives`. The minimum is a positive integer no greater
than the referenced dimension's Primitive count.

`provisional` does not authorize runtime threshold selection. Every real name,
definition, membership, metric, minimum, and threshold remains project-owned.

## Runtime guard and errors

Case-specific low coverage may produce `coverage_warning` and `partial` only after `SEMANTIC_CONFIG_CHECKED`
has passed with all semantic assets complete.
Missing or invalid configuration is `CONFIG_GAP`, never partial.

Use the exact error classes: missing asset or field `CONFIG_GAP`; malformed YAML
`CONFIG_PARSE_ERROR`; wrong type `CONFIG_TYPE_ERROR`; schema or cross-file
version mismatch `CONFIG_VERSION_MISMATCH`; invalid, duplicate, unknown, or
unresolved value `CONFIG_VALUE_ERROR`. Report the most specific zero-based
dot-separated field path and stop at the first failure.

The contract defines configuration structure only. It does not calculate case
coverage, invent dimensions, or permit Narrative.
