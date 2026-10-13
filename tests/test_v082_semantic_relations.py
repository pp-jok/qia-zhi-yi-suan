from destiny_personality.interpretive_models import InterpretiveSignal


def _signal(signal_id, fact_ref, direction):
    return InterpretiveSignal(
        signal_id=signal_id,
        system="bazi" if signal_id.startswith("BAZI") else "astrology",
        fact_refs=(fact_ref,),
        value_predicates=(),
        traditional_rule_ref="test:traditional-reference",
        topic="test topic",
        direction=direction,
        interpretation="test interpretation",
        confidence="moderate",
        limitations=("test limitation",),
        mechanism="test mechanism",
        likely_expression="test expression",
        contexts=("test context",),
    )


def test_explicit_relationship_requires_every_named_signal_and_preserves_provenance():
    from destiny_personality.interpretive_relationships import (
        match_interpretive_relationships,
    )

    matched = match_interpretive_relationships(
        (
            _signal("BAZI-TEN-GOD-EXPRESSION", "bazi.ten_gods[0]", "reflective"),
            _signal("BAZI-TEN-GOD-OUTPUT", "bazi.ten_gods[1]", "outward"),
        )
    )

    assert len(matched) == 1
    relationship = matched[0]
    assert relationship.relationship_rule_id == "REL-BAZI-EXPRESSION-SEQUENCE"
    assert relationship.relationship_type == "contextual_sequence"
    assert relationship.signal_ids == (
        "BAZI-TEN-GOD-EXPRESSION",
        "BAZI-TEN-GOD-OUTPUT",
    )
    assert relationship.fact_refs == ("bazi.ten_gods[0]", "bazi.ten_gods[1]")


def test_missing_relationship_prerequisite_does_not_create_a_dynamic_record():
    from destiny_personality.interpretive_relationships import (
        match_interpretive_relationships,
    )

    assert match_interpretive_relationships(
        (_signal("BAZI-TEN-GOD-EXPRESSION", "bazi.ten_gods[0]", "reflective"),)
    ) == ()


def test_relationship_bundle_rejects_unknown_field(tmp_path):
    from destiny_personality.interpretive_relationships import (
        load_interpretive_relationship_bundle,
    )

    (tmp_path / "interpretive_relationships_v1.yaml").write_text(
        "bundle_version: audited-interpretive-relationships-v1\n"
        "rules:\n"
        "  - relationship_rule_id: REL-TEST\n"
        "    source_signal_ids: [BAZI-TEN-GOD-EXPRESSION, BAZI-TEN-GOD-OUTPUT]\n"
        "    relationship_type: contextual_sequence\n"
        "    pole_a: reflective\n"
        "    pole_b: outward\n"
        "    activation_contexts: [沟通]\n"
        "    interaction_mechanism: test\n"
        "    pressure_hypothesis: test\n"
        "    integration_hypothesis: test\n"
        "    counter_conditions: [test]\n"
        "    limitations: [test]\n"
        "    traditional_rule_ref: test\n"
        "    unexpected: value\n",
        encoding="utf-8",
    )

    try:
        load_interpretive_relationship_bundle(tmp_path)
    except ValueError as error:
        assert str(error) == "INTERPRETIVE_RELATIONSHIP_INVALID"
    else:
        raise AssertionError("invalid relationship asset was accepted")


def test_dynamic_is_formed_only_from_a_matched_relationship_rule():
    from destiny_personality.audited_core_profile import _dynamics
    from destiny_personality.interpretive_relationships import (
        MatchedInterpretiveRelationship,
    )

    relationship = MatchedInterpretiveRelationship(
        relationship_rule_id="REL-TEST",
        relationship_type="contextual_sequence",
        pole_a="理解",
        pole_b="表达",
        activation_contexts=("沟通",),
        interaction_mechanism="先整理再表达。",
        pressure_hypothesis="压力下可能跳过整理。",
        integration_hypothesis="先整理，再表达。",
        counter_conditions=("缺少前提",),
        limitations=("传统反思",),
        traditional_rule_ref="test:relationship",
        signal_ids=("BAZI-TEN-GOD-EXPRESSION", "BAZI-TEN-GOD-OUTPUT"),
        rule_refs=("test:source", "test:relationship"),
        fact_refs=("bazi.ten_gods[0]", "bazi.ten_gods[1]"),
    )

    assert _dynamics(()) == ()
    (dynamic,) = _dynamics((relationship,))
    assert dynamic.relationship_type == "contextual_sequence"
    assert dynamic.source_item_ids == ("relationship:REL-TEST",)
    assert dynamic.pressure_pattern == "压力下可能跳过整理。"
    assert dynamic.integration_pattern == "先整理，再表达。"


def test_v082_rule_bundle_expands_time_sensitive_context_beyond_the_sun():
    from destiny_personality.interpretive_rules import load_interpretive_rule_bundle

    rules = {rule.signal_id: rule for rule in load_interpretive_rule_bundle().rules}

    assert {"ASTROLOGY-MERCURY-HOUSE-CONTEXT", "ASTROLOGY-MARS-HOUSE-CONTEXT"} <= set(rules)
    assert all(
        rule.fact_refs == ("astrology.house_placement",)
        and rule.value_predicates[0].body in {"Mercury", "Mars"}
        and rule.limitations == ("出生时间不可用时必须完全省略。",)
        for rule in (
            rules["ASTROLOGY-MERCURY-HOUSE-CONTEXT"],
            rules["ASTROLOGY-MARS-HOUSE-CONTEXT"],
        )
    )


def test_dynamic_narrative_shows_its_rule_level_counter_conditions():
    from destiny_personality.audited_core_profile import AuditedProfileItem
    from destiny_personality.audited_profile_report import _narrative

    content = _narrative(
        AuditedProfileItem(
            item_id="dynamic:test",
            topic="test",
            title="test",
            statement="test statement",
            signal_ids=("signal",),
            rule_refs=("rule",),
            fact_refs=("fact",),
            limitations=("limitation",),
            salience=1,
            counter_evidence=("缺少一个前提时不适用",),
        )
    )

    assert "不适用或需要收紧的条件：缺少一个前提时不适用" in content
