# 掐指一算 GitHub Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a sanitized standalone copy of the Destiny Personality Skill as the public GitHub repository `pp-jok/qia-zhi-yi-suan`.

**Architecture:** Build an isolated release tree under `release/qia-zhi-yi-suan` with repository documentation at the root and the validated Skill under `destiny-personality/`. Keep all user reports and project-development files outside the release tree, validate locally, then create and verify one public GitHub repository.

**Tech Stack:** Markdown, Git, GitHub CLI, Skill Creator `quick_validate.py`, ripgrep.

## Global Constraints

- Publish only the reusable Skill and repository-level `README.md`, `LICENSE`, and `.gitignore`.
- Do not publish personal reports, PDFs, real birth data, local absolute paths, temporary scripts, tests, or development documents.
- Repository name: `qia-zhi-yi-suan`.
- Display name: `掐指一算`.
- Subtitle: `An Auditable Destiny & Personality Oracle`.
- Description: `以八字为骨，以星盘为镜，将命纹织成一部可审计的人格秘典。`
- License: MIT.
- Default branch: `main`.
- Stop rather than rename if `pp-jok/qia-zhi-yi-suan` already exists.

---

### Task 1: Assemble the isolated release tree

**Files:**
- Create: `release/qia-zhi-yi-suan/destiny-personality/**`
- Create: `release/qia-zhi-yi-suan/.gitignore`

**Interfaces:**
- Consumes: current `destiny-personality/` Skill package.
- Produces: a release tree containing only repository metadata and the nested Skill folder.

- [x] **Step 1: Confirm the remote name is unused**

Run:

```bash
gh repo view pp-jok/qia-zhi-yi-suan
```

Expected: non-zero exit with repository not found. If it exists, stop without changing it.

- [x] **Step 2: Create the release directory and copy the Skill**

Run:

```bash
mkdir -p release/qia-zhi-yi-suan
cp -R destiny-personality release/qia-zhi-yi-suan/destiny-personality
```

Expected: exactly one nested `destiny-personality` Skill package.

- [x] **Step 3: Replace the real-case compact-input example**

In the release copy only, replace `1986.5.25.11:55 北京 男` and its normalized values with the neutral documentation example `2000.1.1.00:00 上海 未指定`, `2000-01-01`, `00:00`, `上海`, and `sex: unspecified` in:

- `release/qia-zhi-yi-suan/destiny-personality/SKILL.md`
- `release/qia-zhi-yi-suan/destiny-personality/schemas/birth-input.md`

- [x] **Step 4: Add the repository ignore file**

Create `release/qia-zhi-yi-suan/.gitignore` with:

```gitignore
.DS_Store
__pycache__/
*.py[cod]
```

### Task 2: Add the mystical public-facing documentation

**Files:**
- Create: `release/qia-zhi-yi-suan/README.md`
- Create: `release/qia-zhi-yi-suan/LICENSE`

**Interfaces:**
- Consumes: the approved public identity and existing Skill contracts.
- Produces: installable public documentation with mystical tone and explicit safety boundaries.

- [x] **Step 1: Write README.md**

The README must contain, in this order:

1. `# 掐指一算`
2. Subtitle `An Auditable Destiny & Personality Oracle`
3. Opening line `观星轨，察五行，循证据之线，照见性格深处的命纹。`
4. A concise positioning statement that this is an agent Skill and validation framework, not bundled calculation software.
5. Capabilities: compact birth input, qualified external calculation calls, controlled inference, fifty-six-chapter portrait, audit appendix, strict stop gates.
6. Neutral input example `2000.1.1.00:00 上海 未指定`.
7. Installation commands cloning the repository and copying `destiny-personality` into `~/.codex/skills/`.
8. Example prompt using `$destiny-personality`.
9. Directory tree.
10. Quality gates and the distinction between `controlled_inference` and `strict`.
11. A disclosure that the output is traditional and inferential, not scientific diagnosis, guaranteed behavior, or prediction.
12. MIT license notice.

