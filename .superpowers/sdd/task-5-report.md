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

## Review remediation: versioned modes and real profile tension

This section supersedes the earlier unversioned CLI mode and demo descriptions.

Added RED tests before remediation. The versioned invocation and direct profile
tension run failed in three places: argparse rejected both versioned mode names,
and the tension fixture produced no conclusion with countervailing signal IDs.
After the first implementation pass, the focused checks passed:

```text
python3 -m pytest \
  tests/test_interpretive_rules.py::test_rule_bundle_defines_a_value_matched_cross_system_tension_pair \
  tests/test_interpretive_cli.py::test_cli_accepts_versioned_public_report_modes \
  tests/test_interpretive_cli.py::test_tension_fixture_creates_countervailing_profile_conclusions -q
4 passed in 0.86s
```

The public CLI now presents exactly these official choices:

```text
standard-interpretive-v1
concise-interpretive-v1
```

Output stores the canonical versioned value in `report_mode`. The old
`standard` and `concise` spellings remain accepted through parse-time alias
normalization, so they do not appear as public help choices or leak into output.
A separate help test was observed failing before this normalization was added.

The versioned V1 rule bundle now defines real cross-system tension under the
same exact topic, `style of expression`:

- `BAZI-TEN-GOD-EXPRESSION`, matched from the declared Ten-God and pillar
  predicates, carries direction `reflective`;
- `ASTROLOGY-PLANET-SIGN-EXPRESSION`, matched from Sun-in-Aries and first-house
  predicates, carries direction `outward`.

For the tension fixture, the public profile builder now creates both directional
conclusions with nonempty `supporting_signal_ids` and
`countervailing_signal_ids`. The test asserts directly on profile conclusions
and requires the exact two actual matched signal IDs; report titles are not
used as evidence of tension.

All three demos were regenerated only through
`--mode standard-interpretive-v1`:

- `docs/demos/v0.5.0/contrast-a-standard.json`
- `docs/demos/v0.5.0/tension-standard.json`
- `docs/demos/v0.5.0/missing-time-standard.json`

The former `missing-time-concise.json` artifact was removed. Missing-time
degradation remains covered by the absence of the time-sensitive
planet/house signal while time-independent signals remain available.

Focused interpretive verification after remediation:

```text
python3 -m pytest \
  tests/test_interpretive_cli.py tests/test_interpretive_rules.py \
  tests/test_interpretive_profile.py tests/test_interpretive_report.py -q
46 passed in 3.85s
```

Final full-suite verification after all review changes:

```text
python3 -m pytest -q
836 passed in 99.97s
```
