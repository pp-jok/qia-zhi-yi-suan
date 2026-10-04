# Autonomous Full Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close every Core Primitive lifecycle without inventing evidence, establish delegated-autonomous governance, and ship a formal Facts → CDP → Report path that is release-ready with explicitly limited semantic coverage.

**Architecture:** Preserve the existing candidate preview and frozen legacy route, but make neither authoritative. Add a small autonomous-decision layer, a generic Bazi relation Evidence Root, a machine-readable release manifest with terminal P001–P006 states, and one formal production path built from approved active assets only. With zero valid PRIMARY_EVIDENCE and Mapping records, the formal path produces six honest `unknown` states and zero signatures/dynamics/themes/archetype, while still generating a useful limitations-first report.

**Tech Stack:** Python 3.9+, frozen dataclasses, PyYAML, JSON codecs, argparse CLI, pytest, setuptools wheel verification, Markdown/YAML governance assets.

## Global Constraints

- Work only inside `qia-zhi-yi-suan`; do not read other projects.
- Historical human Product Owner decisions remain unchanged; delegated autonomous decisions must never use or impersonate `product_owner_*` semantics.
- Decision outcomes are only `PASS`, `FAIL`, `DEFER`, or `CLOSE_ZERO`, with a durable decision record.
- Fact, Methodology, Evidence Root, PRIMARY_EVIDENCE, Mapping, Primitive state, and Renderer remain separate layers.
- `unknown != low`; zero valid PRIMARY_EVIDENCE or Mapping is a valid final result.
- `deterministic_facts.bazi.relations` may support a generic Root but never directly authorizes Dao-Shi, strength, effective control, Primitive direction, or Mapping.
- The old 14-rule Core Profile runtime remains candidate preview only and must not leak into the formal release path.
- Renderer input is validated CDP + ReportPlan only; renderer cannot inspect or reinterpret raw chart facts.
- Signatures, Dynamics, Shadow/Mature, Themes, and Archetype remain empty unless their approved source layers are non-empty.
- Default Skill architecture continues to discover and invoke external calculation capabilities; no calculator or fixed provider is bundled into the Skill.
- Preserve Python 3.9 compatibility and add no runtime dependency beyond PyYAML.
- Use synthetic fixtures only; no real user birth data or desired personality output may shape rules.
- Target release version is `0.4.0`; it is not a 1.0 maturity claim.

---

### Task 1: Delegated Autonomous Governance

**Files:**
- Create: `src/destiny_personality/autonomous_governance.py`
- Create: `governance/autonomous-completion-v1/decision_registry_v1.yaml`
- Create: `docs/governance/autonomous-completion-delegation-2026-10-04.md`
- Create: `docs/governance/decisions/README.md`
- Test: `tests/test_autonomous_decision_governance.py`

**Interfaces:**
- Produces: `AutonomousDecision`, `load_autonomous_decisions(root: Path)`, `validate_decision_binding(record, *, asset_id, asset_fingerprint)`.
- Decision records require `decision_id`, `asset_id`, `asset_type`, `outcome`, `decision_authority`, `decision_mode`, `decision_ref`, `reason`, `evidence_refs`, `test_refs`, `timestamp`, `version`, and `asset_fingerprint`.

- [ ] **Step 1: Write failing governance tests**

```python
def test_autonomous_decision_requires_delegated_authority_and_complete_audit():
    decisions = load_autonomous_decisions(PROJECT_ROOT)
    assert decisions.delegation_mode == "AUTONOMOUS_COMPLETION"
    assert all(item.decision_authority == "delegated_autonomous_executor" for item in decisions.records)

def test_autonomous_decision_cannot_claim_human_product_owner():
    with pytest.raises(ValueError, match="AUTONOMOUS_DECISION_AUTHORITY_INVALID"):
        validate_autonomous_decision({**VALID, "decision_authority": "human_product_owner"})
```

- [ ] **Step 2: Run tests and verify RED**

Run: `PYTHONPATH=src python3 -m pytest tests/test_autonomous_decision_governance.py -q`
Expected: import/module failure because the governance loader does not exist.

- [ ] **Step 3: Implement the minimal strict loader and delegation record**

```python
@dataclass(frozen=True)
class AutonomousDecision:
    decision_id: str
    asset_id: str
    asset_type: str
    outcome: str
    decision_authority: str
    decision_mode: str
    decision_ref: str
    reason: str
    evidence_refs: Tuple[str, ...]
    test_refs: Tuple[str, ...]
    timestamp: str
    version: str
    asset_fingerprint: str
```

