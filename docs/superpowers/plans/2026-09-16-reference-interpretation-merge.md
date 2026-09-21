# Reference Interpretation Merge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Merge approved reference interpretations into the controlled portrait while preserving source and assurance boundaries.

**Architecture:** Extend the portrait contract with an optional reference-derived interpretation layer, then update the current 56-chapter report and its audit appendix. Regenerate the PDF from the Markdown source and validate both framework behavior and rendered output.

**Tech Stack:** Markdown contracts, pytest contract tests, ReportLab PDF renderer, pypdf/Poppler validation.

## Global Constraints

- Read and modify only the current project plus the explicitly supplied reference PDF.
- Do not package the reference PDF or external calculation software in the Skill.
- Never promote a reference-derived interpretation to `project_verified`.
- Keep all 56 chapter dimensions and the existing controlled-inference disclosures.

---

### Task 1: Reference-derived interpretation contract

**Files:**
- Modify: `tests/test_skill_package.py`
- Modify: `destiny-personality/schemas/portrait-report.md`
- Modify: `destiny-personality/references/long-form-report-blueprint.md`
- Modify: `destiny-personality/checklists/portrait-report.md`
- Modify: `destiny-personality/SKILL.md`

**Interfaces:**
- Consumes: a user-approved reference report and accepted calculation facts.
- Produces: provenance-preserving `reference_traditional_interpretation` claims.

- [x] Add assertions requiring `reference_traditional_interpretation`, user approval, fact-conflict rejection, and assurance non-promotion.
- [x] Run `python3 -m pytest tests/test_skill_package.py::test_portrait_report_contract_has_fixed_sections_and_disclosures -q` and observe failure on the absent contract language.
- [x] Add the minimal schema, blueprint, checklist, and router rules.
- [x] Re-run the focused test and require exit code 0.

### Task 2: Merge the current portrait

**Files:**
- Modify: `output/reports/1986-05-25-北京-命格人格书.md`

**Interfaces:**
- Consumes: the existing calculated facts, controlled claims, and approved reference interpretations.
- Produces: a merged 56-chapter reader-facing book with an auditable source split.

- [x] Add the traditional strength/balance and dignity views with explicit traditional-reference language.
- [x] Add identity continuity, interpersonal standard pressure, and life-authorship insights in their relevant chapters.
- [x] Merge the two archetype names without deleting either interpretation.
- [x] Update the audit appendix so the new layer is sourced, limited, and excluded from strict certification.
- [x] Run the local chapter audit and require 56 ordered chapters, three-to-five paragraphs per chapter, and zero duplicate long paragraphs.

### Task 3: Render and verify

**Files:**
- Modify: `output/pdf/1986-05-25-北京-命格人格书-完整版.pdf`
- Modify: `output/reports/1986-05-25-北京-命格人格书.pdf`

**Interfaces:**
- Consumes: the merged Markdown report.
- Produces: two matching, visually validated PDF artifacts.

- [x] Render both PDF paths with the existing ReportLab renderer.
- [x] Render representative pages with `pdftoppm` and inspect for clipping, broken glyphs, hierarchy, and footer errors.
- [x] Run `python3 -m pytest -q` and require all tests to pass.
- [x] Run `python3 /Users/lht/.codex/skills/.system/skill-creator/scripts/quick_validate.py destiny-personality` and require `Skill is valid!`.
