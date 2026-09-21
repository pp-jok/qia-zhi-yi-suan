# Gate 1A Primitive Foundation Contracts Design

**Date:** 2026-09-13  
**Status:** Approved for implementation  
**Scope:** Primitive Ontology and Primitive State Resolution contracts only

## 1. Purpose

Gate 1A establishes the contract boundary required before structured personality
reasoning can be implemented. It defines how project-owned Primitive definitions
and state-resolution policy must be represented and validated without supplying
or inventing their semantic values.

This phase does not make `SEMANTIC_CONFIG_CHECKED` pass. Until real, complete,
project-approved assets are supplied, production execution continues to stop with
`CONFIG_GAP`.

## 2. Architectural boundary

The deliverable has two layers.

### 2.1 Distributable Skill layer

The Skill contains:

- a Primitive Ontology contract;
- a Primitive State Resolution contract;
- a non-production template embedded in documentation;
- loading order, validation gates, and failure behavior;
- explicit prohibitions against inventing Primitive definitions, aliases,
  thresholds, reverse-evidence mappings, or state rules.

The Skill does not contain a usable production ontology or state policy. No
placeholder configuration is added under `destiny-personality/configs/`.

### 2.2 Development reference layer

The Python reference package contains immutable models and a separate
`load_primitive_foundation(config_dir)` entry point. It validates candidate
project-owned assets during development and release checks.

This loader remains separate from `load_runtime_config()`. The existing runtime
configuration baseline and Phase C behavior must remain unchanged, and the
Python package remains development-only rather than a Skill runtime dependency.

## 3. Asset names and loading order

Future production assets use these exact filenames:

1. `primitive_ontology_v1.yaml`
2. `primitive_state_resolution_v1.yaml`

The ontology loads and validates first. State resolution loads only after the
ontology passes. Cross-file versions and references are then validated as one
Primitive foundation bundle.

Neither file is created in the production configuration directory during Gate
1A. Tests create synthetic fixtures in temporary directories.

## 4. Primitive Ontology contract

The root fields are exactly:

- `schema_version`: must be `primitive-ontology-v1`;
- `ontology_version`: a non-empty immutable version identifier;
- `primitives`: a non-empty list.

Each Primitive record contains exactly:

- `primitive_id`: `P` followed by three digits;
- `canonical_name`: non-empty project-owned name;
- `definition`: non-empty project-owned definition;
- `high_expression`: non-empty description of the supported-high pole;
- `low_expression`: non-empty description of the supported-low pole;
- `aliases`: an explicit list of zero or more aliases;
- `limitations`: an explicit list of zero or more forbidden or limited
  inferences.

Validation rules:

- Primitive IDs are unique.
- Canonical names and aliases are non-empty after trimming.
- Canonical names and aliases are globally unambiguous after Unicode-preserving
  case folding and trimming.
- A Primitive's high and low expressions must be distinct after trimming.
- Unknown fields are rejected.
- Existing relation-graph identifiers do not become defined merely because they
  match the `P###` format. Cross-reference acceptance requires a loaded ontology
  containing the identifier.

The ontology defines semantic poles only. It does not decide a case's state.

## 5. Primitive State Resolution contract

The root fields are exactly:

- `schema_version`: must be `primitive-state-resolution-v1`;
- `resolution_version`: a non-empty immutable version identifier;
- `ontology_version`: must match the loaded ontology;
- `score_model_version`: must match the frozen score model version `2.2`;
- `states`: the canonical wire-state list, with each supported state exactly
  once;
- `invariants`: fixed safety invariants;
- `rules`: a non-empty ordered rule list.

The only wire states are:

- `supported_high`;
- `supported_low`;
- `mixed`;
- `unknown`.

The required invariants are exact contract values:

- `no_evidence_state: unknown`;
- `low_requires_explicit_reverse_evidence: true`;
- `unknown_is_not_low: true`;
- `preserve_system_salience: true`;
- `cross_system_validation_changes_trait_salience: false`;
- `tension_reduces_trait_salience: false`.

Each rule contains exactly:

- `rule_id`: unique non-empty identifier;
- `target_state`: one supported wire state;
- `priority`: unique non-negative integer controlling deterministic evaluation
  order;
- `description`: non-empty project-owned explanation;
- `requires_explicit_reverse_evidence`: a boolean that must be `true` for every
  `supported_low` rule;
