from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Optional, Tuple


class TimeBasis(str, Enum):
    TRUE_SOLAR_TIME = "true_solar_time"
    STANDARD_TIME = "standard_time"


class FactMode(str, Enum):
    STABLE_ONLY = "stable_only"
    TIME_SENSITIVE = "time_sensitive"


class PillarPosition(str, Enum):
    YEAR = "year"
    MONTH = "month"
    DAY = "day"
    HOUR = "hour"


class TenGodSourceKind(str, Enum):
    VISIBLE_STEM = "visible_stem"
    HIDDEN_STEM = "hidden_stem"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class BirthInput:
    birth_date: date
    birth_time: Optional[time]
    timezone_name: str
    latitude: Decimal
    longitude: Decimal
    time_basis: TimeBasis
    fact_mode: FactMode


@dataclass(frozen=True)
class NormalizedBirthTime:
    birth_date: date
    historical_civil_time: Optional[datetime]
    local_standard_time: Optional[datetime]
    utc_time: Optional[datetime]
    true_solar_time: Optional[datetime]
    timezone_name: str
    dst_was_applied: Optional[bool]
    time_basis: TimeBasis
    fact_mode: FactMode
    sensitivity_reasons: Tuple[str, ...]


@dataclass(frozen=True)
class BaziPillar:
    heavenly_stem: str
    earthly_branch: str


@dataclass(frozen=True)
class HiddenStemsFact:
    pillar: PillarPosition
    stems: Tuple[str, ...]


@dataclass(frozen=True)
class TenGodFact:
    subject_ref: str
    ten_god: str
    source_pillars: Tuple[PillarPosition, ...]
    source_kind: TenGodSourceKind = TenGodSourceKind.UNKNOWN


@dataclass(frozen=True)
class BaziRelationFact:
    relation_type: str
    participant_refs: Tuple[str, ...]
    source_pillars: Tuple[PillarPosition, ...]


@dataclass(frozen=True)
class BaziChartFacts:
    methodology_version: str
    year_pillar: BaziPillar
    month_pillar: BaziPillar
    day_pillar: BaziPillar
    hour_pillar: Optional[BaziPillar]
    hidden_stems: Tuple[HiddenStemsFact, ...]
    ten_gods: Tuple[TenGodFact, ...]
    relations: Tuple[BaziRelationFact, ...]


@dataclass(frozen=True)
class AstrologyPlacement:
    body: str
    longitude: Decimal
    sign: str
    degree_in_sign: Decimal
    house: Optional[int]


@dataclass(frozen=True)
class AstrologyAspectFact:
    body_a: str
    body_b: str
    aspect_type: str
    orb: Decimal


@dataclass(frozen=True)
class HouseCusp:
    house: int
    longitude: Decimal


@dataclass(frozen=True)
class DignityFact:
    body: str
    dignity: str


@dataclass(frozen=True)
class AstrologyChartFacts:
    methodology_version: str
    placements: Tuple[AstrologyPlacement, ...]
    aspects: Tuple[AstrologyAspectFact, ...]
    ascendant: Optional[Decimal]
    mc: Optional[Decimal]
    house_cusps: Tuple[HouseCusp, ...]
    dignities: Tuple[DignityFact, ...]


@dataclass(frozen=True)
class DeterministicChartFacts:
    normalized_time: NormalizedBirthTime
    bazi: BaziChartFacts
    astrology: AstrologyChartFacts
