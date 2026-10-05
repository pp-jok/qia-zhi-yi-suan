# Semantic Content Production and Non-Zero Core Profile Implementation Plan

> **Execution note:** Follow the repository TDD discipline and execute every task in order. The approved design permits autonomous execution without an additional user checkpoint.

**Goal:** Complete independent Bazi and Hellenistic research for P001, P002, P003, P005, and P006, publish an auditable v0.4.1 deep-research closure, and preserve the formal six-unknown runtime because no candidate clears the semantic and methodological gates.

**Architecture:** Add source-grounded research corpora, per-primitive construct matrices, and expanded final reports. Replace the packaged v1 coverage manifest with a strict v2 manifest whose terminal status distinguishes repository-only review from independent research saturation. Keep the active Mapping bundle empty and assert the unchanged formal resolver behavior end to end.

**Tech stack:** Python 3.9+, PyYAML, pytest, Markdown governance records, YAML release assets, setuptools.

---

## Task 1: Define executable research-closure acceptance tests

**Files:**
- Create: `tests/test_semantic_content_production.py`
- Inspect: `docs/reviews/primitives/P001-final-research-report.md`
- Inspect: `src/destiny_personality/release_assets/v1/primitive_coverage_v1.yaml`

**Step 1: Write failing tests**

Add tests that require:

- one shared Bazi corpus and one Hellenistic corpus with primary/public locators and explicit authority-versus-access-copy handling;
- a construct matrix and expanded final report for each reopened Primitive;
- every report to cover ontology boundary, Bazi search, Astrology search, method feasibility, canonical-fact feasibility, Root/PE/Mapping result, counterevidence, and saturation;
- zero PE and zero Mapping activation statements;
- a v2 release manifest with the five deep-research terminal statuses and frozen P004 status.

**Step 2: Run the focused tests and confirm RED**

Run: `python -m pytest tests/test_semantic_content_production.py -q`

Expected: FAIL because the corpora, matrices, and v2 manifest do not exist.

**Step 3: Commit the RED test contract**

```bash
git add tests/test_semantic_content_production.py
git commit -m "test: define deep semantic research closure contract"
```

## Task 2: Build the shared independent source corpus

**Files:**
- Create: `docs/reviews/semantic-content-bazi-source-corpus.md`
- Create: `docs/reviews/semantic-content-hellenistic-source-corpus.md`
- Modify: `tests/test_semantic_content_production.py`

**Step 1: Record the Bazi corpus**

Document exact work identity, relevant sections/phrases, public locator, access-copy status, translation/OCR limitations, and what each source can and cannot establish. Cover *Yuanhai Ziping*, *Ditian Sui*, *Ziping Zhenquan*, and *Sanming Tonghui*.

**Step 2: Record the Hellenistic corpus**

Use Ptolemy *Tetrabiblos* III.13 as the principal exact-locator text. Record Valens and Dorotheus as discovery/corroborating corpora only to the extent exact locators support a claim. State that traditional methodology evidence is not empirical personality validation.

**Step 3: Run the corpus acceptance slice**

Run: `python -m pytest tests/test_semantic_content_production.py -q`

Expected: corpus checks PASS; matrix/report/manifest checks remain RED.

**Step 4: Commit**

```bash
git add docs/reviews/semantic-content-*-source-corpus.md tests/test_semantic_content_production.py
git commit -m "docs: establish independent semantic source corpora"
```

## Task 3: Complete P006 priority research without semantic inflation

**Files:**
- Create: `docs/reviews/primitives/P006-deep-construct-matrix.md`
- Modify: `docs/reviews/primitives/P006-final-research-report.md`
- Test: `tests/test_semantic_content_production.py`

**Step 1: Populate the closest-candidate matrix**

Compare `治事无规`, `处事有方`/`布置有方`, and Ptolemy's `systematic workers` against both P006 directions. Classify lexical directness separately from construct directness and record missing method inputs, subject selection, aggregation, precedence, and counterexamples.

**Step 2: Expand the final report**

