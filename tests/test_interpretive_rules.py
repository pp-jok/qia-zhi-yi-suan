from pathlib import Path

import pytest

from destiny_personality.interpretive_rules import load_interpretive_rule_bundle


def test_rule_bundle_is_versioned_and_contains_both_systems():
    bundle = load_interpretive_rule_bundle()

    assert bundle.bundle_version == "audited-interpretive-rules-v1"
    assert {rule.system for rule in bundle.rules} == {"bazi", "astrology"}


def test_rule_loader_rejects_unknown_confidence(tmp_path: Path):
    (tmp_path / "interpretive_rules_v1.yaml").write_text(
        "bundle_version: audited-interpretive-rules-v1\n"
        "limitations: [Traditional, non-diagnostic rules.]\n"
        "rules:\n"
        "  - signal_id: TEST-001\n"
        "    system: bazi\n"
        "    fact_refs: [bazi.ten_god]\n"
        "    traditional_rule_ref: Test school\n"
        "    topic: Test topic\n"
        "    direction: Test direction\n"
        "    interpretation: Traditional, non-diagnostic interpretation.\n"
        "    confidence: certain\n"
        "    limitations: [Not an empirical diagnostic.]\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="INTERPRETIVE_RULE_INVALID_CONFIDENCE"):
        load_interpretive_rule_bundle(tmp_path)
