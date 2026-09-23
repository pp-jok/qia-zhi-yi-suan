# Master Semantic Core Completion Implementation Plan

**Goal:** Build the complete candidate-only Semantic Core engineering path while preserving zero semantic activation until explicit Product Owner decisions exist.

**Architecture:** Extend the existing C2-SM governance module with role authority, Mapping v2 candidate lifecycle, promotion/rollback records, and isolated fingerprints. Add a single downstream core pipeline that consumes only approved Mapping output; when approval is absent it returns deterministic blocked/empty results for Primitive v2 shadow, Signature, Dynamic, Shadow/Mature, Theme, Archetype, Report Plan, Renderer, Explainability, Diff, and CLI. Reuse current Candidate Profile, report planner, formation skeletons, and promotion gate instead of replacing them.

**Global Constraints:** Existing approved C1/C2 contracts prevail. Do not alter active semantic/presentation fingerprints, frozen legacy mappings, or runtime behavior. Do not approve the proposed `RULE_GATE`, create new real semantic assets, create real Mapping candidates, or activate/prompt a bundle. All candidate assets remain isolated and all zero/blocked outcomes are valid.

## Tasks

1. Add contract tests for Role Authority, proposed/approved separation, Mapping candidate zero-state, and candidate fingerprint isolation; implement policy loader and mapping candidate engine.
2. Add generic downstream typed pipeline: Primitive shadow gate, signatures, dynamics, shadow/mature, themes, archetype, core profile aggregate, audit and explainability. All stages must return `blocked_by_gate` with zero outputs until approved mappings exist.
3. Add report-planner/renderer containment, source views, profile diff categories, and CLI commands over the generic pipeline without changing the legacy route.
4. Add promotion/rollback state machine and Calibration/Holdout gate adapter, requiring explicit decision artefacts and retaining one-step rollback metadata.
5. Add candidate-only contracts/policies, audit/review packet generation, documentation, exhaustive tests, package verification, and final engineering-versus-semantic readiness report.
