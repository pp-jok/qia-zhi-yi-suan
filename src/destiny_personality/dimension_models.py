from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class DimensionDefinition:
    dimension_id: str
    canonical_name: str
    definition: str
    primitive_refs: Tuple[str, ...]
    limitations: Tuple[str, ...]


@dataclass(frozen=True)
class DimensionRequirement:
    dimension_id: str
    minimum_supported_primitives: int


@dataclass(frozen=True)
class CoveragePolicy:
    threshold_status: str
    coverage_metric: str
    complete_threshold: float
    partial_threshold: float
    partial_portrait_allowed: bool
    partial_status: str
    warning_code: str
    missing_config_code: str
    dimension_requirements: Tuple[DimensionRequirement, ...]


@dataclass(frozen=True)
class DimensionCoveragePolicyConfig:
    schema_version: str
    policy_version: str
    ontology_version: str
    score_model_version: str
    dimension_count: int
    dimensions: Tuple[DimensionDefinition, ...]
    coverage_policy: CoveragePolicy
