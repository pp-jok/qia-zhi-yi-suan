# Gate 1B Context-Aware Mapping Registry Contracts Design

**Date:** 2026-09-13  
**Status:** Approved by the user's standing authorization to continue  
**Scope:** Bazi and astrology Context-Aware Mapping Registry contracts only

## 1. Purpose

Gate 1B defines how deterministic Bazi and astrology facts may produce
Primitive evidence candidates. It supplies contracts, cross-reference checks,
and a development reference validator without supplying or inventing any real
mapping rule, condition, effect, threshold, or Primitive meaning.

The project currently contains opaque `P###` references but no approved
Primitive definitions. Gate 1B therefore must not create production mapping
assets or claim that `SEMANTIC_CONFIG_CHECKED` passes. Missing real registries
remain `CONFIG_GAP`.

## 2. Considered approaches

### 2.1 Separate schemas and loaders per source system

This maximizes local explicitness but duplicates validation and invites the two
registries to drift. It is rejected because their structural contract is the
same and source-specific business values remain external to the validator.

### 2.2 One mixed registry containing both systems

This is compact but weakens the required separation between Bazi and astrology
evidence and makes accidental cross-system interaction easier. It is rejected.

### 2.3 Shared contract, separate assets, one bundle loader

This is selected. A single structural contract governs two required files while
each registry has an exact source identity and methodology version. The loader
returns separate immutable Bazi and astrology registries and validates only
cross-references that are already frozen by accepted project assets.

## 3. Architectural boundary

### 3.1 Distributable Skill layer

The Skill contains:

- one shared Context-Aware Mapping Registry contract;
- one non-production authoring template showing both file shapes;
- loading order, cross-reference checks, error mapping, and prohibitions;
- an explicit rule that following agents call capabilities themselves and may
  not invent mapping semantics.

The Skill contains no executable validator, third-party calculation software,
or usable production registry.

### 3.2 Development reference layer

The Python package adds immutable mapping models and:

```python
load_mapping_registries(
    config_dir: Path,
    primitive_foundation: PrimitiveFoundationConfig,
    runtime_config: RuntimeConfig,
) -> MappingRegistryBundle
```

The caller supplies already accepted Primitive foundation and runtime config
objects. The loader does not reload them or weaken their gates. It is separate
from `load_runtime_config()` and `load_primitive_foundation()` so the existing
failure order and production baseline remain unchanged.

## 4. Asset names and loading order

Future production assets use these exact filenames:

1. `bazi_mapping_registry_v1.yaml`;
2. `astrology_mapping_registry_v1.yaml`.

The bundle loader validates Bazi first, astrology second, and bundle-wide
uniqueness last. A missing earlier asset wins over failures in a later asset.
Neither file is created under a production config directory in Gate 1B.

## 5. Registry root contract

Each file contains exactly:

- `schema_version`: `context-aware-mapping-registry-v1`;
- `registry_version`: non-empty immutable version identifier;
- `source_system`: exact value dictated by the filename, `bazi` or
  `astrology`;
- `methodology_version`: must match the corresponding accepted runtime
  methodology;
- `fact_schema_version`: `deterministic-facts-v1`;
- `score_model_version`: must match the accepted score model, currently `2.2`;
- `ontology_version`: must match the accepted Primitive Ontology;
- `rules`: non-empty list;
- `interactions`: explicit list, which may be empty.

Unknown fields are invalid. Registry versions need not match each other because
the two systems are independently maintained.

## 6. Mapping rule contract

Each rule contains exactly:

- `rule_id`: unique non-empty identifier;
- `priority`: unique non-negative integer within its registry;
- `primary_condition`: non-empty declarative mapping;
- `context`: non-empty declarative mapping;
- `outputs`: non-empty list of Primitive evidence outputs;
- `modifiers`: explicit list, which may be empty;
- `limitations`: explicit list of non-empty strings, which may be empty.

Requiring a non-empty `context` prevents an unconditional single-signal mapping
from passing the contract. Rules are returned in ascending priority order.
Priorities do not cross source-system boundaries.

Gate 1B treats `primary_condition` and `context` as project-owned declarative
data. It validates deterministic YAML-compatible structure but does not execute,
normalize, reinterpret, or complete the predicates.

## 7. Output and modifier contracts

Each output contains exactly:

- `primitive_id`: a `P###` identifier present in the accepted ontology;
- `direction`: a non-empty project-owned wire value;
- `salience`: an integer within the accepted score model's trait-salience
  bounds;
- `limitations`: an explicit list of non-empty strings, which may be empty.

