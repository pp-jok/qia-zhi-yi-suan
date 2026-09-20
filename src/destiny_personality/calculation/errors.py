from typing import Optional


class CalculationError(RuntimeError):
    """A stable failure raised by the deterministic calculation boundary."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        system: Optional[str] = None,
        field: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.system = system
        self.field = field

    def __str__(self) -> str:
        context = [self.code]
        if self.system is not None:
            context.append(self.system)
        if self.field is not None:
            context.append(self.field)
        return f"{' | '.join(context)}: {self.message}"
