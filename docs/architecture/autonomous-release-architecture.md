# Autonomous Release Architecture

## Authoritative flow

```text
Qualified Facts
  -> release manifest and active approved Mapping admission
  -> Core Destiny Profile
  -> bound Report Plan
  -> contained Report
```

Each boundary fails closed. Facts carry independent qualification and
fingerprint evidence. The release manifest defines exact P001-P006 lifecycle
coverage. Mapping admission requires explicit `approved` and `active` status.
The Core Destiny Profile keeps fact assurance separate from semantic assurance.
The Report Plan is fingerprint-bound to one validated profile, and the renderer
cannot read facts or registries or add an unplanned claim.

## Current limited coverage

The v0.4.0 manifest has zero active PRIMARY_EVIDENCE and Mapping references.
All six Primitive states therefore resolve to `unknown`; this never coerces to
`supported_low`. Cross-system results are `non_comparable` and cannot increase
salience. Signatures, Dynamics, Shadow/Mature forms, Themes, and Archetype are
empty.

## Separated compatibility paths

- Candidate Preview remains experimental and cannot feed the formal profile.
- `legacy-long-form-v2` remains a frozen controlled-inference handoff.
- The Skill contains workflow and validation rules, not calculation software.
- Historical review assets remain audit evidence; they are not automatically
  authoritative release assets.
