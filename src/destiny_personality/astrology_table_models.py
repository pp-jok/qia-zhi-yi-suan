from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class AstrologyDignityRow:
    body_id: str
    sign_id: str
    dignity_id: str
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class AstrologyDignityTableConfig:
    schema_version: str
    table_version: str
    methodology_version: str
    vocabulary_version: str
    rows: Tuple[AstrologyDignityRow, ...]