Conclude that the Bazi phrases require unresolved whole-chart conditions and the Ptolemaic phrase is role/capability language inside a multi-factor soul-governor method. Record no Root, no PE, and no Mapping.

**Step 3: Run the P006 acceptance slice**

Run: `python -m pytest tests/test_semantic_content_production.py -q -k P006`

Expected: PASS.

**Step 4: Commit**

```bash
git add docs/reviews/primitives/P006-* tests/test_semantic_content_production.py
git commit -m "docs: close P006 deep construct research"
```

## Task 4: Complete P001 and P002 research

**Files:**
- Create: `docs/reviews/primitives/P001-deep-construct-matrix.md`
- Create: `docs/reviews/primitives/P002-deep-construct-matrix.md`
- Modify: `docs/reviews/primitives/P001-final-research-report.md`
- Modify: `docs/reviews/primitives/P002-final-research-report.md`
- Test: `tests/test_semantic_content_production.py`

**Step 1: Separate adjacent constructs**

For P001, distinguish judgement quality, decisiveness, cognition, and self-will from ownership of judgement standards. For P002, distinguish fixed/changeable structures and temperament from preference for predictable conditions.

**Step 2: Audit method and fact feasibility**

For each system and each direction, record required inputs, missing canonical facts, aggregation problems, exclusions, and opposing-direction symmetry.

**Step 3: Expand both reports**

Include source locators, candidate classifications, counterevidence, saturation logic, and explicit zero Root/PE/Mapping outcome.

**Step 4: Run focused tests**

Run: `python -m pytest tests/test_semantic_content_production.py -q -k 'P001 or P002'`

Expected: PASS.

**Step 5: Commit**

```bash
git add docs/reviews/primitives/P001-* docs/reviews/primitives/P002-* tests/test_semantic_content_production.py
git commit -m "docs: close P001 and P002 deep construct research"
```

## Task 5: Complete P003 and P005 research

**Files:**
- Create: `docs/reviews/primitives/P003-deep-construct-matrix.md`
- Create: `docs/reviews/primitives/P005-deep-construct-matrix.md`
- Modify: `docs/reviews/primitives/P003-final-research-report.md`
- Modify: `docs/reviews/primitives/P005-final-research-report.md`
- Test: `tests/test_semantic_content_production.py`

**Step 1: Separate adjacent constructs**

For P003, distinguish benevolence, affection, social reception, and relationship outcome from responsive coordination. For P005, distinguish emotional intensity, restraint, expression, pathology, and cosmological flow from preferred affect-processing orientation.

**Step 2: Audit method and fact feasibility**

Record whole-chart dependencies, missing strength/priority rules, insufficient semantic bridge, and lack of independent high/low direction support.

**Step 3: Expand both reports and run focused tests**

Run: `python -m pytest tests/test_semantic_content_production.py -q -k 'P003 or P005'`

Expected: PASS.

**Step 4: Commit**

```bash
git add docs/reviews/primitives/P003-* docs/reviews/primitives/P005-* tests/test_semantic_content_production.py
git commit -m "docs: close P003 and P005 deep construct research"
```

## Task 6: Implement strict v2 coverage manifest and package it

**Files:**
- Create: `src/destiny_personality/release_assets/v1/primitive_coverage_v2.yaml`
- Modify: `src/destiny_personality/release_manifest.py`
- Modify: `tests/test_autonomous_evidence_root.py`
- Modify: `tests/test_semantic_content_production.py`

**Step 1: Add loader RED tests**

Require schema `release-primitive-coverage-v2`, the exact five deep-research statuses, unchanged P004 system closures, existing report paths, empty PE/Mapping references, and exact P001-P006 coverage. Require malformed or non-terminal variants to fail closed.

**Step 2: Run focused loader tests and confirm RED**

Run: `python -m pytest tests/test_autonomous_evidence_root.py tests/test_semantic_content_production.py -q`

Expected: FAIL on v1 loader/path/schema.

**Step 3: Add v2 asset and minimal loader change**

Point the package-owned path to v2, update terminal-status constants, verify `research_report_ref` resolves beneath the repository/package project root when a repository manifest is used, and preserve the immutable dataclasses/API shape.

