from decimal import Decimal
from typing import Optional

from ..errors import CalculationError


def input_error(
    message: str, field: Optional[str] = None
) -> CalculationError:
    return CalculationError("BIRTH_INPUT_ERROR", message, field=field)


def contract_error(
    system: str, message: str, field: Optional[str] = None
) -> CalculationError:
    return CalculationError(
        "CALCULATION_CONTRACT_ERROR", message, system=system, field=field
    )


def validate_nonempty_string(value: object, system: str, field: str) -> None:
    if type(value) is not str or not value.strip():
        raise contract_error(system, "value must be a non-empty string", field)


def validate_decimal_range(
    value: object,
    minimum: Decimal,
    maximum: Decimal,
    system: str,
    field: str,
) -> None:
    if type(value) is not Decimal or not value.is_finite():
        raise contract_error(system, "value must be a finite Decimal", field)
    if not minimum <= value < maximum:
        raise contract_error(
            system, f"value must be in [{minimum}, {maximum})", field
        )
