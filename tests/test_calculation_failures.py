import pytest

from destiny_personality.calculation import CalculationError, ChartCalculationService


class Stage:
    def __init__(self, name, result, calls, error=None):
        self.name = name
        self.result = result
        self.calls = calls
        self.error = error

    def _run(self):
        self.calls.append(self.name)
        if self.error is not None:
            raise self.error
        return self.result

    def normalize(self, birth_input, config):
        return self._run()

    def calculate(self, birth_input, normalized_time, methodology):
        return self._run()


@pytest.mark.parametrize(
    ("stage", "expected_code", "expected_calls"),
    [
        ("time", "TIME_NORMALIZATION_ERROR", ["time"]),
        ("bazi", "CALCULATION_FATAL", ["time", "bazi"]),
        (
            "astrology",
            "CALCULATION_FATAL",
            ["time", "bazi", "astrology"],
        ),
    ],
)
def test_unexpected_stage_failures_are_wrapped_and_short_circuit(
    birth_input,
    normalized_time,
    bazi_facts,
    astrology_facts,
    runtime_config,
    stage,
    expected_code,
    expected_calls,
) -> None:
    calls = []
    original = ValueError("backend failed")
    normalizer = Stage(
        "time", normalized_time, calls, original if stage == "time" else None
    )
    bazi = Stage("bazi", bazi_facts, calls, original if stage == "bazi" else None)
    astrology = Stage(
        "astrology",
        astrology_facts,
        calls,
        original if stage == "astrology" else None,
    )
    service = ChartCalculationService(normalizer, bazi, astrology)

    with pytest.raises(CalculationError) as caught:
        service.calculate(birth_input, runtime_config)

    assert caught.value.code == expected_code
    assert caught.value.__cause__ is original
    assert calls == expected_calls


def test_backend_calculation_error_is_propagated_unchanged(
    birth_input,
    normalized_time,
    bazi_facts,
    astrology_facts,
    runtime_config,
) -> None:
    calls = []
    original = CalculationError(
        "CALCULATION_FATAL", "known backend failure", system="bazi"
    )
    service = ChartCalculationService(
        Stage("time", normalized_time, calls),
        Stage("bazi", bazi_facts, calls, original),
        Stage("astrology", astrology_facts, calls),
    )

    with pytest.raises(CalculationError) as caught:
        service.calculate(birth_input, runtime_config)

    assert caught.value is original
    assert calls == ["time", "bazi"]
