# Deterministic Fact Contract

## Packet

At `FACTS_NORMALIZED`, mechanically produce a `deterministic-facts-v1` packet
from accepted calculation envelopes. At `FACTS_VALIDATED`, accept that packet
only after it passes its own structure, methodology, provenance, and required
independent-comparison checks. Required top-level fields are `schema_version`,
`fact_mode`, `methodology_versions`, `provenance_refs`, `normalized_time`,
`bazi`, `astrology`, and `validation_summary`.

`schema_version` is `deterministic-facts-v1`. `fact_mode` is `stable_only` or
`time_sensitive`. `methodology_versions.bazi` is `bazi-core-v1.0`; and
`methodology_versions.astrology` is `western-tropical-v1.0`. `provenance_refs`
contains references to accepted calculation envelopes and validation assets;
it does not promote raw provider output to a fact.

For Candidate Core Profile runtime, pair this packet with a separate
[`fact-qualification-v1`](fact-qualification.md). The packet's
`validation_summary` remains an audit summary; it cannot itself derive or
promote fact assurance.

## Normalized time

`normalized_time` records the birth date, historical civil time, local standard
time, UTC, true solar time, IANA timezone, coordinates, DST state, time basis,
fact mode, sensitivity reasons, and source envelope references. Unknown birth
time leaves every clock-derived value absent; absence is retained rather than
filled with a default.

## Bazi

`bazi` records the methodology version, year, month, and day pillars; optional
`hour_pillar`; hidden stems; Ten Gods; and configured relations. Every derived
item requires `source_pillars` and provenance. `hour_pillar` and its
hour-pillar provenance are permitted only when time-sensitive facts are
supported by known birth time and accepted source evidence.

## Astrology

`astrology` records the methodology version, configured planetary placements,
aspects, Ascendant, MC, twelve `house_cusps` when time-sensitive, dignities,
and provenance. The exact configured set is determined only by the frozen
methodology version and project-owned validation assets.

The YAML says `core.node: true`, while the methodology document calls True
North Node optional and does not freeze its canonical fact identifier or its
aspect, phase, or dignity participation. Reserve node extensibility, but the
current contract must not require, accept as validated, or interpret a node
placement. The missing node rule, canonical fact identifier, phase, and dignity
participation are each `CONFIG_GAP` until the project supplies a consistent
rule.

## Stable only

`stable_only` excludes `hour_pillar`, hour-pillar provenance, Ascendant, MC,
houses, `house_cusps`, angle aspects, and every other field declared
time-sensitive. Their absence is not low evidence. A stable-only packet must
not contain a field that this contract declares time-sensitive.

## Mechanical normalization

Convert only approved aliases, valid decimal representations, containers, and
canonical ordering while retaining omissions and warnings. Do not derive sign,
house, aspect, dignity, hidden stem, Ten God, relation, or a missing default.
Do not wrap an invalid longitude or repair a source result. Mechanical
normalization cannot add a lookup table, alias, threshold, precision, tolerance,
or other policy not supplied by the project.

## Validation order

Validate structure and types; methodology versions; required fields and
uniqueness; ranges; internal consistency; provenance; stable-only exclusions;
and then required independent confirmation. An invalid primary packet is a
calculation contract error and cannot be repaired by any secondary packet.

## Controlled-profile boundary

A `capability_reported` fact basis is not a `deterministic-facts-v1` packet and
must not be certified as one. It may support a `controlled_inference` portrait
only after the external capability, methodology, provenance, structure, range,
internal-consistency, and time-sensitivity checks pass. The original labels,
omissions, warnings, and assurance level remain explicit.
