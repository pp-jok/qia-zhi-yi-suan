# Task 5 report

## TDD evidence

Added `tests/test_interpretive_cli.py` before the CLI implementation and ran:

```text
python3 -m pytest tests/test_interpretive_cli.py::test_cli_builds_traceable_standard_report -q
```

The test failed for the intended reason: argparse rejected the absent
`build-interpretive-report` command with `SystemExit: 2`.

After registering and implementing the command, generating fixture pairs, and
generating the demo artifacts through the command, focused verification was:

```text
python3 -m pytest tests/test_interpretive_cli.py -q
9 passed in 1.82s
```

## Implementation

Added the public CLI interface:

```text
build-interpretive-report FACTS.json \
  --qualification QUALIFICATION.json \
  --mode {standard,concise} \
  --output OUTPUT.json
```

The command branch imports only the public qualified-facts loader (locally
aliased as `load_qualified_facts`), the interpretive profile builder, the
interpretive report builder, and its codec. It does not import or call strict,
candidate-profile, release-renderer, or semantic-core builders.

The persisted product payload distinguishes the two mode concepts explicitly:

- `mode` is the product path identity, `audited_interpretive`;
- `report_mode` is the requested view, `standard` or `concise`.

This satisfies the Task 5 product contract without changing the Task 4 report
object or codec contract. Existing strict command registration and branches
were left unchanged.

Output writes create parent directories and convert filesystem failures to the
controlled `INTERPRETIVE_REPORT_WRITE_FAILED` CLI error.

## Product fixtures and demos

Added five qualification-bound fixture pairs under
`tests/fixtures/interpretive/`:

| Fixture | Deliberate coverage |
| --- | --- |
| `contrast_a` | Bazi Ten-God signal only |
| `contrast_b` | time-sensitive astrology planet/house signal only |
| `relationship_sensitive` | Bazi branch-relation signal only |
| `tension` | all four Bazi and astrology signals, including aspect/dignity tension material |
| `missing_time` | stable-only facts; preserves three time-independent signals and removes the planet/house signal |

Every pair loads successfully through `load_qualified_deterministic_facts`, and
its qualification file is fingerprint-bound to its facts file.

Generated these checked-in artifacts only by invoking the new CLI:

- `docs/demos/v0.5.0/contrast-a-standard.json`
- `docs/demos/v0.5.0/tension-standard.json`
- `docs/demos/v0.5.0/missing-time-concise.json`

Tests regenerate each demo through the CLI and compare the parsed JSON for
exact equality. They also require section signal IDs and rule, facts, and
qualification audit references.

## Product gates

The Task 5 tests prove:

- exact deterministic-facts and qualification fingerprint traceability;
- reader-visible and signal-level differentiation between structural
  contrasts, excluding audit metadata as the basis of comparison;
- retention of both systems and aspect/dignity material in the tension fixture;
- visible missing-time degradation by removal of the house-dependent signal;
- at least five complete, loadable fixture pairs;
- parseability, traceability, and CLI reproducibility of all three demos;
- rejection when independent qualification evidence is missing.

Adjacent interpretive and strict CLI regression verification:

```text
python3 -m pytest \
  tests/test_interpretive_rules.py \
  tests/test_interpretive_profile.py \
  tests/test_interpretive_report.py \
  tests/test_interpretive_cli.py \
  tests/test_release_cli.py tests/test_cli.py -q
60 passed in 9.95s
```

Full-suite verification completed successfully:

```text
python3 -m pytest -p no:terminal -o addopts=
exit 0

python3 -m pytest -q
829 passed in 52.51s
```

Additional verification completed successfully:

```text
python3 -m compileall -q src/destiny_personality/cli.py tests/test_interpretive_cli.py
git diff --check
```
