from dataclasses import dataclass
from decimal import Decimal
from typing import Tuple


@dataclass(frozen=True)
class LogicalComparisonCategory:
    category_id: str
    comparison_mode: str


@dataclass(frozen=True)
class BoundaryMargin:
    category_id: str
    margin: Decimal


@dataclass(frozen=True)
class CanonicalPrecision:
    category_id: str
    decimal_places: int


@dataclass(frozen=True)
class FieldTolerance:
    category_id: str
    absolute_tolerance: Decimal


@dataclass(frozen=True)
class RepresentationEquivalence:
    logical_category_id: str
    vocabulary_category_id: str
    canonical_id: str
    equivalent_values: Tuple[str, ...]


@dataclass(frozen=True)
class FactComparisonPolicyConfig:
    schema_version: str
    policy_version: str
    bazi_methodology_version: str
    astrology_methodology_version: str
    vocabulary_version: str
    fact_schema_version: str
    triggers: Tuple[str, ...]
    logical_categories: Tuple[LogicalComparisonCategory, ...]
    boundary_margins: Tuple[BoundaryMargin, ...]
    canonical_precision: Tuple[CanonicalPrecision, ...]
    tolerances: Tuple[FieldTolerance, ...]
    representation_equivalences: Tuple[RepresentationEquivalence, ...]
