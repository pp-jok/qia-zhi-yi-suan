# Gate 1B Context-Aware Mapping Registry Contracts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. This workspace is not a Git repository, so verification checkpoints replace commit steps.

**Goal:** Add distributable Bazi and astrology Context-Aware Mapping Registry contracts plus a standalone development validator without adding production mapping values.

**Architecture:** One shared Skill contract governs two required source-specific assets. A separate Python loader consumes already accepted runtime and Primitive foundation objects, validates both candidate registries, and returns immutable, source-isolated models. Production assets remain absent, so Gate 1 and Phase D remain blocked by `CONFIG_GAP`.

**Tech Stack:** Markdown Skill contracts, YAML candidate assets, Python 3.9+, immutable dataclasses, PyYAML, pytest.

## Global Constraints

- Read and write only inside `/Users/lht/纷乱的想法/codex主目录/差指一算` except for required system Skill instructions.
- Do not add calculation software, a Python runtime, or Python files to `destiny-personality/`.
- Do not create `bazi_mapping_registry_v1.yaml` or `astrology_mapping_registry_v1.yaml` in either production config location.
- Do not invent Primitive meanings, mapping rules, condition operators, direction semantics, thresholds, effects, or interactions.
- Synthetic fixtures must use `TEST_ONLY_` values and temporary directories.
- Preserve the existing four frozen production configuration files byte-for-byte.
- Keep `load_runtime_config()`, `load_primitive_foundation()`, and the new loader independently callable.
- Missing real registries remain `CONFIG_GAP`; Gate 1 and Phase D remain incomplete.
- Follow RED-GREEN-REFACTOR and run every stated failure before implementation.

---

## File Structure

- Create `destiny-personality/schemas/context-aware-mapping-registry.md`: shared distributable contract for both registries.
- Create `destiny-personality/examples/mapping-registry-template.md`: visibly non-production authoring shapes.
- Create `src/destiny_personality/mapping_models.py`: immutable accepted-registry models.
- Create `src/destiny_personality/mapping_loader.py`: standalone candidate loader and validator.
- Create `tests/test_mapping_registry_config.py`: happy path and validation matrix.
- Modify `src/destiny_personality/__init__.py`: export the public loader and bundle model.
- Modify `destiny-personality/SKILL.md`: route agents through both registries after Primitive foundation validation.
- Modify `destiny-personality/checklists/stage-gates.md`: add deterministic registry order and stopping behavior.
- Modify `destiny-personality/references/methodology-index.md`: record Gate 1B contract status and remaining semantic gaps.
- Modify `tests/test_skill_package.py`: enforce links, prohibition language, and absent production placeholders.
- Modify `tests/test_v2_2_config_integration.py`: enforce source-doc and manifest status consistency.
- Modify the V2.2 README, implementation plan, acceptance criteria, execution architecture, and `manifest.json`: record Gate 1B contracts without claiming Gate 1 completion.
- Create `docs/superpowers/evidence/2026-09-13-gate-1b-verification.md`: RED/GREEN and release evidence.

---

### Task 1: Lock the public API and immutable happy path

**Files:**
- Create: `tests/test_mapping_registry_config.py`
- Create: `src/destiny_personality/mapping_models.py`
- Create: `src/destiny_personality/mapping_loader.py`
- Modify: `src/destiny_personality/__init__.py`

**Interfaces:**
- Consumes: `PrimitiveFoundationConfig`, `RuntimeConfig`, and two YAML files in a caller-supplied directory.
- Produces: `load_mapping_registries(config_dir, primitive_foundation, runtime_config) -> MappingRegistryBundle`.

- [ ] **Step 1: Write the failing happy-path test**

Create synthetic Primitive foundation and mapping fixtures. Assert:

```python
bundle = destiny_personality.load_mapping_registries(
    mapping_config_dir,
    primitive_foundation,
    runtime_config,
)
assert bundle.bazi.source_system == "bazi"
assert bundle.astrology.source_system == "astrology"
assert bundle.bazi.rules[0].outputs[0].primitive_id == "P900"
assert bundle.bazi.rules[0].primary_condition == (
    ("feature", "TEST_ONLY_BAZI_FEATURE"),
)
with pytest.raises(FrozenInstanceError):
    bundle.bazi.registry_version = "changed"
```

- [ ] **Step 2: Run the happy-path test and verify RED**

Run:

```bash
python3 -m pytest tests/test_mapping_registry_config.py::test_load_mapping_registries_returns_immutable_source_isolated_bundle -q
```

