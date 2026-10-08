# Task 1 Report: Rule-family contract and knowledge-asset replacement

## Status

DONE

Implementation commit: `849f489bf1450d2c0f55bf8d2ae34af21001c768`

Review-fix commit: `f747162fa4f2b99d8cca1397c2d8cd22c2577902`

## Changed files

- `src/destiny_personality/interpretive_models.py`
  - Added immutable v2 selector metadata for pillar positions, source kinds,
    relation participants, and occurrence thresholds.
  - Added rule-family narrative fields (`family`, `mechanism`,
    `likely_expression`, `contexts`, `modifiers`) and the explicit
    `requires_exact_demo_chart` guard.
  - Added computed bundle coverage sets for Ten Gods and planets.
- `src/destiny_personality/interpretive_rules.py`
  - Bumped the bundle and predicate contracts to v2.
  - Added closed selector domains and fail-closed validation for every
    declared selector.
  - Added deterministic sign-element and sign-modality resolution.
  - Added position/source/repetition and branch-participant matching while
    retaining the qualified-facts gate.
  - Preserved stable-only behavior by suppressing house predicates only;
    sign, aspect, and dignity facts remain usable when present and qualified.
- `src/destiny_personality/interpretive_assets/v1/interpretive_rules_v1.yaml`
  - Replaced the four demo-shaped entries with a local v2 rule-family bundle.
  - Covers all ten Ten-God identities and Sun, Moon, Mercury, Venus, Mars,
    Jupiter, and Saturn.
  - Includes reusable Ten-God, repetition, branch relation, planet sign
    quality, house, major-aspect, and dignity families with Chinese reader
    fields and traditional-source/limitation metadata.
- `tests/test_interpretive_rules.py`
  - Added the required v0.6 coverage and anti-demo contract tests.
  - Added bounded-selector, Chinese-field, repetition, reverse-aspect,
    missing-time, and invalid-selector coverage.
  - Updated v1 demo-exact assertions to test reusable family behavior.

## TDD evidence

### Required RED

Command:

```text
python3 -m pytest tests/test_interpretive_rules.py -q
```

Initial output before production changes:

```text
.FF.......... [100%]
2 failed, 11 passed in 1.79s
```

The failures were the intended missing-contract failures:

- `InterpretiveRuleBundle` had no `covered_ten_gods` attribute.
- `InterpretiveSignal` had no `requires_exact_demo_chart` attribute.

After adding the rest of the v2 behavior tests, the still-unmodified
production implementation produced:

```text
FFFF.......... [100%]
4 failed, 10 passed in 1.56s
```

This additionally proved that the old bundle was still v1 and had no sign
element/modality selector families.

### Repetition bug RED

Command:

```text
python3 -m pytest tests/test_interpretive_rules.py::test_ten_god_repetition_requires_the_same_identity -q
```

Output before the correction:

```text
F [100%]
1 failed in 0.77s
```

The first implementation counted two different Ten-God identities as a
repetition. The resolver was corrected to apply the threshold per identity.

### Participant-selector RED

Command:

```text
python3 -m pytest tests/test_interpretive_rules.py::test_v060_rule_families_expose_bounded_selectors_and_chinese_narrative_fields -q
```

Output before adding the participant contract:

```text
F [100%]
1 failed in 0.51s
```

The failure demonstrated that branch-relation participant selectors were not
yet represented. The final contract validates canonical `*.branch` refs and
matches them against qualified `participant_refs`.

## GREEN and regression evidence

Required focused command:

```text
python3 -m pytest tests/test_interpretive_rules.py -q
```

Final output:

```text
.................... [100%]
20 passed in 7.49s
```

Strict/candidate/primitive regression command:

```text
python3 -m pytest tests/test_cli.py tests/test_skill_package.py \
  tests/test_candidate_contract.py tests/test_candidate_pipeline.py \
  tests/test_candidate_core_assets.py tests/test_candidate_remediation.py \
  tests/test_candidate_holdout.py tests/test_primitive_foundation_config.py \
  tests/test_primitive_presentation_directions.py \
  tests/test_release_primitive_coverage.py -q
```

Output:

```text
125 passed in 10.45s
```

Full-suite command:

```text
python3 -m pytest -q
```

Output:

```text
4 failed, 846 passed in 114.68s
```

All four failures are confined to the old interpretive CLI expectations:

1. One v0.5 assertion expects unknown birth time to remove the stable
   Sun-sign signal. The v0.6 design explicitly removes only house/angle
   claims, so the stable sign-quality signal now remains.
2. Three checked-in v0.5 demo JSON snapshots no longer equal v2 rule output.
   Task 4 owns regenerated v0.6 demos, so they were deliberately not edited
   in this task.

Additional verification:

```text
git diff --check
python3 -m py_compile src/destiny_personality/interpretive_models.py \
  src/destiny_personality/interpretive_rules.py
```

Both completed successfully with no output.

## Design decisions

- Coverage is computed from validated predicates rather than duplicated as
  editable asset metadata. This makes the public coverage contract reflect
  what the evaluator can actually match.
- The predicate language remains deliberately small: closed value domains and
  a few typed selectors, not a general expression DSL.
