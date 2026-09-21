# Gate 1A Primitive Foundation Contracts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add distributable Primitive Ontology and Primitive State Resolution contracts plus a standalone development validator, without adding production semantic values or changing the existing runtime configuration loader.

**Architecture:** The Skill owns declarative contracts, routing, and a documentation-only template. A separate Python `primitive_loader` validates future project-owned YAML assets and returns immutable models. Production assets remain absent, so Gate 1 and Phase D remain blocked by `CONFIG_GAP`.

**Tech Stack:** Python 3.9+, frozen dataclasses, PyYAML 6, pytest 8, Markdown Skill contracts.

## Global Constraints

- Read and modify project data only inside `/Users/lht/纷乱的想法/codex主目录/差指一算`.
- Do not add `primitive_ontology_v1.yaml` or `primitive_state_resolution_v1.yaml` under `destiny-personality/configs/` or the V2.2 source-doc root.
- Do not invent real Primitive definitions, aliases, thresholds, evidence mappings, or state rules.
- Keep `load_runtime_config()` and the four frozen baseline YAML files unchanged.
- Keep the Python validator development-only; it is not a Skill runtime dependency.
- Do not implement Mapping, Evidence Graph, state evaluation, signatures, Dynamic selection, dimensions, or Narrative.
- Missing real assets continue to produce `CONFIG_GAP`; Gate 1 and Phase D remain incomplete.
- This workspace is not a Git repository, so commit steps are replaced by explicit test and file-scope checkpoints.

## File structure

Create:

- `destiny-personality/schemas/primitive-ontology.md` — distributable ontology contract.
- `destiny-personality/schemas/primitive-state-resolution.md` — distributable policy and result contract.
- `destiny-personality/examples/primitive-foundation-template.md` — annotated, non-loadable template.
- `src/destiny_personality/primitive_models.py` — immutable Primitive foundation models.
- `src/destiny_personality/primitive_loader.py` — standalone YAML parser and validator.
- `tests/test_primitive_foundation_config.py` — synthetic fixture and validator tests.
- `docs/superpowers/evidence/2026-09-13-gate-1a-verification.md` — final RED/GREEN and acceptance evidence.

Modify:

- `src/destiny_personality/__init__.py` — export the standalone loader and bundle model.
- `destiny-personality/SKILL.md` — route semantic preflight to the new contracts.
- `destiny-personality/checklists/stage-gates.md` — name the Primitive foundation sub-gate without claiming Gate 1 completion.
- `destiny-personality/references/methodology-index.md` — distinguish present contracts from absent production values.
- `tests/test_skill_package.py` — enforce links, absence of placeholder production assets, and boundary language.
- `tests/test_v2_2_config_integration.py` — record Gate 1A implementation status without changing Phase C status.
- `destiny_personality_skill_docs_v2_2/00_README_V2_2.md` — record Gate 1A contract status and remaining blockers.
- `destiny_personality_skill_docs_v2_2/10_CODEX_IMPLEMENTATION_PLAN_V2_2.md` — record the Gate 1A boundary.
- `destiny_personality_skill_docs_v2_2/11_ACCEPTANCE_CRITERIA_V2_2.md` — add Gate 1A acceptance language.
- `destiny_personality_skill_docs_v2_2/12_SKILL_EXECUTION_ARCHITECTURE_V2_2.md` — document the standalone validator boundary.
- `destiny_personality_skill_docs_v2_2/manifest.json` — add `gate_1a_status: implemented` only after final verification.

---

### Task 1: Distributable Primitive contracts

**Files:**
- Create: `destiny-personality/schemas/primitive-ontology.md`
- Create: `destiny-personality/schemas/primitive-state-resolution.md`
- Create: `destiny-personality/examples/primitive-foundation-template.md`
- Test: `tests/test_skill_package.py`

**Interfaces:**
- Consumes: the approved design and existing `score_model_v2_2.yaml` wire values.
- Produces: exact contract fields and filenames consumed by Task 2 and linked by Task 4.

- [ ] **Step 1: Write failing contract tests**

Add tests that require both schema files and the template, assert the exact
ontology fields, exact resolution root fields, four wire states, six fixed
invariants, result fields, and warnings that the template is non-production and
must not be loaded.

