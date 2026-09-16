# Bazi Deterministic Tables Contract

## Production asset

The project-owned asset is `bazi_deterministic_tables_v1.yaml`. Its root
contains exactly `schema_version`, `table_version`, `methodology_version`,
`vocabulary_version`, and `tables`. The schema is
`bazi-deterministic-tables-v1`; both referenced versions must match the
accepted runtime methodology and Canonical Fact Vocabulary.

`tables` contains exactly `hidden_stems`, `ten_gods`, and `relations`. Every
section is a non-empty list of rules. A rule contains exactly `rule_id`,
`inputs`, `outputs`, and `limitations`. Rule identifiers are non-empty and
globally unique. Inputs and outputs are non-empty mappings from a `bazi_*`
vocabulary category to a non-empty list of canonical IDs. `limitations` is an
explicit list of strings and may be empty.

The only output category for `hidden_stems` is `bazi_stem`; for `ten_gods` it
is `bazi_ten_god`; and for `relations` it is `bazi_relation`. This freezes the
record shape without supplying any rule values.

## Validation and errors

Every category and canonical ID must exist in the accepted vocabulary. The
loader validates exact keys, types, non-empty values, versions, duplicate IDs,
and references without interpreting a rule's domain meaning. Missing assets or
fields are `CONFIG_GAP`; malformed YAML is `CONFIG_PARSE_ERROR`; wrong types are
`CONFIG_TYPE_ERROR`; incompatible versions are `CONFIG_VERSION_MISMATCH`; and
unknown fields, duplicates, empty values, or invalid references are
`CONFIG_VALUE_ERROR`.

## Product boundary

This contract does not supply hidden-stem, Ten-God, or relation values. Those
are project-owned. Never derive or repair them from conventions, model
knowledge, provider output, or the authoring template.
