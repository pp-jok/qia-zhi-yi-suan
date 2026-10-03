import json
from dataclasses import replace

import pytest

from destiny_personality.calculation import (
    BaziPillar,
    BaziRelationFact,
    DeterministicChartFacts,
    HiddenStemsFact,
    PillarPosition,
)
from destiny_personality.canonical_bazi_relations import (
    CanonicalBaziRelationError,
    load_canonical_bazi_relation_policy,
    validate_canonical_bazi_relations,
)
from destiny_personality.deterministic_facts_codec import (
    deterministic_facts_to_dict,
    load_validated_deterministic_facts,
)


def _canonical_chart(bazi_facts):
    return replace(
        bazi_facts,
        year_pillar=BaziPillar("甲", "午"),
        month_pillar=BaziPillar("戊", "辰"),
        day_pillar=BaziPillar("壬", "子"),
        hour_pillar=BaziPillar("丁", "午"),
        hidden_stems=(
            HiddenStemsFact(PillarPosition.YEAR, ("丁", "己")),
            HiddenStemsFact(PillarPosition.MONTH, ("戊", "乙", "癸")),
            HiddenStemsFact(PillarPosition.DAY, ("癸",)),
            HiddenStemsFact(PillarPosition.HOUR, ("丁", "己")),
        ),
    )


def _relation(controller, controlled, pillars, *, version="wuxing-control-v1"):
    return BaziRelationFact(
        "five_element_controls", (controller, controlled),
        pillars, version,
    )


def test_canonical_relation_resolves_real_subjects_and_control_truth(bazi_facts):
    chart = replace(
        _canonical_chart(bazi_facts),
        relations=(
            _relation(
                "month.stem", "day.stem",
                (PillarPosition.MONTH, PillarPosition.DAY),
            ),
            _relation(
                "year.stem", "month.stem",
                (PillarPosition.YEAR, PillarPosition.MONTH),
            ),
        ),
    )

    validate_canonical_bazi_relations(
        chart, load_canonical_bazi_relation_policy()
    )


@pytest.mark.parametrize(
    ("relation", "detail"),
    [
        (
            _relation(
                "year.stem", "hour.stem",
                (PillarPosition.YEAR, PillarPosition.HOUR),
            ),
            "CONTROL_TRUTH_MISMATCH",
        ),
        (
            _relation(
                "year.stem", "month.hidden_stem.9",
                (PillarPosition.YEAR, PillarPosition.MONTH),
            ),
            "SUBJECT_REF_UNRESOLVED",
        ),
        (
            _relation(
                "year.stem", "month.stem",
                (PillarPosition.YEAR, PillarPosition.MONTH),
                version="wuxing-control-custom",
            ),
            "RULE_VERSION_UNAPPROVED",
        ),
    ],
)
def test_canonical_relation_rejects_false_or_unresolved_claims(
    bazi_facts, relation, detail
):
    chart = replace(_canonical_chart(bazi_facts), relations=(relation,))

    with pytest.raises(CanonicalBaziRelationError, match=detail):
        validate_canonical_bazi_relations(
            chart, load_canonical_bazi_relation_policy()
        )


def test_canonical_relation_requires_project_hidden_stem_order(bazi_facts):
    chart = _canonical_chart(bazi_facts)
    chart = replace(
        chart,
        hidden_stems=(
            chart.hidden_stems[0],
            HiddenStemsFact(PillarPosition.MONTH, ("癸", "乙", "戊")),
            *chart.hidden_stems[2:],
        ),
        relations=(
            _relation(
                "year.stem", "month.stem",
                (PillarPosition.YEAR, PillarPosition.MONTH),
            ),
        ),
    )

    with pytest.raises(CanonicalBaziRelationError, match="HIDDEN_STEM_ORDER_MISMATCH"):
        validate_canonical_bazi_relations(
            chart, load_canonical_bazi_relation_policy()
        )


def test_canonical_relation_rejects_duplicate_identity_and_unstable_order(bazi_facts):
    first = _relation(
        "year.stem", "month.stem",
        (PillarPosition.YEAR, PillarPosition.MONTH),
    )
    second = _relation(
        "month.stem", "day.stem",
        (PillarPosition.MONTH, PillarPosition.DAY),
    )
    policy = load_canonical_bazi_relation_policy()

    with pytest.raises(CanonicalBaziRelationError, match="DUPLICATE_IDENTITY"):
        validate_canonical_bazi_relations(
            replace(_canonical_chart(bazi_facts), relations=(first, first)), policy
        )
    with pytest.raises(CanonicalBaziRelationError, match="ORDER_INVALID"):
        validate_canonical_bazi_relations(
            replace(_canonical_chart(bazi_facts), relations=(first, second)), policy
        )


def test_empty_and_legacy_relation_collections_remain_compatible(bazi_facts):
    policy = load_canonical_bazi_relation_policy()
    validate_canonical_bazi_relations(bazi_facts, policy)
    validate_canonical_bazi_relations(
        replace(
            bazi_facts,
            relations=(
                BaziRelationFact(
                    "six_clashes",
                    ("year.branch", "month.branch"),
                    (PillarPosition.YEAR, PillarPosition.MONTH),
                ),
            ),
        ),
        policy,
    )


def test_public_qualified_facts_loader_enforces_canonical_relation_boundary(
    tmp_path, normalized_time, bazi_facts, astrology_facts
):
    invalid_chart = replace(
        _canonical_chart(bazi_facts),
        relations=(
            _relation(
                "year.stem", "hour.stem",
                (PillarPosition.YEAR, PillarPosition.HOUR),
            ),
        ),
    )
    facts = DeterministicChartFacts(normalized_time, invalid_chart, astrology_facts)
    payload = deterministic_facts_to_dict(facts)
    payload.update(
        {
            "schema_version": "deterministic-facts-v1",
            "fact_mode": facts.normalized_time.fact_mode.value,
            "methodology_versions": {
                "bazi": facts.bazi.methodology_version,
                "astrology": facts.astrology.methodology_version,
            },
            "provenance_refs": ["test:canonical-boundary"],
            "validation_summary": {"structure": "passed"},
        }
    )
    path = tmp_path / "facts.json"
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(ValueError, match="BAZI_RELATION_FACT_INVALID"):
        load_validated_deterministic_facts(path)
