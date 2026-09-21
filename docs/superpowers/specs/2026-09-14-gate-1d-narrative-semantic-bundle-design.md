# Gate 1D Narrative Rules and Semantic Contract Bundle Design

**Date:** 2026-09-14  
**Status:** Approved by standing authorization  
**Scope:** Narrative guard contract and semantic-asset aggregation only

## Decision

Use a declarative `narrative_rules_v1.yaml` plus a development-only semantic
bundle loader. The asset constrains rendering of an already complete IR; it
contains no ready-made prose, personality claims, archetypes, or domain
interpretations. The bundle loader validates semantic assets and relation-graph
references but does not bypass the earlier calculation gate or claim Gate 1 is
complete.

Embedding narrative instructions in `SKILL.md` alone was rejected because they
would be unversioned. Storing prose templates was rejected because it would
encourage template collapse and could create unsupported claims.

## Narrative asset

The root contains exactly `schema_version`, `narrative_version`,
`ontology_version`, `dimension_policy_version`, `sections`, `invariants`, and
`rules`. Schema is `narrative-rules-v1`; versions reference accepted assets;
sections are unique non-empty project-owned identifiers; rules are non-empty
and cover every section.

Fixed invariants are:

- `complete_ir_required: true`;
- `narrative_changes_core_claims: false`;
- `unsupported_claims_allowed: false`;
- `unknown_may_be_rendered_as_certain: false`;
- `secondary_may_be_promoted: false`;
- `chart_anchor_required: true`;
- `traditional_interpretation_claimed_scientific: false`.

Each rule contains exactly `rule_id`, `priority`, `target_section`,
`source_kinds`, `requires_chart_anchor`, `rendering_constraints`,
`prohibited_inferences`, and `limitations`. IDs and priorities are unique;
section references resolve; source kinds are unique and drawn from `primitive`,
`signature`, `core_dynamic`, `dimension`, `shadow`, `mature`, `fate`, and
`archetype`; chart anchor is always required; constraints are non-empty
declarative data; prohibited inferences are non-empty strings. Rules are sorted
by priority.

## Semantic contract bundle

`load_semantic_contract_bundle(config_dir, runtime_config)` loads in exact order:

1. Primitive foundation;
2. Bazi and astrology Mapping registries;
3. Dimension Coverage Policy;
4. Narrative Rules;
5. relation-graph-to-ontology references.

It returns immutable `SemanticContractBundle`. A relation endpoint not present
in the ontology is `CONFIG_VALUE_ERROR` against
`primitive_relation_graph_v1.yaml` with its precise relation field. Missing
assets retain existing first-failure `CONFIG_GAP` behavior.

This is a development reference for candidate semantic assets. It does not
execute Mapping, resolve state, create IR, render Narrative, or validate missing
hidden-stem/Ten-God/Bazi-relation/astrology-dignity tables, aliases, node rules,
margins, or tolerances. Therefore semantic bundle acceptance alone never opens
`REASONING_ALLOWED`.

## Delivery and testing

Add Skill contract and non-production template, immutable Python models and
loaders, TDD validation/error matrices, Skill routing, status documentation,
and package checks. Do not create production Narrative or other missing assets.
All fixture semantics use `TEST_ONLY_` values.
