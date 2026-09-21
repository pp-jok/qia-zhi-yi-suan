from pathlib import Path

import yaml

from destiny_personality.calculation import AstrologyAspectFact, DeterministicChartFacts, TenGodFact, TenGodSourceKind
from destiny_personality.calculation.models import PillarPosition


def test_d1_design_set_runs_deterministically_and_preserves_candidate_limits(
    normalized_time, bazi_facts, astrology_facts
) -> None:
    from destiny_personality.core_profile_builder import (
        build_candidate_core_profile,
        normalize_core_profile,
    )
    from destiny_personality.core_profile_similarity import (
        build_candidate_similarity_matrix,
        evaluate_candidate_similarity_matrix,
    )

    profiles = {
        case_id: build_candidate_core_profile(
            _facts_from_design_case(
                path, normalized_time, bazi_facts, astrology_facts
            ),
            fact_assurance="capability_reported",
        )
        for case_id, path in _design_cases().items()
    }

    assert len(profiles) == 8
    assert len({normalize_core_profile(profile) for profile in profiles.values()}) == 8
    assert len(
        {
            tuple(
                (primitive_id, state.state)
                for primitive_id, state in sorted(profile.primitive_states.items())
            )
            for profile in profiles.values()
        }
    ) == 8
    assert profiles["cross_system_tension"].primitive_states["P002"].state == "context_differentiated"
    assert profiles["unknown_birth_time"].astrology_primitive_candidates
    assert all(
        candidate.evidence_stability == "stable"
        for candidate in profiles["unknown_birth_time"].astrology_primitive_candidates
    )
    assert all(not hasattr(profile, "core_dynamics") for profile in profiles.values())
    assert all(not hasattr(profile, "archetype") for profile in profiles.values())

    calibration = evaluate_candidate_similarity_matrix(
        build_candidate_similarity_matrix(tuple(profiles.values()))
    )
    assert calibration.max_similarity == 0.75
    assert calibration.threshold == 0.75
    assert calibration.errors == ()


def _design_cases() -> dict[str, Path]:
    design_set = Path(__file__).parent / "fixtures" / "core_profile_calibration" / "design_set"
    return {
        payload["case_id"]: path
        for path in sorted(design_set.glob("*.yaml"))
        for payload in (yaml.safe_load(path.read_text(encoding="utf-8")),)
    }


def _facts_from_design_case(path, normalized_time, bazi_facts, astrology_facts):
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
                "fixture",
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
