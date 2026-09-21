# Canonical Fact Vocabulary Contract Design

**Date:** 2026-09-14  
**Status:** Approved by standing authorization  
**Scope:** Calculation-configuration vocabulary structure only

## Decision

Add one project-owned candidate asset named
`canonical_fact_vocabulary_v1.yaml`. It centralizes canonical identifiers and
approved aliases used by mechanical normalization. Later Bazi, astrology,
node, boundary, and comparison assets will reference its canonical IDs rather
than defining their own spellings.

Embedding aliases in each future lookup table was rejected because it would
duplicate normalization rules. Adding aliases to the deterministic-facts
schema was rejected because schemas define packet shape, while aliases are
versioned project configuration.

No production vocabulary is created in this milestone.

## Asset structure

The root contains exactly:

- `schema_version`: `canonical-fact-vocabulary-v1`;
- `vocabulary_version`: non-empty immutable project version;
- `methodology_versions`: exactly `bazi` and `astrology`, matching the accepted
  runtime configuration;
- `categories`: exactly the ten required normalization categories.

Required categories are:

```text
bazi_stem
bazi_branch
bazi_ten_god
bazi_relation
astrology_body
astrology_sign
astrology_aspect
astrology_angle
astrology_dignity
astrology_node
```

Each category contains exactly `entries`, a non-empty list. Each entry contains
exactly `canonical_id` and `aliases`. `canonical_id` is a non-empty string;
`aliases` is an explicit list of non-empty strings and may be empty.

Within one category, canonical IDs and aliases are globally unambiguous after
trimming and Unicode-preserving case folding. The same token may occur in
different categories because normalization always carries its field category.
List order is preserved and returned models are immutable.

The `astrology_node` category supplies only canonical naming. It does not
decide True North Node output shape, aspect participation, phase, dignity, or
weight; those remain separate `CONFIG_GAP` items.

## API and error contract

The development reference API is:

```python
load_canonical_fact_vocabulary(
    config_dir: Path,
    runtime_config: RuntimeConfig,
) -> CanonicalFactVocabularyConfig
```

Error mapping follows existing configuration loaders:

| Failure | Error code |
|---|---|
| Missing file or required field | `CONFIG_GAP` |
| Malformed or unreadable YAML | `CONFIG_PARSE_ERROR` |
| Wrong mapping, list, key, or scalar type | `CONFIG_TYPE_ERROR` |
| Wrong schema or methodology version | `CONFIG_VERSION_MISMATCH` |
| Unknown field/category, empty value/list, or ambiguous token | `CONFIG_VALUE_ERROR` |

Errors identify `canonical_fact_vocabulary_v1.yaml` and the most specific
dot-separated field path.

## Skill and release boundary

Add a Skill schema reference and a documentation-only template. Route the
asset inside `CALCULATION_CONFIG_CHECKED`, before all future deterministic
lookup tables and node/comparison policies. Examples and placeholders never
satisfy the gate. Agents may normalize only aliases present in an accepted
vocabulary; absence is not permission to guess.

The contract does not complete calculation configuration, Gate 1, or any
reasoning phase. The Skill remains an agent-executed workflow with no Python or
fixed tool dependency.

