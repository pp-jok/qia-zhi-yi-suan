# Semantic Candidate Validation CLI Implementation Plan

**Goal:** Provide one read-only development command for validating a complete
candidate Semantic Contract Bundle and document the human-controlled release
gate without adding production semantics.

**Architecture:** The CLI explicitly combines an accepted runtime baseline with
a separate candidate semantic directory, delegates all validation to the
existing loaders, and emits a deterministic summary. The distributable Skill
contains only workflow and validation instructions.

**Tech Stack:** Python, argparse, frozen dataclasses, pytest, Markdown.

## Constraints

- TDD first and preserve `validate-config` compatibility.
- Require an explicit runtime baseline directory.
- Read-only validation; no copy, approval, or promotion command.
- No production semantic YAMLs and no template-derived values.
- No Python, executable, or fixed tool dependency inside the Skill.

### Task 1: CLI contract

- [x] Add failing tests for parser routing, load order, stable success JSON,
  explicit runtime baseline, and deterministic failure behavior.
- [x] Implement `validate-semantic-contracts` with the smallest direct CLI
  change and reuse `load_runtime_config` plus
  `load_semantic_contract_bundle`.
- [x] Preserve existing `validate-config` output and exit codes.

### Task 2: Candidate release workflow

- [x] Add failing Skill-package tests for the candidate validation checklist,
  state transitions, human approval, no automatic promotion, and router link.
- [x] Add the checklist and route it from `SKILL.md` at
  `SEMANTIC_CONFIG_CHECKED`.
- [x] State that the Skill does not require or invoke the development CLI.

### Task 3: Verification

- [x] Run focused CLI and Skill tests.
- [x] Run full pytest, syntax checks, JSON validation, frozen-config checks,
  forbidden-binary scan, production inventory, official Skill validation, and
  Wheel build-install-run verification after the final mutation.
