from dataclasses import replace
from datetime import datetime, time, timezone
from decimal import Decimal

import pytest

from destiny_personality.calculation import (
    BirthInput,
    CalculationError,
    ChartCalculationService,
    FactMode,
    TimeBasis,
)


class RecordingNormalizer:
    def __init__(self, result, calls):
        self.result = result
        self.calls = calls

    def normalize(self, birth_input, config):
        self.calls.append(("time", birth_input, config))
        return self.result


class RecordingBaziCalculator:
    def __init__(self, result, calls):
        self.result = result
        self.calls = calls

    def calculate(self, birth_input, normalized_time, methodology):
        self.calls.append(("bazi", birth_input, normalized_time, methodology))
        return self.result


class RecordingAstrologyCalculator:
    def __init__(self, result, calls):
        self.result = result
        self.calls = calls

    def calculate(self, birth_input, normalized_time, methodology):
        self.calls.append(("astrology", birth_input, normalized_time, methodology))
        return self.result


def _service(normalized_time, bazi_facts, astrology_facts, calls):
    return ChartCalculationService(
        RecordingNormalizer(normalized_time, calls),
        RecordingBaziCalculator(bazi_facts, calls),
        RecordingAstrologyCalculator(astrology_facts, calls),
    )


def test_service_calls_isolated_backends_in_order(
    birth_input, normalized_time, bazi_facts, astrology_facts, runtime_config
) -> None:
    calls = []
    service = _service(normalized_time, bazi_facts, astrology_facts, calls)

    result = service.calculate(birth_input, runtime_config)

    assert [call[0] for call in calls] == ["time", "bazi", "astrology"]
    assert calls[1][3] is runtime_config.bazi
    assert calls[2][3] is runtime_config.astrology
    assert result.normalized_time is normalized_time
    assert result.bazi is bazi_facts
    assert result.astrology is astrology_facts


@pytest.mark.parametrize(
    ("changes", "field"),
    [
        ({"birth_date": datetime(1990, 1, 2)}, "birth_date"),
        ({"birth_time": time(3, 4, tzinfo=timezone.utc)}, "birth_time"),
        ({"timezone_name": "  "}, "timezone_name"),
        ({"latitude": 31.2}, "latitude"),
        ({"latitude": Decimal("NaN")}, "latitude"),
        ({"longitude": Decimal("Infinity")}, "longitude"),
        ({"latitude": Decimal("90.1")}, "latitude"),
        ({"longitude": Decimal("-180.1")}, "longitude"),
        (
            {"birth_time": None, "fact_mode": FactMode.TIME_SENSITIVE},
            "fact_mode",
        ),
    ],
)
def test_invalid_birth_input_fails_before_backends(
    birth_input,
    normalized_time,
    bazi_facts,
    astrology_facts,
    runtime_config,
    changes,
    field,
) -> None:
    calls = []
    service = _service(normalized_time, bazi_facts, astrology_facts, calls)

    with pytest.raises(CalculationError) as caught:
        service.calculate(replace(birth_input, **changes), runtime_config)

    assert caught.value.code == "BIRTH_INPUT_ERROR"
    assert caught.value.field == field
    assert calls == []


def test_standard_time_requires_methodology_permission(
    birth_input, normalized_time, bazi_facts, astrology_facts, runtime_config
) -> None:
    calls = []
    service = _service(normalized_time, bazi_facts, astrology_facts, calls)
    blocked_time = replace(runtime_config.bazi.time, allow_standard_time_mode=False)
    blocked_bazi = replace(runtime_config.bazi, time=blocked_time)
    blocked_config = replace(runtime_config, bazi=blocked_bazi)
    standard_input = replace(birth_input, time_basis=TimeBasis.STANDARD_TIME)

    with pytest.raises(CalculationError) as caught:
        service.calculate(standard_input, blocked_config)

    assert caught.value.code == "BIRTH_INPUT_ERROR"
    assert caught.value.field == "time_basis"
    assert calls == []
