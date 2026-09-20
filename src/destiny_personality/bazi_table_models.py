from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class BaziTableRule:
    rule_id: str
    inputs: Tuple[Tuple[str, Tuple[str, ...]], ...]
    outputs: Tuple[Tuple[str, Tuple[str, ...]], ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class BaziTableSection:
    section_id: str
    rules: Tuple[BaziTableRule, ...]


@dataclass(frozen=True)
class BaziDeterministicTablesConfig:
    schema_version: str
    table_version: str
    methodology_version: str
    vocabulary_version: str
    tables: Tuple[BaziTableSection, ...]
