# Gate 1C Dimension Coverage Policy Contract Design

**Date:** 2026-09-14  
**Status:** Approved by the user's standing authorization to continue  
**Scope:** Twelve-dimension definitions, coverage threshold, and partial-portrait policy contract only

## Purpose and boundary

Gate 1C defines one versioned asset, `dimension_coverage_policy_v1.yaml`, that
keeps twelve project-owned portrait dimensions and their coverage policy in one
atomic unit. It does not define real dimension names, meanings, Primitive
membership, metrics, or thresholds. No production asset is created and missing
real values remain `CONFIG_GAP`.

One combined asset is preferred over separate definition and threshold files
because partial eligibility depends on the exact dimension set being measured.
Separate files would permit incompatible versions to pass independently.

## Two-layer architecture

The distributable Skill receives a structural contract and visibly
non-production template. The development package receives immutable models and:

```python
load_dimension_coverage_policy(
    config_dir: Path,
    primitive_foundation: PrimitiveFoundationConfig,
    runtime_config: RuntimeConfig,
) -> DimensionCoveragePolicyConfig
```

The loader consumes accepted dependencies and remains separate from existing
loaders. The Skill does not depend on Python to execute.

## Root contract

The root contains exactly:

- `schema_version`: `dimension-coverage-policy-v1`;
- `policy_version`: non-empty immutable version;
- `ontology_version`: accepted ontology version;
- `score_model_version`: accepted score model version;
- `dimension_count`: integer `12`;
- `dimensions`: exactly twelve records;
- `coverage_policy`: one policy record.

## Dimension records

Each dimension contains exactly:

- `dimension_id`: unique `D##` identifier;
- `canonical_name`: non-empty project-owned name, globally unique after trim
  and case-fold;
- `definition`: non-empty project-owned meaning;
- `primitive_refs`: non-empty unique list of accepted ontology IDs;
- `limitations`: explicit list of non-empty strings, which may be empty.

The validator does not infer dimensions from Primitive names or require every
Primitive to belong to a dimension.

## Coverage policy

The policy contains exactly:

- `threshold_status`: exact value `provisional`;
- `coverage_metric`: non-empty project-owned metric identifier;
- `complete_threshold`: finite number in `[0, 1]`;
- `partial_threshold`: finite number in `[0, complete_threshold)`;
- `partial_portrait_allowed`: exact value `true`;
- `partial_status`: exact value `partial`;
- `warning_code`: exact value `coverage_warning`;
- `missing_config_code`: exact value `CONFIG_GAP`;
- `dimension_requirements`: exactly one record per declared dimension.

Each requirement contains exactly `dimension_id` and
`minimum_supported_primitives`. The minimum is a positive integer no larger
than that dimension's number of Primitive references. Requirement order is
normalized to declared dimension order.

The thresholds are product-owned even though their allowed range and ordering
are structural. `provisional` means calibration is unfinished, not that an
agent may choose or change a value at runtime.

## Runtime rule

`coverage_warning` is legal only after all semantic assets pass
`SEMANTIC_CONFIG_CHECKED` and valid case facts and mappings exist. Missing,
malformed, or cross-reference-invalid configuration is `CONFIG_GAP`, never a
partial portrait. Gate 1C validates configuration only and does not calculate
case coverage.

## Error behavior

Use the existing deterministic mapping: missing asset/field `CONFIG_GAP`;
malformed YAML `CONFIG_PARSE_ERROR`; wrong type `CONFIG_TYPE_ERROR`; schema or
cross-file version mismatch `CONFIG_VERSION_MISMATCH`; invalid, duplicate,
unknown, or unresolved value `CONFIG_VALUE_ERROR`. Report the most specific
zero-based dot-separated field path and stop at the first failure.

## Non-goals

Gate 1C does not create real dimension semantics, select Primitive membership,
choose coverage metrics or thresholds, calculate coverage, authorize partial
before the semantic gate, define Narrative Rules, or complete Gate 1/Phase D/E.

## Acceptance

The contract, template, immutable models, reference loader, Skill routing, and
tests must agree; synthetic fixtures use only `TEST_ONLY_` values; no production
placeholder is added; existing configs remain frozen; all tests, Skill checks,
and package verification pass.
