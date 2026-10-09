# v0.6.0 Product Differentiation Review

## Decision

Pass for the v0.6.0 internal product gate. The 12 qualified fixtures produce
12 different reader semantic signatures after interpolated evidence is
normalized, normal complete charts expose 7–12 real topics, both systems
contribute to every normal report, and the five checked-in demos are
byte-for-JSON reproducible through the production CLI.

## Review method

For each fixture, the review built a standard report through the public
qualified-facts boundary. It derives a per-section semantic signature from the
reader-visible topic, conclusion, mechanism, likely expression and context.
The signature normalizes only each dynamic `命中依据` interpolation; audit
metadata, fingerprints, signal IDs and limitations are excluded. This prevents
different factual values from disguising a shared reader-facing template. The
suite also scans reader content for raw calculation paths while requiring those
paths in the separate signal provenance records.

## Actual-report differentiation

| Fixture | Reader-body SHA-256 prefix | Distinct reader semantics |
| --- | --- | --- |
| bazi-dominated | `561bf69b47dc` | Reflection, autonomy, output, resources, responsibility, repetition and relational dynamics lead. |
| astrology-dominated | `36cbc25be736` | Seven planetary functions, life arena, aspect and dignity lead. |
| cross-system-agreement | `aecc68c831ad` | Food-god creative output and fire/fixed solar expression converge on visible creation. |
| cross-system-tension | `acb11f407dbe` | Seal reflection and fire/cardinal solar outwardness remain named as coexisting poles. |
| missing-time | `c7d8adfcfa3f` | House/angle claims disappear and the boundary notice is shown without suppressing stable topics. |
| practical-builder | `4ede1d610514` | Resource handling, standards, peer agency and earth-sign pacing foreground self-directed delivery. |
| relational-connector | `ee7f52736df2` | Peer agency, branch dynamics and relationship-oriented placements foreground reciprocity. |
| expressive-creator | `6c45f8c70f87` | Output and fire-sign evidence foreground public making, expression and momentum. |
| structured-steward | `4091f592d3c2` | Authority and earth-sign evidence foreground boundaries, duty and sustained mastery. |
| reflective-scholar | `212609893c39` | Seal and water-sign evidence foreground absorption, emotional processing and contemplation. |
| adaptive-explorer | `174b0ba633bb` | Peer/output and air/mutable evidence foreground experimentation and flexible learning. |
| boundary-mentor | `daf06c503625` | Authority, resources and fixed-water relational evidence foreground standards with care. |

The hash prefixes are review aids, not runtime contracts. Automated tests make
the stronger assertion that all 12 normalized reader semantic signatures are
unique.

## Five demo reads

- `bazi-dominated`: seven Bazi signals versus two astrology signals; both remain visible.
- `astrology-dominated`: ten astrology signals versus one Bazi signal; the Bazi anchor is not erased.
- `cross-system-agreement`: reader-level convergence is shown in one “表达与创造” section by
  `BAZI-TEN-GOD-OUTPUT` and `ASTROLOGY-PLANET-SIGN-EXPRESSION`. The exact-topic
  synthesis layer correctly keeps them non-comparable rather than fabricating a
  formal validation relationship.
- `cross-system-tension`: the shared exact topic `style of expression` produces
  a formal tension between reflective and outward directions, retaining both
  systems' contexts and evidence.
- `missing-time`: `ASTROLOGY-SUN-HOUSE-CONTEXT` is absent; metadata records
  `astrology.houses` and `astrology.angles` as omitted, and the reader sees the
  controlled omission notice.

## Template collapse review

The first normalized-signature review found a collapse between
`practical-builder` and `boundary-mentor`: their original reports differed only
in interpolated `命中依据` values. `practical-builder` now carries an additional
peer-agency signal, yielding a reader-visible `自主与协作` section and a distinct
topic/conclusion/mechanism/likely-expression/context signature. The gate
rejects equality after evidence normalization; shuffled signal IDs, different
fingerprints, or synonym-only metadata cannot satisfy it.

The review also found no raw calculation path in reader content. Exact paths
such as qualified placement and ten-god references remain available only in
`signal_provenance`, where they support traceability without turning the reader
body into an audit dump.

## Fixture inventory

The qualified pairs are: bazi-dominated, astrology-dominated,
cross-system-agreement, cross-system-tension, missing-time, practical-builder,
relational-connector, expressive-creator, structured-steward,
reflective-scholar, adaptive-explorer, and boundary-mentor.
