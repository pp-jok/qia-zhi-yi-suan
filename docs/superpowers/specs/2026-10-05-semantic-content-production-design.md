# Semantic Content Production and Deep Research Closure Design

## Purpose

Move the project from repository-only zero-coverage closure to a source-grounded,
independent research result for P001, P002, P003, P005, and P006. The work must
attempt a real Source -> Construct -> Method -> Fact -> PRIMARY_EVIDENCE ->
Mapping chain, but it must stop at the first unsupported bridge.

## Decision

The selected outcome is a v0.4.1 research-closure release, not v0.5.0.

Independent Bazi and Hellenistic research found direct-looking words but no
candidate that is both ontology-direct and method-reproducible:

- P001 candidates describe decisiveness, judgement quality, self-will, or
  cognition, not ownership of judgement standards.
- P002 candidates describe stability/change of temperament or technical chart
  structures, not preference for predictable conditions.
- P003 candidates describe affection, benevolence, friendship, or relationship
  outcome, not responsive coordination in interaction.
- P005 candidates describe intensity, expression, restraint, pathology, or
  cosmological flow, not the preferred processing of affect.
- P006 has the closest lexical candidates: `治事无规`, `布置有方`, and
  `systematic workers`. The Bazi candidates depend on unresolved whole-chart
  strength and ambiguous subject-selection rules; the Ptolemaic candidate is a
  role/capability description embedded in a complete soul-governor method, not
  a direct task-organization orientation.

No PRIMARY_EVIDENCE or Mapping will be created merely to obtain a non-zero
profile. P004 remains frozen.

## Alternatives rejected

### Activate a narrow P006 Mapping

Rejected. A narrow work context does not cure semantic indirectness. Treating
`systematic workers` as a preference for pre-set task structure would elevate a
role/capability phrase. Treating `治事无规` as an executable rule would require
inventing `蹇地`, `太柔`, strength, subject selection, aggregation, and exception
precedence.

### Widen the Primitive ontology

Rejected. Redefining P006 as competence, P001 as decisiveness, P003 as
affection, P005 as emotional intensity, or P002 as behavioural persistence
would erase the approved ownership boundaries.

### Switch schools until a match is found

Rejected. The selected Hellenistic corpus and the named Zi Ping corpus are
sufficient for saturation. Switching to psychological astrology or modern
personality shorthand solely to obtain coverage would be method shopping.

## Architecture

The mature runtime remains unchanged. Research results are represented in four
existing layers:

1. Source-grounded review documents with exact locators and access-copy
   limitations.
2. Primitive-specific candidate matrices using the project's existing direct,
   nearby, role, temperament, structural, and unresolved classifications.
3. A new versioned release coverage manifest that records deep independent
   saturation and explicit zero PE/Mapping counts without changing P004.
4. A final research-closure report and delegated autonomous decision bound to
   the exact coverage asset fingerprint.

The formal resolver continues to load a governed empty Mapping bundle. It must
still return six `unknown` states, zero candidates, and zero downstream
formations. The release version is 0.4.1 because no formal non-zero semantic
capability exists.

## Research corpus and authority rules

The Bazi corpus covers *Yuanhai Ziping*, *Ditian Sui* and separately identified
later commentary, *Ziping Zhenquan*, and *Sanming Tonghui*. Scan identity and
digital transcription are recorded separately. OCR or community transcription
is an access representation, not an additional authority.

The Astrology corpus covers the selected Hellenistic natal boundary, with
Ptolemy *Tetrabiblos* III.13 as the principal directly locatable source and
Valens/Dorotheus as corroborating discovery corpora only where an exact locator
is available. Traditional claims are methodology evidence, not empirical
personality validation.

Every Primitive report includes ontology, both source-system searches, source
corpus, direct and nearby candidates, method feasibility, canonical-fact
feasibility, Root/PE/Mapping result, counterevidence, saturation, and final
status. High and Low are assessed independently.

## Versioned coverage contract

Create `primitive_coverage_v2.yaml` rather than rewriting v1. It preserves the
same six Core Primitive IDs and records:

- P001/P002/P003/P005/P006:
  `CLOSED_AFTER_DEEP_INDEPENDENT_RESEARCH_NO_EXECUTABLE_DIRECT_CONSTRUCT`.
- P004: its existing system-specific frozen conclusion and overall `unknown`.
- `primary_evidence_refs: []` and `mapping_refs: []` for every Primitive.
- references to the new deep research reports.

The release-manifest loader moves to schema v2 and fails closed on missing
Primitive coverage, non-terminal status, non-zero references, or report paths
that do not exist. This is the only runtime-adjacent change and exists solely to
make the deeper research basis auditable.

## Test strategy

Use TDD for the manifest and governance changes. Tests must first fail because
v2 and the new reports do not exist, then pass after implementation.

Required gates:

- every reopened Primitive has a sufficiently structured deep report and
  construct matrix;
- source URLs/locators and both Bazi/Astrology paths are explicit;
- no report claims PE or Mapping activation;
- coverage v2 preserves exactly P001-P006 and P004's frozen result;
- formal CDP remains six `unknown` with zero formations;
- Candidate Preview and legacy do not leak into the formal path;
- package contains coverage v2 and loads it after isolated installation;
- full pytest, package verification, Python 3.9/3.11/3.12 CI, and five-role
  review pass before any release.

## Release decision

If all gates pass, publish v0.4.1 as:

`ALL_REOPENED_CORE_PATHS_DEEP_RESEARCH_SATURATED__NO_FORMAL_RUNTIME_ACTIVATION`

The release must explicitly state that it improves the evidentiary basis of
`unknown`; it does not add substantive personality output. v0.5.0 remains
reserved for at least one approved PE, active Mapping, and formal non-unknown
Primitive.
