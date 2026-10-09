from pathlib import Path

from destiny_personality.deterministic_facts_codec import (
    load_qualified_deterministic_facts,
)
from destiny_personality.interpretive_rules import extract_interpretive_signals
from destiny_personality.interpretive_system_profiles import (
    build_interpretive_system_profiles,
)


FIXTURE_DIRECTORY = Path(__file__).parent / "fixtures" / "interpretive"


def _qualified(scenario: str):
    return load_qualified_deterministic_facts(
        FIXTURE_DIRECTORY / f"{scenario}-facts.json",
        FIXTURE_DIRECTORY / f"{scenario}-qualification.json",
    )


def test_system_profiles_are_independent_and_topic_bound():
    qualified = _qualified("tension")
    bazi_profile, astrology_profile = build_interpretive_system_profiles(
        qualified
    )
    matched = extract_interpretive_signals(qualified)

    assert bazi_profile.system == "bazi"
    assert astrology_profile.system == "astrology"
    assert bazi_profile.signal_ids
    assert astrology_profile.signal_ids
    assert set(bazi_profile.signal_ids).isdisjoint(astrology_profile.signal_ids)
    assert set(bazi_profile.signal_ids) == {
        signal.signal_id for signal in matched if signal.system == "bazi"
    }
    assert set(astrology_profile.signal_ids) == {
        signal.signal_id for signal in matched if signal.system == "astrology"
    }
    assert all(topic.signal_ids for topic in bazi_profile.topics)
    assert all(topic.signal_ids for topic in astrology_profile.topics)


def test_system_profile_preserves_only_its_qualified_signal_provenance():
    bazi_profile, astrology_profile = build_interpretive_system_profiles(
        _qualified("tension")
    )

    for profile in (bazi_profile, astrology_profile):
        provenance = tuple(
            item
            for topic in profile.topics
            for item in topic.signal_provenance
        )
        assert {item.signal_id for item in provenance} == set(
            profile.signal_ids
        )
        assert all(item.system == profile.system for item in provenance)
        assert all(
            fact_ref.startswith(f"{profile.system}.")
            for item in provenance
            for fact_ref in item.fact_refs
        )
