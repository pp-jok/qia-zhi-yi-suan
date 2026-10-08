# Audited Interpretive Production Mode Design

## Goal

Deliver the first usable personality-analysis product (`v0.5.0`) without
weakening the existing Strict / Research Mode. A qualified deterministic fact
packet must produce a differentiated, traceable standard report through a
separate `audited_interpretive` path.

## Product boundary

Two modes remain explicit and non-interchangeable:

- `strict`: existing Core Destiny Profile and release renderer. It continues to
  require formal semantic activation and may return only `unknown` states.
- `audited_interpretive`: a product path based on qualified facts, versioned
  traditional interpretation rules, controlled signal synthesis, and a
  user-readable report. It does not create PRIMARY_EVIDENCE, alter Primitive
  state, or promote candidate rules.

The report contains one short boundary statement: traditional Bazi/astrology
interpretation is not an empirical psychological diagnosis.

## Architecture

```text
QualifiedFacts
  -> Bazi rules -> InterpretiveSignal[]
  -> Astrology rules -> InterpretiveSignal[]
  -> Cross-system comparison -> SynthesisSignal[]
  -> Interpretive profile -> planned standard report
  -> JSON report with a compact user view and audit appendix
```

Every conclusion in the profile refers to one or more signal identifiers and
retains the matched signal's concrete fact paths, traditional-rule reference,
system, and limitations. The public product report builder accepts only
fingerprint-bound `QualifiedFacts`, revalidates that boundary, then runs the
profile builder and a private renderer in one trusted flow. Caller-constructed
profiles and raw facts are never accepted by the public report entry point.
Strict core artifacts remain separate types and are never accepted as
interpretive input.

## Rule bundle

Create `src/destiny_personality/interpretive_assets/v1/interpretive_rules_v1.yaml`
and package it in wheels. A rule is deliberately small:

```yaml
rule_id: BZ-INT-01
system: bazi
topic: judgement_style
fact_conditions: {ten_gods_any: [正印, 偏印]}
direction: reflective
contexts: [decision, work]
interpretation: "..."
confidence_default: moderate
method_version: bazi-interpretive-v1
school: traditional_bazi_general
limitations: ["...]
source_refs: ["..."]
```

V1 covers only facts already represented in `DeterministicChartFacts`:

- Bazi: Ten-God presence and pillar distribution, day-master/month branch,
  relation facts, and explicit availability of the hour pillar.
- Astrology: planet placements/signs/houses, major aspects, dignities, angles,
  and availability of time-sensitive data.

Rules are descriptive traditional interpretations, not formal Mappings and not
claims of empirical validation. The loader validates exact schema, unique IDs,
known systems/topics/assurance values, non-empty rule provenance, and
fact-condition shapes. The runtime only emits a signal when all declared
conditions are met.

## Runtime types

New module `interpretive_models.py` defines frozen dataclasses:

- `InterpretiveSignal`: source-system observation with fact refs, rule ref,
  topic, direction, contexts, interpretation, confidence, method/school,
  limitations.
- `SynthesisSignal`: comparison result for one topic, source signal refs,
  alignment type (`validation`, `complement`, `contextualization`, `tension`,
  `unresolved`, `non_comparable`), interpretation, confidence, limitations.
- `InterpretiveCoreProfile`: product-level core identity, signatures,
  strengths, blind spots, patterns, tensions, growth directions, fate themes,
  optional archetype, assurance summary, limitations, and audit refs.
- `InterpretiveReport`: mode, profile reference, standard sections, concise
  assurance summary, one boundary statement, and audit appendix.

`confidence` is exactly one of `high`, `moderate`, `exploratory`, or
`insufficient`. `high` requires a valid cross-system confirmation; a single
system can produce at most `moderate`; uncertainty changes language and scope
instead of erasing supported material.

## Signal extraction and synthesis

`interpretive_rules.py` loads the bundled YAML and applies rules to
`DeterministicChartFacts`. It returns separate Bazi and astrology collections
without comparing them.

The V1 bundle includes an explicit, value-matched cross-system tension pair:
the Bazi resource/expression rule and the astrology Sun-in-Aries first-house
rule share the exact `style of expression` topic while retaining opposite
`reflective` and `outward` directions. The profile synthesizer, not the report
renderer, therefore preserves each matched signal as countervailing evidence.

`interpretive_synthesis.py` compares same-topic signals only. It never raises
confidence mechanically: agreement can validate an existing signal, different
but compatible directions can complement it, and opposing directions produce a
tension signal with both source refs. No cross-system signal is emitted when
topics are not comparable.

`interpretive_profile.py` selects only supported signals and synthesis records.
It creates a finite, deterministic set of topic-bound conclusions. Every
profile item carries signal refs; unsupported content is rejected by the
profile validator. Formal Primitive states, if supplied in the future, may be
represented as separately labelled `formal` support but V1 does not depend on
them.

## Report

`interpretive_report.py` plans and renders `standard-interpretive-v1` first.
It has these sections when evidence exists: core identity, judgement and
thinking, action, emotional/pressure pattern, relationships, work style,
internal tension, strengths, blind spots, growth direction, life theme, and
summary. A section gives conclusion, basis, mechanism, and real-world
expression in natural language, with confidence-sensitive wording. Internal
rule, fact, and signal IDs occur only in the audit appendix.

`concise-interpretive-v1` is a smaller view over the same profile. Long-form is
out of scope for this release and the legacy 56-chapter route remains frozen.
Every structured report section carries `signal_provenance` that resolves each
listed signal ID to concrete matched fact paths and its traditional rule. The
report audit metadata preserves `fact_mode`, birth-time status, sensitivity
reasons, and omitted time-sensitive claim categories. When birth time is
unavailable or uncertain, both report modes include a mandatory visible notice
that house and angle claims were omitted; filler-section limits cannot remove
that notice.

## CLI and Skill

Add:

```text
build-interpretive-report FACTS.json --qualification QUALIFICATION.json \
  --mode {concise-interpretive-v1,standard-interpretive-v1} --output REPORT.json
```

It loads `QualifiedFacts`, rejects raw facts, builds the interpretive profile,
and persists JSON. Existing `build-release-report` remains strict.
The two versioned mode names are the only choices shown in CLI help and are
persisted in `report_mode`; the former `standard` and `concise` spellings are
accepted only as compatibility aliases and normalize to the versioned names.

Update the Skill routing so normal user-facing personality analysis defaults to
`audited_interpretive`; `strict` remains opt-in for research/audit. If no
calculation provider or qualified facts are available, the process stops rather
than inventing a chart. Missing time removes hour/house/angle-dependent rules
while retaining time-independent signals.

## Product test gate

Add five synthetic, fact-qualified fixtures with deliberately different Bazi
and astrology structures: reflective/stable, expressive/action-oriented,
relationship-sensitive, cross-system tension, and missing-time. Their expected
outcomes verify deterministic repeatability, structural differentiation,
signal traceability, tension preservation, and time-sensitive degradation.

The product review records a compact diff matrix and three generated standard
demo reports. It passes only if all five profiles render, no report conclusion
lacks signal refs, report fingerprints differ for structurally distinct facts,
the tension fixture retains both directions, missing-time avoids unavailable
topics, Strict tests continue to pass, and package verification succeeds.

## Non-goals

- No modification, activation, or replacement of Strict Mode assets.
- No Primitive ontology redesign, Semantic Bridge expansion, PRIMARY_EVIDENCE
  promotion, or candidate asset promotion.
- No embedded calculator and no unsupported inference from birth input.
- No claim of empirical personality diagnosis.
