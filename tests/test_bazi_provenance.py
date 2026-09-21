from dataclasses import replace

import pytest

from destiny_personality.calculation import (
    BaziRelationFact,
    CalculationError,
    ChartCalculationService,
    FactMode,
    HiddenStemsFact,
    PillarPosition,
    TenGodFact,
    TenGodSourceKind,
)


class FixedNormalizer:
    def __init__(self, result, calls):
        self.result = result
        self.calls = calls

    def normalize(self, birth_input, config):
        self.calls.append("time")
        return self.result


class FixedBazi:
    def __init__(self, result, calls):
        self.result = result
        self.calls = calls

    def calculate(self, birth_input, normalized_time, methodology):
        self.calls.append("bazi")
        return self.result


class FixedAstrology:
    def __init__(self, result, calls):
        self.result = result
        self.calls = calls

    def calculate(self, birth_input, normalized_time, methodology):
        self.calls.append("astrology")
        return self.result


def _service(normalized_time, bazi_facts, astrology_facts, calls):
    return ChartCalculationService(
        FixedNormalizer(normalized_time, calls),
        FixedBazi(bazi_facts, calls),
        FixedAstrology(astrology_facts, calls),
    )


@pytest.mark.parametrize(
    ("facts_update", "field"),
    [
        (
            {"hidden_stems": (HiddenStemsFact("year", ("庚",)),)},
            "hidden_stems.0.pillar",
        ),
        (
            {
                "ten_gods": (
                    TenGodFact("year.stem", "peer", ()),
                )
            },
            "ten_gods.0.source_pillars",
        ),
        (
            {
                "ten_gods": (
                    TenGodFact(
                        "year.stem",
                        "peer",
                        (PillarPosition.YEAR, PillarPosition.YEAR),
                    ),
                )
            },
            "ten_gods.0.source_pillars.1",
        ),
        (
            {
                "relations": (
                    BaziRelationFact(
                        "clash",
                        ("year.branch", "day.branch"),
                        ("year",),
                    ),
                )
            },
            "relations.0.source_pillars.0",
        ),
    ],
)
def test_invalid_declared_pillar_provenance_is_rejected(
    birth_input,
    normalized_time,
    bazi_facts,
    astrology_facts,
    runtime_config,
    facts_update,
    field,
) -> None:
    calls = []
    invalid_bazi = replace(bazi_facts, **facts_update)
    service = _service(normalized_time, invalid_bazi, astrology_facts, calls)

    with pytest.raises(CalculationError) as caught:
        service.calculate(birth_input, runtime_config)

    assert caught.value.code == "CALCULATION_CONTRACT_ERROR"
    assert caught.value.system == "bazi"
    assert caught.value.field == field
    assert calls == ["time", "bazi"]


@pytest.mark.parametrize(
    ("facts_update", "field"),
    [
        (
            {"hidden_stems": (HiddenStemsFact(PillarPosition.HOUR, ("庚",)),)},
            "hidden_stems.0.pillar",
        ),
        (
            {
                "ten_gods": (
                    TenGodFact(
                        "hour.stem",
                        "peer",
                        (PillarPosition.HOUR, PillarPosition.DAY),
                    ),
                )
            },
            "ten_gods.0.source_pillars.0",
        ),
        (
            {
                "relations": (
                    BaziRelationFact(
                        "clash",
                        ("year.branch", "hour.branch"),
                        (PillarPosition.YEAR, PillarPosition.HOUR),
                    ),
                )
            },
            "relations.0.source_pillars.1",
        ),
    ],
)
def test_stable_only_rejects_declared_hour_provenance(
    birth_input,
    normalized_time,
    bazi_facts,
    astrology_facts,
    runtime_config,
    facts_update,
    field,
) -> None:
    stable_input = replace(birth_input, fact_mode=FactMode.STABLE_ONLY)
    stable_time = replace(normalized_time, fact_mode=FactMode.STABLE_ONLY)
    invalid_bazi = replace(bazi_facts, hour_pillar=None, **facts_update)
    calls = []
    service = _service(stable_time, invalid_bazi, astrology_facts, calls)

    with pytest.raises(CalculationError) as caught:
        service.calculate(stable_input, runtime_config)

    assert caught.value.code == "CALCULATION_CONTRACT_ERROR"
    assert caught.value.system == "bazi"
    assert caught.value.field == field
    assert calls == ["time", "bazi"]


def test_time_sensitive_accepts_valid_declared_hour_provenance(
    birth_input,
    normalized_time,
    bazi_facts,
    astrology_facts,
    runtime_config,
) -> None:
    bazi_with_provenance = replace(
        bazi_facts,
        hidden_stems=(HiddenStemsFact(PillarPosition.HOUR, ("庚",)),),
        ten_gods=(
            TenGodFact(
                "hour.stem",
                "peer",
                (PillarPosition.HOUR, PillarPosition.DAY),
            ),
        ),
        relations=(
            BaziRelationFact(
                "clash",
                ("year.branch", "hour.branch"),
                (PillarPosition.YEAR, PillarPosition.HOUR),
            ),
        ),
    )
    calls = []
    service = _service(
        normalized_time, bazi_with_provenance, astrology_facts, calls
    )

    result = service.calculate(birth_input, runtime_config)

    assert result.bazi is bazi_with_provenance
    assert calls == ["time", "bazi", "astrology"]


def test_ten_god_source_kind_is_preserved_in_validated_facts(
    birth_input,
    normalized_time,
    bazi_facts,
    astrology_facts,
    runtime_config,
) -> None:
    bazi_with_source_kind = replace(
        bazi_facts,
        ten_gods=(
            TenGodFact(
                "year.stem",
                "peer",
                (PillarPosition.YEAR,),
                TenGodSourceKind.VISIBLE_STEM,
            ),
        ),
    )
    calls = []
    service = _service(
        normalized_time, bazi_with_source_kind, astrology_facts, calls
    )

    result = service.calculate(birth_input, runtime_config)

    assert result.bazi.ten_gods[0].source_kind is TenGodSourceKind.VISIBLE_STEM
