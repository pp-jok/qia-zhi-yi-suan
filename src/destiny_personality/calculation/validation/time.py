from datetime import datetime, timedelta

from ..models import BirthInput, NormalizedBirthTime, TimeBasis
from .common import contract_error


def validate_normalized_time(
    birth_input: BirthInput, normalized_time: NormalizedBirthTime
) -> None:
    if type(normalized_time) is not NormalizedBirthTime:
        raise contract_error(
            "time", "normalizer must return NormalizedBirthTime"
        )
    expected_fields = (
        ("birth_date", normalized_time.birth_date, birth_input.birth_date),
        (
            "timezone_name",
            normalized_time.timezone_name,
            birth_input.timezone_name,
        ),
        ("time_basis", normalized_time.time_basis, birth_input.time_basis),
        ("fact_mode", normalized_time.fact_mode, birth_input.fact_mode),
    )
    for field, actual, expected in expected_fields:
        if actual != expected or type(actual) is not type(expected):
            raise contract_error(
                "time", "normalized value does not match birth input", field
            )
    if type(normalized_time.sensitivity_reasons) is not tuple or any(
        type(reason) is not str or not reason.strip()
        for reason in normalized_time.sensitivity_reasons
    ):
        raise contract_error(
            "time",
            "sensitivity reasons must be a tuple of non-empty strings",
            "sensitivity_reasons",
        )
    if birth_input.birth_time is None:
        nullable_fields = (
            "historical_civil_time",
            "local_standard_time",
            "utc_time",
            "true_solar_time",
            "dst_was_applied",
        )
        for field in nullable_fields:
            if getattr(normalized_time, field) is not None:
                raise contract_error(
                    "time", "unknown birth time cannot produce clock values", field
                )
        return

    for field in ("historical_civil_time", "local_standard_time"):
        _validate_naive_datetime(getattr(normalized_time, field), field)
    if type(normalized_time.utc_time) is not datetime:
        raise contract_error("time", "UTC time must be a datetime", "utc_time")
    if normalized_time.utc_time.utcoffset() != timedelta(0):
        raise contract_error(
            "time", "UTC time must have a zero UTC offset", "utc_time"
        )
    if type(normalized_time.dst_was_applied) is not bool:
        raise contract_error(
            "time", "DST status must be a boolean", "dst_was_applied"
        )
    if birth_input.time_basis is TimeBasis.TRUE_SOLAR_TIME:
        _validate_naive_datetime(
            normalized_time.true_solar_time, "true_solar_time"
        )
    elif normalized_time.true_solar_time is not None:
        raise contract_error(
            "time",
            "standard time mode cannot return true solar time",
            "true_solar_time",
        )


def _validate_naive_datetime(value: object, field: str) -> None:
    if type(value) is not datetime:
        raise contract_error("time", "value must be a datetime", field)
    if value.tzinfo is not None:
        raise contract_error(
            "time", "local datetime must be timezone-naive", field
        )
