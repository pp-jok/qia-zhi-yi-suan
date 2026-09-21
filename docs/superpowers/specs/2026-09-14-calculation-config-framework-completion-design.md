# Calculation Configuration Framework Completion Design

**Date:** 2026-09-14  
**Status:** Approved by explicit continuous-execution authorization  
**Scope:** All remaining configuration contracts and validators that do not require invented domain values

## Outcome

Complete the structural path to `CALCULATION_CONFIG_CHECKED` with four
project-owned candidate assets, an ordered aggregate loader, stable raw-byte
fingerprinting, and a development CLI. No production values are created.

## Assets and order

After the four frozen runtime files and accepted
`canonical_fact_vocabulary_v1.yaml`, require:

1. `bazi_deterministic_tables_v1.yaml` — hidden-stem, Ten-God, and supported
   Bazi-relation tables, referencing vocabulary canonical IDs;
2. `astrology_dignity_table_v1.yaml` — dignity rows referencing body, sign,
   and dignity canonical IDs;
3. `astrology_node_policy_v1.yaml` — canonical True North Node fact identifier,
   output inclusion, phase, aspect, dignity, and time-sensitivity decisions;
4. `fact_comparison_policy_v1.yaml` — confirmation triggers, affected logical
   categories, boundary margins, canonical decimal precision, numerical
   tolerances, and representation-equivalence rules.

Each root has an exact schema/version/methodology/vocabulary reference and no
unknown fields. Declarative rule rows use project-owned IDs and explicit
conditions/results; loaders validate structure, uniqueness, references, types,
ranges, and cross-file versions without interpreting domain meaning.

Separate assets are preferred to a universal YAML because ownership, failure
paths, and version changes remain local. Embedding values in Skill prose is
rejected because it would be unversioned. Implementing inference engines before
approved assets is rejected because behavior could only be guessed.

## Aggregate and CLI

`load_calculation_contract_bundle(config_dir, runtime_config)` loads vocabulary
then the four assets in the order above and returns immutable models.

`validate-calculation-contracts CANDIDATE_DIR --runtime-config-dir BASELINE`
performs two complete `validate -> fingerprint` passes. It reports versions,
row counts, nine raw-file SHA-256 values, and one canonical bundle SHA-256 only
when both fingerprints match. Existing `ConfigError` codes and empty-stdout
failure behavior are preserved.

## Skill boundary

The Skill loads only the contracts needed at `CALCULATION_CONFIG_CHECKED` and
continues to invoke external deterministic capabilities itself. Templates are
authoring aids and never production configuration. A structurally accepted
bundle still needs project-owner review and approval of its exact fingerprint.

Until real approved calculation assets and the previously listed semantic
assets exist, `CALCULATION_CONFIG_CHECKED`, Gate 1, Phase D, Phase E, and final
release remain closed. No code may replace those assets with conventions or
model knowledge.

## Verification

Every loader receives happy-path immutability, exact-key, missing/parse/type,
version, duplicate, range, and reference tests. The aggregate receives ordered
failure and stable-snapshot tests. Skill tests forbid production placeholders
and executable dependencies. Final verification includes the full suite,
official Skill validation, frozen-byte checks, inventory scans, and isolated
Wheel build/install/run.
