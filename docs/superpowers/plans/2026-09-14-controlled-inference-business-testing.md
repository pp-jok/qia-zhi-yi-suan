# Controlled Inference Business Testing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `portrait` business testing possible with externally calculated facts and constrained agent interpretation while preserving the complete strict validation path.

**Architecture:** Keep the three user-facing modes and add `controlled_inference` and `strict` execution profiles. The Skill branches after calculation baseline validation, records fact assurance explicitly, enforces an anchored analysis contract and fixed portrait report, and preserves all existing strict loaders and CLIs.

**Tech Stack:** Markdown Skill contracts, YAML metadata, Python pytest structural tests, existing official Skill validator.

## Global Constraints

- Read and modify only the current project and temporary validation directories.
- Do not add calculators, Python, binaries, fixed providers, or executable dependencies to the Skill.
- Do not let a language model calculate or repair chart facts.
- Keep all five calculation candidates and six semantic candidates absent from production `configs/`.
- Preserve `facts_only` and strict audit behavior.
- Use test-first RED, observed failure, minimal GREEN, and full regression verification.
- The directory is not a Git repository; do not fabricate commit steps or claim commits.

---

### Task 1: Execution profile and gate branch

**Files:**
- Modify: `tests/test_skill_package.py`
- Modify: `destiny-personality/SKILL.md`
- Modify: `destiny-personality/checklists/preflight.md`
- Modify: `destiny-personality/checklists/stage-gates.md`
- Modify: `destiny-personality/checklists/capability-preflight.md`

**Interfaces:**
- Consumes: existing `portrait`, `facts_only`, and `audit` modes.
- Produces: `controlled_inference`, `strict`, `CALCULATION_BASELINE_CHECKED`, `FACT_BASIS_VALIDATED`, `CONTROLLED_INFERENCE_CHECKED`, `CONTROLLED_INFERENCE_ALLOWED`, and `REPORT_VALIDATED` routes.

- [x] Add structural tests requiring both profiles, the two ordered branches, `portrait` defaulting to controlled inference, and strict behavior for `facts_only`.
- [x] Run the focused test and observe failure because the profile branch is absent.
- [x] Update the Skill and checklists with the exact branch and unchanged external-capability ownership.
- [x] Run the focused tests and verify both new and legacy routing assertions pass.

### Task 2: Fact assurance and controlled-inference contracts

**Files:**
- Create: `destiny-personality/schemas/controlled-inference.md`
- Create: `destiny-personality/checklists/controlled-inference.md`
- Modify: `destiny-personality/schemas/deterministic-facts.md`
- Modify: `destiny-personality/references/execution-boundaries.md`
- Modify: `tests/test_skill_package.py`

**Interfaces:**
- Consumes: qualified capability envelopes and mechanically normalized facts.
- Produces: `project_verified`, `capability_reported`, and `none` assurance levels plus anchored claim records containing `claim_id`, `claim`, `claim_type`, `systems`, `basis_refs`, `confidence`, and `limitations`.

- [x] Add failing tests for assurance levels, no language-model chart calculation, claim anchoring, cross-system evidence, omitted node behavior, and prohibition on promoting reported facts.
- [x] Run the focused tests and observe missing-resource or missing-invariant failures.
- [x] Write the contract and checklist, link them from the Skill, and clarify the strict deterministic-facts boundary.
- [x] Run focused tests and preserve all existing deterministic contract assertions.

### Task 3: Fixed portrait report and Execution Report extension

**Files:**
- Create: `destiny-personality/schemas/portrait-report.md`
- Create: `destiny-personality/references/long-form-report-blueprint.md`
- Create: `destiny-personality/checklists/portrait-report.md`
- Modify: `destiny-personality/schemas/execution-report.md`
- Modify: `destiny-personality/SKILL.md`
- Modify: `tests/test_skill_package.py`

