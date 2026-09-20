from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class BaziCalendarConfig:
    input_calendar: str
    month_boundary: str
    day_boundary: str
    day_boundary_time_basis: str


@dataclass(frozen=True)
class BaziTimeConfig:
    historical_timezone_required: bool
    dst_correction_required: bool
    true_solar_time_default: bool
    allow_standard_time_mode: bool


@dataclass(frozen=True)
class BaziRelationsConfig:
    heavenly_stem_combinations: bool
    six_combinations: bool
    three_harmonies: bool
    three_meetings: bool
    six_clashes: bool
    six_harms: bool
    three_punishments: bool
    self_punishments: Tuple[str, ...]


@dataclass(frozen=True)
class PersonalityScopeConfig:
    include_luck_cycles: bool
    include_annual_transits: bool


@dataclass(frozen=True)
class BaziMethodologyConfig:
    methodology_version: str
    calendar: BaziCalendarConfig
    time: BaziTimeConfig
    month_mapping: Tuple[Tuple[str, str], ...]
    relations: BaziRelationsConfig
    personality_scope: PersonalityScopeConfig


@dataclass(frozen=True)
class AstrologyCoreConfig:
    zodiac: str
    reference: str
    house_system: str
    true_node: bool


@dataclass(frozen=True)
class AstrologyBodiesConfig:
    planets: Tuple[str, ...]
    angles: Tuple[str, ...]


@dataclass(frozen=True)
class AstrologyAspectsConfig:
    enabled: Tuple[str, ...]
    minor_aspects_enabled: bool
    max_orbs: Tuple[Tuple[str, int], ...]
    luminary_orb_bonus: int
    angle_orb: int


@dataclass(frozen=True)
class SalienceByOrbConfig:
    dominant_max: int
    strong_max: int
    moderate_max: int


@dataclass(frozen=True)
class DignityConfig:
    enabled: bool
    dignity_types: Tuple[str, ...]
    role: str


@dataclass(frozen=True)
class OuterPlanetsConfig:
    require_personal_or_angle_contact_for_high_weight: bool


@dataclass(frozen=True)
class AstrologyMethodologyConfig:
    methodology_version: str
    core: AstrologyCoreConfig
    bodies: AstrologyBodiesConfig
    aspects: AstrologyAspectsConfig
    salience_by_orb: SalienceByOrbConfig
    dignity: DignityConfig
    outer_planets: OuterPlanetsConfig


@dataclass(frozen=True)
class IntegerRange:
    minimum: int
    maximum: int


@dataclass(frozen=True)
class SynthesisPriorityConfig:
    minimum: int
    maximum: int
    core_threshold: int


@dataclass(frozen=True)
class ScoreRulesConfig:
    cross_system_validation_changes_trait_salience: bool
    tension_reduces_trait_salience: bool
    tension_can_raise_synthesis_priority: bool
    unknown_is_not_low: bool


@dataclass(frozen=True)
class ScoreModelConfig:
    score_model_version: str
    trait_salience: IntegerRange
    evidence_stability: Tuple[str, ...]
    cross_system_relation: Tuple[str, ...]
    synthesis_priority: SynthesisPriorityConfig
    rules: ScoreRulesConfig


@dataclass(frozen=True)
class PrimitiveRelation:
    left: str
    right: str
    relation: str
    dynamic_family: Optional[str]


@dataclass(frozen=True)
class PrimitiveRelationGraphConfig:
    relation_graph_version: str
    relations: Tuple[PrimitiveRelation, ...]


@dataclass(frozen=True)
class RuntimeConfig:
    bazi: BaziMethodologyConfig
    astrology: AstrologyMethodologyConfig
    score_model: ScoreModelConfig
    relation_graph: PrimitiveRelationGraphConfig
