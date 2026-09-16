# Context-Aware Mapping Registry Contract

## Production assets

The project-owned production assets are named
`bazi_mapping_registry_v1.yaml` and
`astrology_mapping_registry_v1.yaml`. They use the same structural contract but
remain separate assets. Bazi evidence and astrology evidence must retain
source-system isolation until the later Cross-System Synthesizer.

Each registry root contains exactly:

- `schema_version`: `context-aware-mapping-registry-v1`;
- `registry_version`: a non-empty immutable version identifier;
- `source_system`: `bazi` for the Bazi file and `astrology` for the astrology
  file;
- `methodology_version`: the corresponding accepted methodology version;
- `fact_schema_version`: `deterministic-facts-v1`;
- `score_model_version`: the accepted score model version, currently `2.2`;
- `ontology_version`: the accepted Primitive Ontology version;
- `rules`: a non-empty list;
- `interactions`: an explicit list, which may be empty.

Load and validate Bazi first, then astrology. Unknown root fields are invalid.
The two `registry_version` values may differ.

## Mapping rules

Each rule contains exactly `rule_id`, `priority`, `primary_condition`,
`context`, `outputs`, `modifiers`, and `limitations`.

- `rule_id` is a non-empty identifier and is globally unique across both
  registries.
- `priority` is a unique non-negative integer within one registry. Return rules
  in ascending priority order; priority does not cross source systems.
- `primary_condition` is a non-empty project-owned declarative mapping.
- A non-empty `context` is mandatory. An unconditional single-signal mapping
  cannot pass this contract.
- `outputs` is a non-empty list.
- `modifiers` and `limitations` are explicit lists and may be empty.

Conditions are validated as data, not executed or completed by the agent. The
agent must not infer a missing operator, feature path, threshold, or context.

## Outputs and modifiers

Each output contains exactly `primitive_id`, `direction`, `salience`, and
`limitations`.

- `primitive_id` is `P###` and must exist in the accepted ontology.
- A rule cannot output the same Primitive twice.
- `direction` is a non-empty project-owned wire value. This contract does not
  invent or freeze its semantic vocabulary.
- `salience` is an integer inside the accepted score model's trait-salience
  range.
- `limitations` is an explicit list of non-empty strings and may be empty.

Each modifier contains exactly `when` and `effects`. `when` is a non-empty
declarative mapping. `effects` is a non-empty list of non-empty declarative
mappings. Their meaning remains project-owned.

## Interactions

Each interaction contains exactly `interaction_id`, `requires`, `produces`,
and `limitations`.

- `interaction_id` is non-empty and globally unique across both registries.
- `requires` contains at least two distinct rule IDs from the same registry.
- `produces` is a non-empty declarative mapping.
- `limitations` is an explicit list of non-empty strings and may be empty.

A same-registry reference is mandatory: an interaction cannot join Bazi and
astrology rules. Declared interaction order is preserved but does not create
precedence.

## Declarative value safety

Nested declarative values may contain only string mapping keys, mappings,
lists, strings, booleans, integers, finite floats, and null. Reject YAML dates,
non-string keys, non-finite floats, or other YAML-specific objects. Recursively
freeze accepted collections before returning them from a reference validator.

## Error classification

Use this exact mapping and close `SEMANTIC_CONFIG_CHECKED`:

| Failure | Error code |
|---|---|
| Missing asset or required field | `CONFIG_GAP` |
| Malformed YAML | `CONFIG_PARSE_ERROR` |
| Wrong container, scalar, mapping-key, or nested declarative type | `CONFIG_TYPE_ERROR` |
| Unsupported schema, ontology, methodology, fact-schema, or score-model reference | `CONFIG_VERSION_MISMATCH` |
| Invalid, duplicate, unresolved, or unknown value | `CONFIG_VALUE_ERROR` |

Record the most specific zero-based dot-separated field path available, such
as `rules.0.outputs.1.primitive_id`.

## Product boundary

The contract supplies structure only. Real conditions, contexts, directions,
effects, mappings, limitations, interactions, and thresholds are project-owned.
Do not derive them from examples, common Bazi or astrology knowledge, relation
IDs, or model inference. The absence of either real registry is `CONFIG_GAP`;
the documentation template never satisfies the gate.
