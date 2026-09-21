import pytest

from destiny_personality.calculation import DeterministicChartFacts


def test_candidate_profile_json_round_trip(tmp_path, normalized_time, bazi_facts, astrology_facts):
    from destiny_personality.core_profile_builder import build_candidate_core_profile
    from destiny_personality.core_profile_codec import load_candidate_profile, write_candidate_profile

    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
    )
    path = tmp_path / "profile.json"
    write_candidate_profile(profile, path)
    assert load_candidate_profile(path) == profile


def test_candidate_profile_codec_rejects_non_candidate_payload():
    from destiny_personality.core_profile_codec import candidate_profile_from_dict

    with pytest.raises(ValueError, match="CANDIDATE_PROFILE_SCHEMA_INVALID"):
        candidate_profile_from_dict({"schema_version": "other"})