**Step 4: Run focused tests and confirm GREEN**

Run: `python -m pytest tests/test_autonomous_evidence_root.py tests/test_semantic_content_production.py -q`

Expected: PASS.

**Step 5: Commit**

```bash
git add src/destiny_personality/release_manifest.py src/destiny_personality/release_assets/v1/primitive_coverage_v2.yaml tests/test_autonomous_evidence_root.py tests/test_semantic_content_production.py
git commit -m "feat: publish strict v2 deep research coverage"
```

## Task 7: Prove formal runtime remains zero activated

**Files:**
- Modify: `tests/test_semantic_content_production.py`
- Inspect: `src/destiny_personality/release_assets/v1/active_mapping_bundle_v1.yaml`
- Inspect: `src/destiny_personality/release_semantics.py`

**Step 1: Add end-to-end invariants**

Assert the release manifest has zero PE/Mapping refs, the active bundle has zero rules, a formal build yields exactly P001-P006 as `unknown`, and formations remain empty. Assert candidate/legacy assets cannot supply formal semantics.

**Step 2: Run the semantic release suites**

Run: `python -m pytest tests/test_semantic_content_production.py tests/test_autonomous_evidence_root.py tests/test_semantic_core_completion.py tests/test_master_semantic_core.py -q`

Expected: PASS.

**Step 3: Commit**

```bash
git add tests/test_semantic_content_production.py
git commit -m "test: freeze zero activation after deep research"
```

## Task 8: Close governance, version, and release narrative

**Files:**
- Create: `docs/reviews/semantic-content-production-final-report.md`
- Create: `docs/reviews/semantic-content-production-five-role-review.md`
- Modify: `docs/reviews/autonomous-completion-final-report.md`
- Modify: `README.md`
- Modify: `pyproject.toml`
- Modify: `src/destiny_personality/__init__.py`

**Step 1: Write final autonomous decision**

Record the exact outcome token:

`ALL_REOPENED_CORE_PATHS_DEEP_RESEARCH_SATURATED__NO_FORMAL_RUNTIME_ACTIVATION`

Explain why this is a stronger `unknown`, not a non-zero feature release, and reserve v0.5.0 for an approved PE plus active Mapping plus formal non-unknown Primitive.

**Step 2: Perform five-role review**

Review as Product Owner, semantic-methodology reviewer, evidence/governance reviewer, runtime engineer, and release/QA reviewer. Each role must state evidence inspected, findings, blockers, and verdict.

**Step 3: Bump to v0.4.1**

Update package and exported version references. Update README release language without claiming substantive personality output.

**Step 4: Run documentation/version tests**

Run: `python -m pytest tests/test_semantic_content_production.py tests/test_semantic_core_completion.py -q`

Expected: PASS.

**Step 5: Commit**

```bash
git add docs/reviews README.md pyproject.toml src/destiny_personality/__init__.py
git commit -m "release: close semantic content research at v0.4.1"
```

## Task 9: Full verification, isolated package check, and publication

**Files:**
- Modify only if verification finds a defect.

**Step 1: Run the full suite**

Run: `python -m pytest -q`

Expected: all tests PASS.

**Step 2: Build and inspect distributions**

Run: `python -m build`

Inspect the wheel and sdist for `primitive_coverage_v2.yaml` and absence of unintended local artifacts.

**Step 3: Test isolated installation**

Create a temporary virtual environment, install the wheel, load the release manifest, and assert schema v2, six unknown closures, and zero PE/Mapping refs.

**Step 4: Verify supported Python CI**

Run the repository CI workflow or equivalent Python 3.9/3.11/3.12 matrix when interpreters are available. Treat CI as authoritative for unavailable local interpreters.

**Step 5: Review branch diff and rebase/merge latest main safely**

Fetch origin, confirm the clean branch is based on current main, inspect `git diff origin/main...HEAD`, and rerun the focused release tests after any integration.

**Step 6: Publish**

Push the branch, open/merge the pull request only after required checks pass, verify merged main, then create the v0.4.1 tag/release with the zero-activation disclosure. Do not create v0.5.0.

