from pathlib import Path

from destiny_personality.deterministic_facts_codec import load_qualified_deterministic_facts
from destiny_personality.audited_core_profile import (
    build_audited_interpretive_core_profile,
)


ROOT = Path(__file__).parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "interpretive" / "v060"


def _qualified(name: str):
    return load_qualified_deterministic_facts(
        FIXTURES / f"{name}-facts.json",
        FIXTURES / f"{name}-qualification.json",
    )


def test_audited_profile_uses_only_qualified_signal_evidence():
    qualified = _qualified("cross-system-agreement")

    profile = build_audited_interpretive_core_profile(qualified)

    assert profile.schema_version == "audited-interpretive-cdp-v1"
    assert profile.fact_fingerprint == qualified.fact_fingerprint
    assert profile.semantic_model_assurance == "audited_interpretive_rule_derived"
    assert {candidate.system for candidate in profile.bazi_candidates} == {"bazi"}
    assert {candidate.system for candidate in profile.astrology_candidates} == {"astrology"}
    assert profile.dominant_signatures
    assert all(item.signal_ids and item.rule_refs and item.fact_refs for item in profile.dominant_signatures)
    assert "formal primitive coverage is not asserted" in profile.limitations


def test_audited_profile_keeps_cross_system_relationships_bounded():
    profile = build_audited_interpretive_core_profile(_qualified("cross-system-tension"))

    assert any(item.kind == "tension" for item in profile.cross_system_alignments)
    assert any(item.kind == "tension" for item in profile.core_dynamics)
    assert all(item.signal_ids for item in profile.cross_system_alignments)
    assert all(item.signal_ids for item in profile.core_dynamics)
    assert profile.shadow_mature_forms
    assert profile.archetype is not None
