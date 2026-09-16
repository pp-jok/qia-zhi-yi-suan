# Primitive Ontology Contract

## Production asset

The project-owned production asset is named `primitive_ontology_v1.yaml`.
Its root contains exactly `schema_version`, `ontology_version`, and
`primitives`. `schema_version` is `primitive-ontology-v1`;
`ontology_version` is a non-empty immutable version identifier; and
`primitives` is a non-empty list.

Each Primitive contains exactly:

- `primitive_id`: `P###`, where each `#` is an ASCII digit;
- `canonical_name`: the non-empty project-owned name;
- `definition`: the non-empty project-owned meaning;
- `high_expression`: the non-empty supported-high pole;
- `low_expression`: the non-empty supported-low pole;
- `aliases`: an explicit list, which may be empty;
- `limitations`: an explicit list, which may be empty.

These fields define a semantic axis. They do not determine an individual
case's state and do not authorize an agent to infer evidence or thresholds.

## Validation

Primitive IDs are unique. Canonical names and aliases must be non-empty after
trimming and globally unambiguous after trimming and Unicode-preserving case
folding. A canonical name therefore cannot also be an alias for another
Primitive. `high_expression` and `low_expression` must remain distinct after
trimming. Unknown fields are invalid.

A relation-graph reference is valid only when its `P###` identifier occurs in
the accepted ontology. Matching the identifier format alone does not define a
Primitive.

## Error classification

Use this exact mapping and close `SEMANTIC_CONFIG_CHECKED`:

| Failure | Error code |
|---|---|
| Missing asset or required field | `CONFIG_GAP` |
| Malformed YAML | `CONFIG_PARSE_ERROR` |
| Wrong container or scalar type | `CONFIG_TYPE_ERROR` |
| Unsupported schema or cross-file version | `CONFIG_VERSION_MISMATCH` |
| Invalid, ambiguous, duplicate, or unknown value | `CONFIG_VALUE_ERROR` |

Record the most specific dot-separated field path, including zero-based list
indices, such as `primitives.1.canonical_name`.

## Product boundary

The contract supplies structure only. Names, meanings, expressions, aliases,
limitations, and the membership of `primitives` are product-owned values. Do
not derive them from relation IDs, examples, general psychology, Bazi, or
astrology conventions.