**Interfaces:**
- Consumes: controlled-inference claim records and fact assurance.
- Produces: `portrait-report-v1` using `long-form-personality-book-v1`, with front matter, prologue, four parts, fifty-six chapter dimensions, finale, audit appendix, and conditional Execution Report fields `execution_profile`, `fact_assurance`, `analysis_basis`, `configuration_limitations`, and `inference_disclosure`.
- Enforces chapter depth through at least three distinct evidence, mechanism, lived-expression, or integration moves in each supported chapter; repetition and paraphrase padding do not count.

- [x] Add failing tests for the exact long-form section order, all fifty-six chapter dimensions, required disclosures, per-chapter anchors or `insufficient_basis`, profile-scoped permission flags, and report validation.
- [x] Run the tests and observe missing contracts.
- [x] Implement the report schema, checklist, Execution Report rules, and router links.
- [x] Run focused tests and fix any conflict with legacy mode/report assertions.

### Task 4: Failure policy, methodology index, and runtime rules

**Files:**
- Modify: `destiny-personality/references/failure-policy.md`
- Modify: `destiny-personality/references/methodology-index.md`
- Modify: `destiny_personality_skill_docs_v2_2/09_PRODUCTION_RUNTIME_RULES.md`
- Modify: `tests/test_phase_c_skill_protocol.py`
- Modify: `tests/test_skill_package.py`

**Interfaces:**
- Consumes: mode, execution profile, missing asset, and claim dependency.
- Produces: `CONFIG_LIMITATION` warning and `INFERENCE_GUARD_ERROR` fatal classification without changing existing calculation failure meanings.

- [x] Add failing tests distinguishing safe optional-asset omission from an asset required by an emitted claim.
- [x] Run focused tests and observe the old universal `CONFIG_GAP` behavior.
- [x] Update failure precedence, runtime rules, and methodology index with profile-specific behavior.
- [x] Run focused tests and confirm strict `CONFIG_GAP` remains intact.

### Task 5: Status, business-test rubric, and release consistency

**Files:**
- Create: `destiny-personality/checklists/business-test.md`
- Modify: `destiny_personality_skill_docs_v2_2/manifest.json`
- Modify: `destiny_personality_skill_docs_v2_2/00_README_V2_2.md`
- Modify: `destiny_personality_skill_docs_v2_2/10_CODEX_IMPLEMENTATION_PLAN_V2_2.md`
- Modify: `destiny_personality_skill_docs_v2_2/11_ACCEPTANCE_CRITERIA_V2_2.md`
- Modify: `destiny_personality_skill_docs_v2_2/12_SKILL_EXECUTION_ARCHITECTURE_V2_2.md`
- Modify: `tests/test_v2_2_config_integration.py`
- Modify: `tests/test_skill_package.py`

**Interfaces:**
- Produces: `controlled_inference_status: implemented`, `business_test_workflow_status: ready`, and `strict_production_status: blocked_by_project_assets` with no false strict-completion claim.

- [x] Add failing cross-document and manifest tests for all three statuses and the business-test quality rubric.
- [x] Run focused tests and observe missing status fields and resources.
- [x] Update the four authoritative documents, manifest, Skill router, and business-test checklist.
- [x] Run integration and package tests and verify production candidate files remain absent.

### Task 6: Final verification and evidence

**Files:**
- Create: `docs/superpowers/evidence/2026-09-14-controlled-inference-business-testing.md`
- Modify: `docs/superpowers/plans/2026-09-14-controlled-inference-business-testing.md`

**Interfaces:**
- Produces: reproducible final evidence without promoting candidate assets.

- [x] Run all focused tests and the complete pytest suite.
- [x] Run Python compilation with cache under `/tmp`, Manifest JSON validation, official Skill validation, link checks, config inventory, and binary scans.
- [x] Run isolated Wheel build/install/public-import/CLI verification to prove strict developer tooling remains intact.
- [x] Record exact results, mark completed plan items, and rerun the full suite plus official Skill validation after the final documentation mutation.
