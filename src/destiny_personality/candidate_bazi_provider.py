"""Explicit, inactive-by-default provider for neutral Bazi relations."""

from dataclasses import replace

from .calculation.models import BaziChartFacts
from .neutral_bazi_relations import (
    canonicalize_bazi_subjects,
    derive_canonical_neutral_relations,
    validate_ten_god_subject_refs,
)
from .canonical_bazi_relations import CanonicalBaziRelationPolicy


class CandidateNeutralRelationBaziCalculator:
    """Decorate a Bazi calculator without changing the default runtime path."""

    def __init__(self, delegate: object, policy: CanonicalBaziRelationPolicy) -> None:
        self._delegate = delegate
        self._policy = policy

    def calculate(self, birth_input, normalized_time, methodology) -> BaziChartFacts:
        facts = self._delegate.calculate(birth_input, normalized_time, methodology)
        if type(facts) is not BaziChartFacts:
            raise ValueError("BAZI_CHART_FACTS_REQUIRED")
        if any(
            relation.relation_type == self._policy.relation_type
            for relation in facts.relations
        ):
            raise ValueError("GOVERNED_BAZI_RELATIONS_ALREADY_PRESENT")

        facts = canonicalize_bazi_subjects(facts, self._policy)
        validate_ten_god_subject_refs(facts, self._policy)
        generated = derive_canonical_neutral_relations(facts, self._policy)
        return replace(facts, relations=facts.relations + generated)
