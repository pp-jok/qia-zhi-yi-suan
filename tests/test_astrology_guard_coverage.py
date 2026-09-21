from dataclasses import replace
from decimal import Decimal

import pytest

from destiny_personality.calculation import (
    AstrologyAspectFact,
    CalculationError,
    ChartCalculationService,
    DignityFact,
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


def _assert_rejected(
    birth_input,
    normalized_time,
    bazi_facts,
    astrology_facts,
    runtime_config,
    expected_field,
) -> None:
    calls = []
    service = ChartCalculationService(
        FixedNormalizer(normalized_time, calls),
        FixedBazi(bazi_facts, calls),
        FixedAstrology(astrology_facts, calls),
    )

    with pytest.raises(CalculationError) as caught:
        service.calculate(birth_input, runtime_config)

    assert caught.value.code == "CALCULATION_CONTRACT_ERROR"
    assert caught.value.system == "astrology"
    assert caught.value.field == expected_field
    assert calls == ["time", "bazi", "astrology"]


@pytest.mark.parametrize(
    ("facts_factory", "field"),
    [
        (
            lambda facts, config: replace(
                facts,
                placements=(
                    facts.placements[0],
                    replace(facts.placements[1], body=facts.placements[0].body),
                    *facts.placements[2:],
                ),
            ),
            "placements.1.body",
        ),
        (
            lambda facts, config: replace(
                facts,
                aspects=(
                    AstrologyAspectFact(
                        "Sun", "Moon", "conjunction", Decimal("1")
                    ),
                    AstrologyAspectFact(
                        "Moon", "Sun", "conjunction", Decimal("1")
                    ),
                ),
            ),
            "aspects.1",
        ),
        (
            lambda facts, config: replace(
                facts,
                dignities=(
                    DignityFact("Sun", "domicile"),
                    DignityFact("Sun", "domicile"),
                ),
            ),
            "dignities.1",
        ),
    ],
)
def test_duplicate_astrology_facts_are_rejected(
    birth_input,
    normalized_time,
    bazi_facts,
    astrology_facts,
    runtime_config,
    facts_factory,
    field,
) -> None:
    _assert_rejected(
        birth_input,
        normalized_time,
        bazi_facts,
        facts_factory(astrology_facts, runtime_config),
        runtime_config,
        field,
    )


@pytest.mark.parametrize(
    ("facts_factory", "field"),
    [
        (
            lambda facts: replace(
                facts,
                house_cusps=(
                    replace(facts.house_cusps[0], house=0),
                    *facts.house_cusps[1:],
                ),
            ),
            "house_cusps.0.house",
        ),
        (
            lambda facts: replace(
                facts,
                house_cusps=(
                    facts.house_cusps[0],
                    replace(facts.house_cusps[1], house=1),
                    *facts.house_cusps[2:],
                ),
            ),
            "house_cusps.1.house",
        ),
        (
            lambda facts: replace(
                facts,
                house_cusps=(
                    replace(facts.house_cusps[0], longitude=Decimal("360")),
                    *facts.house_cusps[1:],
                ),
            ),
            "house_cusps.0.longitude",
        ),
        (
            lambda facts: replace(facts, house_cusps=facts.house_cusps[:-1]),
            "house_cusps",
        ),
    ],
)
def test_invalid_house_cusps_are_rejected(
    birth_input,
    normalized_time,
    bazi_facts,
    astrology_facts,
    runtime_config,
    facts_factory,
    field,
) -> None:
    _assert_rejected(
        birth_input,
        normalized_time,
        bazi_facts,
        facts_factory(astrology_facts),
        runtime_config,
        field,
    )


@pytest.mark.parametrize(
    ("aspect_factory", "field"),
    [
        (
            lambda config: AstrologyAspectFact(
                "Ascendant", "MC", "square", Decimal("1")
            ),
            "aspects.0",
        ),
        (
            lambda config: AstrologyAspectFact(
                "Sun", "Ascendant", "trine", Decimal("1")
            ),
            "aspects.0.aspect_type",
        ),
        (
            lambda config: AstrologyAspectFact(
                "Sun",
                "Ascendant",
                "conjunction",
                Decimal(config.astrology.aspects.angle_orb) + Decimal("0.1"),
            ),
            "aspects.0.orb",
        ),
    ],
)
def test_invalid_angle_aspects_are_rejected(
    birth_input,
    normalized_time,
    bazi_facts,
    astrology_facts,
    runtime_config,
    aspect_factory,
    field,
) -> None:
    invalid_facts = replace(
        astrology_facts, aspects=(aspect_factory(runtime_config),)
    )
    _assert_rejected(
        birth_input,
        normalized_time,
        bazi_facts,
        invalid_facts,
        runtime_config,
        field,
    )


@pytest.mark.parametrize(
    ("facts_factory", "field"),
    [
        (lambda facts: replace(facts, placements=list(facts.placements)), "placements"),
        (lambda facts: replace(facts, aspects=(object(),)), "aspects.0"),
        (lambda facts: replace(facts, house_cusps=(object(),)), "house_cusps.0"),
        (lambda facts: replace(facts, dignities=(object(),)), "dignities.0"),
    ],
)
def test_invalid_astrology_collection_shapes_are_rejected(
    birth_input,
    normalized_time,
    bazi_facts,
    astrology_facts,
    runtime_config,
    facts_factory,
    field,
) -> None:
    _assert_rejected(
        birth_input,
        normalized_time,
        bazi_facts,
        facts_factory(astrology_facts),
        runtime_config,
        field,
    )
