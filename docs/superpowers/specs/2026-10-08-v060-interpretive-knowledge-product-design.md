# v0.6.0 Interpretive Knowledge Product Design

## Goal

Deliver the first internal-test-ready personality product: qualified birth-chart
facts produce differentiated, reader-facing Bazi × astrology reports with
multiple supported themes, concrete cross-system synthesis, visible
missing-time degradation, and complete per-signal provenance.

## Frozen boundary

`strict`, candidate mappings, primitive resolution, semantic bridges and their
governance assets remain behaviorally unchanged. The new work stays in the
audited-interpretive product path. Traditional interpretation remains
non-diagnostic and cannot invent facts, rules, confidence, or agreement.

## Rule-family contract

Replace the four demo-shaped rules with a versioned v2 bundle. A rule family
has a bounded selector vocabulary and emits a signal only when every declared
condition matches a qualified fact. Families describe reusable structures, not
one chart configuration:

- Bazi: all ten-god identities, pillar position, visible/hidden source,
  repetition, and canonical branch relation type/participants.
- Astrology: planet function, sign element/modality, house context when time
  is available, major aspect type, and dignity as an expression qualifier.

The asset records topic, direction, Chinese core interpretation, mechanism,
likely expression, contexts, modifiers, limitations, and traditional source.
The runtime keeps one small predicate evaluator rather than an expression DSL.

## Product pipeline

```text
QualifiedFacts
  -> audited rule-family signals
  -> Bazi profile + astrology profile
  -> cross-system alignments/tensions
  -> trusted core profile + narrative packet
  -> reader report + audit appendix
```

System-specific profiles are derived independently. Cross-system synthesis
compares their topic/direction evidence and emits concrete `validation`,
`complement`, `contextualization`, `tension`, `correction`, `unresolved`, or
`non_comparable` records. A tension names both poles, real-life contexts, and
an integration direction; it is never represented by a bare label.

## Reader report

The reader body contains only evidence-backed analysis: core identity,
dominant patterns, thinking, action, expression, relationships, work, stress,
tensions, strengths/blind spots, growth, and synthesis when actually present.
It does not pad with audit sections. Sparse evidence yields a short report plus
one boundary statement. Audit metadata and signal provenance remain in the
appendix/JSON rather than the reader body. Confidence is rendered as natural
language, not repetitive labels.

## Input and release gates

The Skill workflow accepts birth fields, calls an available calculation provider
and qualification pipeline, then invokes audited interpretation. If no provider
is available it returns `CAPABILITY_GAP`; it never asks a normal user for JSON
or computes a chart in free-form reasoning.

Release requires at least 12 differentiated qualified fixtures, five reader
demos generated through the product pipeline, multiple real themes for normal
complete charts, actual Bazi and astrology contribution, real synthesis,
missing-time degradation, traceability, strict regression, package verification
and Python 3.9/3.11/3.12 CI.

## Explicit non-goals

- No new primitive ontology, governance layer, PRIMARY_EVIDENCE work, or
  strict-pipeline refactor.
- No unsupported 旺衰、格局 or 用神 product inference.
- No user-facing audit padding, rule-count target, randomized paraphrasing, or
  direct LLM access to raw charts.

## Source decision

This design implements the attached Product Owner v0.6.0 execution directive.
That directive grants autonomous execution, so it serves as design approval for
the recommended product-first approach.
