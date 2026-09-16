# Canonical Fact Vocabulary Contract

## Production asset

The project-owned production asset is
`canonical_fact_vocabulary_v1.yaml`. Its root contains exactly
`schema_version`, `vocabulary_version`, `methodology_versions`, and
`categories`. `schema_version` is `canonical-fact-vocabulary-v1`;
`vocabulary_version` is a non-empty immutable version; and
`methodology_versions` contains exactly `bazi` and `astrology`, matching the
accepted runtime methodologies.

`categories` contains exactly:

- `bazi_stem`
- `bazi_branch`
- `bazi_ten_god`
- `bazi_relation`
- `astrology_body`
- `astrology_sign`
- `astrology_aspect`
- `astrology_angle`
- `astrology_dignity`
- `astrology_node`

Each category contains exactly `entries`, a non-empty list. Each entry contains
exactly `canonical_id` and `aliases`. `canonical_id` is a non-empty string.
`aliases` is an explicit list of non-empty strings and may be empty.

## Validation

Within each category, all canonical IDs and aliases are unambiguous after
trimming and Unicode-preserving case folding. List order is preserved. Tokens
may repeat across categories because normalization always retains its category.
Unknown root fields, categories, category fields, and entry fields are invalid.

An agent may mechanically replace a source token only when an accepted entry
lists it as an alias. Missing aliases remain unknown and must not be guessed.

The `astrology_node` category defines naming only. It does not define the True North Node output rule,
canonical fact shape, aspect participation, phase,
dignity, or weight; those require separately approved configuration.

## Error classification

| Failure | Error code |
|---|---|
| Missing asset or required field | `CONFIG_GAP` |
| Malformed or unreadable YAML | `CONFIG_PARSE_ERROR` |
| Wrong mapping, list, key, or scalar type | `CONFIG_TYPE_ERROR` |
| Unsupported schema or methodology version | `CONFIG_VERSION_MISMATCH` |
| Unknown field/category, empty value/list, or ambiguous token | `CONFIG_VALUE_ERROR` |

Record `canonical_fact_vocabulary_v1.yaml` and the most specific dot-separated
field path, including zero-based entry and alias indices.

## Product boundary

This contract supplies structure only. Category membership, canonical IDs,
aliases, completeness claims, and versions are project-owned values. Do not
derive them from examples, provider output, general knowledge, Bazi, or
astrology conventions.
