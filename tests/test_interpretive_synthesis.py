from pathlib import Path

from destiny_personality.deterministic_facts_codec import (
    load_qualified_deterministic_facts,
)
from destiny_personality.interpretive_codec import (
    encode_narrative_synthesis_packet,
)
from destiny_personality.interpretive_synthesis import (
    ALLOWED_RELATIONSHIP_KINDS,
    build_narrative_synthesis_packet,
)


FIXTURE_DIRECTORY = Path(__file__).parent / "fixtures" / "interpretive"


def _qualified(scenario: str):
    return load_qualified_deterministic_facts(
        FIXTURE_DIRECTORY / f"{scenario}-facts.json",
        FIXTURE_DIRECTORY / f"{scenario}-qualification.json",
    )


def test_packet_keeps_independent_profiles_and_structured_relationships():
    packet = build_narrative_synthesis_packet(_qualified("tension"))

    assert packet.bazi_profile.signal_ids
    assert packet.astrology_profile.signal_ids
    assert packet.alignments
    assert {item.kind for item in packet.alignments} <= ALLOWED_RELATIONSHIP_KINDS
    assert ALLOWED_RELATIONSHIP_KINDS == {
        "validation",
        "complement",
        "contextualization",
        "tension",
        "correction",
        "unresolved",
        "non_comparable",
    }
    assert all(item.signal_provenance for item in packet.alignments)


def test_tension_explains_poles_context_and_integration():
    packet = build_narrative_synthesis_packet(_qualified("tension"))
    tension = packet.tensions[0]

    assert tension.topic == "style of expression"
    assert tension.left_pole and tension.right_pole
    assert tension.contexts
    assert tension.integration
    assert tension.bazi_signal_ids == ("BAZI-TEN-GOD-EXPRESSION",)
    assert tension.astrology_signal_ids == (
        "ASTROLOGY-PLANET-SIGN-EXPRESSION",
    )
    assert {item.signal_id for item in tension.signal_provenance} == {
        "BAZI-TEN-GOD-EXPRESSION",
        "ASTROLOGY-PLANET-SIGN-EXPRESSION",
    }


def test_unmatched_topics_never_become_unsupported_agreement():
    packet = build_narrative_synthesis_packet(_qualified("contrast_b"))

    assert packet.alignments
    assert {item.kind for item in packet.alignments} == {"non_comparable"}
    assert not packet.tensions
    assert all(
        not (item.bazi_signal_ids and item.astrology_signal_ids)
        for item in packet.alignments
    )


def test_packet_is_attached_to_core_profile_and_has_deterministic_codec():
    from destiny_personality.interpretive_profile import (
        build_interpretive_core_profile,
    )

    qualified = _qualified("tension")
    packet = build_narrative_synthesis_packet(qualified)
    profile = build_interpretive_core_profile(qualified)

    assert profile.synthesis_packet == packet
    assert encode_narrative_synthesis_packet(packet) == (
        encode_narrative_synthesis_packet(packet)
    )
    encoded = encode_narrative_synthesis_packet(packet)
    assert encoded["audit_refs"] == list(packet.audit_refs)
    assert encoded["tensions"][0]["signal_provenance"]
