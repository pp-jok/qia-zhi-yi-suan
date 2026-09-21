from datetime import date, datetime, timezone
from decimal import Decimal
from hashlib import sha256
from pathlib import Path

from destiny_personality.calculation import (
    AstrologyAspectFact,
    AstrologyChartFacts,
    AstrologyPlacement,
    BaziChartFacts,
    BaziPillar,
    DeterministicChartFacts,
    FactMode,
    HouseCusp,
    NormalizedBirthTime,
    TimeBasis,
    TenGodFact,
    TenGodSourceKind,
)
from destiny_personality.calculation.models import PillarPosition


def test_candidate_ir_preserves_context_and_unknown_time_boundaries() -> None:
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    bazi = BaziChartFacts(
        methodology_version="synthetic-v1",
        year_pillar=BaziPillar("庚", "午"),
        month_pillar=BaziPillar("庚", "午"),
        day_pillar=BaziPillar("庚", "午"),
        hour_pillar=None,
        hidden_stems=(),
        ten_gods=(
            TenGodFact("resource", "正印", (PillarPosition.YEAR,), TenGodSourceKind.VISIBLE_STEM),
            TenGodFact("authority", "正官", (PillarPosition.MONTH,), TenGodSourceKind.VISIBLE_STEM),
        ),
        relations=(),
    )
    astrology = _astrology(
        aspects=(AstrologyAspectFact("Uranus", "Sun", "square", 1),),
        known_time=False,
    )

    profile = build_candidate_core_profile(
        DeterministicChartFacts(_normalized_time(), bazi, astrology),
        fact_assurance="capability_reported",
    )

    assert profile.schema_version == "candidate-core-profile-v1"
    assert profile.semantic_capability_level == "primitive_only"
    assert profile.primitive_states["P002"].state == "context_differentiated"
    assert profile.primitive_states["P002"].context_states == {
        "change": "supported_low",
        "pressure+work": "supported_high",
    }
    candidate = next(item for item in profile.astrology_primitive_candidates if item.primitive_id == "P002")
    assert candidate.evidence_stability == "stable"
    assert "astrology.aspect_expression:effortful:high" in candidate.modifier_refs
    assert not any(ref.startswith("astrology.angular:") for ref in candidate.modifier_refs)


def test_packaged_candidate_assets_match_canonical_assets() -> None:
    project_root = Path(__file__).resolve().parents[1]
    canonical_root = project_root / "candidates" / "core-profile-v1"
    packaged_root = project_root / "src" / "destiny_personality" / "candidate_assets" / "core-profile-v1"

    assert {path.name for path in canonical_root.glob("*.yaml")} == {
        path.name for path in packaged_root.glob("*.yaml")
    }
    for canonical_path in canonical_root.glob("*.yaml"):
        assert sha256(canonical_path.read_bytes()).digest() == sha256(
            (packaged_root / canonical_path.name).read_bytes()
        ).digest(), ("CANDIDATE_ASSET_DRIFT_ERROR", canonical_path.name)


def _normalized_time() -> NormalizedBirthTime:
    value = datetime(2000, 1, 1, tzinfo=timezone.utc)
    return NormalizedBirthTime(
        birth_date=date(2000, 1, 1),
        historical_civil_time=value.replace(tzinfo=None),
        local_standard_time=value.replace(tzinfo=None),
        utc_time=value,
        true_solar_time=value.replace(tzinfo=None),
        timezone_name="UTC",
        dst_was_applied=False,
        time_basis=TimeBasis.STANDARD_TIME,
        fact_mode=FactMode.STABLE_ONLY,
        sensitivity_reasons=("synthetic unknown-time fixture",),
    )


def _astrology(*, aspects, known_time: bool) -> AstrologyChartFacts:
    bodies = ("Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus")
    placements = tuple(
        AstrologyPlacement(body, Decimal(index * 20), "Aries", Decimal(0), index + 1)
        for index, body in enumerate(bodies)
    )
    return AstrologyChartFacts(
        methodology_version="synthetic-v1",
        placements=placements,
        aspects=aspects,
        ascendant=Decimal(0) if known_time else None,
        mc=Decimal(90) if known_time else None,
        house_cusps=tuple(HouseCusp(index, Decimal(index * 30)) for index in range(1, 13)) if known_time else (),
        dignities=(),
    )
