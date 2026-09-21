from dataclasses import FrozenInstanceError
from datetime import date, datetime, time, timezone
from decimal import Decimal

import pytest

from destiny_personality.calculation import (
    AstrologyAspectFact,
    AstrologyChartFacts,
    AstrologyPlacement,
    BaziChartFacts,
    BaziPillar,
    BaziRelationFact,
    BirthInput,
    DeterministicChartFacts,
    DignityFact,
    FactMode,
    HiddenStemsFact,
    HouseCusp,
    NormalizedBirthTime,
    PillarPosition,
    TenGodFact,
    TimeBasis,
)


def test_calculation_models_are_immutable_and_use_stable_wire_values() -> None:
    birth_input = BirthInput(
        birth_date=date(1990, 1, 2),
        birth_time=time(3, 4, 5),
        timezone_name="Asia/Shanghai",
        latitude=Decimal("31.2304"),
        longitude=Decimal("121.4737"),
        time_basis=TimeBasis.TRUE_SOLAR_TIME,
        fact_mode=FactMode.TIME_SENSITIVE,
    )
    normalized = NormalizedBirthTime(
        birth_date=birth_input.birth_date,
        historical_civil_time=datetime(1990, 1, 2, 3, 4, 5),
        local_standard_time=datetime(1990, 1, 2, 3, 4, 5),
        utc_time=datetime(1990, 1, 1, 19, 4, 5, tzinfo=timezone.utc),
        true_solar_time=datetime(1990, 1, 2, 3, 10),
        timezone_name=birth_input.timezone_name,
        dst_was_applied=False,
        time_basis=birth_input.time_basis,
        fact_mode=birth_input.fact_mode,
        sensitivity_reasons=(),
    )
    pillar = BaziPillar("庚", "午")
    bazi = BaziChartFacts(
        methodology_version="bazi-core-v1.0",
        year_pillar=pillar,
        month_pillar=pillar,
        day_pillar=pillar,
        hour_pillar=pillar,
        hidden_stems=(HiddenStemsFact(PillarPosition.YEAR, ("丁", "己")),),
        ten_gods=(
            TenGodFact(
                "year.stem",
                "比肩",
                (PillarPosition.YEAR, PillarPosition.DAY),
            ),
        ),
        relations=(
            BaziRelationFact(
                "six_clashes",
                ("year", "month"),
                (PillarPosition.YEAR, PillarPosition.MONTH),
            ),
        ),
    )
    astrology = AstrologyChartFacts(
        methodology_version="western-tropical-v1.0",
        placements=(
            AstrologyPlacement(
                "Sun", Decimal("281.0"), "Capricorn", Decimal("11.0"), 2
            ),
        ),
        aspects=(
            AstrologyAspectFact(
                "Sun", "Moon", "conjunction", Decimal("1.0")
            ),
        ),
        ascendant=Decimal("210.0"),
        mc=Decimal("120.0"),
        house_cusps=(HouseCusp(1, Decimal("210.0")),),
        dignities=(DignityFact("Sun", "detriment"),),
    )
    facts = DeterministicChartFacts(normalized, bazi, astrology)

    assert TimeBasis.TRUE_SOLAR_TIME.value == "true_solar_time"
    assert FactMode.STABLE_ONLY.value == "stable_only"
    assert [position.value for position in PillarPosition] == [
        "year",
        "month",
        "day",
        "hour",
    ]
    assert facts.bazi.hidden_stems[0].pillar is PillarPosition.YEAR
    assert facts.bazi.ten_gods[0].source_pillars == (
        PillarPosition.YEAR,
        PillarPosition.DAY,
    )
    assert facts.bazi.relations[0].source_pillars == (
        PillarPosition.YEAR,
        PillarPosition.MONTH,
    )
    assert isinstance(facts.bazi.hidden_stems, tuple)
    assert isinstance(facts.astrology.placements, tuple)
    with pytest.raises(FrozenInstanceError):
        facts.normalized_time.fact_mode = FactMode.STABLE_ONLY
