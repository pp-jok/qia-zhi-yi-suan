import json

from destiny_personality.calculation import DeterministicChartFacts


def test_independent_fact_round_trips_produce_identical_formal_core(
    normalized_time, bazi_facts, astrology_facts
):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile
    from destiny_personality.core_destiny_profile_codec import core_destiny_profile_to_dict
    from destiny_personality.deterministic_facts_codec import (
        deterministic_facts_from_dict,
        deterministic_facts_to_dict,
    )

    facts = DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts)
    transported = json.loads(json.dumps(deterministic_facts_to_dict(facts)))
    independently_loaded = deterministic_facts_from_dict(transported)

    left = build_core_destiny_profile(facts, fact_assurance="capability_reported")
    right = build_core_destiny_profile(
        independently_loaded, fact_assurance="capability_reported"
    )

    assert core_destiny_profile_to_dict(left) == core_destiny_profile_to_dict(right)


def test_zero_coverage_is_consistently_unknown_not_low(
    normalized_time, bazi_facts, astrology_facts
):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile

    facts = DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts)
    profile = build_core_destiny_profile(facts, fact_assurance="capability_reported")

    assert {state.state for state in profile.primitive_states.values()} == {"unknown"}
    assert all(item.status == "non_comparable" for item in profile.cross_system_alignment)
    assert all(item.salience_delta == 0 for item in profile.cross_system_alignment)
