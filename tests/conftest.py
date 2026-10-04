from pathlib import Path
from datetime import date, datetime, time, timezone
from decimal import Decimal
import json
import shutil

import pytest

from destiny_personality import load_runtime_config
from destiny_personality.dimension_models import CoveragePolicy, DimensionCoveragePolicyConfig, DimensionDefinition, DimensionRequirement
from destiny_personality.primitive_models import PrimitiveDefinition, PrimitiveFoundationConfig, PrimitiveOntologyConfig, PrimitiveStateResolutionConfig
from destiny_personality.calculation import (
    AstrologyChartFacts,
    AstrologyPlacement,
    BaziChartFacts,
    BaziPillar,
    BirthInput,
    FactMode,
    HouseCusp,
    NormalizedBirthTime,
    TimeBasis,
)


CONFIG_FILENAMES = (
    "bazi_methodology_v1.yaml",
    "astrology_methodology_v1.yaml",
    "score_model_v2_2.yaml",
    "primitive_relation_graph_v1.yaml",
)


@pytest.fixture
def valid_config_dir(tmp_path: Path) -> Path:
    project_root = Path(__file__).resolve().parents[1]
    source = project_root / "destiny_personality_skill_docs_v2_2"
    for filename in CONFIG_FILENAMES:
        shutil.copyfile(source / filename, tmp_path / filename)
    return tmp_path


@pytest.fixture
def runtime_config(valid_config_dir: Path):
    return load_runtime_config(valid_config_dir)


@pytest.fixture
def primitive_foundation() -> PrimitiveFoundationConfig:
    ontology = PrimitiveOntologyConfig("primitive-ontology-v1", "test-only-ontology-1", (PrimitiveDefinition("P900", "TEST_ONLY_PRIMITIVE", "TEST_ONLY_DEFINITION", "TEST_ONLY_HIGH", "TEST_ONLY_LOW", (), ()),))
    resolution = PrimitiveStateResolutionConfig("primitive-state-resolution-v1", "test-only-resolution-1", ontology.ontology_version, "2.2", ("supported_high", "supported_low", "mixed", "unknown"), (), ())
    return PrimitiveFoundationConfig(ontology, resolution)


@pytest.fixture
def dimension_policy() -> DimensionCoveragePolicyConfig:
    dimensions = tuple(DimensionDefinition(f"D{i:02d}", f"TEST_ONLY_DIMENSION_{i:02d}", f"TEST_ONLY_DEFINITION_{i:02d}", ("P900",), ()) for i in range(1, 13))
    requirements = tuple(DimensionRequirement(item.dimension_id, 1) for item in dimensions)
    coverage = CoveragePolicy("provisional", "TEST_ONLY_METRIC", 0.8, 0.4, True, "partial", "coverage_warning", "CONFIG_GAP", requirements)
    return DimensionCoveragePolicyConfig("dimension-coverage-policy-v1", "test-only-policy-1", "test-only-ontology-1", "2.2", 12, dimensions, coverage)


@pytest.fixture
def birth_input() -> BirthInput:
    return BirthInput(
        birth_date=date(1990, 1, 2),
        birth_time=time(3, 4, 5),
        timezone_name="Asia/Shanghai",
        latitude=Decimal("31.2304"),
        longitude=Decimal("121.4737"),
        time_basis=TimeBasis.TRUE_SOLAR_TIME,
        fact_mode=FactMode.TIME_SENSITIVE,
    )


@pytest.fixture
def normalized_time(birth_input: BirthInput) -> NormalizedBirthTime:
    return NormalizedBirthTime(
        birth_date=birth_input.birth_date,
        historical_civil_time=datetime(1990, 1, 2, 3, 4, 5),
        local_standard_time=datetime(1990, 1, 2, 3, 4, 5),
        utc_time=datetime(1990, 1, 1, 19, 4, 5, tzinfo=timezone.utc),
        true_solar_time=datetime(1990, 1, 2, 3, 10),
        timezone_name=birth_input.timezone_name,
        dst_was_applied=False,
        time_basis=birth_input.time_basis,
        fact_mode=birth_input.fact_mode,
        sensitivity_reasons=(),
    )


@pytest.fixture
def bazi_facts() -> BaziChartFacts:
    pillar = BaziPillar("庚", "午")
    return BaziChartFacts(
        methodology_version="bazi-core-v1.0",
        year_pillar=pillar,
        month_pillar=pillar,
        day_pillar=pillar,
        hour_pillar=pillar,
        hidden_stems=(),
        ten_gods=(),
        relations=(),
    )


@pytest.fixture
def astrology_facts(runtime_config) -> AstrologyChartFacts:
    placements = tuple(
        AstrologyPlacement(
            body=body,
            longitude=Decimal(index * 20),
            sign="Aries",
            degree_in_sign=Decimal((index * 20) % 30),
            house=(index % 12) + 1,
        )
        for index, body in enumerate(runtime_config.astrology.bodies.planets)
    )
    cusps = tuple(
        HouseCusp(house=house, longitude=Decimal((house - 1) * 30))
        for house in range(1, 13)
    )
    return AstrologyChartFacts(
        methodology_version="western-tropical-v1.0",
        placements=placements,
        aspects=(),
        ascendant=Decimal("5"),
        mc=Decimal("95"),
        house_cusps=cusps,
        dignities=(),
    )


@pytest.fixture
def qualified_facts(tmp_path, normalized_time, bazi_facts, astrology_facts):
    """Create qualification-bound synthetic facts through the public loader."""

    from destiny_personality.calculation import DeterministicChartFacts
    from destiny_personality.deterministic_facts_codec import (
        deterministic_facts_fingerprint,
        deterministic_facts_to_dict,
        load_qualified_deterministic_facts,
    )

    facts = DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts)
    payload = deterministic_facts_to_dict(facts)
    payload.update(
        {
            "schema_version": "deterministic-facts-v1",
            "fact_mode": facts.normalized_time.fact_mode.value,
            "methodology_versions": {
                "bazi": facts.bazi.methodology_version,
                "astrology": facts.astrology.methodology_version,
            },
            "provenance_refs": ["test:qualified-facts"],
            "validation_summary": {"structure": "passed"},
        }
    )
    qualification = {
        "schema_version": "fact-qualification-v1",
        "fact_fingerprint": deterministic_facts_fingerprint(facts),
        "qualification_status": "passed",
        "derived_fact_assurance": "capability_reported",
        "fact_contract_version": "deterministic-facts-v1",
        "methodology_versions": payload["methodology_versions"],
        "validation_refs": ["test:validation"],
        "provenance_refs": ["test:provenance"],
        "calculation_envelope_refs": ["test:envelope"],
        "comparison": {"required": False, "status": "not_required"},
        "validation_summary": {
            "structure": "passed",
            "methodology": "passed",
            "provenance": "passed",
            "internal_consistency": "passed",
            "time_scope": "passed",
            "calculation_config": "not_available",
        },
    }
    facts_path = tmp_path / "qualified-facts.json"
    qualification_path = tmp_path / "qualified-facts-qualification.json"
    facts_path.write_text(json.dumps(payload), encoding="utf-8")
    qualification_path.write_text(json.dumps(qualification), encoding="utf-8")
    return load_qualified_deterministic_facts(facts_path, qualification_path)
