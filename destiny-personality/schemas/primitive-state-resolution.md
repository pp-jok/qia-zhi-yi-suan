# Primitive State Resolution Contract

## Production asset

The project-owned production asset is named
`primitive_state_resolution_v1.yaml`. Its root contains exactly
`schema_version`, `resolution_version`, `ontology_version`,
`score_model_version`, `states`, `invariants`, and `rules`.

- `schema_version` is `primitive-state-resolution-v1`.
- `resolution_version` is a non-empty immutable version identifier.
- `ontology_version` matches the accepted Primitive Ontology.
- `score_model_version` is the frozen score model version `2.2`.
- `states` contains each wire state exactly once: `supported_high`,
  `supported_low`, `mixed`, and `unknown`.
- `rules` is non-empty and covers every wire state.

## Safety invariants

`invariants` contains exactly these values:

- `no_evidence_state`: `unknown`;
- `low_requires_explicit_reverse_evidence`: `true`;
- `unknown_is_not_low`: `true`;
- `preserve_system_salience`: `true`;
- `cross_system_validation_changes_trait_salience`: `false`;
- `tension_reduces_trait_salience`: `false`.

No rule may weaken an invariant. In particular, absent evidence never produces
`supported_low`; low requires explicit reverse evidence, and simultaneous
supported forces may remain `mixed` without reducing either salience value.

## Rule records

Each rule contains exactly `rule_id`, `target_state`, `priority`, `description`,
`requires_explicit_reverse_evidence`, `evidence_requirements`, `thresholds`, and
`limitations`.

- `rule_id` is a unique non-empty identifier.
- `target_state` is one declared wire state.
- `priority` is a unique non-negative integer and is the deterministic rule
  evaluation order.
- `description` is non-empty project-owned text.
- `requires_explicit_reverse_evidence` is a boolean and must be `true` for every
  `supported_low` rule.
- `evidence_requirements` is a non-empty mapping.
- `thresholds` is an explicit mapping and may be empty only when the rule needs
  no numeric threshold.
- `limitations` is an explicit list and may be empty.

The contract validates rule structure but does not supply or execute semantic
predicates. Evidence vocabulary, reverse-evidence mappings, threshold values,
and rule meanings remain project-owned. Missing real values are `CONFIG_GAP`.

## Resolution result

A later resolver emits one result per evaluated Primitive with
`primitive_id`, `state`, `bazi_salience`, `astrology_salience`,
`evidence_stability`, `evidence_refs`, `resolution_rule_ref`, and
`limitations`.

Trait salience stays isolated by source system. Cross-System Relation and
Synthesis Priority are separate later-stage values and must not be folded into
Primitive State.

## Loading order

Validate the ontology first, then this state policy, then cross-file versions.
This contract alone does not complete Gate 1 or permit entry into structured
personality reasoning.

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
indices. A rule that weakens a fixed invariant and a duplicate priority are
invalid values, not missing configuration.
