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
