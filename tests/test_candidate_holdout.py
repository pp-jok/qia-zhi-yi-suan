from pathlib import Path

import yaml

from destiny_personality.calculation import (
    AstrologyAspectFact,
    DeterministicChartFacts,
    TenGodFact,
    TenGodSourceKind,
)
from destiny_personality.calculation.models import PillarPosition


def test_holdout_cases_preserve_candidate_safety_boundaries(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    cases = _holdout_cases()
    profiles = {
        case_id: build_candidate_core_profile(
            _facts_from_holdout_case(path, normalized_time, bazi_facts, astrology_facts),
            fact_assurance="capability_reported",
        )
        for case_id, path in cases.items()
    }

    assert set(profiles) == {
        "middle_autonomy_middle_stability",
        "near_equal_primitive_signals",
        "no_dominant_signature",
        "no_clear_core_dynamic",
        "unknown_or_limited_context",
    }
    assert all(not hasattr(profile, "core_dynamics") for profile in profiles.values())
    assert all(not hasattr(profile, "archetype") for profile in profiles.values())
    assert profiles["unknown_or_limited_context"].astrology_primitive_candidates
    assert all(
        candidate.evidence_stability == "stable"
        for candidate in profiles["unknown_or_limited_context"].astrology_primitive_candidates
    )
    assert all(
        candidate.fact_refs and candidate.semantic_rule_refs
        for profile in profiles.values()
        for candidate in profile.bazi_primitive_candidates + profile.astrology_primitive_candidates
    )


def _holdout_cases() -> dict[str, Path]:
    holdout_set = Path(__file__).parent / "fixtures" / "core_profile_calibration" / "holdout_set"
    return {
        payload["case_id"]: path
        for path in sorted(holdout_set.glob("*.yaml"))
        for payload in (yaml.safe_load(path.read_text(encoding="utf-8")),)
    }


def _facts_from_holdout_case(path, normalized_time, bazi_facts, astrology_facts):
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    bazi = bazi_facts.__class__(
        methodology_version=bazi_facts.methodology_version,
        year_pillar=bazi_facts.year_pillar,
        month_pillar=bazi_facts.month_pillar,
        day_pillar=bazi_facts.day_pillar,
        hour_pillar=bazi_facts.hour_pillar,
        hidden_stems=bazi_facts.hidden_stems,
        ten_gods=tuple(
            TenGodFact(
                "holdout",
                ten_god,
                (
                    (
                        PillarPosition.YEAR,
                        PillarPosition.MONTH,
                        PillarPosition.DAY,
                        PillarPosition.HOUR,
                    )[index % 4],
                ),
                TenGodSourceKind.VISIBLE_STEM,
            )
            for index, ten_god in enumerate(payload["bazi_ten_gods"])
        ),
        relations=bazi_facts.relations,
    )
    astrology = astrology_facts.__class__(
        methodology_version=astrology_facts.methodology_version,
        placements=astrology_facts.placements,
        aspects=tuple(
            AstrologyAspectFact(body_a, body_b, "trine", 0)
            for body_a, body_b in payload["astrology"]["aspect_pairs"]
        ),
        ascendant=astrology_facts.ascendant if payload["astrology"]["known_birth_time"] else None,
        mc=astrology_facts.mc,
        house_cusps=astrology_facts.house_cusps,
        dignities=astrology_facts.dignities,
    )
    return DeterministicChartFacts(normalized_time, bazi, astrology)
