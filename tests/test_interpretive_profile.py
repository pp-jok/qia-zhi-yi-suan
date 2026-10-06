from typing import Optional

from destiny_personality.interpretive_models import InterpretiveSignal
from destiny_personality.interpretive_profile import (
    ALLOWED_CONFIDENCES,
    build_interpretive_core_profile,
    synthesize_interpretive_core_profile,
)
from destiny_personality.interpretive_rules import extract_interpretive_signals


def _signal(
    signal_id: str,
    *,
    system: str,
    topic: str,
    direction: str,
    confidence: str = "moderate",
    rule_ref: Optional[str] = None,
) -> InterpretiveSignal:
    return InterpretiveSignal(
        signal_id=signal_id,
        system=system,
        fact_refs=(f"{system}.test[0].value",),
        value_predicates=(),
        traditional_rule_ref=rule_ref or f"tradition:{signal_id}",
        topic=topic,
        direction=direction,
        interpretation=f"Interpretation for {signal_id}.",
        confidence=confidence,
        limitations=("Traditional interpretation only.",),
    )


def test_builder_uses_only_signals_extracted_from_qualified_facts(qualified_facts):
    extracted = extract_interpretive_signals(qualified_facts)

    profile = build_interpretive_core_profile(qualified_facts)

    conclusion_ids = {
        signal_id
        for conclusion in profile.conclusions
        for signal_id in (
            conclusion.supporting_signal_ids
            + conclusion.countervailing_signal_ids
        )
    }
    assert profile.mode == "audited_interpretive"
    assert conclusion_ids
    assert conclusion_ids == {signal.signal_id for signal in extracted}


def test_profile_preserves_cross_system_agreement_and_tension():
    signals = (
        _signal(
            "BAZI-AGREEMENT",
            system="bazi",
            topic="expression",
            direction="outward",
        ),
        _signal(
            "ASTROLOGY-AGREEMENT",
            system="astrology",
            topic="expression",
            direction="outward",
        ),
        _signal(
            "BAZI-TENSION",
            system="bazi",
            topic="pace",
            direction="deliberate",
        ),
        _signal(
            "ASTROLOGY-TENSION-SUPPORT",
            system="astrology",
            topic="pace",
            direction="deliberate",
        ),
        _signal(
            "ASTROLOGY-TENSION",
            system="astrology",
            topic="pace",
            direction="spontaneous",
        ),
    )

    profile = synthesize_interpretive_core_profile(signals)

    agreement = next(
        item
        for item in profile.conclusions
        if item.topic == "expression" and item.direction == "outward"
    )
    tensions = tuple(item for item in profile.conclusions if item.topic == "pace")
    assert agreement.supporting_signal_ids == (
        "ASTROLOGY-AGREEMENT",
        "BAZI-AGREEMENT",
    )
    assert agreement.countervailing_signal_ids == ()
    assert agreement.confidence == "high"
    assert {item.direction for item in tensions} == {"deliberate", "spontaneous"}
    assert all(item.supporting_signal_ids for item in tensions)
    assert all(item.countervailing_signal_ids for item in tensions)
    assert {item.confidence for item in tensions} == {"exploratory"}


def test_profile_applies_the_controlled_confidence_policy():
    signals = (
        _signal(
            "BAZI-INDEPENDENT-1",
            system="bazi",
            topic="learning",
            direction="reflective",
            rule_ref="rule:one",
        ),
        _signal(
            "BAZI-INDEPENDENT-2",
            system="bazi",
            topic="learning",
            direction="reflective",
            rule_ref="rule:two",
        ),
        _signal(
            "BAZI-STABLE",
            system="bazi",
            topic="work",
            direction="structured",
        ),
        _signal(
            "ASTROLOGY-PARTIAL",
            system="astrology",
            topic="relationships",
            direction="receptive",
            confidence="exploratory",
        ),
    )

    profile = synthesize_interpretive_core_profile(
        signals,
        requested_topics=("learning", "work", "relationships", "stress"),
    )

    confidence_by_topic = {
        conclusion.topic: conclusion.confidence
        for conclusion in profile.conclusions
    }
    assert confidence_by_topic == {
        "learning": "high",
        "relationships": "exploratory",
        "stress": "insufficient",
        "work": "moderate",
    }
    insufficient = next(
        item for item in profile.conclusions if item.topic == "stress"
    )
    assert insufficient.supporting_signal_ids == ()
    assert insufficient.countervailing_signal_ids == ()


def test_profile_uses_only_allowed_confidence_labels():
    profile = synthesize_interpretive_core_profile(
        (
            _signal(
                "BAZI-STABLE",
                system="bazi",
                topic="work",
                direction="structured",
            ),
        ),
        requested_topics=("work", "unmatched"),
    )

    assert {item.confidence for item in profile.conclusions} <= ALLOWED_CONFIDENCES
