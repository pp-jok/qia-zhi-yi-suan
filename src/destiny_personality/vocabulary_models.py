from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class VocabularyEntry:
    canonical_id: str
    aliases: Tuple[str, ...]


@dataclass(frozen=True)
class VocabularyCategory:
    category_id: str
    entries: Tuple[VocabularyEntry, ...]


@dataclass(frozen=True)
class CanonicalFactVocabularyConfig:
    schema_version: str
    vocabulary_version: str
    bazi_methodology_version: str
    astrology_methodology_version: str
    categories: Tuple[VocabularyCategory, ...]
