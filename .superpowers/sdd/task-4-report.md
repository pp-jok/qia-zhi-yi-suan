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

## Review remediation: evidence fidelity, Chinese rendering, and provenance

This section supersedes the original sparse-profile behavior described above.
Review found that round-robin fallback relabelled a sparse conclusion as
unrelated product topics and copied packaged English rule prose into a nominally
Chinese report. It also found missing audited-profile validation and a mutable
audit-reference alias.

Added the review regression tests before changing production code. The first
focused RED run produced:

```text
python3 -m pytest tests/test_interpretive_report.py -q
8 failed, 5 passed in 0.44s
```

The failures directly covered the four review findings: arbitrary topic
fallback, English rule text exposure, four incomplete-provenance cases, and
post-build mutation of a caller-owned audit-reference list. A second RED cycle
for malformed provenance (`None` and a non-string reference) produced:

```text
2 failed, 13 passed in 0.36s
```

The final implementation removes both standard and concise round-robin
fallbacks. Conclusions are grouped only into controlled topics they actually
support. A standard report has 8-12 product sections only when distinct
evidence supports that depth. Sparse profiles instead contain their supported
sections plus a Chinese `证据覆盖说明` section; uncovered themes are not
inferred, relabelled, or filled to reach a target count. The concise report
uses the same evidence-preserving grouping.

The four packaged rule signals now have controlled Chinese topic, body, and
limitation mappings. Known English topic/direction/interpretation/limitation
fields are not copied into user-visible output. Unknown English-only profile
text receives a conservative Chinese no-expansion statement rather than a
translation-like invented claim.

The report boundary now requires exactly `audited_interpretive` mode and a
nonempty, string-only audit-reference collection containing all three required
prefixes: `interpretive-rules:`, `deterministic-facts:`, and
`fact-qualification:`. Invalid and malformed profiles fail with the stable
`AUDITED_INTERPRETIVE_PROFILE_REQUIRED` error. Audit references are converted
to a tuple before validation and report construction, preventing later caller
mutation from changing report metadata.

Final focused verification:

```text
python3 -m pytest tests/test_interpretive_report.py -q
15 passed in 0.26s
```

Final interpretive-path regression verification:

```text
python3 -m pytest tests/test_interpretive_report.py tests/test_interpretive_profile.py tests/test_interpretive_rules.py -q
30 passed in 1.05s
```

Final full regression suite:

```text
python3 -m pytest -q
820 passed in 49.49s
```

`compileall`, `git diff --check`, and a source scan again confirmed that no raw
facts, `QualifiedFacts`, chart facts, or strict/candidate/release dependency was
introduced.

## Final review remediation: sparse standard-report depth

This section supersedes the preceding statement that a sparse standard report
may contain fewer than eight sections. Final review required standard output to
always contain 8-12 sections while preserving the prohibition on relabelling a
sparse conclusion as unrelated personality topics.

Updated the one-conclusion regression before production code. It now requires:

- 8-12 standard sections and a strictly shorter concise report;
- exactly one genuine personality-topic section carrying the conclusion;
- all remaining standard sections to be explicitly labelled evidence or method
  boundaries and to say they do not make personality-trait judgments;
- the conclusion body to appear exactly once;
- every section to carry only the actual known signal ID.

The focused RED run showed the expected depth failure:

```text
python3 -m pytest tests/test_interpretive_report.py -q
1 failed, 14 passed in 0.56s
```

Standard composition now retains all genuine evidence-backed topic sections.
When fewer than eight such sections exist, it fills only the remaining slots
with a stable sequence of non-personality audit sections:

1. 证据范围
2. 八字观察范围
3. 占星观察范围
4. 跨体系覆盖与张力
5. 置信度校准
6. 时间范围与局限
7. 可追溯性与使用边界

These sections describe only evidence availability, system coverage,
counter-signal presence, confidence labels, time limitations, traceability,
and use boundaries. They never repeat the conclusion body or introduce a new
trait claim. Each retains the profile's actual signal IDs as its audit anchor.
Rich profiles keep their existing evidence-backed 8-12-section behavior.

The concise composition remains evidence-preserving and strictly shorter. For
the single-conclusion regression it contains the genuine grouped conclusion
and one coverage boundary section, compared with eight standard sections.

Final verification:

```text
python3 -m pytest tests/test_interpretive_report.py -q
15 passed in 0.28s

python3 -m pytest tests/test_interpretive_report.py tests/test_interpretive_profile.py tests/test_interpretive_rules.py -q
30 passed in 0.97s

python3 -m pytest -q
820 passed in 48.44s
```

`compileall`, `git diff --check`, and the forbidden-dependency source scan also
passed. No raw facts, strict, candidate, or release import was introduced.
