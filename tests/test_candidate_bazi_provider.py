from dataclasses import replace
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
from destiny_personality.canonical_bazi_relations import (
    canonical_relation_identity,
    load_canonical_bazi_relation_policy,
)


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
    return load_canonical_bazi_relation_policy()


def _provider(facts):
    return CandidateNeutralRelationBaziCalculator(FixedCalculator(facts), _policy())


def _conforming_facts(bazi_facts):
    return replace(
        bazi_facts,
        year_pillar=replace(
            bazi_facts.year_pillar, heavenly_stem="甲", earthly_branch="午"
        ),
        month_pillar=replace(
            bazi_facts.month_pillar, heavenly_stem="戊", earthly_branch="辰"
        ),
        hidden_stems=(
            HiddenStemsFact(PillarPosition.YEAR, ("丁", "己")),
            HiddenStemsFact(PillarPosition.MONTH, ("戊", "乙", "癸")),
            HiddenStemsFact(PillarPosition.DAY, ("丁", "己")),
            HiddenStemsFact(PillarPosition.HOUR, ("丁", "己")),
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
    assert policy.provider_authority == "conformance_reference_only"
    assert policy.default_provider_activation is False
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


def test_provider_hidden_stem_order_cannot_change_subject_identity(
    bazi_facts,
) -> None:
    canonical = _conforming_facts(bazi_facts)
    reversed_month = replace(
        canonical,
        hidden_stems=tuple(
            HiddenStemsFact(item.pillar, ("癸", "乙", "戊"))
            if item.pillar is PillarPosition.MONTH
            else item
            for item in canonical.hidden_stems
        ),
        ten_gods=tuple(
            replace(item, subject_ref="month.hidden_stem.2")
            if item.source_kind is TenGodSourceKind.HIDDEN_STEM
            else item
            for item in canonical.ten_gods
        ),
    )

    canonical_result = _provider(canonical).calculate(None, None, None)
    reversed_result = _provider(reversed_month).calculate(None, None, None)

    assert canonical_result == reversed_result
    assert canonical_result.hidden_stems[1].stems == ("戊", "乙", "癸")
    assert canonical_result.ten_gods[1].subject_ref == "month.hidden_stem.0"
    assert tuple(map(canonical_relation_identity, canonical_result.relations)) == tuple(
        map(canonical_relation_identity, reversed_result.relations)
    )


def test_candidate_provider_rejects_wrong_hidden_stem_membership(bazi_facts) -> None:
    facts = _conforming_facts(bazi_facts)
    invalid = replace(
        facts,
        hidden_stems=tuple(
            HiddenStemsFact(item.pillar, ("戊", "乙", "壬"))
            if item.pillar is PillarPosition.MONTH
            else item
            for item in facts.hidden_stems
        ),
    )

    with pytest.raises(ValueError, match="HIDDEN_STEM_SET_MISMATCH"):
        _provider(invalid).calculate(None, None, None)


def test_candidate_provider_requires_hidden_stems_for_every_present_pillar(
    bazi_facts,
) -> None:
    facts = _conforming_facts(bazi_facts)
    incomplete = replace(
        facts,
        hidden_stems=tuple(
            item
            for item in facts.hidden_stems
            if item.pillar is not PillarPosition.HOUR
        ),
    )

    with pytest.raises(ValueError, match="HIDDEN_STEM_PILLAR_MISSING"):
        _provider(incomplete).calculate(None, None, None)


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
