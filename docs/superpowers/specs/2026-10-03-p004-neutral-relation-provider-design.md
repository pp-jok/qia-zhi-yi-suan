# P004 Neutral Bazi Relation Provider Design

Date: 2026-10-03

## Objective

Close the next candidate engineering gate identified by the P004 integration
review: emit deterministic, versioned, school-neutral Bazi element-control
relations from an explicitly selected provider and prove that Ten-God subjects
use the same reference convention.

This work does not make a Dao-Shi judgement, create an Evidence Root, add
PRIMARY_EVIDENCE, create Mapping assets, or activate the candidate in the
default calculation service.

## Considered approaches

### 1. Explicit provider decorator — selected

Wrap a caller-supplied `BaziChartCalculator`. The decorator validates the
returned Ten-God subject references, derives neutral relations, adds rule
provenance, and returns a new immutable `BaziChartFacts` value.

This keeps activation explicit, follows the existing calculator protocol, and
lets `ChartCalculationService` apply its normal contract validation without a
candidate-specific dependency.

### 2. Service post-processing hook — rejected

Adding candidate logic directly to `ChartCalculationService` would make an
inactive research asset part of the default runtime path and blur the boundary
between orchestration and Bazi calculation.

### 3. Backend-specific implementation — rejected

Changing an external Bazi backend would couple the project-owned fact contract
to a particular calculator and would not provide a reusable conformance gate.

## Architecture

`CandidateNeutralRelationBaziCalculator` implements the existing
`BaziChartCalculator` protocol by composition:

1. Call the wrapped calculator.
2. Build the governed subject catalogue from visible stems and indexed hidden
   stems.
3. Require every Ten-God with a declared source kind to use the matching
   subject reference and source pillar. Reject `UNKNOWN` source kind because it
   cannot be joined deterministically.
4. Derive directed `five_element_controls` relations using the candidate
   policy.
5. Preserve unrelated relation types, reject pre-existing governed relations,
   and attach `wuxing-control-v1` as rule provenance.
6. Return a replaced immutable `BaziChartFacts` instance.

The wrapper is exported as a candidate utility but is never instantiated by
the default service, CLI, or skill runtime.

## Contract changes

`BaziRelationFact` gains a `rule_version` field with the compatibility default
`unversioned`. The deterministic facts codec serializes and restores it. The
normal Bazi validator requires a non-empty rule version and applies stricter
checks to `five_element_controls`: exactly two distinct governed participant
references and source pillars equal to the pillars named by those references.

The candidate YAML status advances from `candidate_implementation_not_emitted`
to `candidate_provider_available_not_activated`. It remains `candidate_only`
and `inactive`.

## Failure policy

The candidate wrapper fails closed with stable `ValueError` codes for unknown
Ten-God source kind, invalid subject reference, mismatched source pillar,
duplicate governed relations, and invalid candidate policy. The calculation
service converts unexpected wrapper failures into its existing
`CALCULATION_FATAL` Bazi boundary.

## Verification

Tests must demonstrate:

- a red-green provider integration path through `ChartCalculationService`;
- visible and hidden Ten-God subject-reference conformance;
- rejection of ambiguous or mismatched Ten-God references;
- deterministic relation output with rule provenance;
- preservation of unrelated relations and rejection of duplicate governed
  input;
- codec round-trip and validation of the new provenance field;
- unchanged default service behaviour;
- unchanged active semantic and presentation fingerprints;
- zero Evidence Root, PRIMARY_EVIDENCE, Mapping, and production activation.

## Exit state

On success, `deterministic_facts.bazi.relations` is a reproducible candidate
provider output and is ready for a separate Evidence Root proposal review. It
is not an approved Evidence Root and does not improve the `NOT_READY` Dao-Shi
method status.
