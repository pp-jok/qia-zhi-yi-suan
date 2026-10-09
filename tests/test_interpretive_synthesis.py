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


def test_serialized_alignment_keeps_the_compared_source_content_per_side():
    packet = build_narrative_synthesis_packet(_qualified("tension"))
    encoded = encode_narrative_synthesis_packet(packet)
    alignment = next(
        item for item in encoded["alignments"]
        if item["topic"] == "style of expression"
    )

    bazi_source = alignment["bazi_source"]
    assert bazi_source["signal_ids"] == ["BAZI-TEN-GOD-EXPRESSION"]
    assert bazi_source["interpretations"] == [
        "印星信号将注意力引向理解、吸收与内在整理。（命中依据：正印）"
    ]
    assert bazi_source["mechanisms"] == [
        "通过接收信息、建立解释框架后再表达，因而形成偏反思的表达节奏。"
    ]
    assert bazi_source["likely_expressions"] == [
        "在学习或沟通中，可能先听、先理解，再给出经过组织的回应。"
    ]
    assert bazi_source["contexts"] == ["学习", "沟通"]

    astrology_source = alignment["astrology_source"]
    assert astrology_source["signal_ids"] == [
        "ASTROLOGY-PLANET-SIGN-EXPRESSION"
    ]
    assert len(astrology_source["interpretations"]) == 1
    assert "火象取向会以直接投入" in astrology_source["interpretations"][0]
    assert "开创模式更重视发起" in astrology_source["interpretations"][0]
    assert "命中依据：元素：火象；模式：开创" in astrology_source[
        "interpretations"
    ][0]
    assert "火象通过热度、意愿与即时反馈" in astrology_source["mechanisms"][0]
    assert "命中开创模式时" in astrology_source["likely_expressions"][0]
    assert astrology_source["contexts"] == [
        "自我表达",
        "启动任务",
        "需要迅速投入的情境",
        "新任务与转换阶段",
    ]


def test_each_serialized_alignment_keeps_or_explicitly_omits_each_side_source():
    packet = build_narrative_synthesis_packet(_qualified("contrast_b"))
    encoded = encode_narrative_synthesis_packet(packet)
    profiles = {
        profile["system"]: {topic["topic"]: topic for topic in profile["topics"]}
        for profile in (encoded["bazi_profile"], encoded["astrology_profile"])
    }

    for alignment in encoded["alignments"]:
        for system, source_key in (
            ("bazi", "bazi_source"),
            ("astrology", "astrology_source"),
        ):
            source = alignment[source_key]
            expected = profiles[system].get(alignment["topic"])
            assert source == expected


def test_tension_explains_poles_context_and_integration():
    packet = build_narrative_synthesis_packet(_qualified("tension"))
    tension = packet.tensions[0]

    assert tension.topic == "style of expression"
    assert tension.left_pole and tension.right_pole
    assert tension.contexts
    assert tension.integration
    assert tension.why_coexist
    assert tension.left_contexts == ("学习", "沟通")
    assert tension.right_contexts == (
        "自我表达",
        "启动任务",
        "需要迅速投入的情境",
        "新任务与转换阶段",
    )
    assert "bazi.ten_gods[0].ten_god" in tension.why_coexist
    assert "astrology.placements[0].sign" in tension.why_coexist
    assert "先听、先理解，再给出经过组织的回应" in tension.integration
    assert "需要表态或承担核心角色" in tension.integration
    assert "不将一端解释为另一端的否定" not in tension.integration
    assert tension.bazi_signal_ids == ("BAZI-TEN-GOD-EXPRESSION",)
    assert tension.astrology_signal_ids == (
        "ASTROLOGY-PLANET-SIGN-EXPRESSION",
    )
    assert {item.signal_id for item in tension.signal_provenance} == {
        "BAZI-TEN-GOD-EXPRESSION",
        "ASTROLOGY-PLANET-SIGN-EXPRESSION",
    }

    encoded_tension = encode_narrative_synthesis_packet(packet)["tensions"][0]
    assert encoded_tension["why_coexist"] == tension.why_coexist
    assert encoded_tension["left_contexts"] == ["学习", "沟通"]
    assert encoded_tension["right_contexts"] == [
        "自我表达",
        "启动任务",
        "需要迅速投入的情境",
        "新任务与转换阶段",
    ]


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
