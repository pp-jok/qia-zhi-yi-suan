from dataclasses import replace

from destiny_personality.calculation import DeterministicChartFacts


def test_every_primitive_routes_high_and_low_states_to_distinct_approved_expressions(normalized_time, bazi_facts, astrology_facts) -> None:
    from destiny_personality.core_portrait import build_candidate_profile_summary, render_core_standard
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts), fact_assurance="capability_reported"
    )
    for primitive_id in sorted(profile.primitive_states):
        presentation = _presentation(primitive_id)
        assert presentation["high_expression"] != presentation["low_expression"]
        for state, expression in (("supported_high", presentation["high_expression"]), ("supported_low", presentation["low_expression"])):
            changed = replace(profile.primitive_states[primitive_id], state=state, context_states={})
            rendered_profile = replace(profile, primitive_states={**profile.primitive_states, primitive_id: changed})
            body = "\n".join(section.body for section in render_core_standard(build_candidate_profile_summary(rendered_profile)).sections)
            assert expression in body


def test_p002_low_expression_is_not_the_stability_expression(normalized_time, bazi_facts, astrology_facts) -> None:
    from destiny_personality.core_portrait import build_candidate_profile_summary, render_core_standard
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    profile = build_candidate_core_profile(DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts), fact_assurance="capability_reported")
    state = replace(profile.primitive_states["P002"], state="supported_low", context_states={})
    body = "\n".join(section.body for section in render_core_standard(build_candidate_profile_summary(replace(profile, primitive_states={**profile.primitive_states, "P002": state}))).sections)

    assert "更能接受变化、开放性和较低确定性的环境" in body
    assert "更倾向寻求稳定、明确和可预期的结构" not in body


def _presentation(primitive_id: str) -> dict:
    import yaml
    from destiny_personality.candidate_assets import candidate_asset_root

    return yaml.safe_load((candidate_asset_root() / "candidate_primitive_presentation_v1.yaml").read_text(encoding="utf-8"))[primitive_id]
