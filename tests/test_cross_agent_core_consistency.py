def test_independent_repeats_produce_identical_formal_core(qualified_facts):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile
    from destiny_personality.core_destiny_profile_codec import core_destiny_profile_to_dict
    left = build_core_destiny_profile(qualified_facts)
    right = build_core_destiny_profile(qualified_facts)

    assert core_destiny_profile_to_dict(left) == core_destiny_profile_to_dict(right)


def test_zero_coverage_is_consistently_unknown_not_low(qualified_facts):
    from destiny_personality.core_destiny_profile import build_core_destiny_profile

    profile = build_core_destiny_profile(qualified_facts)

    assert {state.state for state in profile.primitive_states.values()} == {"unknown"}
    assert all(item.status == "non_comparable" for item in profile.cross_system_alignment)
    assert all(item.salience_delta == 0 for item in profile.cross_system_alignment)
