from destiny_personality.config_models import RuntimeConfig

from .errors import CalculationError
from .models import BirthInput, DeterministicChartFacts
from .protocols import (
    AstrologyChartCalculator,
    BaziChartCalculator,
    TimeNormalizer,
)
from .validation.astrology import validate_astrology_facts
from .validation.bazi import validate_bazi_facts
from .validation.input import validate_birth_input
from .validation.time import validate_normalized_time


class ChartCalculationService:
    def __init__(
        self,
        time_normalizer: TimeNormalizer,
        bazi_calculator: BaziChartCalculator,
        astrology_calculator: AstrologyChartCalculator,
    ) -> None:
        self._time_normalizer = time_normalizer
        self._bazi_calculator = bazi_calculator
        self._astrology_calculator = astrology_calculator

    def calculate(
        self, birth_input: BirthInput, config: RuntimeConfig
    ) -> DeterministicChartFacts:
        validate_birth_input(birth_input, config)
        try:
            normalized_time = self._time_normalizer.normalize(birth_input, config)
        except CalculationError:
            raise
        except Exception as error:
            raise CalculationError(
                "TIME_NORMALIZATION_ERROR",
                "birth time normalization failed",
                system="time",
            ) from error
        validate_normalized_time(birth_input, normalized_time)

        try:
            bazi = self._bazi_calculator.calculate(
                birth_input, normalized_time, config.bazi
            )
        except CalculationError:
            raise
        except Exception as error:
            raise CalculationError(
                "CALCULATION_FATAL", "Bazi calculation failed", system="bazi"
            ) from error
        validate_bazi_facts(bazi, normalized_time.fact_mode, config)

        try:
            astrology = self._astrology_calculator.calculate(
                birth_input, normalized_time, config.astrology
            )
        except CalculationError:
            raise
        except Exception as error:
            raise CalculationError(
                "CALCULATION_FATAL",
                "astrology calculation failed",
                system="astrology",
            ) from error
        validate_astrology_facts(astrology, normalized_time.fact_mode, config)

        return DeterministicChartFacts(normalized_time, bazi, astrology)
