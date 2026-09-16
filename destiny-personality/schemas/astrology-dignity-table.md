# Astrology Dignity Table Contract

## Production asset

The project-owned asset is `astrology_dignity_table_v1.yaml`. Its root contains
exactly `schema_version`, `table_version`, `methodology_version`,
`vocabulary_version`, and `rows`. The schema is
`astrology-dignity-table-v1`; referenced versions must match the accepted
astrology methodology and vocabulary.

Each non-empty `rows` entry contains exactly `body_id`, `sign_id`,
`dignity_id`, and `limitations`. The first three fields reference the
`astrology_body`, `astrology_sign`, and `astrology_dignity` vocabulary
categories. The combined key is unique. `limitations` is an explicit string
list and may be empty.

## Validation and errors

Exact keys, versions, scalar types, non-empty rows, references, and duplicate
keys are validated mechanically. Missing assets or fields are `CONFIG_GAP`;
malformed YAML is `CONFIG_PARSE_ERROR`; wrong types are `CONFIG_TYPE_ERROR`;
incompatible versions are `CONFIG_VERSION_MISMATCH`; invalid values and
references are `CONFIG_VALUE_ERROR`.

## Product boundary

This schema supplies no dignity assignments. Do not infer them from astrological
conventions, external sources, or the template.