- `evidence_requirements`: a non-empty mapping supplied by the product asset;
- `thresholds`: an explicit mapping supplied by the product asset, which may be
  empty only for a rule that needs no numeric threshold;
- `limitations`: an explicit list.

Gate 1A validates the rule contract but does not implement the semantic rule
evaluator. Predicate meaning, evidence vocabulary, reverse-evidence mappings,
and threshold values remain project-owned and cannot be inferred from fixture
examples.

Every supported state must have at least one rule. The `states` list declares
the wire vocabulary and does not control evaluation. Rule priority is the only
allowed evaluation order; duplicate priorities are rejected. A low-state rule
does not override the invariant requiring explicit reverse evidence.

## 6. Resolution result contract

A later resolver must emit one result per evaluated Primitive with:

- `primitive_id`;
- `state`;
- `bazi_salience`;
- `astrology_salience`;
- `evidence_stability`;
- `evidence_refs`;
- `resolution_rule_ref`;
- `limitations`.

Trait salience remains isolated by source system. Cross-System Relation and
Synthesis Priority are not Primitive State fields and remain later Phase D
contracts.

## 7. Error behavior

The first failed validation wins:

1. missing asset or required field: `CONFIG_GAP`;
2. malformed YAML: `CONFIG_PARSE_ERROR`;
3. wrong container or scalar type: `CONFIG_TYPE_ERROR`;
4. unsupported schema or cross-file version: `CONFIG_VERSION_MISMATCH`;
5. unknown field, invalid value, empty production collection, ambiguous alias,
   duplicate ID, duplicate rule, or duplicate priority: `CONFIG_VALUE_ERROR`,
   with the most specific field path available.

An absent production asset is not replaced by the documentation template. The
Skill stops at `SEMANTIC_CONFIG_CHECKED` and reports the missing asset.

## 8. Skill data flow

After `FACTS_VALIDATED`:

1. check that both Primitive foundation assets exist;
2. load the ontology and verify its structure and uniqueness;
3. load the state policy and verify fixed invariants;
4. verify ontology and score-model version references;
5. verify rule coverage and deterministic priority;
6. verify every Primitive reference required by later semantic assets against
   the accepted ontology;
7. keep `SEMANTIC_CONFIG_CHECKED` closed until all remaining Gate 1 assets also
   pass.

This phase provides only steps 1 through 5. Mapping, relation-graph activation,
dimension coverage, narrative rules, and the final combined semantic gate remain
future work.

## 9. Non-production template

The template is Markdown containing annotated YAML with unmistakable placeholder
tokens. It is stored outside the production `configs/` directory and states that
it must not be loaded as runtime configuration. Synthetic names, definitions,
thresholds, and rules in tests are fixtures only and have no product meaning.

## 10. Testing strategy

Implementation follows RED-GREEN-REFACTOR.

Tests cover:

- missing files and required fields;
- YAML parse and type failures;
- exact schema versions and cross-file version matching;
- Primitive ID format and uniqueness;
- name and alias ambiguity;
- high/low expression distinction;
- exact state set and rule coverage;
- fixed no-evidence, low-state, salience, validation, and tension invariants;
- duplicate rule IDs and priorities;
- preservation of current `load_runtime_config()` behavior;
- absence of production placeholder assets;
- Skill package links, routing, and prohibition language;
- full regression, official Skill validation, package verification, and frozen
  baseline checks.

## 11. Non-goals

Gate 1A does not:

- define any real Primitive name, meaning, alias, or limitation;
- choose salience, mixed-state, reverse-evidence, or stability thresholds;
- create Bazi or astrology Mapping Registry values;
- activate the Primitive Relation Graph;
- implement the state evaluator, Evidence Graph, signatures, Dynamic selection,
  dimensions, or Narrative;
- complete deterministic lookup tables or the True North Node policy;
- make Gate 1 or Phase D complete.

## 12. Acceptance criteria

Gate 1A is complete when:

- the two contracts are unambiguous and linked from the Skill;
- the non-production template cannot be mistaken for runtime configuration;
- the standalone development loader accepts a complete synthetic bundle and
  rejects every specified invalid class deterministically;
- existing runtime configuration loading and frozen assets remain unchanged;
- no real product semantic value is introduced;
- production continues to report `CONFIG_GAP` until project-approved assets are
  supplied;
- all automated, Skill, package, and scope checks pass.