Reject missing fields, unknown outcomes, human authority, manual mode, empty evidence/test refs, and duplicate IDs. The registry initially contains only decisions created by later tasks; an empty list is valid.

- [ ] **Step 4: Verify GREEN and commit**

Run: `PYTHONPATH=src python3 -m pytest tests/test_autonomous_decision_governance.py -q`
Commit: `feat: add delegated autonomous governance`

### Task 2: Generic Bazi Relation Root and P004 Final Closure

**Files:**
- Modify: `candidates/semantic-mechanisms-v1/semantic_evidence_root_contract_v1.yaml`
- Modify: `candidates/semantic-mechanisms-v1/semantic_evidence_root_registry_v1.yaml`
- Modify: `src/destiny_personality/semantic_mechanisms.py`
- Modify: `governance/autonomous-completion-v1/decision_registry_v1.yaml`
- Create: `docs/governance/decisions/auto-er-bz-relation-instance-v1.md`
- Create: `docs/reviews/primitives/P004-final-research-report.md`
- Test: `tests/test_autonomous_evidence_root.py`
- Modify: `tests/test_semantic_evidence_roots.py`

**Interfaces:**
- Adds Root `ER-BZ-RELATION-INSTANCE-V1` for `deterministic_facts.bazi.relations`.
- Approved Root supports either legacy human `product_owner_decision_ref` or the exact autonomous triplet `decision_authority`, `decision_mode`, `decision_ref`; never both.

- [ ] **Step 1: Write failing Root authority and scope tests**

```python
def test_generic_relation_root_is_identity_only_and_autonomously_decided():
    root = root_by_id("ER-BZ-RELATION-INSTANCE-V1")
    assert root["scope"]["identity_fields"] == ["relation_type", "participant_refs", "rule_version"]
    assert root["decision_authority"] == "delegated_autonomous_executor"
    assert "dao_shi_assertion" in root["prohibited_use"]
```

Also test legacy human roots still load, autonomous roots cannot set `product_owner_decision_ref`, and missing registry decision fails closed.

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=src python3 -m pytest tests/test_autonomous_evidence_root.py tests/test_semantic_evidence_roots.py -q`
Expected: missing root / unsupported autonomous authority.

- [ ] **Step 3: Implement Root and backward-compatible authority validation**

Keep the Root generic. Approved use is limited to `fact_instance_identification` and `candidate_mechanism_evidence_reference`. Prohibit effective control, strength, Dao-Shi, rescue, Primitive state, and Mapping creation. Bind its decision record to the canonical relation policy fingerprint.

- [ ] **Step 4: Close P004 without creating PE or Mapping**

Record Astrology as `CLOSED_UNDER_CURRENT_HELLENISTIC_METHODOLOGY`, Bazi execution as `DEFERRED_WITH_REASON / METHOD_RESEARCH_SATURATED`, overall resolver capability as `UNKNOWN`, PRIMARY_EVIDENCE and Mapping as `CLOSE_ZERO`.

- [ ] **Step 5: Verify and commit**

Run: `PYTHONPATH=src python3 -m pytest tests/test_autonomous_decision_governance.py tests/test_autonomous_evidence_root.py tests/test_semantic_evidence_roots.py tests/test_p004_po_gate_closure.py -q`
Commit: `feat: approve generic Bazi relation evidence root`

### Task 3: All-Core Primitive Lifecycle Closure

**Files:**
- Create: `src/destiny_personality/release_assets/v1/primitive_coverage_v1.yaml`
- Create: `src/destiny_personality/release_manifest.py`
- Create: `docs/reviews/semantic-asset-master-backlog.md`
- Create: `docs/reviews/primitives/P001-final-research-report.md`
- Create: `docs/reviews/primitives/P002-final-research-report.md`
- Create: `docs/reviews/primitives/P003-final-research-report.md`
- Create: `docs/reviews/primitives/P005-final-research-report.md`
- Create: `docs/reviews/primitives/P006-final-research-report.md`
- Create: `docs/reviews/semantic-core-final-coverage-report.md`
- Test: `tests/test_release_primitive_coverage.py`

**Interfaces:**
- Produces `ReleaseManifest` and `PrimitiveClosure`.
- P001–P006 are Core; Extended inventory is explicitly empty/deferred for v1.
- P001/P002/P003/P005/P006 finish `CLOSED_NO_DEFENSIBLE_CONSTRUCT_UNDER_REVIEWED_ASSETS` with state capability `UNKNOWN`, zero PE, zero Mapping.
- P004 uses Task 2's system-specific closure and overall `UNKNOWN`.

- [ ] **Step 1: Write failing coverage completeness tests**

```python
def test_every_core_primitive_has_terminal_lifecycle_state():
    manifest = load_release_manifest()
    assert set(manifest.core_primitives) == {"P001", "P002", "P003", "P004", "P005", "P006"}
    assert all(item.final_status not in {"TODO", "TBD", "PENDING"} for item in manifest.core_primitives.values())
    assert all(item.resolver_capability == "unknown" for item in manifest.core_primitives.values())
