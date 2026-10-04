import pytest

from destiny_personality.calculation import DeterministicChartFacts


def test_formal_profile_is_complete_and_zero_safe(normalized_time, bazi_facts, astrology_facts):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile

    profile = build_core_destiny_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
    )

    assert profile.schema_version == "core-destiny-profile-v1"
    assert set(profile.primitive_states) == {"P001", "P002", "P003", "P004", "P005", "P006"}
    assert {state.state for state in profile.primitive_states.values()} == {"unknown"}
    assert profile.bazi_primitive_candidates == ()
    assert profile.astrology_primitive_candidates == ()
    assert len(profile.cross_system_alignment) == 6
    assert {item.status for item in profile.cross_system_alignment} == {"non_comparable"}
    assert profile.dominant_signatures == ()
    assert profile.core_dynamics == ()
    assert profile.shadow_mature_forms == ()
    assert profile.fate_themes == ()
    assert profile.archetype is None
    assert profile.fact_assurance != profile.semantic_model_assurance


def test_formal_profile_codec_is_deterministic_and_round_trips(tmp_path, normalized_time, bazi_facts, astrology_facts):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile
    from destiny_personality.core_destiny_profile_codec import (
        load_core_destiny_profile,
        write_core_destiny_profile,
    )

    profile = build_core_destiny_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
    )
    left = tmp_path / "left.json"
    right = tmp_path / "right.json"
    write_core_destiny_profile(profile, left)
    write_core_destiny_profile(profile, right)

    assert left.read_bytes() == right.read_bytes()
    assert load_core_destiny_profile(left) == profile


def test_formal_profile_rejects_semantic_assurance_copied_from_fact_assurance(normalized_time, bazi_facts, astrology_facts):
    from dataclasses import replace

    from destiny_personality.core_destiny_profile import build_core_destiny_profile
    from destiny_personality.core_destiny_profile_validation import validate_core_destiny_profile

    profile = build_core_destiny_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
    )

    assert "FORMAL_SEMANTIC_ASSURANCE_SEPARATION_REQUIRED" in validate_core_destiny_profile(
        replace(profile, semantic_model_assurance="capability_reported")
    )


def test_codec_rejects_candidate_rule_reference(normalized_time, bazi_facts, astrology_facts):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile
    from destiny_personality.core_destiny_profile_codec import core_destiny_profile_from_dict, core_destiny_profile_to_dict

    profile = build_core_destiny_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
    )
    payload = core_destiny_profile_to_dict(profile)
    payload["primitive_states"]["P001"]["resolution_rule_ref"] = "candidate-rule-v1"

    with pytest.raises(ValueError, match="FORMAL_CANDIDATE_RULE_REF_PROHIBITED"):
        core_destiny_profile_from_dict(payload)


def test_validator_rejects_duplicate_alignment_primitive_ids(normalized_time, bazi_facts, astrology_facts):
    from dataclasses import replace

    from destiny_personality.core_destiny_profile import build_core_destiny_profile
    from destiny_personality.core_destiny_profile_validation import validate_core_destiny_profile

    profile = build_core_destiny_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
    )
    duplicated = replace(profile.cross_system_alignment[1], primitive_id="P001")
    malformed = replace(
        profile,
        cross_system_alignment=(profile.cross_system_alignment[0], duplicated)
        + profile.cross_system_alignment[2:],
    )

    assert "FORMAL_ALIGNMENT_PRIMITIVE_COVERAGE_INVALID" in validate_core_destiny_profile(malformed)


def test_validator_rejects_fabricated_non_comparable_alignment_refs(normalized_time, bazi_facts, astrology_facts):
    from dataclasses import replace

    from destiny_personality.core_destiny_profile import build_core_destiny_profile
    from destiny_personality.core_destiny_profile_validation import validate_core_destiny_profile

    profile = build_core_destiny_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
    )
    fabricated = replace(
        profile.cross_system_alignment[0],
        bazi_rule_refs=("SMC-FORGED",),
    )
    malformed = replace(
        profile,
        cross_system_alignment=(fabricated,) + profile.cross_system_alignment[1:],
    )

    errors = validate_core_destiny_profile(malformed)
    assert "FORMAL_ALIGNMENT_REFERENCE_INVALID" in errors
    assert "FORMAL_NON_COMPARABLE_ALIGNMENT_INVALID" in errors


def test_mapped_semantic_assurance_requires_traceable_admitted_candidates(normalized_time, bazi_facts, astrology_facts):
    from dataclasses import replace

    from destiny_personality.core_destiny_profile import build_core_destiny_profile
    from destiny_personality.core_destiny_profile_validation import validate_core_destiny_profile

    profile = build_core_destiny_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
    )

    assert "FORMAL_MAPPED_ASSURANCE_TRACEABILITY_REQUIRED" in validate_core_destiny_profile(
        replace(profile, semantic_model_assurance="limited_coverage_approved_mapping")
    )