- [x] **Step 2: Add the MIT license**

Use the standard MIT License text with `Copyright (c) 2026 pp-jok`.

### Task 3: Validate the release contents

**Files:**
- Inspect: `release/qia-zhi-yi-suan/**`

**Interfaces:**
- Consumes: completed release tree.
- Produces: evidence that the package is valid and contains no scoped private data.

- [x] **Step 1: Verify the public file boundary**

Run:

```bash
find release/qia-zhi-yi-suan -type f | sort
```

Expected: only root metadata and files below `destiny-personality/`; no `output/`, `docs/`, tests, PDF, or temporary files.

- [x] **Step 2: Run sensitive-data and absolute-path scans**

Run:

```bash
rg -n '1986\.5\.25|1986-05-25|北京|/Users/|Downloads/|命格人格书\.pdf|gho_|api[_-]?key|password|secret' release/qia-zhi-yi-suan
```

Expected: no personal birth data, absolute local path, credential, or report filename. Generic words such as `secret` in a security prohibition must be manually inspected rather than blindly rejected.

- [x] **Step 3: Validate the copied Skill**

Run:

```bash
python3 /Users/lht/.codex/skills/.system/skill-creator/scripts/quick_validate.py release/qia-zhi-yi-suan/destiny-personality
```

Expected: `Skill is valid!`.

- [x] **Step 4: Run the source Skill contract tests**

Run:

```bash
python3 -m pytest tests/test_skill_package.py -q
```

Expected: all Skill package contract tests pass.

- [x] **Step 5: Confirm source and release differ only by approved sanitization**

Run:

```bash
diff -ru destiny-personality release/qia-zhi-yi-suan/destiny-personality
```

Expected: differences only in the compact-input example and its normalized values.

### Task 4: Create and publish the Git repository

**Files:**
- Create: `release/qia-zhi-yi-suan/.git/**`

**Interfaces:**
- Consumes: validated release tree and authenticated GitHub CLI account `pp-jok`.
- Produces: public repository `https://github.com/pp-jok/qia-zhi-yi-suan` on branch `main`.

- [x] **Step 1: Initialize and commit locally**

Run inside `release/qia-zhi-yi-suan`:

```bash
git init -b main
git add .
git commit -m "feat: unveil the Qia Zhi Yi Suan oracle skill"
```

Expected: one root commit and a clean working tree.

- [x] **Step 2: Create the public repository and push**

Run:

```bash
gh repo create pp-jok/qia-zhi-yi-suan --public --source . --remote origin --push --description '以八字为骨，以星盘为镜，将命纹织成一部可审计的人格秘典。'
```

Expected: remote repository created and `main` pushed without force.

- [x] **Step 3: Add repository topics**

Run:

```bash
gh repo edit pp-jok/qia-zhi-yi-suan --add-topic agent-skill --add-topic bazi --add-topic western-astrology --add-topic personality --add-topic oracle --add-topic chinese-metaphysics
```

Expected: all six topics appear on the repository.

### Task 5: Verify the published repository

**Files:**
- Inspect: local Git state and GitHub repository metadata.

**Interfaces:**
- Consumes: published repository.
- Produces: final release evidence and URL.

- [x] **Step 1: Verify local Git state**

Run:

```bash
git status --short
git branch --show-current
git log -1 --oneline
```

Expected: empty status, branch `main`, and the release commit.

- [x] **Step 2: Verify remote metadata**

Run:

```bash
gh repo view pp-jok/qia-zhi-yi-suan --json url,visibility,defaultBranchRef,description,repositoryTopics
```

Expected: public visibility, URL `https://github.com/pp-jok/qia-zhi-yi-suan`, default branch `main`, approved description, and six topics.

- [x] **Step 3: Verify remote files**

Run:

```bash
gh api repos/pp-jok/qia-zhi-yi-suan/contents --jq '.[].name'
```

Expected root entries: `.gitignore`, `LICENSE`, `README.md`, and `destiny-personality`.