```

Assert zero active PRIMARY_EVIDENCE and Mapping refs are explicit, not omitted.

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=src python3 -m pytest tests/test_release_primitive_coverage.py -q`

- [ ] **Step 3: Build manifest and evidence-based closure reports**

Use existing C1/C2 rule remediation, P004 research, and zero Mapping registries as reviewed evidence. Do not create new source claims merely to fill coverage. Each report answers construct, sources, method, facts, Root, PE, Mapping, counterevidence, contexts, limitations, and saturation.

- [ ] **Step 4: Verify and commit**

Run: `PYTHONPATH=src python3 -m pytest tests/test_release_primitive_coverage.py tests/test_c1_primitive_ontology_v2.py tests/test_mapping_v2_registry.py -q`
Commit: `docs: close all core primitive lifecycles`

### Task 4: Formal Resolver, Alignment, and Core Destiny Profile

**Files:**
- Create: `src/destiny_personality/release_semantics.py`
- Create: `src/destiny_personality/core_destiny_profile.py`
- Create: `src/destiny_personality/core_destiny_profile_codec.py`
- Create: `src/destiny_personality/core_destiny_profile_validation.py`
- Modify: `src/destiny_personality/core_profile_models.py`
- Test: `tests/test_release_semantics.py`
- Test: `tests/test_core_destiny_profile.py`

**Interfaces:**
- Produces `resolve_release_primitive_states(mappings, manifest)`, `align_release_states(...)`, `build_core_destiny_profile(facts, *, fact_assurance)` and deterministic CDP JSON codec.
- Formal builder reads only the release manifest and approved active mapping bundle. It must never import candidate mapping registries.

- [ ] **Step 1: Write failing resolver and non-inflation tests**

```python
def test_no_mapping_produces_unknown_not_low():
    states = resolve_release_primitive_states((), load_release_manifest())
    assert {item.state for item in states.values()} == {"unknown"}

def test_cross_system_agreement_does_not_increase_salience():
    alignment = align_release_states(BAZI_HIGH, ASTROLOGY_HIGH)
    assert alignment.status == "validation"
    assert alignment.salience_delta == 0
```

Test context promotion requires explicit global authority or at least two representative contexts with independent roots, same direction, and no material countercontext.

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=src python3 -m pytest tests/test_release_semantics.py tests/test_core_destiny_profile.py -q`

- [ ] **Step 3: Implement formal zero-safe pipeline**

Build a complete `CoreDestinyProfile` with separate fact and semantic assurance, P001–P006 states, per-system candidate tuples, cross-system `non_comparable` results when one/both systems lack approved evidence, zero downstream formations, contradictions, limitations, unresolved questions, and audit trail.

- [ ] **Step 4: Implement deterministic codec and validation**

Reject missing primitive coverage, unknown-as-low coercion, cross-system salience inflation, untraceable downstream records, semantic assurance copied from fact assurance, and any candidate-only rule ref in the formal profile.

- [ ] **Step 5: Verify and commit**

Run: `PYTHONPATH=src python3 -m pytest tests/test_release_semantics.py tests/test_core_destiny_profile.py tests/test_core_profile_codec.py tests/test_semantic_core_nonzero_pipeline.py -q`
Commit: `feat: build formal zero-safe Core Destiny Profile`

### Task 5: CDP Report Planner, Renderer, and Public CLI

**Files:**
- Modify: `src/destiny_personality/report_plan_models.py`
- Modify: `src/destiny_personality/report_planner.py`
- Create: `src/destiny_personality/release_renderer.py`
- Modify: `src/destiny_personality/cli.py`
- Modify: `src/destiny_personality/__init__.py`
- Test: `tests/test_release_report_planner.py`
- Test: `tests/test_release_renderer.py`
- Test: `tests/test_release_cli.py`

**Interfaces:**
- Produces `build_release_report_plan(profile, renderer_profile)` and `render_release_report(profile, plan)`.
- Supports `concise-portrait-v1`, `standard-portrait-v1`, `dynamic-long-form-v1`, and `legacy-long-form-v2` compatibility handoff.
- CLI: `build-release-report FACTS --qualification QUALIFICATION --mode MODE --output OUTPUT`.

- [ ] **Step 1: Write failing planner containment tests**

```python
def test_sparse_profile_still_plans_an_honest_report():
    plan = build_release_report_plan(ALL_UNKNOWN_PROFILE, "standard-portrait-v1")
    assert "limitations" in plan.section_ids
    assert not any(section.startswith("primitive:") for section in plan.section_ids)

