# Task 2 report

## RED

Command:

```text
python3 -m pytest tests/test_interpretive_rules.py -q
```

Observed result before the fix: 1 failed, 6 passed.  The missing-time case
expected `BAZI-TEN-GOD-EXPRESSION`, but it was absent because
`_elemental_balance_paths` required an hour pillar.

## GREEN

`_elemental_balance_paths` now references the stable year, month, and day
pillars, and appends the hour pillar only when it exists.  This keeps
time-sensitive house placement signals unavailable in `stable_only` mode while
preserving qualified Bazi and astrology facts that do not depend on birth time.

Focused verification:

```text
python3 -m pytest tests/test_interpretive_rules.py -q
7 passed in 1.13s
```

All test files were also re-run in bounded batches after the single full-suite
output truncated.  Combined result: `797 passed`.

The extractor audit found that emitted references are concrete paths on the
qualified fact model (for example, `bazi.ten_gods[0].ten_god` and
`astrology.aspects[0].aspect_type`).  A rule is emitted only if every declared
fact category has available matching facts; there is no fallback that emits a
rule from unrelated values.

## Predicate review fix — RED

The prior extractor checked only for non-empty fact categories.  Added a
same-structure/different-values contrast case: the input still contained Ten
God, relation, hidden-stem, placement, aspect, and dignity facts, but used
`wealth`, `clash`, `甲`, Sun in Taurus, an opposition, and detriment.

Before the predicate fix:

```text
python3 -m pytest tests/test_interpretive_rules.py -q
2 failed, 6 passed
```

The failures proved both defects: all four rules emitted for non-matching
values, and the Ten-God signal included `bazi.ten_gods[1].ten_god` even though
that fact was `wealth`, not the rule's selected `resource` value.

## Predicate review fix — GREEN

The audited asset now declares `predicate_version:
audited-interpretive-value-predicates-v1` and every rule has validated,
explicit `value_predicates`.  The small supported vocabulary is fixed to the
actual rule facts: selected Ten-God, relation and hidden-stem values; selected
year/month/day pillars; named planet/sign and house; and named aspect/dignity.
No generic expression evaluator was added.  Extraction returns only concrete
paths whose facts satisfy all of a rule's predicates.

Focused verification:

```text
python3 -m pytest tests/test_interpretive_rules.py -q
8 passed in 1.05s
```

A bounded suite shard also passed after the model and asset contract change:

```text
python3 -m pytest -q <tests 1-10>
100 passed in 13.71s
```

The full-suite runner repeatedly stopped emitting before completion at about
20 seconds in this execution channel; the earlier pre-review full suite was
fully green (`797 passed`), while the post-review focused tests and bounded
suite shard above are green.

## Re-review vocabulary, symmetry, and domain fix — RED

Added tests for project-valid Ten-God values, reverse-order aspect facts, and
unsupported predicate values.  Before the fix:

```text
python3 -m pytest tests/test_interpretive_rules.py -q
4 failed, 6 passed
```

The project-valid `正印` fact did not match the asset's invalid category label
`resource`; the reverse `Moon`/`Sun` conjunction did not match the ordered
predicate; and the loader accepted an impossible `resource` predicate value.

## Re-review vocabulary, symmetry, and domain fix — GREEN

The Ten-God predicate now uses real `TenGodFact.ten_god` values (`正印`,
`偏印`), while the contrast fixture uses `正财`.  Aspect matching accepts either
body ordering and retains the source aspect path.  Loader validation now uses
a deliberately small fixed domain per supported fact reference, including
pillars, houses, bodies, signs, aspects, dignities, ten-gods, relation terms,
and hidden stems; out-of-domain values fail with
`INTERPRETIVE_RULE_INVALID_PREDICATE_VALUE`.

```text
python3 -m pytest tests/test_interpretive_rules.py -q
10 passed in 1.33s
```
