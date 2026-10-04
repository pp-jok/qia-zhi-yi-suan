from dataclasses import replace

import pytest

from destiny_personality.core_profile_models import PrimitiveCandidate
from destiny_personality.release_manifest import load_release_manifest
from destiny_personality.release_mapping_bundle import load_active_release_mapping_bundle


def _candidate(source_system, direction, *, contexts=(), rule_ref="MAP-TEST"):
    return PrimitiveCandidate(
        primitive_id="P001",
        source_system=source_system,
        direction=direction,
        fact_refs=("fact:test",),
        semantic_rule_refs=(rule_ref,),
        contexts=contexts,
        salience="high",
        evidence_stability="stable",
        modifier_refs=(),
        counterevidence_refs=(),
        expression_mode="direct",
        tension_level="low",
        counterweight_effect=None,
        limitations=(),
    )


def test_governed_empty_bundle_produces_unknown_not_low():
    from destiny_personality.release_semantics import resolve_release_primitive_states

    states = resolve_release_primitive_states(
        load_active_release_mapping_bundle(), load_release_manifest()
    )

    assert set(states) == {"P001", "P002", "P003", "P004", "P005", "P006"}
    assert {item.state for item in states.values()} == {"unknown"}
    assert all("NO_ACTIVE_APPROVED_MAPPING" in item.limitations for item in states.values())


def test_resolver_rejects_raw_or_forged_mapping_input():
    from destiny_personality.release_semantics import resolve_release_primitive_states

    with pytest.raises(ValueError, match="RELEASE_MAPPING_BUNDLE_INVALID"):
        resolve_release_primitive_states((), load_release_manifest())
    valid = load_active_release_mapping_bundle()
    with pytest.raises(ValueError, match="RELEASE_MAPPING_BUNDLE_INVALID"):
        resolve_release_primitive_states(
            replace(valid, asset_fingerprint="forged"), load_release_manifest()
        )


def test_cross_system_agreement_does_not_increase_salience():
    from destiny_personality.release_semantics import align_release_states

    alignment = align_release_states(
        _candidate("bazi", "high"), _candidate("astrology", "high")
    )

    assert alignment.status == "validation"
    assert alignment.salience_delta == 0
    assert alignment.direction_relation == "agreement"


def test_missing_system_evidence_is_non_comparable():
    from destiny_personality.release_semantics import align_release_states

    alignment = align_release_states(_candidate("bazi", "high"), None)
    assert alignment.status == "non_comparable"
    assert alignment.salience_delta == 0
    assert alignment.bazi_rule_refs == ()
    assert alignment.astrology_rule_refs == ()


def test_internal_system_contradiction_cannot_be_hidden_by_first_candidate():
    from destiny_personality.release_semantics import align_release_candidate_sets

    alignment = align_release_candidate_sets(
        (
            _candidate("bazi", "high", rule_ref="BZ-HIGH"),
            _candidate("bazi", "low", rule_ref="BZ-LOW"),
        ),
        (_candidate("astrology", "high", rule_ref="AS-HIGH"),),
        primitive_id="P001",
    )

    assert alignment.status == "unresolved"
    assert alignment.direction_relation == "internal_contradiction"
    assert alignment.bazi_rule_refs == ("BZ-HIGH", "BZ-LOW")
    assert alignment.salience_delta == 0
