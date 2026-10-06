# Task 4 report

## RED

Added `tests/test_interpretive_report.py` before production code and ran:

```text
python3 -m pytest tests/test_interpretive_report.py -q
```

Observed the expected feature failure during collection:

```text
ModuleNotFoundError: No module named 'destiny_personality.interpretive_codec'
```

The tests established the report contract before implementation: eight named
standard topics, a shorter four-section concise report, section-level signal
IDs and limitations, boundary language, grouped audit provenance,
deterministic plain-data encoding, and explicit rejection of unsupported input.

## Implementation

Added immutable report, section, and audit-metadata models in
`interpretive_report.py`. `build_interpretive_report` accepts only an
`InterpretiveCoreProfile`; neither report module imports deterministic facts,
qualification objects, chart types, or strict/candidate/release paths.

The standard report always renders these eight Chinese product topics in a
stable order:

1. 核心底色
2. 思考与学习
3. 表达与创造
4. 关系与边界
5. 工作与驱动
6. 压力与能量
7. 成长张力
8. 综合观察

Up to four unmatched, evidence-bearing profile topics are appended as
supplementary observations, keeping standard output within 8-12 sections.
Sparse profiles reuse only an available, traceable conclusion to complete the
eight-topic reading frame; they never manufacture a new factual conclusion.

The concise report deterministically folds the same profile conclusions into
four sections. Every section exposes the union of supporting and
countervailing signal IDs and a brief limitation derived from conclusion and
profile limitations. A report cannot be rendered when no conclusion has a
signal ID.

Report-level audit metadata preserves all profile audit references and groups
the rule-bundle, deterministic-fact, and fact-qualification references for
direct inspection. The boundary statement identifies the output as a
traditional interpretive aid rather than an empirical personality measure,
medical or psychological diagnosis, or decision substitute.

Added `encode_interpretive_report` to produce deterministic JSON-compatible
plain dictionaries and lists without losing section or audit traceability.

## GREEN and verification

Focused Task 4 verification:

```text
python3 -m pytest tests/test_interpretive_report.py -q
6 passed in 0.09s
```

Interpretive-path regression verification:

```text
python3 -m pytest tests/test_interpretive_report.py tests/test_interpretive_profile.py tests/test_interpretive_rules.py -q
21 passed in 0.86s
```

Full regression suite:

```text
python3 -m pytest -q
811 passed in 51.93s
```

Additional checks completed successfully:

```text
python3 -m compileall -q src/destiny_personality/interpretive_report.py src/destiny_personality/interpretive_codec.py tests/test_interpretive_report.py
git diff --check
```

A source scan of the two production modules and their test found no imports or
references to raw deterministic facts, `QualifiedFacts`, chart facts, or
strict/candidate/release paths.
