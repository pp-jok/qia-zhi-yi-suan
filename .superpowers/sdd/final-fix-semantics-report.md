# v0.6.0 Final Semantic P1 Fix Report

## Scope

This change closes the three final-review semantic P1 findings on the
qualification-bound audited interpretive route:

1. standard reports no longer discard supported topics after the 12th group;
2. astrology element/modality matches now change reader semantics beyond the
   interpolated `命中依据` label;
3. the official `cross-system-agreement` fixture now produces a genuine,
   provenance-backed synthesis relationship.

The strict Core Profile, candidate assets, calculation facts, and qualification
fixtures are unchanged.

## TDD evidence

The regression tests were written before production changes and run with:

```text
python3 -m pytest -q \
  tests/test_interpretive_report.py::test_standard_report_consolidates_supported_topics_beyond_twelve \
  tests/test_interpretive_rules.py::test_astrology_quality_values_change_reader_semantics_beyond_evidence_labels \
  tests/test_interpretive_product_quality.py::test_product_matrix_contains_the_five_required_reader_semantics
```

RED result: `3 failed` for the expected reasons:

- `EXTRA-13` was absent from the rendered standard report;
- fire/cardinal and earth/fixed signals had identical semantics after removing
  `命中依据`;
- `cross-system-agreement` had no `validation` relationship.

After the minimum implementation, the same three regressions plus the bounded
registry and reusable-family guard reported `5 passed`.

## Standard report preservation

The standard renderer still emits at most 12 sections. When more than 12 topic
groups are supported, it renders the first 11 groups normally and consolidates
all remaining conclusions into section 12, `其他有据主题（合并展示）`.

The consolidated section is built by the normal section renderer, so it keeps:

- every conclusion's reader text;
- every supporting and countervailing signal ID;
- exact ordered signal provenance;
- conclusion, rule, and profile limitations.

The v0.6.0 product matrix now asserts that every extracted signal appears in
the standard report. This covers real fixtures such as `practical-builder`,
whose supported evidence previously exceeded the visible section cap.

## Reusable value-specific astrology semantics

The audited interpretive bundle is now
`audited-interpretive-rules-v3` / `audited-interpretive-value-predicates-v3`.
Its validated `value_narratives` registry covers exactly:

- four sign elements: fire, earth, air, and water;
- three sign modalities: cardinal, fixed, and mutable.

Each entry supplies bounded interpretation, mechanism, likely expression, and
contexts; element entries also supply the synthesis direction. Extraction
selects these entries only from exact matched values and composes them with the
planet family's existing body-specific narrative. The registry is shared by
all charts and core-planet families. It contains no fixture name, fingerprint,
or exact-chart conjunction.

The existing structural guard still rejects single-sign and cross-family
demo-specific rule configurations. Tests also normalize away `命中依据` and
require different matched qualities to retain different reader semantics.

## Genuine agreement fixture

`BAZI-TEN-GOD-OUTPUT` now expresses its existing Food God / Hurting Officer
output evidence on the exact `style of expression` topic with the `outward`
direction. In the official agreement facts, this independently matches the
fire-element Sun rule, whose selected direction is also `outward`.

The synthesis engine therefore derives `validation` through its existing
same-topic, same-direction policy. The product test requires both exact signal
IDs, both source systems, and non-empty qualified fact paths. No validation
flag or chart-specific exception was added, and the tension fixture continues
to derive a real `tension` between reflective Seal evidence and outward solar
evidence.

## Generated artifacts and documentation

The production CLI regenerated all affected checked-in reports:

- three `docs/demos/v0.5.0` standard reports;
- five `docs/demos/v0.6.0` standard reports.

README, Skill instructions, changelog, rule coverage, differentiation review,
product readiness, and v0.6.0 release notes now describe overflow
consolidation, v3 value-specific semantics, and the evidence-backed agreement.

## Verification

- Focused interpretive/report/rule/synthesis/product/CLI suite:
  `122 passed in 24.14s`.
- Full suite: `924 passed in 88.16s`.
- Package verifier: built and installed the 0.6.0 wheel, exercised installed
  strict/candidate smoke checks, and ended with `package verification passed`.
- `git diff --check`: clean.

Pre-existing untracked SDD briefs, review diffs, and progress files remain
untouched and are excluded from this change.