def test_renderer_cannot_add_unplanned_claim():
    with pytest.raises(ValueError, match="REPORT_CONTAINMENT_VIOLATION"):
        render_release_report(PROFILE, TAMPERED_PLAN)
```

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=src python3 -m pytest tests/test_release_report_planner.py tests/test_release_renderer.py tests/test_release_cli.py -q`

- [ ] **Step 3: Implement planner and natural-language renderer**

Planner selects sections and refs only from CDP. Renderer emits `facts_summary`, `core_profile`, `report`, `assurance`, `limitations`, and `audit_refs`; uses uncertainty language; omits unsupported sections; never reads facts or registries. `legacy-long-form-v2` returns a separate frozen compatibility handoff rather than reusing new semantics.

- [ ] **Step 4: Implement CLI from qualified facts**

Use `load_qualified_deterministic_facts`, formal CDP builder, planner, and renderer. Missing methodology evidence degrades to omitted sections; invalid fact qualification still fails the whole command.

- [ ] **Step 5: Verify and commit**

Run: `PYTHONPATH=src python3 -m pytest tests/test_release_report_planner.py tests/test_release_renderer.py tests/test_release_cli.py tests/test_cli.py -q`
Commit: `feat: add contained release report pipeline`

### Task 6: End-to-End, Degradation, Consistency, and Legacy Gates

**Files:**
- Create: `tests/fixtures/end_to_end/scenarios_v1.yaml`
- Create: `tests/test_release_end_to_end.py`
- Create: `tests/test_cross_agent_core_consistency.py`
- Create: `tests/test_release_traceability.py`
- Modify: `tests/test_skill_package.py`
- Modify: `destiny-personality/SKILL.md`
- Modify: `destiny-personality/references/core-profile-runtime.md`

**Interfaces:**
- Synthetic scenario matrix covers known time, unknown hour/stable-only, time boundary, timezone, DST, diverse Bazi/Astrology structures, zero/low coverage, test-only high candidate coverage, contradiction, and context differentiation.

- [ ] **Step 1: Write failing E2E tests**

```python
@pytest.mark.parametrize("scenario", load_scenarios())
def test_birth_input_to_accepted_facts_to_cdp_to_report(scenario):
    result = execute_synthetic_external_provider_flow(scenario)
    assert result.report["audit_refs"]
    assert result.report["assurance"]["fact"] != result.report["assurance"]["semantic"]
```

