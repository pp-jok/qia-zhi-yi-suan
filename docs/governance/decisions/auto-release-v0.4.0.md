# Autonomous Release Decision: v0.4.0

- Decision ID: `AUTO-RELEASE-V0.4.0`
- Authority: `delegated_autonomous_executor`
- Mode: `AUTONOMOUS_COMPLETION`
- Outcome: `PASS`
- Release classification: `RELEASE_READY_WITH_LIMITED_SEMANTIC_COVERAGE`
- Audited implementation commit: `25787d45ceaeab26130630d6d88c6d54754006b3`
- Asset fingerprint: `git-commit-sha1:25787d45ceaeab26130630d6d88c6d54754006b3`
- Decision time: `2026-10-04T15:49:53Z`

## Decision

The audited implementation snapshot may be published as v0.4.0 with limited
semantic coverage. This is a release-readiness decision, not a claim that the
semantic knowledge base is complete.

The implementation has a complete formal lifecycle and an auditable
limitations-first no-conclusion report path, while truthfully resolving all six
Core Primitives to `unknown`. No
PRIMARY_EVIDENCE, active Mapping, dominant signature, dynamic, shadow/mature
form, fate theme, or archetype is fabricated to improve apparent coverage.

## Binding method

The decision binds to the immutable Git implementation commit above. The
decision and final audit documents are attestations created after that snapshot
and are deliberately excluded from the fingerprint, avoiding a self-referential
hash. Publication must use a descendant that changes only these audit records
or changes subsequently reverified by the complete release gates.

## Release conditions satisfied

- P001-P006 each have a terminal research state and formal `unknown` runtime
  state; `unknown` is never coerced to low.
- The active release Mapping bundle is explicitly empty, fingerprinted, and
  bound at runtime to a packaged delegated `CLOSE_ZERO` decision.
- Formal fact admission revalidates facts, retained qualification material,
  derived assurance, and both fingerprints on every build.
- Candidate Preview and frozen legacy routes remain available but cannot enter
  the formal resolver.
- The formal planner and renderer emit limitations-first reports without
  adding unplanned semantic claims.
- Synthetic end-to-end, regression, packaging, isolated-install, and Skill
  boundary checks pass.
- Five-role review has no unresolved Critical or Important finding.

## Non-claims and deferrals

- v0.4.0 is not a 1.0 semantic maturity claim.
- The release does not bundle a chart calculator, Swiss Ephemeris, fonts, or a
  fixed provider. The Skill instructs the hosting agent to discover and invoke
  external calculation capability.
- Extended Primitive inventory and real PRIMARY_EVIDENCE/Mapping construction
  remain future semantic-asset work.
- `project_verified` is not granted by the current candidate runtime; a request
  for it is conservatively derived as `capability_reported`.

The detailed evidence is recorded in
`docs/reviews/autonomous-completion-final-report.md`.
