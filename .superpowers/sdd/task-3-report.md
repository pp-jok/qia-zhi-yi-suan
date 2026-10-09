# Task 3 Report: Reader-first interpretive reports

## Scope delivered

- Standard reports now contain only evidence-backed analysis sections; audit
  padding sections were removed.
- Every reader claim is rendered in Chinese in this order: conclusion,
  mechanism, likely expression, contextual variation, and one natural
  confidence statement.
- Mechanisms and likely expressions are selected from the claim's supporting
  signals only. Countervailing evidence remains available for contextual
  tension without contaminating the claim mechanism.
- Maturity or imbalance wording is not invented when no matched signal supplies
  it.
- Section evidence IDs and provenance remain structured data, while audit IDs,
  fact paths, and English internal topics do not enter the reader narrative.
- Missing-birth-time scope is folded into an existing analysis section instead
  of creating an audit-only reader section.
- The qualified-facts-only public builder and existing strict, candidate, and
  primitive routes remain unchanged.

## RED evidence

1. After adding the requested sparse/rich reader-body tests:

   `python3 -m pytest tests/test_interpretive_report.py -q`

   Result: `1 failed, 19 passed`. The sparse report expected 3-4 analysis
   sections but received 8 sections because audit sections padded the body.

2. After adding the conclusion-first narrative contract:

   Result: `2 failed, 20 passed`. The sparse report was still padded and report
   content did not start with `结论：`.

3. Self-review regression tests were also observed RED before their fixes:

   - `test_each_claim_uses_only_its_supporting_mechanism` failed because an
     outward claim included the reflective counter-signal mechanism.
   - `test_reader_body_keeps_audit_terms_out_of_narrative` failed because the
     tension prose exposed English signal IDs and fact paths.

## GREEN evidence

- Focused report and CLI suite:

  `python3 -m pytest tests/test_interpretive_report.py tests/test_interpretive_cli.py -q`

  Result: `41 passed in 4.17s`.

- Fresh full regression suite:

  `python3 -m pytest -q`

  Result: `872 passed in 68.38s`.

- Patch hygiene:

  `git diff --check`

  Result: clean.

## Codec, CLI, and demo compatibility

- The report codec now emits `kind: "analysis"` for reader sections.
- No CLI routing change was necessary; the existing
  `build-interpretive-report` command already uses the updated builder and
  codec while preserving its qualification boundary and versioned modes.
- The three checked-in v0.5 interpretive demos were regenerated through that
  CLI because the existing CLI regression test requires byte-equivalent parsed
  payloads. These are Task 3 compatibility artifacts, not unrelated Task 4
  content:

  - `docs/demos/v0.5.0/contrast-a-standard.json`
  - `docs/demos/v0.5.0/tension-standard.json`
  - `docs/demos/v0.5.0/missing-time-standard.json`

## Self-review

- Sparse qualified chart: 3 analysis sections, no audit-padding titles.
- Rich qualified chart: 6 reader topics.
- Confidence appears exactly once per rendered claim.
- Each claim's mechanism/likely expression uses supporting evidence only.
- Reader prose contains no ASCII audit identifiers or internal fact paths.
- Provenance, signal IDs, limitation trails, fact/qualification refs, and
  birth-time audit fields remain serialized.
- Existing strict/candidate/primitive behavior is covered by the full green
  suite.
