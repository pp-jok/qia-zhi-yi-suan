from dataclasses import replace
from datetime import datetime
from decimal import Decimal

import pytest

from destiny_personality.calculation import (
    AstrologyAspectFact,
    DignityFact,
    BaziPillar,
    CalculationError,
    ChartCalculationService,
    FactMode,
    NormalizedBirthTime,
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


def _service(normalized, bazi, astrology, calls):
    return ChartCalculationService(
        FixedNormalizer(normalized, calls),
        FixedBazi(bazi, calls),
        FixedAstrology(astrology, calls),
    )


@pytest.mark.parametrize(
    ("normalized_factory", "field"),
    [
        (lambda value: object(), None),
        (
            lambda value: replace(value, timezone_name="Europe/London"),
            "timezone_name",
        ),
        (
            lambda value: replace(value, utc_time=datetime(1990, 1, 1, 19, 4, 5)),
            "utc_time",
        ),
        (lambda value: replace(value, true_solar_time=None), "true_solar_time"),
        (
            lambda value: replace(value, sensitivity_reasons=["boundary"]),
            "sensitivity_reasons",
        ),
    ],
)
def test_invalid_normalized_time_stops_before_calculators(
    birth_input,
    normalized_time,
    bazi_facts,
    astrology_facts,
    runtime_config,
    normalized_factory,
    field,
) -> None:
    calls = []
    service = _service(
        normalized_factory(normalized_time), bazi_facts, astrology_facts, calls
    )

    with pytest.raises(CalculationError) as caught:
        service.calculate(birth_input, runtime_config)

    assert caught.value.code == "CALCULATION_CONTRACT_ERROR"
    assert caught.value.system == "time"
    assert caught.value.field == field
    assert calls == ["time"]


def test_unknown_time_cannot_return_normalized_clock_values(
    birth_input, bazi_facts, astrology_facts, runtime_config
) -> None:
    unknown_input = replace(
        birth_input, birth_time=None, fact_mode=FactMode.STABLE_ONLY
    )
    invalid_normalized = NormalizedBirthTime(
        birth_date=unknown_input.birth_date,
        historical_civil_time=datetime(1990, 1, 2, 3, 4, 5),
        local_standard_time=None,
        utc_time=None,
        true_solar_time=None,
        timezone_name=unknown_input.timezone_name,
        dst_was_applied=None,
        time_basis=unknown_input.time_basis,
        fact_mode=unknown_input.fact_mode,
        sensitivity_reasons=(),
    )
    calls = []
    service = _service(invalid_normalized, bazi_facts, astrology_facts, calls)

    with pytest.raises(CalculationError) as caught:
        service.calculate(unknown_input, runtime_config)

    assert caught.value.code == "CALCULATION_CONTRACT_ERROR"
    assert caught.value.field == "historical_civil_time"
    assert calls == ["time"]


def test_bazi_methodology_version_must_match_runtime_config(
    birth_input, normalized_time, bazi_facts, astrology_facts, runtime_config
) -> None:
    calls = []
    service = _service(
        normalized_time,
        replace(bazi_facts, methodology_version="bazi-core-v9.9"),
        astrology_facts,
        calls,
    )

    with pytest.raises(CalculationError) as caught:
        service.calculate(birth_input, runtime_config)

    assert caught.value.code == "METHODOLOGY_VERSION_MISMATCH"
    assert caught.value.system == "bazi"
    assert calls == ["time", "bazi"]


@pytest.mark.parametrize(
    ("bazi_factory", "field"),
    [
        (lambda value: object(), None),
        (
            lambda value: replace(
                value, year_pillar=BaziPillar("", "午")
            ),
            "year_pillar.heavenly_stem",
        ),
        (lambda value: replace(value, hour_pillar=None), "hour_pillar"),
        (lambda value: replace(value, hidden_stems=[]), "hidden_stems"),
    ],
)
def test_invalid_bazi_facts_stop_before_astrology(
    birth_input,
    normalized_time,
    bazi_facts,
    astrology_facts,
    runtime_config,
    bazi_factory,
    field,
) -> None:
    calls = []
    service = _service(
        normalized_time, bazi_factory(bazi_facts), astrology_facts, calls
    )

    with pytest.raises(CalculationError) as caught:
        service.calculate(birth_input, runtime_config)

    assert caught.value.code == "CALCULATION_CONTRACT_ERROR"
    assert caught.value.system == "bazi"
    assert caught.value.field == field
    assert calls == ["time", "bazi"]


def test_stable_only_bazi_cannot_return_hour_pillar(
    birth_input, normalized_time, bazi_facts, astrology_facts, runtime_config
) -> None:
    stable_input = replace(birth_input, fact_mode=FactMode.STABLE_ONLY)
    stable_normalized = replace(normalized_time, fact_mode=FactMode.STABLE_ONLY)
    calls = []
    service = _service(stable_normalized, bazi_facts, astrology_facts, calls)

    with pytest.raises(CalculationError) as caught:
        service.calculate(stable_input, runtime_config)

    assert caught.value.code == "CALCULATION_CONTRACT_ERROR"
    assert caught.value.field == "hour_pillar"
    assert calls == ["time", "bazi"]


def test_astrology_methodology_version_must_match_runtime_config(
    birth_input, normalized_time, bazi_facts, astrology_facts, runtime_config
) -> None:
    calls = []
    service = _service(
        normalized_time,
        bazi_facts,
        replace(astrology_facts, methodology_version="western-tropical-v9.9"),
        calls,
    )

    with pytest.raises(CalculationError) as caught:
        service.calculate(birth_input, runtime_config)

    assert caught.value.code == "METHODOLOGY_VERSION_MISMATCH"
    assert caught.value.system == "astrology"


@pytest.mark.parametrize(
    ("astrology_factory", "field"),
    [
        (lambda value: object(), None),
        (lambda value: replace(value, placements=value.placements[:-1]), "placements"),
        (
            lambda value: replace(
                value,
                placements=(
                    replace(value.placements[0], longitude=Decimal("360")),
                    *value.placements[1:],
                ),
            ),
            "placements.0.longitude",
        ),
        (lambda value: replace(value, ascendant=None), "ascendant"),
        (
            lambda value: replace(
                value,
                aspects=(
                    AstrologyAspectFact(
                        "Sun", "Moon", "conjunction", Decimal("10")
                    ),
                ),
            ),
            "aspects.0.orb",
        ),
        (
            lambda value: replace(
                value, dignities=(DignityFact("Sun", "peregrine"),)
            ),
            "dignities.0.dignity",
        ),
    ],
)
def test_invalid_astrology_facts_are_rejected(
    birth_input,
    normalized_time,
    bazi_facts,
    astrology_facts,
    runtime_config,
    astrology_factory,
    field,
) -> None:
    calls = []
    service = _service(
        normalized_time, bazi_facts, astrology_factory(astrology_facts), calls
    )

    with pytest.raises(CalculationError) as caught:
        service.calculate(birth_input, runtime_config)

    assert caught.value.code == "CALCULATION_CONTRACT_ERROR"
    assert caught.value.system == "astrology"
    assert caught.value.field == field


def test_stable_only_accepts_only_time_independent_facts(
    birth_input, normalized_time, bazi_facts, astrology_facts, runtime_config
) -> None:
    stable_input = replace(birth_input, fact_mode=FactMode.STABLE_ONLY)
    stable_normalized = replace(normalized_time, fact_mode=FactMode.STABLE_ONLY)
    stable_bazi = replace(bazi_facts, hour_pillar=None)
    stable_placements = tuple(
        replace(placement, house=None) for placement in astrology_facts.placements
    )
    stable_astrology = replace(
        astrology_facts,
        placements=stable_placements,
        ascendant=None,
        mc=None,
        house_cusps=(),
    )
    calls = []
    service = _service(stable_normalized, stable_bazi, stable_astrology, calls)

    result = service.calculate(stable_input, runtime_config)

    assert result.astrology is stable_astrology
    assert calls == ["time", "bazi", "astrology"]
