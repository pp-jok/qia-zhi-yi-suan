# Core Personality Ontology Review v1

**Stage:** C1 — Core Personality Ontology Review
**Status:** C1 accepted for C2 review on 2026-09-18; no production approval
**Scope:** system-neutral personality vocabulary before Bazi or Astrology mappings.

## Boundary

This review proposes six candidate Core Primitives. They describe observable
personality tendencies, not fate, diagnosis, identity, life outcome, virtue, or
deficit. They are not chart structures, report chapters, Golden Sample themes,
Shadow forms, Fate Themes, or Archetypes.

This document is an input to C2 Mapping Review, not a mapping rule. It does not
authorize inference from chart facts. Until C1–C4 receive product-owner
approval, every entry remains `review_status: accepted_for_c2` and cannot be projected
into a runtime configuration.

## State-resolution proposal

| State | Candidate decision rule |
| --- | --- |
| `supported_high` | Approved C2 rules supply convergent high-expression evidence without an unresolved reversing exclusion. |
| `supported_low` | Approved C2 rules supply explicit reverse-direction evidence; absence is never reverse evidence. |
| `mixed` | Approved evidence supports materially different directions across contexts or systems without a valid resolver. |
| `unknown` | Evidence is absent, unusable, unmapped, or insufficiently comparable. |

All states require audit references, modifiers, counterevidence where present,
and limitations. Cross-system agreement cannot independently raise system-local
salience. `correction` can qualify semantic scope, never chart facts.

## Candidate primitive set

### CP-CORE-01 — Agentic Self-Direction

- **Definition:** tendency to initiate, evaluate and sustain consequential
  choices from an internally owned frame of reference.
- **High / low expression:** independent position and choice ownership /
  explicit deference of consequential evaluation or choice to external direction.
- **Non-implications:** rebellion, isolation, selfishness, leadership,
  competence, or lack of care for others.
- **Candidate evidence families:** agency, self-initiation, decision ownership,
  feedback dependence, and role-bound choice; exact system conditions are C2 work.
- **Counterevidence:** self-initiation only in low-stakes work, or deference
  limited to intimate and high-risk contexts.
- **Sample-bias risk:** overfitting prior themes of judgment, freedom, exit,
  authorship, or control.
- **Review status:** `accepted_for_c2`.

### CP-CORE-02 — Predictability Orientation

- **Definition:** tendency to seek, maintain, or function best with continuity,
  known constraints, and manageable change.
- **High / low expression:** stabilizes routines, commitments, expectations, or
  risk exposure / explicit preference for novelty, reversibility, variation, or
  rapid adaptation.
- **Non-implications:** rigidity, fear, conservatism, reliability, boredom, or
  resistance to all change.
- **Candidate evidence families:** continuity, constraint tolerance,
  change-seeking, risk containment, and transition handling.
- **Counterevidence:** stability in resources but novelty in relationships;
  externally imposed routine without internal preference.
- **Sample-bias risk:** reducing nuance to “freedom versus structure.”
- **Review status:** `accepted_for_c2`.

### CP-CORE-03 — Relational Attunement

- **Definition:** tendency to organize attention and evaluation around mutual
  response, belonging, reciprocity, and relational impact.
- **High / low expression:** incorporates relational signals into important
  choices / explicit limited weighting of relational feedback in priorities.
- **Non-implications:** sociability, dependency, agreeableness, empathy,
  popularity, or relationship success.
- **Candidate evidence families:** affiliation, reciprocity, feedback
  sensitivity, attachment orientation, and boundary management.
- **Counterevidence:** high attunement in close relationships but not groups;
  care expressed through duty rather than feedback tracking.
- **Sample-bias risk:** gendered or moralized relationship framing.
- **Review status:** `accepted_for_c2`.

### CP-CORE-04 — Action Mobilization

- **Definition:** tendency to convert intention, pressure, or opportunity into
  observable initiation and sustained action.
- **High / low expression:** begins, tests, or advances action with limited
  delay / explicit delayed initiation, prolonged preparation, or inhibition
  despite an available direction.
- **Non-implications:** productivity, ambition, impulsivity, courage,
  discipline, achievement, or moral worth.
- **Candidate evidence families:** initiation, pace, activation under pressure,
  execution, inhibition, and completion.
- **Counterevidence:** fast initiation with low completion; high action only in
  crisis; practical constraints mistaken for trait.
- **Sample-bias risk:** visibility, disability, resource, and opportunity bias.
- **Review status:** `accepted_for_c2`.

### CP-CORE-05 — Affective Regulation Orientation

- **Definition:** tendency to notice, modulate, contain, express, or organize
  affective activation while making meaning and decisions.
- **High / low expression:** uses identifiable regulation, containment,
  reflection, or expression processes / explicitly limited access to or use of
  such processes in the mapped context.
- **Non-implications:** emotional intensity, mental health, sensitivity,
  authenticity, coldness, pathology, or absence of feeling.
- **Candidate evidence families:** affect processing, response modulation,
  emotional safety needs, and expression timing.
- **Counterevidence:** high private regulation with public expression;
  situational stress response mistaken for a stable orientation.
- **Sample-bias risk:** pathologizing normal emotion or cultural expression.
- **Review status:** `accepted_for_c2`.

### CP-CORE-06 — Structuring Orientation

- **Definition:** tendency to organize information, commitments, and action
  through explicit models, categories, standards, sequences, or constraints.
- **High / low expression:** relies on explicit framing, prioritization,
  standards, procedures, or models / explicit preference for emergent,
  intuitive, situational, or minimally pre-structured organization.
- **Non-implications:** intelligence, perfectionism, bureaucracy,
  conscientiousness, creativity, rule obedience, or intolerance of ambiguity.
- **Candidate evidence families:** ordering, categorization, standards,
  procedural reliance, improvisation, and ambiguity handling.
- **Counterevidence:** high structure at work but emergent private style;
  externally imposed rules mistaken for internal orientation.
- **Sample-bias risk:** education, occupation, and class-coded communication bias.
- **Review status:** `accepted_for_c2`.

## C1 decisions required

For each candidate, product review must accept, revise, split, merge, or reject
it and record rationale, counterexamples to preserve, and required C2 evidence.
Rejected or unresolved entries cannot appear in candidate YAML or Mapping review.
No C1 decision may create a Dynamic, Shadow Form, Mature Integration, Fate Theme,
Archetype, report topic, or default user narrative.
