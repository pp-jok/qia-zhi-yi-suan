# Final Interpretive Productization Fix Report

## Scope

This change closes the three Important final-review blockers for the v0.5.0
audited interpretive route without invoking the strict or candidate runtime:

1. preserve concrete signal-level provenance through profile synthesis, report
   sections, JSON encoding, and checked-in demos;
2. prevent caller-constructed profiles from entering the public audited report
   builder;
3. preserve birth-time scope metadata and make missing-time degradation visible
   in both standard and concise reports.

## TDD evidence

The first focused run added five assertions and failed for the expected missing
behaviors:

- a forged public `InterpretiveCoreProfile` was accepted;
- a valid `QualifiedFacts` value was rejected by the old profile-only report
  signature;
- JSON sections had no `signal_provenance`;
- missing-time audit metadata had no `fact_mode` or birth-time state;
- standard and concise missing-time reports had no mandatory visible omission
  notice.

Command:

```text
python3 -m pytest -q \
  tests/test_interpretive_report.py::test_public_report_builder_rejects_caller_forged_profile \
  tests/test_interpretive_report.py::test_public_report_builder_accepts_only_valid_qualified_route \
  tests/test_interpretive_cli.py::test_cli_builds_traceable_standard_report \
  tests/test_interpretive_cli.py::test_missing_time_reports_metadata_and_visible_omission_notice
```

Initial result: `5 failed`. After the minimum implementation, the same command
reported `5 passed`.

## Trusted public boundary

`build_interpretive_report` now accepts only `QualifiedFacts` and calls
`require_qualified_facts` before synthesis. It then builds the profile and calls
the private `_render_interpretive_report` policy helper in one trusted flow.
There is no public raw-facts or caller-profile rendering route.

The CLI follows the same public qualified path. Its public command syntax,
versioned modes, compatibility aliases, and persisted top-level `mode` and
`report_mode` remain compatible.

No tuple/profile seal was introduced. The existing qualification-boundary seal
on `QualifiedFacts` remains unchanged and is revalidated by the public report
builder.

## Signal-level provenance

`InterpretiveSignalProvenance` records, per matched signal:

- `signal_id`;
- source `system`;
- concrete matched `fact_refs` resolved against qualified deterministic facts;
- `traditional_rule_ref`;
- rule limitations.

Every synthesized conclusion carries the exact provenance entries for its
supporting and countervailing signal IDs. The private renderer rejects a
conclusion when the ordered IDs and provenance entries do not match or when a
fact/rule reference is empty. Every normal, coverage, audit-scope, and
missing-time report section copies an exact, ordered provenance set matching its
`signal_ids`. The codec persists these entries in each JSON section.

Tests compare conclusion provenance with the extracted signals field by field
and verify each serialized section's provenance IDs exactly equal its listed
signal IDs.

## Birth-time scope and visible degradation

Trusted profile synthesis now preserves:

- `fact_mode`;
- `birth_time_status`;
- `time_sensitivity_reasons`;
- `omitted_time_sensitive_claims`.

Report audit metadata carries the same values. A `stable_only` report records
`unavailable_or_uncertain` and omits `astrology.houses` and
`astrology.angles`.

Both standard and concise rendering append a mandatory reader-visible section
stating that birth time is unavailable or uncertain and that house/angle claims
were omitted. For a full standard report the notice is retained within the
12-section limit by replacing the last optional section, so filler truncation
cannot remove the notice.

## Generated artifacts and documentation

The following demos were regenerated through the public CLI:

- `docs/demos/v0.5.0/contrast-a-standard.json`;
- `docs/demos/v0.5.0/tension-standard.json`;
- `docs/demos/v0.5.0/missing-time-standard.json`.

The missing-time demo now has nine sections, `fact_mode: stable_only`,
`birth_time_status: unavailable_or_uncertain`, explicit omitted claim
categories, and the visible time-scope notice. All demo sections pass an exact
signal-ID/provenance consistency check.

README and audited-interpretive design/plan documents now describe the
qualified-only public API, per-section provenance, and mandatory missing-time
behavior.

## Verification

- Focused interpretive suite:
  `50 passed in 2.40s`.
- Full suite:
  `841 passed in 49.97s`.
- Demo audit script:
  all three JSON files parsed; every section's provenance exactly matched its
  signal IDs; the missing-time text assertions passed.
- Package verifier:
  built and installed the 0.5.0 wheel in a clean virtual environment, ran the
  installed smoke and CLI checks, audited wheel members, and ended with
  `package verification passed`.
- `git diff --check`: clean.

The final commit intentionally excludes pre-existing untracked SDD briefs,
review diffs, and progress files.
