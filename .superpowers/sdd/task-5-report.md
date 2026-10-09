# Task 5 Report: Birth-input Workflow and v0.6.0 Readiness

## Scope delivered

- Made ordinary birth information the only normal-user input. The Skill now
  discovers and invokes an available calculation/qualification provider.
- Added an explicit stopped `CAPABILITY_GAP` result when no suitable provider
  exists. Facts JSON and qualification records remain internal interfaces;
  free-form chart calculation, reconstruction, and repair are forbidden.
- Preserved all v0.5.0 strict, formal limited-coverage, Candidate Preview, and
  explicit legacy routes.
- Added the machine-readable v0.6.0 readiness summary, release notes, changelog
  entry, README workflow, and package version 0.6.0.
- Changed no runtime source, rule assets, fixtures, or v0.5.0 demos.

## TDD evidence

### RED

Added `tests/test_interpretive_product_flow.py` and the v0.6.0 package metadata
contract in `tests/test_skill_package.py` before changing Skill or release
documentation.

Command:

```text
python3 -m pytest tests/test_interpretive_product_flow.py tests/test_skill_package.py -q
```

Initial result:

```text
3 failed, 37 passed in 0.94s
```

The failures were the intended missing-contract failures:

1. The documented product flow did not state the birth-only provider workflow
   and explicit `CAPABILITY_GAP` branch.
2. `docs/v0.6.0-product-readiness.md` did not exist.
3. `docs/release/v0.6.0-release-notes.md` did not exist.

The first GREEN attempt exposed a misplaced pre-existing assertion after the
new package test (`NameError: failures is not defined`): `1 failed, 39 passed`.
The assertion was restored to its original test before rerunning.

### GREEN

Focused command after implementation and test-structure correction:

```text
python3 -m pytest tests/test_interpretive_product_flow.py tests/test_skill_package.py -q
........................................                                 [100%]
40 passed in 0.62s
```

The readiness test parses the fenced YAML between explicit markers and checks
the complete workflow, compatibility, version, product status, and quality-gate
mapping rather than searching prose for a single readiness word.

## Product-quality and full regression evidence

Product gate command:

```text
python3 -m pytest tests/test_interpretive_product_quality.py -q
.................................                                        [100%]
33 passed in 5.48s
```

This verifies that normal complete fixtures retain six or more real topics,
sparse/missing-time output remains scoped, visible conclusions carry signal
provenance, and checked-in v0.6.0 demos remain reproducible.

Required full-suite command:

```text
python3 -m pytest -p no:terminal -o addopts=
exit 0
```

The disabled terminal plugin intentionally emits no summary; the process
completed with exit code 0.

Additional release-test verification:

```text
python3 -m pytest tests/test_verify_package_script.py -q
........                                                                 [100%]
8 passed in 0.11s
```

## Wheel and asset evidence

Required build command:

```text
python3 -m build --wheel
Successfully built qia_zhi_yi_suan_candidate-0.6.0-py3-none-any.whl
```

Setuptools emitted only its existing future deprecation warning for the
TOML-table license declaration. The build exited 0.

Direct wheel inspection:

```text
destiny_personality/interpretive_assets/v1/interpretive_rules_v1.yaml
qia_zhi_yi_suan_candidate-0.6.0.dist-info/METADATA
Version: 0.6.0
```

The package-data declaration continues to include candidate, canonical,
interpretive, and release YAML assets. No package-data pattern was removed.

## Skill validation and self-review

`skill-creator` validation:

```text
python3 /Users/lht/.codex/skills/.system/skill-creator/scripts/quick_validate.py destiny-personality
Skill is valid!
```

Self-review findings:

- The added Skill section is a five-step imperative workflow containing only
  the non-obvious provider, qualification, and fail-closed boundaries.
- Normal users are never asked for facts JSON. Existing explicit `facts_only`
  and `audit` routes remain available because they are not normal portrait
  input flows.
- The README labels the facts/qualification CLI as an internal provider/runtime
  integration interface.
- `CAPABILITY_GAP` is used only when the required capability is unavailable;
  it does not relax fact qualification or any strict gate.
- The readiness summary says `internal_test_product`; it does not claim an
  empirical personality product or unconditional public publication.
- The Python 3.9/3.11/3.12 CI and package-verification matrix remains defined in
  `.github/workflows/tests.yml`. Remote merged-branch CI was not run locally,
  so publication remains explicitly conditional on that green run.
- `git diff --check` completed with no output.
