# Task 1 Report: Rule-family contract and knowledge-asset replacement

## Status

DONE_WITH_CONCERNS

Implementation commit: `849f489bf1450d2c0f55bf8d2ae34af21001c768`

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