```python
def test_primitive_foundation_contracts_are_distributable() -> None:
    ontology = read_skill_file("schemas/primitive-ontology.md")
    resolution = read_skill_file("schemas/primitive-state-resolution.md")
    template = read_skill_file("examples/primitive-foundation-template.md")
    for field in (
        "schema_version", "ontology_version", "primitives", "primitive_id",
        "canonical_name", "definition", "high_expression", "low_expression",
        "aliases", "limitations",
    ):
        assert f"`{field}`" in ontology
    for state in ("supported_high", "supported_low", "mixed", "unknown"):
        assert f"`{state}`" in resolution
    assert "must not be loaded as runtime configuration" in template


def test_no_primitive_placeholder_is_a_production_config() -> None:
    for filename in (
        "primitive_ontology_v1.yaml",
        "primitive_state_resolution_v1.yaml",
    ):
        assert not (SKILL_ROOT / "configs" / filename).exists()
```

- [ ] **Step 2: Run the tests and confirm RED**

Run:

```bash
python3 -m pytest tests/test_skill_package.py -k primitive_foundation -v
```

Expected: FAIL because the three resources do not exist.

- [ ] **Step 3: Write the contracts and template**

Use the exact fields and invariants from the approved design. The template must
use visibly invalid tokens such as `<PROJECT_OWNED_NAME>` inside Markdown and
must state that copying it into `configs/` is prohibited until every value is
approved.

- [ ] **Step 4: Run Task 1 GREEN tests**

Run the Step 2 command. Expected: all selected tests PASS.

- [ ] **Step 5: Scope checkpoint**

Run:

```bash
find destiny-personality/configs -maxdepth 1 -type f -print | sort
```

Expected: only the original four frozen YAML files.

---

### Task 2: Immutable models and happy-path loader

**Files:**
- Create: `src/destiny_personality/primitive_models.py`
- Create: `src/destiny_personality/primitive_loader.py`
- Create: `tests/test_primitive_foundation_config.py`
- Modify: `src/destiny_personality/__init__.py`

**Interfaces:**
- Consumes: `primitive_ontology_v1.yaml` and `primitive_state_resolution_v1.yaml` from a caller-supplied directory.
- Produces: `load_primitive_foundation(config_dir: Path) -> PrimitiveFoundationConfig`.

Required immutable models:

```python
@dataclass(frozen=True)
class PrimitiveDefinition:
    primitive_id: str
    canonical_name: str
    definition: str
    high_expression: str
    low_expression: str
    aliases: Tuple[str, ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class PrimitiveOntologyConfig:
    schema_version: str
    ontology_version: str
    primitives: Tuple[PrimitiveDefinition, ...]


@dataclass(frozen=True)
class PrimitiveStateRule:
    rule_id: str
    target_state: str
    priority: int
    description: str
    requires_explicit_reverse_evidence: bool
    evidence_requirements: Tuple[Tuple[str, Any], ...]
    thresholds: Tuple[Tuple[str, Any], ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class PrimitiveStateResolutionConfig:
    schema_version: str
    resolution_version: str
    ontology_version: str
    score_model_version: str
    states: Tuple[str, ...]
    invariants: Tuple[Tuple[str, Any], ...]
    rules: Tuple[PrimitiveStateRule, ...]


@dataclass(frozen=True)
class PrimitiveFoundationConfig:
    ontology: PrimitiveOntologyConfig
    resolution: PrimitiveStateResolutionConfig
```

`requires_explicit_reverse_evidence` must be `true` for every `supported_low`
rule. Other rule meanings and threshold values remain project-owned.

- [ ] **Step 1: Create a complete synthetic fixture and failing happy-path test**

The fixture contains four synthetic rules, one for each state, and one synthetic
Primitive. All names and descriptions begin with `TEST_ONLY_`.

```python
def test_load_primitive_foundation_returns_immutable_bundle(
    primitive_config_dir: Path,
) -> None:
    bundle = load_primitive_foundation(primitive_config_dir)
    assert bundle.ontology.schema_version == "primitive-ontology-v1"
    assert bundle.ontology.primitives[0].primitive_id == "P900"
    assert bundle.resolution.states == (
        "supported_high", "supported_low", "mixed", "unknown"
    )
    assert bundle.resolution.ontology_version == bundle.ontology.ontology_version
```

- [ ] **Step 2: Run the happy-path test and confirm RED**

Run:

```bash
python3 -m pytest tests/test_primitive_foundation_config.py::test_load_primitive_foundation_returns_immutable_bundle -v
```