Add normalized-equivalence repeats, unknown propagation, no salience inflation, report traceability, and frozen legacy 56-chapter contract checks.

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=src python3 -m pytest tests/test_release_end_to_end.py tests/test_cross_agent_core_consistency.py tests/test_release_traceability.py tests/test_skill_package.py -q`

- [ ] **Step 3: Implement only fixture helpers and Skill routing required to pass**

The external-provider helper is test-only and returns precomputed synthetic facts; it is not a calculator. Update Skill routing to distinguish formal limited-coverage report, candidate preview, controlled-inference legacy, and strict failure/degradation.

- [ ] **Step 4: Verify and commit**

Run: `PYTHONPATH=src python3 -m pytest tests/test_release_end_to_end.py tests/test_cross_agent_core_consistency.py tests/test_release_traceability.py tests/test_skill_package.py tests/test_phase_c_skill_protocol.py -q`
Commit: `test: close release end-to-end quality gates`

### Task 7: Package, License, Documentation, and Version Closure

**Files:**
- Modify: `pyproject.toml`
- Modify: `scripts/verify_package.py`
- Modify: `tests/test_verify_package_script.py`
- Modify: `README.md`
- Create: `CHANGELOG.md`
- Create: `THIRD_PARTY_NOTICES.md`
- Create: `docs/architecture/autonomous-release-architecture.md`
- Create: `docs/release/v0.4.0-release-readiness.md`
- Create: `docs/reviews/archive/README.md`
- Modify: `.github/workflows/tests.yml`

**Interfaces:**
- Package version `0.4.0`.
- Wheel includes canonical and release YAML assets and can execute the formal limited-coverage report smoke test from an isolated venv.

- [ ] **Step 1: Write failing package metadata and verifier tests**

Assert version, PEP 621 readme/license metadata, packaged release assets, installed CDP build/render smoke, and no calculator/forbidden binary bundled.

- [ ] **Step 2: Verify RED**

Run: `PYTHONPATH=src python3 -m pytest tests/test_verify_package_script.py tests/test_skill_package.py -q`

- [ ] **Step 3: Update packaging and installed verification**

Add `release_assets/v1/*.yaml` to package data. Extend the verifier to import/load the release manifest, build a formal sparse CDP and render it inside the installed venv. Preserve the external Skill/config boundary explicitly.

- [ ] **Step 4: Complete public documentation and license audit**

README accurately states limited coverage and unknown behavior. Record PyYAML/pytest status, no bundled Swiss Ephemeris/pyswisseph/font/text assets, and archive classification without moving tested historical paths.

- [ ] **Step 5: Verify and commit**

Run: `PYTHONPATH=src python3 -m pytest tests/test_verify_package_script.py tests/test_skill_package.py -q`
Run: `python3 scripts/verify_package.py`
Commit: `chore: prepare v0.4.0 limited coverage release`

### Task 8: Final Autonomous Audit, Release Decision, and Publication

**Files:**
- Create: `docs/reviews/autonomous-completion-final-report.md`
- Create: `docs/governance/decisions/auto-release-v0.4.0.md`
- Modify: `governance/autonomous-completion-v1/decision_registry_v1.yaml`
- Modify: `docs/release/v0.4.0-release-readiness.md`

**Interfaces:**
- Final outcome may be `RELEASE_READY_WITH_LIMITED_SEMANTIC_COVERAGE` only when every Core Primitive is terminal, all active assets have valid decisions, candidate leakage tests pass, E2E/report containment/legacy/assurance gates pass, full pytest passes, wheel verification passes, and CI passes.

- [ ] **Step 1: Run five-role autonomous review**

Review as Research, Architecture, Semantic, Test, and Product reviewer. Record unsupported bridges, layer mixing, nearby-construct leakage, happy-path-only tests, readability/template collapse, and fixes. Any Critical/Important finding is fixed and re-reviewed.

- [ ] **Step 2: Run fresh complete verification**

Run: `PYTHONPATH=src python3 -m pytest -q`
Run: `python3 scripts/verify_package.py`
Run: `git diff --check`
Expected: zero failures and package verification terminal success.

- [ ] **Step 3: Create the final report and bound decision**

Record baseline, final HEAD, assets/counts, six Primitive closures, zero PE/Mapping, zero formations, formal CDP/Planner/Renderer, legacy boundary, E2E/package results, limitations, deferrals, rejections, and machine-readable summary. Bind release decision to the final asset fingerprint and exact test refs.

- [ ] **Step 4: Synchronize, publish, and wait for CI**

Fetch latest `main`; merge/rebase only if content-safe; push branch; open PR; self-review; wait for Python 3.9/3.11/3.12 and package CI; fix any failures; merge without deleting the active worktree prematurely.

- [ ] **Step 5: Tag only after merged-main verification**

Create annotated tag `v0.4.0-autonomous-limited-coverage` and GitHub release notes only if merged `main` still passes all release gates. Otherwise record `NOT_READY` with exact blocker and do not tag.

---

## Self-Review

- Spec coverage: all 32 stages are represented either by an implementation task or an explicit zero/closed result. Core is P001–P006; Extended is explicitly absent/deferred and cannot block v1.
- No asset is approved from a raw fact, old candidate mapping, desired output, or renderer wording.
- P004 generic relation Root and P004 semantic closure remain separate.
- The formal CDP route is active even with zero semantic conclusions; downstream formation is correctly zero rather than blocked by unfinished engineering.
- Legacy compatibility stays separate and frozen.
- No placeholders, artificial conclusion quota, production calculator dependency, or user approval checkpoint remains.
