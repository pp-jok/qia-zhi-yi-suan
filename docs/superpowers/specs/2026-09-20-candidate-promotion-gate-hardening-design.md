# Candidate Promotion Gate Hardening Design

## Goal

Make the candidate-to-production promotion gate reject incomplete or unreviewed
candidate assets without creating production semantic values.

## Decision

Use a focused, asset-aware validator in `core_profile_promotion.py` rather than
a new schema framework or a file-presence-only check.

## Required behavior

1. `CANDIDATE_REVIEW_PENDING` remains until every candidate YAML asset has
   `review_status: approved`; candidate `pending` status never becomes a
   production permission.
2. `BAZI_DAY_MASTER_ENVIRONMENT_UNAVAILABLE` is returned when the environment
   table is absent, structurally incomplete, or has blank mapped values. It
   must contain every project-table stem and month-branch key.
3. `BAZI_VISIBLE_HIDDEN_PROVENANCE_UNAVAILABLE` is returned unless every Bazi
   rule requires at least two distinct pillars, explicitly allows both visible
   and hidden source kinds, and requires a day-master environment.
4. `ASTROLOGY_DIGNITY_MODIFIER_UNIMPLEMENTED` and
   `ASTROLOGY_ANGLE_HOUSE_BRANCH_UNIMPLEMENTED` are returned unless a single
   astrology rule provides non-empty, structurally valid modifier fields.
5. The existing public call remains usable without parameters. An optional
   candidate-root argument exists only for isolated tests and diagnostics.

## Boundaries

- No candidate YAML is copied to `destiny-personality/configs/`.
- No review status is changed automatically.
- No table values, mapping directions, thresholds, or narrative semantics are
  introduced or modified.
- The gate reports blockers only; it never promotes an asset.

## Validation

Tests exercise a fully valid temporary candidate bundle, then independently
remove a table mapping, a Bazi provenance requirement, and an astrology
modifier field. The repository suite must remain green.