Expected: collection FAIL because `primitive_loader` does not exist.

- [ ] **Step 3: Implement the models and minimal loader**

The loader must use `yaml.safe_load`, exact root and record key sets, explicit
`type(value) is ...` checks so booleans do not pass as integers, and existing
`ConfigError` codes. It must load ontology first, resolution second, and export
only the public loader and result model through `__init__.py`.

- [ ] **Step 4: Run the happy-path test and confirm GREEN**

Run the Step 2 command. Expected: PASS.

- [ ] **Step 5: Confirm the existing loader remains independent**

Run:

```bash
python3 -m pytest tests/test_config_loader.py tests/test_config_validation.py -q
```

Expected: all existing tests PASS without Primitive assets in `valid_config_dir`.

---

### Task 3: Deterministic validation failures

**Files:**
- Modify: `src/destiny_personality/primitive_loader.py`
- Modify: `tests/test_primitive_foundation_config.py`

**Interfaces:**
- Consumes: Task 2's loader and synthetic fixture.
- Produces: deterministic `ConfigError` code, file, and field values for every design-specified invalid class.

- [ ] **Step 1: Add parameterized failing validation tests**

Cover this exact matrix:

| Mutation | Code | Field |
|---|---|---|
| remove ontology file | `CONFIG_GAP` | none |
| malformed ontology YAML | `CONFIG_PARSE_ERROR` | none |
| ontology root is list | `CONFIG_TYPE_ERROR` | none |
| unsupported ontology schema | `CONFIG_VERSION_MISMATCH` | `schema_version` |
| empty primitives | `CONFIG_VALUE_ERROR` | `primitives` |
| invalid or duplicate Primitive ID | `CONFIG_VALUE_ERROR` | mutated record path |
| ambiguous canonical name or alias | `CONFIG_VALUE_ERROR` | mutated name/alias path |
| identical high/low expression | `CONFIG_VALUE_ERROR` | `primitives.<n>.low_expression` |
| resolution ontology version mismatch | `CONFIG_VERSION_MISMATCH` | `ontology_version` |
| score model version mismatch | `CONFIG_VERSION_MISMATCH` | `score_model_version` |
| missing/duplicate/unknown state | `CONFIG_VALUE_ERROR` | `states` |
| changed safety invariant | `CONFIG_VALUE_ERROR` | `invariants.<key>` |
| missing state rule coverage | `CONFIG_VALUE_ERROR` | `rules` |
| duplicate rule ID | `CONFIG_VALUE_ERROR` | `rules.<n>.rule_id` |
| bool priority or duplicate priority | `CONFIG_TYPE_ERROR` or `CONFIG_VALUE_ERROR` | `rules.<n>.priority` |
| low rule without `requires_explicit_reverse_evidence: true` | `CONFIG_VALUE_ERROR` | `rules.<n>.requires_explicit_reverse_evidence` |
| empty evidence requirements | `CONFIG_VALUE_ERROR` | `rules.<n>.evidence_requirements` |
| unknown root or record field | `CONFIG_VALUE_ERROR` | exact unknown path |

Use a helper that mutates one copied fixture document, calls the public loader,
and asserts `code`, `file`, and `field`.

- [ ] **Step 2: Run the new matrix and confirm RED**

Run:

```bash
python3 -m pytest tests/test_primitive_foundation_config.py -q
```

Expected: multiple FAIL results for unimplemented validation guards.

- [ ] **Step 3: Implement the minimum guards**

Keep validation helpers private to `primitive_loader.py`. Reject the first error
in document order, preserve exact field paths, case-fold names and aliases only
for collision checks, and never normalize stored product text.

- [ ] **Step 4: Run Task 3 GREEN tests**

Run the Step 2 command. Expected: all Primitive foundation tests PASS.

- [ ] **Step 5: Run Python regression**

Run:

```bash
python3 -m pytest -q
```

Expected: all tests PASS.

---

### Task 4: Skill routing and source-document integration

**Files:**
- Modify: `destiny-personality/SKILL.md`
- Modify: `destiny-personality/checklists/stage-gates.md`
- Modify: `destiny-personality/references/methodology-index.md`
- Modify: `tests/test_skill_package.py`
- Modify: `tests/test_v2_2_config_integration.py`
- Modify: `destiny_personality_skill_docs_v2_2/00_README_V2_2.md`
- Modify: `destiny_personality_skill_docs_v2_2/10_CODEX_IMPLEMENTATION_PLAN_V2_2.md`
- Modify: `destiny_personality_skill_docs_v2_2/11_ACCEPTANCE_CRITERIA_V2_2.md`
- Modify: `destiny_personality_skill_docs_v2_2/12_SKILL_EXECUTION_ARCHITECTURE_V2_2.md`