A rule may reference a Primitive only once. Gate 1B does not freeze the
`direction` vocabulary or convert it into a Primitive state; that requires
approved product semantics and the later evaluator.

Each modifier contains exactly:

- `when`: a non-empty declarative mapping;
- `effects`: a non-empty list of non-empty declarative mappings.

Modifier order is preserved. Effects remain opaque project-owned data.

## 8. Interaction contract

Each interaction contains exactly:

- `interaction_id`: unique non-empty identifier;
- `requires`: at least two distinct rule IDs from the same registry;
- `produces`: a non-empty declarative mapping;
- `limitations`: an explicit list of non-empty strings, which may be empty.

Every required rule must exist in the same registry. Interactions cannot join
Bazi and astrology rules before the Cross-System Synthesizer. Declared
interaction order is preserved and does not imply precedence.

## 9. Declarative value safety

Opaque declarative mappings and lists may contain only:

- string keys;
- mappings and lists;
- strings, booleans, integers, finite floats, and null values.

YAML-specific objects, non-string keys, and non-finite floats are rejected.
Accepted nested collections are recursively frozen into tuples in returned
models so callers cannot mutate an accepted bundle.

## 10. Bundle-wide checks

After both registries pass local validation:

- rule IDs are globally unique across both systems;
- interaction IDs are globally unique across both systems;
- every output Primitive exists in the accepted ontology;
- both ontology references match the same accepted ontology;
- each methodology reference matches its source system;
- both registries retain separate output collections.

The loader does not activate the Primitive Relation Graph, merge evidence,
resolve Primitive state, or calculate synthesis priority.

## 11. Error behavior

The first failed validation wins:

1. missing asset or required field: `CONFIG_GAP`;
2. malformed YAML: `CONFIG_PARSE_ERROR`;
3. wrong container, scalar, mapping-key, or nested declarative type:
   `CONFIG_TYPE_ERROR`;
4. unsupported schema, ontology, methodology, fact-schema, or score-model
   reference: `CONFIG_VERSION_MISMATCH`;
5. unknown field, invalid value, empty required collection, unresolved
   reference, duplicate identifier, or duplicate priority:
   `CONFIG_VALUE_ERROR`.

Errors record the exact filename and most specific zero-based dot-separated
field path available.

## 12. Skill data flow

After `FACTS_VALIDATED` and accepted Primitive foundation assets:

1. require the Bazi registry;
2. validate its source, methodology, fact-schema, and ontology versions;
3. validate rules, outputs, modifiers, and interactions;
4. repeat for the astrology registry;
5. validate bundle-wide identifier uniqueness;
6. keep Bazi and astrology candidate evidence isolated;
7. keep `SEMANTIC_CONFIG_CHECKED` closed until every remaining Gate 1 asset
   also passes.

The authoring template cannot satisfy any step.

## 13. Testing strategy

Implementation follows RED-GREEN-REFACTOR. Synthetic fixtures use only
`TEST_ONLY_` meanings and identifiers and cover:

- missing files, required fields, parse failures, and wrong types;
- exact schema, source, methodology, fact-schema, and ontology versions;
- non-empty context and rule collections;
- duplicate rule IDs and priorities;
- output Primitive resolution and score bounds;
- modifier structure and recursive declarative-value safety;
- interaction cardinality, uniqueness, and same-registry references;
- cross-registry identifier collisions;
- deterministic rule ordering and immutable nested values;
- preservation of current runtime and Primitive loaders;
- absence of production registry placeholders;
- Skill links, routing, packaging, and forbidden bundled runtime checks.

## 14. Non-goals

Gate 1B does not:

- define real Primitive values;
- create real Bazi or astrology mapping rules;
- freeze direction vocabulary, condition operators, feature paths, modifier
  effects, thresholds, or interaction meanings;
- implement a mapping evaluator or Primitive state resolver;
- merge Bazi and astrology evidence;
- activate the relation graph, build an Evidence Graph, extract signatures,
  select Dynamics, define dimensions, or render narrative;
- complete deterministic lookup tables;
- make Gate 1 or Phase D complete.

## 15. Acceptance criteria

Gate 1B is complete when:

- the shared Skill contract unambiguously governs both required assets;
- the template is visibly non-production and cannot satisfy the gate;
- the standalone loader accepts a complete synthetic bundle and rejects every
  specified invalid class deterministically;
- accepted objects are immutable and source-system outputs remain separate;
- existing loaders, production configs, and frozen source assets remain
  unchanged;
- no real product mapping value is introduced;
- missing production registries continue to produce `CONFIG_GAP`;
- all automated, Skill, package, and scope checks pass.
