# Core Portrait Semantic / Presentation Remediation Plan

> **Goal:** make the Candidate Core Profile safe to evolve as two explicit layers: a frozen semantic IR and a versioned user-facing presentation layer.

## Scope and release target

Release `v0.3.5-core-portrait-semantic-presentation` keeps the current D1-only candidate boundary. It adds no birth-chart calculation and does not claim production authorization.

## Implementation order

1. **Freeze the layer boundary.** Split semantic and presentation fingerprints, persist the presentation fingerprint on every portrait, and update calibration assets to the new semantic fingerprint. Regression tests prove that presentation-only changes cannot alter semantic fingerprints or normalized IR, while mapping changes do.
2. **Preserve semantic direction in Chinese.** Add `high_expression` and `low_expression` for every approved primitive. Resolve a summary item's direction from its state and context states; render only localized context labels and expressions in overview, item, evidence, and comparison sections. Add a user-view guard that forbids raw `P00x` IDs and raw context keys.
3. **Close fact-scope and runtime contracts.** Derive `CandidateFactScope` only from `NormalizedBirthTime.fact_mode`, reject stable-only facts containing ascendant/MC/house/hour-pillar data, and provide a deterministic JSON codec plus `build-core-profile` CLI that consumes qualified facts rather than calculating charts.
4. **Make distribution verification truthful.** Resolve the wheel name from the project `pyproject.toml`, test hyphen/underscore normalization, and add an isolated Python 3.11 package-verification CI job.
5. **Package and release hygiene.** Make section-count language explicitly target-based, remove any remotely tracked generated egg-info paths, mirror candidate assets into the packaged tree, run focused then full gates, publish a pre-release, and independently install/test the release archive.

## Gates

- **R2:** direction-aware user output, no raw identifiers/contexts in user sections, and context states retain scoped high/low direction.
- **U2:** facts JSON builds a valid candidate profile without running a calculation engine; stable-only contradictions fail closed.
- **B:** package verifier discovers the actual distribution name; CI package job and clean remote tree are verified.

## Non-goals

- No production semantic authorization, dynamic formation, relation graph, chart calculation, or full report expansion.
- No semantic inference from presentation text.
