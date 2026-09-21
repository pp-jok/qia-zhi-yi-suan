# Semantic Candidate Validation CLI Design

**Date:** 2026-09-14  
**Status:** Approved by standing authorization  
**Scope:** Read-only candidate validation and human release workflow

## Decision

Extend the development reference CLI with `validate-semantic-contracts`. The
command validates a complete candidate Semantic Contract Bundle without
creating, repairing, approving, copying, or promoting any semantic asset.

The candidate directory is a required positional argument. The frozen runtime
baseline directory is selected with required `--runtime-config-dir`; keeping
the two locations explicit prevents a candidate from silently replacing the
accepted Bazi, astrology, score-model, or relation-graph baseline.

The Python package remains development tooling outside the distributable Skill.
The Skill tells the executing agent which contracts and gates to apply; it does
not invoke or depend on this CLI at runtime.

## Command contract

```text
destiny-personality-reference-validate validate-semantic-contracts \
  CANDIDATE_DIR --runtime-config-dir RUNTIME_CONFIG_DIR
```

Validation order is fixed:

1. load the runtime baseline;
2. load Primitive Ontology and Primitive State Resolution;
3. load Bazi and astrology Mapping registries;
4. load Dimension Coverage Policy;
5. load Narrative Rules;
6. validate relation-graph endpoints against the accepted ontology.

Success is one deterministic JSON object containing `status`, `command`,
versions, structural counts, and the exact-input fingerprint defined by the
follow-up Semantic Bundle Fingerprint design. Failure keeps the existing CLI contract:
exit code `2`, no stdout, and the exact `ConfigError` text on stderr. Paths are
not included in success JSON so reports remain stable across machines.

## Human release workflow

Add a Skill checklist with four states:

```text
candidate -> validated -> reviewed -> approved -> promoted
```

Only schema and cross-reference validation may move an asset to `validated`.
Human review must confirm provenance, domain meaning, methodology ownership,
and non-placeholder content. Explicit project-owner approval is required before
promotion. Promotion is an external, deliberate file operation and is not
implemented by the CLI.

An accepted semantic bundle does not prove calculation configuration is
complete and does not open `REASONING_ALLOWED` by itself.

## Non-goals

- generate or infer business semantics;
- load example templates as configuration;
- write into `destiny-personality/configs/`;
- automate approval or promotion;
- add executable code or dependencies to the Skill;
- claim Gate 1 or Phase D complete.