Expected: FAIL because the public loader is missing.

- [ ] **Step 3: Add focused immutable models**

Define frozen dataclasses:

```python
MappingOutput
MappingModifier
MappingRule
MappingInteraction
ContextAwareMappingRegistryConfig
MappingRegistryBundle
```

Use tuples for all accepted collections and recursively frozen declarative
values. Do not add evaluator methods.

- [ ] **Step 4: Implement the minimum valid loader**

Add exact filenames and schema constants, parse both files in Bazi-then-
astrology order, validate the required happy-path fields and references, sort
rules by priority, and export the API from `__init__.py`.

- [ ] **Step 5: Run the happy-path test and verify GREEN**

Run the command from Step 2. Expected: `1 passed`.

---

### Task 2: Complete deterministic validation behavior

**Files:**
- Modify: `tests/test_mapping_registry_config.py`
- Modify: `src/destiny_personality/mapping_loader.py`

**Interfaces:**
- Consumes: the public API created in Task 1.
- Produces: deterministic `ConfigError(code, file, field)` results for every contract failure.

- [ ] **Step 1: Add the failing validation matrix**

Cover at minimum:

```text
missing Bazi/astrology file or required field -> CONFIG_GAP
malformed YAML -> CONFIG_PARSE_ERROR
non-mapping roots/records and wrong scalar types -> CONFIG_TYPE_ERROR
unsupported schema/source/methodology/fact/score-model/ontology version -> CONFIG_VERSION_MISMATCH
unknown fields and empty required collections -> CONFIG_VALUE_ERROR
empty context -> CONFIG_VALUE_ERROR
duplicate local/global rule IDs -> CONFIG_VALUE_ERROR
duplicate local priorities -> CONFIG_VALUE_ERROR
unknown or duplicate output Primitive -> CONFIG_VALUE_ERROR
salience outside runtime score bounds -> CONFIG_VALUE_ERROR
non-string nested key, YAML date, or non-finite float -> CONFIG_TYPE_ERROR
empty modifier condition/effects -> CONFIG_VALUE_ERROR
interaction with fewer than two rules -> CONFIG_VALUE_ERROR
duplicate or unresolved interaction requirement -> CONFIG_VALUE_ERROR
duplicate local/global interaction IDs -> CONFIG_VALUE_ERROR
```

Every assertion must include the expected filename and most specific field path.

- [ ] **Step 2: Run the mapping suite and verify RED**

Run:

```bash
python3 -m pytest tests/test_mapping_registry_config.py -q
```

Expected: the newly added cases fail against the minimum loader.

- [ ] **Step 3: Implement validation in first-failure order**

Add small direct helpers for exact keys, strings, integers, string lists,
declarative values, outputs, modifiers, rules, interactions, and bundle-wide
uniqueness. Reject `bool` where an integer is required and reject non-finite
floats recursively.

- [ ] **Step 4: Run the mapping suite and verify GREEN**

Run the command from Step 2. Expected: all mapping tests pass.

- [ ] **Step 5: Run prior loader regression tests**

Run:

```bash
python3 -m pytest tests/test_config_loader.py tests/test_config_validation.py tests/test_primitive_foundation_config.py -q
```

Expected: all prior runtime and Primitive tests pass unchanged.

---

### Task 3: Add the distributable Skill contract and routing

**Files:**
- Create: `destiny-personality/schemas/context-aware-mapping-registry.md`
- Create: `destiny-personality/examples/mapping-registry-template.md`
- Modify: `destiny-personality/SKILL.md`
- Modify: `destiny-personality/checklists/stage-gates.md`
- Modify: `destiny-personality/references/methodology-index.md`
- Modify: `tests/test_skill_package.py`

**Interfaces:**
- Consumes: the schema and failure behavior fixed in Tasks 1-2.
- Produces: a self-contained agent contract with no Python/runtime dependency.

- [ ] **Step 1: Add failing package tests**

Assert that:

```python
for path in (
    "schemas/context-aware-mapping-registry.md",
    "examples/mapping-registry-template.md",
):
    assert f"]({path})" in skill
for filename in (
    "bazi_mapping_registry_v1.yaml",
    "astrology_mapping_registry_v1.yaml",
):
    assert not (SKILL_ROOT / "configs" / filename).exists()
```

Also require the exact five configuration error mappings, Bazi-before-
astrology ordering, source isolation, non-empty context, same-registry
interaction references, template prohibition, and a statement that Gate 1
remains incomplete.

