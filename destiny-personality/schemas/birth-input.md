# Birth Input Contract

## Input profile

Use `input_profile: compact-or-structured-birth-input-v1` for a new portrait.
Accept either explicit fields or one unambiguous compact line. For example,
`2000.1.1.00:00 上海 未指定` is equivalent to a local Gregorian birth date of
`2000-01-01`, a local civil birth time of `00:00`, birth place `上海`, and
`sex: unspecified` with the original display label `未指定`.

For unambiguous compact input, normalize separators and field names silently;
do not ask for confirmation merely because the user used dots, spaces, Chinese
date markers, or comma-separated prose. Ask one focused question only when a
required value has more than one plausible reading. In particular, reject or
clarify locale-ambiguous numeric dates such as `05/06/1986`; do not choose a
month/day order from model knowledge.

The normalized portrait input is:

1. `birth_date`: Gregorian local date in `YYYY-MM-DD` form.
2. `birth_time`: local civil time in `HH:MM[:SS]` form, or `unknown`.
3. `birth_place`: the user's non-empty place text before later resolution.
4. `sex`: optional `male`, `female`, or `unspecified`; preserve any supplied
   source label separately for display.
5. `requested_mode`: `portrait` unless the request clearly selects another
   supported mode.

Sex is display and capability input, not permission to invent a rule. The
agent must not infer sex from a name, writing style, relationship role, or any
other context. When omitted, use `unspecified`; ask only if a declared external
methodology actually requires it for an emitted result.

## User input

Require:

- `birth_date`: Gregorian local calendar date in `YYYY-MM-DD` form.
- `birth_time`: local civil time in `HH:MM[:SS]` form, or explicit `unknown`.
- `birth_place`: a non-empty place name suitable for later resolution.

Accept optionally:

- `sex`: `male`, `female`, or `unspecified`, plus an optional verbatim display
  label supplied by the user.
- `timezone_name`: IANA timezone name supplied or verified by an external capability.
- `latitude`: finite decimal in `[-90, 90]`.
- `longitude`: finite decimal in `[-180, 180]`.

Do not require the user to know timezone or coordinates. Phase C may resolve missing values through an authorized external capability and must record provenance.

## Normalized execution input

Record `requested_mode` as `portrait`, `facts_only`, or `audit`. Default to `portrait` only when the request clearly asks for a new portrait.

When `birth_time` is `unknown`, set `fact_mode` to `stable_only`. Reject any attempt to use an hour pillar, Ascendant, MC, houses, or facts that declare an hour-pillar source.

When time is known, preserve it as local civil time. Do not infer historical UTC, DST, true solar time, coordinates, or timezone from model knowledge.

Compact parsing changes representation only. It never authorizes calculation,
timezone resolution, coordinate lookup, historical-time repair, or personality
inference before the corresponding gates pass.

## Failure

Return `BIRTH_INPUT_ERROR` for a missing required field, invalid date/time syntax, invalid coordinate, contradictory time status, or an audit request without an auditable object. Do not misclassify input failure as `CONFIG_GAP` or `CAPABILITY_GAP`.
