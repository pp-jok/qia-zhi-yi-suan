from typing import Protocol

from destiny_personality.config_models import (
    AstrologyMethodologyConfig,
    BaziMethodologyConfig,
    RuntimeConfig,
)

from .models import (
    AstrologyChartFacts,
    BaziChartFacts,
    BirthInput,
    NormalizedBirthTime,
)


class TimeNormalizer(Protocol):
    def normalize(
        self, birth_input: BirthInput, config: RuntimeConfig
    ) -> NormalizedBirthTime:
        ...


class BaziChartCalculator(Protocol):
    def calculate(
        self,
        birth_input: BirthInput,
        normalized_time: NormalizedBirthTime,
        methodology: BaziMethodologyConfig,
    ) -> BaziChartFacts:
        ...


class AstrologyChartCalculator(Protocol):
    def calculate(
        self,
        birth_input: BirthInput,
        normalized_time: NormalizedBirthTime,
        methodology: AstrologyMethodologyConfig,
    ) -> AstrologyChartFacts:
        ...
