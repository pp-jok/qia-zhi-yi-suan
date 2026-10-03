from dataclasses import replace
from pathlib import Path

import pytest

from destiny_personality.calculation import (
    BaziRelationFact,
    ChartCalculationService,
    HiddenStemsFact,
    PillarPosition,
    TenGodFact,
    TenGodSourceKind,
)
from destiny_personality.candidate_bazi_provider import (
    CandidateNeutralRelationBaziCalculator,
)
from destiny_personality.neutral_bazi_relations import (
    load_neutral_bazi_relation_policy,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
POLICY_ROOT = PROJECT_ROOT / "candidates" / "calculation-v1"


class FixedCalculator:
    def __init__(self, result):
        self.result = result

    def calculate(self, *_args):
        return self.result


class FixedNormalizer:
    def __init__(self, result):
        self.result = result

    def normalize(self, *_args):
        return self.result


def _policy():
    return load_neutral_bazi_relation_policy(POLICY_ROOT)


def _provider(facts):
    return CandidateNeutralRelationBaziCalculator(FixedCalculator(facts), _policy())


def _conforming_facts(bazi_facts):
    return replace(
        bazi_facts,
        year_pillar=replace(bazi_facts.year_pillar, heavenly_stem="甲"),
        month_pillar=replace(bazi_facts.month_pillar, heavenly_stem="戊"),
        hidden_stems=(
            HiddenStemsFact(PillarPosition.MONTH, ("戊", "己")),
        ),
        ten_gods=(
            TenGodFact(
                "year.stem",
                "比肩",
                (PillarPosition.YEAR, PillarPosition.DAY),
                TenGodSourceKind.VISIBLE_STEM,
            ),
            TenGodFact(
                "month.hidden_stem.0",
                "偏印",
                (PillarPosition.MONTH, PillarPosition.DAY),
                TenGodSourceKind.HIDDEN_STEM,
            ),
        ),
    )


def test_explicit_candidate_provider_emits_versioned_relations_through_service(
    birth_input,
    normalized_time,
    bazi_facts,
    astrology_facts,
    runtime_config,
) -> None:
    policy = _policy()
    assert policy.implementation_status == (
        "candidate_provider_available_not_activated"
    )
    provider = CandidateNeutralRelationBaziCalculator(
        FixedCalculator(_conforming_facts(bazi_facts)), policy
    )
    service = ChartCalculationService(
        FixedNormalizer(normalized_time),
        provider,
        FixedCalculator(astrology_facts),
    )

    result = service.calculate(birth_input, runtime_config)

    governed = tuple(
        relation
        for relation in result.bazi.relations
        if relation.relation_type == "five_element_controls"
    )
    assert governed
    assert {item.rule_version for item in governed} == {"wuxing-control-v1"}
    assert any(
        item.participant_refs == ("year.stem", "month.hidden_stem.0")
        for item in governed
    )


def test_candidate_provider_preserves_unrelated_relations(bazi_facts) -> None:
    unrelated = BaziRelationFact(
        "six_clashes",
        ("year.branch", "month.branch"),
        (PillarPosition.YEAR, PillarPosition.MONTH),
        "branch-relations-v1",
    )
    facts = replace(_conforming_facts(bazi_facts), relations=(unrelated,))

    result = _provider(facts).calculate(None, None, None)

    assert result.relations[0] is unrelated
    assert any(item.relation_type == "five_element_controls" for item in result.relations)


def test_candidate_provider_rejects_preexisting_governed_relations(bazi_facts) -> None:
    existing = BaziRelationFact(
        "five_element_controls",
        ("year.stem", "month.stem"),
        (PillarPosition.YEAR, PillarPosition.MONTH),
        "wuxing-control-v1",
    )
    facts = replace(_conforming_facts(bazi_facts), relations=(existing,))

    with pytest.raises(ValueError, match="GOVERNED_BAZI_RELATIONS_ALREADY_PRESENT"):
        _provider(facts).calculate(None, None, None)


@pytest.mark.parametrize(
    ("ten_god", "error"),
    [
        (
            TenGodFact(
                "year.stem",
                "比肩",
                (PillarPosition.YEAR,),
                TenGodSourceKind.UNKNOWN,
            ),
            "TEN_GOD_SUBJECT_KIND_UNRESOLVED",
        ),
        (
            TenGodFact(
                "year.hidden_stem.0",
                "比肩",
                (PillarPosition.YEAR,),
                TenGodSourceKind.VISIBLE_STEM,
            ),
            "TEN_GOD_SUBJECT_REF_INVALID",
        ),
        (
            TenGodFact(
                "month.hidden_stem.9",
                "偏印",
                (PillarPosition.MONTH,),
                TenGodSourceKind.HIDDEN_STEM,
            ),
            "TEN_GOD_SUBJECT_REF_INVALID",
        ),
        (
            TenGodFact(
                "year.stem",
                "比肩",
                (PillarPosition.DAY,),
                TenGodSourceKind.VISIBLE_STEM,
            ),
            "TEN_GOD_SOURCE_PILLAR_MISMATCH",
        ),
    ],
)
def test_candidate_provider_rejects_unjoinable_ten_god_subjects(
    bazi_facts, ten_god, error
) -> None:
    facts = replace(_conforming_facts(bazi_facts), ten_gods=(ten_god,))

    with pytest.raises(ValueError, match=error):
        _provider(facts).calculate(None, None, None)


def test_candidate_provider_is_deterministic(bazi_facts) -> None:
    facts = _conforming_facts(bazi_facts)

    first = _provider(facts).calculate(None, None, None)
    second = _provider(facts).calculate(None, None, None)

    assert first == second


def test_default_service_does_not_activate_candidate_provider(
    birth_input,
    normalized_time,
    bazi_facts,
    astrology_facts,
    runtime_config,
) -> None:
    service = ChartCalculationService(
        FixedNormalizer(normalized_time),
        FixedCalculator(bazi_facts),
        FixedCalculator(astrology_facts),
    )

    result = service.calculate(birth_input, runtime_config)

    assert result.bazi.relations == ()
