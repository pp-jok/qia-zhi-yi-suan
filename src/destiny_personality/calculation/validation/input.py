from datetime import date, time
from decimal import Decimal

from destiny_personality.config_models import RuntimeConfig

from ..models import BirthInput, FactMode, TimeBasis
from .common import input_error


def validate_birth_input(
    birth_input: BirthInput, config: RuntimeConfig
) -> None:
    if type(birth_input) is not BirthInput:
        raise input_error("birth input must be a BirthInput")
    if type(birth_input.birth_date) is not date:
        raise input_error("birth date must be a date", "birth_date")
    if birth_input.birth_time is not None:
        if type(birth_input.birth_time) is not time:
            raise input_error("birth time must be a time", "birth_time")
        if birth_input.birth_time.tzinfo is not None:
            raise input_error(
                "birth time must be a naive local civil time", "birth_time"
            )
    if (
        type(birth_input.timezone_name) is not str
        or not birth_input.timezone_name.strip()
    ):
        raise input_error(
            "timezone name must be a non-empty string", "timezone_name"
        )
    _validate_coordinate(
        birth_input.latitude, Decimal("-90"), Decimal("90"), "latitude"
    )
    _validate_coordinate(
        birth_input.longitude, Decimal("-180"), Decimal("180"), "longitude"
    )
    if type(birth_input.time_basis) is not TimeBasis:
        raise input_error("invalid time basis", "time_basis")
    if type(birth_input.fact_mode) is not FactMode:
        raise input_error("invalid fact mode", "fact_mode")
    if (
        birth_input.birth_time is None
        and birth_input.fact_mode is not FactMode.STABLE_ONLY
    ):
        raise input_error("unknown birth time requires stable-only facts", "fact_mode")
    if (
        birth_input.time_basis is TimeBasis.STANDARD_TIME
        and not config.bazi.time.allow_standard_time_mode
    ):
        raise input_error(
            "standard time mode is disabled by methodology", "time_basis"
        )


def _validate_coordinate(
    value: Decimal, minimum: Decimal, maximum: Decimal, field: str
) -> None:
    if type(value) is not Decimal:
        raise input_error("coordinate must be a Decimal", field)
    if not value.is_finite():
        raise input_error("coordinate must be finite", field)
    if not minimum <= value <= maximum:
        raise input_error(
            f"coordinate must be between {minimum} and {maximum}", field
        )
