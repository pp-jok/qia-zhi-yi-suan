from dataclasses import fields, replace
import pytest

from destiny_personality.calculation import HiddenStemsFact, PillarPosition
from destiny_personality.calculation.models import BaziRelationFact
from destiny_personality.calculation import DeterministicChartFacts


def _load_policy():
    from destiny_personality.canonical_bazi_relations import (
        load_canonical_bazi_relation_policy,
    )

    return load_canonical_bazi_relation_policy()


def _derive(facts):
    from destiny_personality.neutral_bazi_relations import (
        derive_candidate_neutral_relations,
    )

    return derive_candidate_neutral_relations(facts, _load_policy())


@pytest.mark.parametrize(
    ("controller", "controlled"),
    [
        ("甲", "戊"),
        ("戊", "壬"),
        ("壬", "丙"),
        ("丙", "庚"),
        ("庚", "甲"),
    ],
)
def test_raw_five_element_control_pairs_are_project_deterministic(
    bazi_facts, controller: str, controlled: str
) -> None:
    chart = replace(
        bazi_facts,
        year_pillar=replace(bazi_facts.year_pillar, heavenly_stem=controller),
        month_pillar=replace(bazi_facts.month_pillar, heavenly_stem=controlled),
        hidden_stems=(),
    )

    relations = _derive(chart)

    assert BaziRelationFact(
        "five_element_controls",
        ("year.stem", "month.stem"),
        (PillarPosition.YEAR, PillarPosition.MONTH),
        "wuxing-control-v1",
    ) in relations


def test_relation_participant_direction_is_stable(bazi_facts) -> None:
    chart = replace(
        bazi_facts,
        year_pillar=replace(bazi_facts.year_pillar, heavenly_stem="甲"),
        month_pillar=replace(bazi_facts.month_pillar, heavenly_stem="戊"),
        hidden_stems=(),
    )

    relations = _derive(chart)

    assert any(
        relation.participant_refs == ("year.stem", "month.stem")
        for relation in relations
    )
    assert not any(
        relation.participant_refs == ("month.stem", "year.stem")
        and relation.relation_type == "five_element_controls"
        for relation in relations
    )


def test_bazi_relation_facts_are_deterministic_and_deduplicated(bazi_facts) -> None:
    first = _derive(bazi_facts)
    second = _derive(bazi_facts)

    assert first == second
    identities = [
        (item.relation_type, item.participant_refs, item.source_pillars)
        for item in first
    ]
    assert identities == sorted(identities)
    assert len(identities) == len(set(identities))


def test_relation_fact_uses_stable_visible_and_hidden_subject_refs(bazi_facts) -> None:
    chart = replace(
        bazi_facts,
        year_pillar=replace(bazi_facts.year_pillar, heavenly_stem="甲"),
        hidden_stems=(
            HiddenStemsFact(PillarPosition.MONTH, ("戊", "己")),
        ),
    )

    relations = _derive(chart)
    refs = {ref for item in relations for ref in item.participant_refs}

    assert "year.stem" in refs
    assert "month.hidden_stem.0" in refs
    assert "month.hidden_stem.1" in refs


def test_relation_fact_rejects_unknown_stem(bazi_facts) -> None:
    chart = replace(
        bazi_facts,
        year_pillar=replace(bazi_facts.year_pillar, heavenly_stem="UNKNOWN"),
    )

    with pytest.raises(ValueError, match="UNKNOWN_BAZI_STEM"):
        _derive(chart)


def test_relation_fact_contains_no_methodology_fields() -> None:
    policy = _load_policy()
    model_fields = {field.name for field in fields(BaziRelationFact)}

    assert model_fields == {
        "relation_type",
        "participant_refs",
        "source_pillars",
        "rule_version",
    }
    assert model_fields.isdisjoint(policy.prohibited_fields)
    assert {
        "operative",
        "qualification",
        "rescue",
        "effective",
        "strength_score",
        "dao_shi",
        "primitive_direction",
    }.issubset(policy.prohibited_fields)


def test_candidate_relations_round_trip_existing_fact_codec(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.deterministic_facts_codec import (
        deterministic_facts_from_dict,
        deterministic_facts_to_dict,
    )

    chart = replace(
        bazi_facts,
        year_pillar=replace(bazi_facts.year_pillar, heavenly_stem="甲"),
        month_pillar=replace(bazi_facts.month_pillar, heavenly_stem="戊"),
        hidden_stems=(),
    )
    chart = replace(chart, relations=_derive(chart))
    facts = DeterministicChartFacts(normalized_time, chart, astrology_facts)

    payload = deterministic_facts_to_dict(facts)
    decoded = deterministic_facts_from_dict(payload)

    assert payload["bazi"]["relations"][0]["rule_version"] == "wuxing-control-v1"
    assert decoded.bazi.relations == chart.relations
