# Astrology Node Policy Contract

## Production asset

The project-owned asset is `astrology_node_policy_v1.yaml`. Its root contains
exactly `schema_version`, `policy_version`, `methodology_version`,
`vocabulary_version`, `node_id`, and `output`. The schema is
`astrology-node-policy-v1`; the versions must match the accepted astrology
methodology and vocabulary. `node_id` references `astrology_node`.

`output` contains exactly the explicit fields `included`, `phase`,
`aspect_participation`, `dignity_participation`, `weight_role`, and
`time_sensitive`. Inclusion and all participation/sensitivity fields are
booleans. Phase and weight role are non-empty project-owned identifiers. An
excluded node cannot participate in aspects or dignities. `included` must also
match the accepted astrology methodology's frozen `true_node` switch.

## Validation and errors

There are no defaults. Missing decisions are `CONFIG_GAP`; malformed YAML is
`CONFIG_PARSE_ERROR`; wrong types are `CONFIG_TYPE_ERROR`; incompatible
versions are `CONFIG_VERSION_MISMATCH`; invalid references, unknown fields,
empty identifiers, and contradictions are `CONFIG_VALUE_ERROR`.

## Product boundary

The contract resolves the earlier structural ambiguity only after a real
approved asset is supplied. It does not choose whether the True North Node is
included or how it participates.
