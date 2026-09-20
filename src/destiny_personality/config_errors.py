from typing import Optional


class ConfigError(ValueError):
    """A deterministic configuration failure exposed to callers and the CLI."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        file: Optional[str] = None,
        field: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.file = file
        self.field = field

    def __str__(self) -> str:
        context = [self.code]
        if self.file is not None:
            context.append(self.file)
        if self.field is not None:
            context.append(self.field)
        return f"{' | '.join(context)}: {self.message}"
