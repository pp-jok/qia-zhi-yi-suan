# Gate 1D Narrative Rules and Semantic Contract Bundle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans`. This is a non-Git workspace; passing checkpoints replace commits.

**Goal:** Add a versioned Narrative guard contract and ordered semantic bundle validator without adding production semantics.

**Architecture:** The standalone Narrative loader consumes accepted Primitive and dimension assets. The bundle loader composes all semantic loaders and validates relation graph endpoints last, while earlier calculation gaps remain authoritative.

**Tech Stack:** Markdown, YAML, Python frozen dataclasses, PyYAML, pytest.

## Constraints

- No production `narrative_rules_v1.yaml` or other semantic placeholders.
- No prose templates, claims, archetypes, or inferred business values.
- Skill contains no Python or third-party executable.
- TDD first; preserve prior APIs and four frozen YAML files.

### Task 1: Narrative loader

- [ ] Create `tests/test_narrative_rules.py` with a valid synthetic asset and
  assert immutable ordered output; run and observe missing API RED.
- [ ] Create `narrative_models.py`, `narrative_loader.py`, and public exports;
  require exact versions, sections, seven fixed invariants, rule uniqueness,
  source-kind vocabulary, section coverage, chart anchors, and declarative
  constraints; rerun GREEN.
- [ ] Add failure tests for missing/parse/type/version/value/reference cases and
  precise field paths; require the complete test module to pass.

### Task 2: Semantic bundle

- [ ] Create `tests/test_semantic_contract_bundle.py` with monkeypatched loader
  order and a synthetic accepted bundle; observe missing API RED.
- [ ] Add `SemanticContractBundle` and
  `load_semantic_contract_bundle(config_dir, runtime_config)` using the exact
  five-step order from the design.
- [ ] Test that an unknown relation endpoint reports `CONFIG_VALUE_ERROR` with
  `primitive_relation_graph_v1.yaml` and `relations.<n>.<side>`, and that an
  earlier missing ontology wins.

### Task 3: Skill and release state

- [ ] Add failing Skill tests for `schemas/narrative-rules.md`, the template,
  fixed invariants, bundle order, and absent production asset.
- [ ] Add the contract/template and route after dimension coverage; explicitly
  state that bundle acceptance never bypasses calculation configuration.
- [ ] Add failing then passing `gate_1d_status` integration tests and synchronize
  the four authoritative documents and manifest.
- [ ] Run full pytest, official Skill validation, syntax/JSON/frozen/inventory
  checks, and Wheel build-install-run verification after the final mutation.