- [ ] **Step 2: Run focused package tests and verify RED**

Run:

```bash
python3 -m pytest tests/test_skill_package.py -q
```

Expected: FAIL because the mapping contract and routes are absent.

- [ ] **Step 3: Write the shared contract and template**

Mirror the design exactly. Mark every template value as `TEST_ONLY_` or an
angle-bracket placeholder and state that the template must not be copied,
renamed, or loaded as production configuration.

- [ ] **Step 4: Wire the Skill and semantic gate checklist**

After the Primitive foundation contract, require Bazi then astrology mapping
registries. State that agents validate and use externally supplied values but
must not invent mappings or rely on the Python reference package.

- [ ] **Step 5: Run focused package tests and verify GREEN**

Run the command from Step 2. Expected: all Skill package tests pass.

---

### Task 4: Synchronize V2.2 source status and manifest

**Files:**
- Modify: `destiny_personality_skill_docs_v2_2/00_README_V2_2.md`
- Modify: `destiny_personality_skill_docs_v2_2/10_CODEX_IMPLEMENTATION_PLAN_V2_2.md`
- Modify: `destiny_personality_skill_docs_v2_2/11_ACCEPTANCE_CRITERIA_V2_2.md`
- Modify: `destiny_personality_skill_docs_v2_2/12_SKILL_EXECUTION_ARCHITECTURE_V2_2.md`
- Modify: `destiny_personality_skill_docs_v2_2/manifest.json`
- Modify: `tests/test_v2_2_config_integration.py`

**Interfaces:**
- Consumes: verified Gate 1B contracts.
- Produces: consistent source-document status without semantic-completion claims.

- [ ] **Step 1: Add a failing status test**

Require `gate_1b_status == "implemented"` and the same sentence in all four
source documents:

```text
Gate 1B Context-Aware Mapping Registry contracts are implemented and verified on 2026-09-13.
```

Also require an explicit statement that real mapping values, Gate 1, and Phase D
remain incomplete.

- [ ] **Step 2: Run the status test and verify RED**

Run:

```bash
python3 -m pytest tests/test_v2_2_config_integration.py -q
```

Expected: FAIL because Gate 1B status is absent.

- [ ] **Step 3: Update docs and manifest consistently**

Add only contract status. Do not add the two mapping files to the manifest's
production `documents` list and do not change the four frozen YAML assets.

- [ ] **Step 4: Run the status test and verify GREEN**

Run the command from Step 2. Expected: all integration tests pass.

---

### Task 5: Release verification and evidence

**Files:**
- Create: `docs/superpowers/evidence/2026-09-13-gate-1b-verification.md`

**Interfaces:**
- Consumes: all Gate 1B deliverables.
- Produces: auditable RED/GREEN and release evidence.

- [ ] **Step 1: Record the observed RED/GREEN commands and results**

The evidence file must distinguish deliberate RED runs from final passing
verification and state that no real semantic value was introduced.

- [ ] **Step 2: Run the complete test suite**

```bash
python3 -m pytest -q
```

Expected: zero failures.

- [ ] **Step 3: Validate the distributable Skill**

```bash
python3 /Users/lht/.codex/skills/.system/skill-creator/scripts/quick_validate.py destiny-personality
```

Expected: `Skill is valid!`

- [ ] **Step 4: Verify frozen assets, forbidden files, and production inventory**

```bash
python3 -m pytest tests/test_skill_package.py::test_baseline_configs_are_byte_identical_to_source -q
find destiny-personality -type f \( -name '*.py' -o -name '*.pyc' -o -name '*.so' -o -name '*.dylib' -o -name '*.dll' \) -print
find destiny-personality/configs -maxdepth 1 -type f -print | sort
```

Expected: frozen test passes, forbidden-file scan is empty, and inventory lists
only the original four production YAML files.

- [ ] **Step 5: Verify syntax and package installation**

```bash
PYTHONPYCACHEPREFIX=/private/tmp/gate1b-pycache python3 -m py_compile src/destiny_personality/mapping_models.py src/destiny_personality/mapping_loader.py
python3 scripts/verify_package.py
```

Expected: compile exits zero and package verification prints
`package verification passed`.

- [ ] **Step 6: Re-run the full suite after the final status mutation**

```bash
python3 -m pytest -q
```

Expected: zero failures. Do not make a completion claim from an earlier run.
