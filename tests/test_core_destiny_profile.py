from dataclasses import replace

import pytest

from destiny_personality.calculation import DeterministicChartFacts


def test_formal_profile_is_complete_and_zero_safe(qualified_facts):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile

    profile = build_core_destiny_profile(qualified_facts)

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
    assert dict(profile.semantic_model_versions)["active_mapping_bundle"]


def test_formal_builder_rejects_raw_facts_and_caller_selected_assurance(
    normalized_time, bazi_facts, astrology_facts, qualified_facts
):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile

    raw = DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts)
    with pytest.raises(ValueError, match="QUALIFIED_FACTS_REQUIRED"):
        build_core_destiny_profile(raw)
    with pytest.raises(TypeError):
        build_core_destiny_profile(raw, fact_assurance="project_verified")
    with pytest.raises(ValueError, match="QUALIFIED_FACTS_REQUIRED"):
        build_core_destiny_profile(
            replace(qualified_facts, fact_assurance="project_verified")
        )
    with pytest.raises(ValueError, match="QUALIFIED_FACTS_REQUIRED"):
        build_core_destiny_profile(
            replace(qualified_facts, qualification_fingerprint="made-up")
        )


def test_formal_profile_codec_is_deterministic_and_round_trips(tmp_path, qualified_facts):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile
    from destiny_personality.core_destiny_profile_codec import (
        load_core_destiny_profile,
        write_core_destiny_profile,
    )

    profile = build_core_destiny_profile(qualified_facts)
    left = tmp_path / "left.json"
    right = tmp_path / "right.json"
    write_core_destiny_profile(profile, left)
    write_core_destiny_profile(profile, right)

    assert left.read_bytes() == right.read_bytes()
    assert load_core_destiny_profile(left) == profile


def test_formal_profile_rejects_semantic_assurance_copied_from_fact_assurance(
    qualified_facts,
):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile
    from destiny_personality.core_destiny_profile_validation import validate_core_destiny_profile

    profile = build_core_destiny_profile(qualified_facts)
    assert "FORMAL_SEMANTIC_ASSURANCE_SEPARATION_REQUIRED" in validate_core_destiny_profile(
        replace(profile, semantic_model_assurance="capability_reported")
    )


def test_codec_rejects_candidate_rule_reference(qualified_facts):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile
    from destiny_personality.core_destiny_profile_codec import core_destiny_profile_from_dict, core_destiny_profile_to_dict

    payload = core_destiny_profile_to_dict(build_core_destiny_profile(qualified_facts))
    payload["primitive_states"]["P001"]["resolution_rule_ref"] = "candidate-rule-v1"
    with pytest.raises(ValueError, match="FORMAL_CANDIDATE_RULE_REF_PROHIBITED"):
        core_destiny_profile_from_dict(payload)


def test_validator_rejects_duplicate_or_fabricated_alignment(qualified_facts):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile
    from destiny_personality.core_destiny_profile_validation import validate_core_destiny_profile

    profile = build_core_destiny_profile(qualified_facts)
    duplicated = replace(profile.cross_system_alignment[1], primitive_id="P001")
    malformed = replace(
        profile,
        cross_system_alignment=(profile.cross_system_alignment[0], duplicated)
        + profile.cross_system_alignment[2:],
    )
    assert "FORMAL_ALIGNMENT_PRIMITIVE_COVERAGE_INVALID" in validate_core_destiny_profile(malformed)

    fabricated = replace(profile.cross_system_alignment[0], bazi_rule_refs=("SMC-FORGED",))
    malformed = replace(profile, cross_system_alignment=(fabricated,) + profile.cross_system_alignment[1:])
    errors = validate_core_destiny_profile(malformed)
    assert "FORMAL_ALIGNMENT_REFERENCE_INVALID" in errors
    assert "FORMAL_NON_COMPARABLE_ALIGNMENT_INVALID" in errors


def test_current_release_rejects_mapped_or_non_unknown_profile(qualified_facts):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile
    from destiny_personality.core_destiny_profile_validation import validate_core_destiny_profile

    profile = build_core_destiny_profile(qualified_facts)
    forged = replace(
        profile.primitive_states["P001"],
        state="supported_high",
        evidence_refs=("fact:forged",),
        supporting_candidates=("SMC-FORGED",),
    )
    malformed = replace(
        profile,
        semantic_model_assurance="limited_coverage_approved_mapping",
        primitive_states={**profile.primitive_states, "P001": forged},
    )
    errors = validate_core_destiny_profile(malformed)
    assert "FORMAL_RELEASE_MAPPING_BUNDLE_COVERAGE_INVALID" in errors
    assert "FORMAL_MAPPED_ASSURANCE_TRACEABILITY_REQUIRED" in errors


def test_profile_must_bind_exact_packaged_mapping_bundle(qualified_facts):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile
    from destiny_personality.core_destiny_profile_validation import validate_core_destiny_profile

    profile = build_core_destiny_profile(qualified_facts)
    versions = tuple(
        (key, "forged") if key == "active_mapping_bundle" else (key, value)
        for key, value in profile.semantic_model_versions
    )
    assert "FORMAL_RELEASE_MAPPING_BUNDLE_BINDING_INVALID" in validate_core_destiny_profile(
        replace(profile, semantic_model_versions=versions)
    )
