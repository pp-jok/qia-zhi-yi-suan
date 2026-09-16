# Narrative Rules Contract

The production asset is `narrative_rules_v1.yaml`. It constrains rendering of
an already complete IR and does not contain prose templates, personality
claims, or default interpretations.

The root contains exactly `schema_version`, `narrative_version`,
`ontology_version`, `dimension_policy_version`, `sections`, `invariants`, and
`rules`. Schema is `narrative-rules-v1`; referenced versions must match;
sections are unique non-empty identifiers; rules are non-empty and cover every
section.

`invariants` contains exactly:

- `complete_ir_required`: `true`;
- `narrative_changes_core_claims`: `false`;
- `unsupported_claims_allowed`: `false`;
- `unknown_may_be_rendered_as_certain`: `false`;
- `secondary_may_be_promoted`: `false`;
- `chart_anchor_required`: `true`;
- `traditional_interpretation_claimed_scientific`: `false`.

Each rule contains `rule_id`, `priority`, `target_section`, `source_kinds`,
`requires_chart_anchor`, `rendering_constraints`, `prohibited_inferences`, and
`limitations`, with no extra fields. IDs and priorities are unique. The section
must resolve; source kinds are unique members of `primitive`, `signature`,
`core_dynamic`, `dimension`, `shadow`, `mature`, `fate`, and `archetype`;
`requires_chart_anchor` is true; constraints and prohibited inferences are
non-empty. Rules are evaluated by ascending priority.

Missing/field, parse, type, version, and invalid/reference failures use
`CONFIG_GAP`, `CONFIG_PARSE_ERROR`, `CONFIG_TYPE_ERROR`,
`CONFIG_VERSION_MISMATCH`, and `CONFIG_VALUE_ERROR` respectively, with the most
specific dot-separated field path. Narrative may only express loaded IR and
must never add, promote, repair, or scientifically reframe a claim.