- Former multi-condition demo rules were split into reusable families so no
  rule requires one complete example chart.
- Ten-God repetition is evaluated per identity, not as a count of unrelated
  Ten-God facts.
- House selectors fail closed in `stable_only`; sign quality, aspects, and
  dignity remain available because they are not inherently house/angle facts.
- `extract_interpretive_signals` still calls `require_qualified_facts` before
  reading any deterministic fact, so no raw or free-form calculation path was
  introduced.

## Self-review

- Only the three specified production files and the specified rule test were
  included in the implementation commit.
- No strict, candidate, primitive, semantic-bridge, calculation, or codec file
  was changed.
- Unknown selectors, unknown selector values, invalid occurrence bounds,
  duplicate IDs, wrong-system refs, confidence labels, and demo-specific rules
  fail closed.
- Sign quality is derived from the already-qualified sign string through a
  fixed local mapping; no external lookup or unqualified inference is used.
- The implementation intentionally does not update report rendering, CLI
  expectations, or demos because those belong to later v0.6 tasks.

## Concerns / follow-up

- Task 3 should update the missing-time CLI assertion so it distinguishes
  stable sign quality from time-sensitive house/angle context.
- Task 4 must regenerate the three checked-in demos through the official CLI
  after the v0.6 report pipeline is complete.
- Until those later tasks land, the focused Task 1 tests and frozen-pipeline
  regressions are green, but the repository-wide suite remains red by the four
  explicitly listed transitional failures.

## Review-fix evidence

The first review found three contract weaknesses: enumerated family values did
not survive extraction, the Sun selector was equivalent to Aries, and the
anti-demo rule trusted an asset-authored boolean. Focused behavior tests were
added before the fixes.

### Review RED

Command:

```text
python3 -m pytest tests/test_interpretive_rules.py -q
```

Output before review fixes:

```text
..F...FF........FF..... [100%]
5 failed, 18 passed in 11.20s
```

The failures proved that:

- the asset still authored `requires_exact_demo_chart`;
- the Sun family did not match Taurus;
- extracted signals did not expose exact matched selector values;
- loader validation accepted a `fire + cardinal` single-sign configuration;
- loader validation accepted a Ten-God plus elemental-balance demo join.

### Review implementation

- Added `InterpretiveMatchedValue` and preserved exact qualified
  `fact_ref`/`fact_path`/`value` matches on every extracted signal. A shared
  Sun family now records `fire/cardinal` for Aries and `earth/fixed` for
  Taurus, while paired Ten-God families retain the actual matched identity.
- Expanded the Sun family to all four elements and all three modalities and
  changed its Chinese narrative to reference the actual matched qualities
  instead of hard-coding fire/cardinal behavior.
- Removed `requires_exact_demo_chart` from the asset schema. The loader now
  derives demo specificity from predicate structure and rejects single-sign
  selectors and cross-family exact-chart joins.

### Review GREEN

Required focused command:

```text
python3 -m pytest tests/test_interpretive_rules.py -q
```

Output:

```text
....................... [100%]
23 passed in 8.15s
```

Frozen-pipeline regression command remained green:

```text
125 passed in 14.32s
```

The broader interpretive regression produced `58 passed, 4 failed`; these are
the same previously documented v0.5 missing-time assertion and three stale
demo snapshots, with no new failure class introduced by the review fix.

## Follow-up repair evidence

The follow-up review found that the v2 loader kept matched values in internal
signal metadata but did not use them in reader-visible rule text. This left
full-domain sign, house, aspect, and dignity rules with identical prose even
when their actual matches differed. It also needed to prove that a discarded
asset boolean could not change the result of structural anti-demo validation.

### Repair RED

Focused command:

```text
python3 -m pytest \
  tests/test_interpretive_rules.py::test_extraction_makes_matched_astrology_values_reader_visible \
  tests/test_interpretive_rules.py::test_asset_boolean_cannot_hide_a_structural_demo_condition -q
```

Output before the repair:

```text
FF [100%]
2 failed in 0.98s
```

The first failure showed that a matching Sun in Aries still produced generic
text without `火象` or `开创`. The second showed that a `false`
`requires_exact_demo_chart` asset field caused the generic invalid-rule path
before the `fire + cardinal` single-sign condition was structurally rejected.

### Repair implementation

- Extraction now appends a reader-facing `命中依据` clause to the rule
  interpretation. It uses the exact qualified matched values and translates
  sign elements, modalities, houses, major aspects, and dignities into the
  reader-visible labels used by the report (for example `火象`/`开创`,
  `第1宫`, `合相`, and `入庙`).
- Rule loading now parses required fields and evaluates structural demo
  specificity before rejecting surplus keys. Therefore an obsolete asset
  boolean cannot mask a single-chart or single-sign selector condition; a
  non-demo surplus key remains invalid after that check.

### Repair GREEN

Required focused command:

```text
python3 -m pytest tests/test_interpretive_rules.py -q
```

Output:

```text
......................... [100%]
25 passed in 5.83s
```

`git diff --check` completed with no output. The repair changes only the Task
1 rule loader, its focused tests, and this evidence report; no strict,
candidate, or primitive code was changed.
