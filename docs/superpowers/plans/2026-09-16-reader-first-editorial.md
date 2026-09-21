# Reader-First Editorial Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Separate immersive reader prose from audit mechanics and restore one memorable archetype without losing merged analysis.

**Architecture:** Strengthen the Portrait Report rendering contract first, then edit only the report's presentation layer. Keep structured provenance and limitations unchanged in the audit appendix and regenerate both PDF artifacts from the revised Markdown.

**Tech Stack:** Markdown contracts, pytest, ReportLab, pypdf, Poppler.

## Global Constraints

- Keep all 56 chapter dimensions and three-to-five paragraph depth.
- Do not remove calculated facts, traditional interpretations, or limitations.
- Do not expose internal workflow language in reader-facing chapters.
- Keep `有根的远行者` as the dominant archetype and `有根的探索者` as a cognitive subtype.

---

### Task 1: Reader-first rendering contract

**Files:**
- Modify: `tests/test_skill_package.py`
- Modify: `destiny-personality/schemas/portrait-report.md`
- Modify: `destiny-personality/references/long-form-report-blueprint.md`
- Modify: `destiny-personality/checklists/portrait-report.md`
- Modify: `destiny-personality/SKILL.md`

- [x] Add failing assertions for audit-only source qualification, dominant archetype hierarchy, and prohibition of internal workflow narration in prose.
- [x] Run the focused contract test and observe the expected failure.
- [x] Add the minimal contract, blueprint, checklist, and routing rules.
- [x] Re-run the focused test and require exit code 0.

### Task 2: Editorial rewrite

**Files:**
- Modify: `output/reports/1986-05-25-北京-命格人格书.md`

- [x] Move cover and chapter source qualifications into the existing audit appendix.
- [x] Rewrite traditional conclusions as natural reader prose without changing their assurance.
- [x] Restore `有根的远行者` as the main archetype and retain `有根的探索者` as its cognitive subtype.
- [x] Differentiate judgment, expression, choice, interpretation, and public authorship chapters.
- [x] Recast repeated procedures as mature-expression prose while retaining useful distinctions.
- [x] Run the chapter and phrase audit.

### Task 3: PDF and full verification

**Files:**
- Modify: `output/pdf/1986-05-25-北京-命格人格书-完整版.pdf`
- Modify: `output/reports/1986-05-25-北京-命格人格书.pdf`

- [x] Render both PDF artifacts.
- [x] Inspect representative pages for narrative hierarchy and layout defects.
- [x] Run the full pytest suite and official Skill validator.
- [x] Verify both PDF artifacts have identical pages and extracted text.