**Interfaces:**
- Consumes: Task 1 contracts and Task 2 public development loader.
- Produces: an agent-readable Gate 1A route that cannot be mistaken for completed Gate 1.

- [ ] **Step 1: Write failing integration tests**

Require `SKILL.md` to link both contracts and the template; require the stage gate
to load ontology before resolution policy; require the methodology index to say
contracts are present but product values absent; require all four source docs to
say Gate 1A contracts are implemented while Gate 1, production semantic config,
and Phase D remain incomplete.

```python
def test_skill_routes_gate_1a_without_claiming_semantic_completion() -> None:
    text = read_skill_file("SKILL.md")
    for path in (
        "schemas/primitive-ontology.md",
        "schemas/primitive-state-resolution.md",
        "examples/primitive-foundation-template.md",
    ):
        assert f"]({path})" in text
    assert "do not treat the template as configuration" in text.lower()
    assert "Gate 1 remains incomplete" in text
```

- [ ] **Step 2: Run integration tests and confirm RED**

Run:

```bash
python3 -m pytest tests/test_skill_package.py tests/test_v2_2_config_integration.py -q
```

Expected: FAIL because routing and source-document status are absent.

- [ ] **Step 3: Add minimal routing and status language**

Keep detailed field rules in the two schema documents. `SKILL.md` only decides
when to load them and preserves the hard stop. Do not duplicate the full schemas
in the router or source documents.

- [ ] **Step 4: Run Task 4 GREEN tests**

Run the Step 2 command. Expected: all selected tests PASS.

- [ ] **Step 5: Run official Skill validation**

Run:

```bash
python3 /Users/lht/.codex/skills/.system/skill-creator/scripts/quick_validate.py destiny-personality
```

Expected: `Skill is valid!`.

---

### Task 5: Final verification and truthful status

**Files:**
- Create: `docs/superpowers/evidence/2026-09-13-gate-1a-verification.md`
- Modify after all checks pass: `destiny_personality_skill_docs_v2_2/manifest.json`
- Modify: `tests/test_v2_2_config_integration.py`

**Interfaces:**
- Consumes: all prior tasks.
- Produces: verified `gate_1a_status: implemented` and evidence without claiming Gate 1 or Phase D completion.

- [ ] **Step 1: Run full and boundary verification before status mutation**

Run:

```bash
python3 -m pytest -q
python3 /Users/lht/.codex/skills/.system/skill-creator/scripts/quick_validate.py destiny-personality
python3 scripts/verify_package.py
python3 -m pytest tests/test_skill_package.py::test_baseline_configs_are_byte_identical_to_source -v
find destiny-personality -type f \( -name '*.py' -o -name '*.pyc' -o -name '*.so' -o -name '*.dylib' -o -name '*.dll' \) -print
```

Expected: full suite PASS, `Skill is valid!`, package verification PASS, frozen
configuration PASS, and an empty forbidden-file scan.

- [ ] **Step 2: Write evidence with exact command results**

Record the Task 1–4 RED/GREEN sequence, final counts, scope scan, unchanged
baseline behavior, remaining product-value gaps, and the non-Git environment.

- [ ] **Step 3: Write a failing manifest status test**

```python
def test_manifest_declares_gate_1a_contracts_implemented() -> None:
    manifest = json.loads(
        (DOCS_DIR / "manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["gate_1a_status"] == "implemented"
    assert manifest["phase_c_status"] == "implemented"
```

Run that single test. Expected: FAIL with missing `gate_1a_status`.

- [ ] **Step 4: Update manifest and confirm GREEN**

Add only:

```json
"gate_1a_status": "implemented"
```

Run the single status test. Expected: PASS.

- [ ] **Step 5: Run final regression after the last mutation**

Run the Step 1 verification commands again. Expected: every check PASS.

- [ ] **Step 6: Final scope review**

Compare `src/destiny_personality/config_loader.py`, `pyproject.toml`, and all four
frozen YAML files with their pre-Gate-1A state. Confirm no production Primitive
asset, evaluator, Mapping, or real semantic value was introduced.
