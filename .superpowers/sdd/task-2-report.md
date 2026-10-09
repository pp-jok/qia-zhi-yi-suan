# Task 2 report

## TDD evidence

Added `tests/test_interpretive_system_profiles.py` and
`tests/test_interpretive_synthesis.py` before production changes, then ran:

```text
python3 -m pytest \
  tests/test_interpretive_system_profiles.py \
  tests/test_interpretive_synthesis.py -q
```

RED failed during collection for the intended missing behavior:

```text
ModuleNotFoundError: No module named
'destiny_personality.interpretive_system_profiles'
ImportError: cannot import name 'encode_narrative_synthesis_packet'
2 errors in 1.23s
```

After the minimal implementation, the same command produced:

```text
......                                                                   [100%]
6 passed in 1.45s
```

## Implementation

- Added frozen, plain-data models for source-local topics and profiles,
  structured cross-system relationships, concrete tensions, and the narrative
  synthesis packet.
- Built Bazi and astrology profiles independently from the exact matched
  signal tuple returned by the qualified-facts extraction route.
- Compared only exact topics. A topic present on one side only becomes
  `non_comparable`; it cannot become validation or tension.
- Added the complete bounded relationship vocabulary: `validation`,
  `complement`, `contextualization`, `tension`, `correction`, `unresolved`, and
  `non_comparable`. The current evidence-driven classifier conservatively emits
  validation, tension, unresolved, or non-comparable; it does not invent
  complement/contextualization/correction without an explicit semantic basis.
- Expanded each tension into named Bazi and astrology poles, matched real-life
  contexts, an integration direction, source signal IDs, limitations, and
  per-signal provenance.
- Attached the packet to the audited interpretive core profile and added a
  deterministic JSON-compatible packet codec.

## Self-review

- Public builders accept only `QualifiedFacts` and call
  `require_qualified_facts`; raw chart facts cannot enter this product path.
- System filtering occurs before topic grouping, so neither profile can absorb
  another system's signal IDs or fact references.
- Validation requires real matched signals from both systems on the same topic
  with identical direction sets. One-sided topics are explicitly
  non-comparable.
- Tension requires real matched signals from both systems on the same topic
  with disjoint direction sets. Both poles and provenance are retained; no
  signal is cancelled or rewritten.
- Changes are confined to the audited interpretive modules and new focused
  tests. Strict, candidate, primitive, mapping, and semantic-bridge code and
  assets were not modified.
- The implementation stays Python 3.9 compatible and adds no dependency.

## Verification

Focused interpretive regression:

```text
python3 -m pytest \
  tests/test_interpretive_system_profiles.py \
  tests/test_interpretive_synthesis.py \
  tests/test_interpretive_profile.py \
  tests/test_interpretive_report.py -q

29 passed in 2.05s
```

All tests except the four failures already present at the Task 2 baseline:

```text
python3 -m pytest -q -k \
  'not test_missing_time_visibly_degrades_time_sensitive_output and \
   not test_checked_in_demos_are_cli_generated_parseable_and_traceable'

860 passed, 4 deselected in 80.99s
```

The pre-change full-suite baseline was `854 passed, 4 failed`; the four failures
are Task 1 missing-time/demo snapshot expectations in
`tests/test_interpretive_cli.py`. Task 2 did not modify those files or their
behavior.

Additional checks:

```text
python3 -m compileall -q <Task 2 Python files>
git diff --check
python3 scripts/verify_package.py

package verification passed
```

## Review repair: serialized source content and evidence-backed tensions

### RED

Added focused assertions to `tests/test_interpretive_synthesis.py` before the
repair. They require every serialized alignment to retain the corresponding
per-system topic object (or `null` when that system has no topic), including
its interpretations, mechanisms, likely expressions, and contexts. They also
require a tension to preserve pole-specific contexts, cite the qualified fact
paths that explain coexistence, and base its practical integration on the
source likely expressions instead of the previous generic wording.

```text
python3 -m pytest \
  tests/test_interpretive_system_profiles.py \
  tests/test_interpretive_synthesis.py -q

...FFF..                                                                 [100%]
KeyError: 'bazi_source'
KeyError: 'bazi_source'
AttributeError: 'InterpretiveTension' object has no attribute 'why_coexist'
3 failed, 5 passed in 2.00s
```

The failures demonstrate the review finding directly: alignments serialized
only topic/direction-level synthesis and signal IDs, while tensions had only a
merged context tuple and a generic integration template.

### GREEN

- Each `InterpretiveSynthesisRelationship` now keeps its exact Bazi and
  astrology `InterpretiveSystemTopic` inputs. The deterministic codec emits
  them as `bazi_source` and `astrology_source`; a one-sided relationship emits
  `null` for the absent source.
- Every retained source includes the matched topic's interpretations,
  mechanisms, likely expressions, contexts, limitations, and provenance. The
  relation builder receives these objects from the profiles built from the same
  qualified matched signals; it does not create a new semantic summary.
- `InterpretiveTension` now carries `left_contexts`, `right_contexts`, and
  `why_coexist`. The coexistence explanation names the actual signal IDs,
  concrete qualified fact paths, directions, and pole-specific contexts.
- Tension integration now tells the reader where to observe each pole and
  reproduces each side's source likely expression. It no longer uses the
  generic "do not treat one side as the negation of the other" template.

```text
python3 -m pytest \
  tests/test_interpretive_system_profiles.py \
  tests/test_interpretive_synthesis.py -q

........                                                                 [100%]
8 passed in 1.54s
```

Final focused re-verification after recording this evidence:

```text
python3 -m pytest tests/test_interpretive_system_profiles.py tests/test_interpretive_synthesis.py -q
........                                                                 [100%]
8 passed in 1.36s

python3 -m compileall -q src/destiny_personality/interpretive_models.py src/destiny_personality/interpretive_synthesis.py src/destiny_personality/interpretive_codec.py
git diff --check
```
