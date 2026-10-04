from destiny_personality.core_profile_models import PrimitiveCandidate
from destiny_personality.release_manifest import load_release_manifest


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


def test_no_mapping_produces_unknown_not_low():
    from destiny_personality.release_semantics import resolve_release_primitive_states

    states = resolve_release_primitive_states((), load_release_manifest())

    assert set(states) == {"P001", "P002", "P003", "P004", "P005", "P006"}
    assert {item.state for item in states.values()} == {"unknown"}
    assert all("NO_ACTIVE_APPROVED_MAPPING" in item.limitations for item in states.values())


def test_cross_system_agreement_does_not_increase_salience():
    from destiny_personality.release_semantics import align_release_states

    alignment = align_release_states(_candidate("bazi", "high"), _candidate("astrology", "high"))

    assert alignment.status == "validation"
    assert alignment.salience_delta == 0
    assert alignment.direction_relation == "agreement"


def test_context_evidence_requires_explicit_promotion_before_global_state():
    from destiny_personality.release_semantics import resolve_release_primitive_states

    mapping = {
        "mapping_candidate_id": "MAP-CONTEXT",
        "primitive_id": "P001",
        "source_system": "bazi",
        "review_status": "approved",
        "proposed_direction": {"state": "supported_high"},
        "contexts": ["work"],
        "canonical_fact_requirements": ["fact:test"],
        "semantic_mechanism_refs": ["SMC-TEST"],
        "evidence_root_refs": ["ER-TEST"],
    }

    state = resolve_release_primitive_states((mapping,), load_release_manifest())["P001"]

    assert state.state == "unknown"
    assert state.context_states == {"work": "supported_high"}
    assert "CONTEXT_EVIDENCE_NOT_PROMOTED" in state.limitations


def test_context_promotion_requires_independent_evidence_roots():
    from destiny_personality.release_semantics import resolve_release_primitive_states

    mappings = (
        {
            "mapping_candidate_id": "MAP-WORK",
            "primitive_id": "P001",
            "source_system": "bazi",
            "review_status": "approved",
            "proposed_direction": {"state": "supported_high"},
            "contexts": ["work"],
            "canonical_fact_requirements": ["fact:work"],
            "semantic_mechanism_refs": ["SMC-WORK"],
            "evidence_root_refs": ["ER-SHARED"],
        },
        {
            "mapping_candidate_id": "MAP-RELATIONSHIP",
            "primitive_id": "P001",
            "source_system": "astrology",
            "review_status": "approved",
            "proposed_direction": {"state": "supported_high"},
            "contexts": ["relationship"],
            "canonical_fact_requirements": ["fact:relationship"],
            "semantic_mechanism_refs": ["SMC-RELATIONSHIP"],
            "evidence_root_refs": ["ER-SHARED"],
        },
    )

    state = resolve_release_primitive_states(mappings, load_release_manifest())["P001"]

    assert state.state == "unknown"


def test_context_promotion_rejects_material_counterevidence():
    from destiny_personality.release_semantics import resolve_release_primitive_states

    mappings = tuple(
        {
            "mapping_candidate_id": "MAP-" + context,
            "primitive_id": "P001",
            "source_system": "bazi",
            "review_status": "approved",
            "proposed_direction": {"state": "supported_high"},
            "contexts": [context],
            "canonical_fact_requirements": ["fact:" + context],
            "semantic_mechanism_refs": ["SMC-" + context],
            "evidence_root_refs": ["ER-" + context],
            "counterevidence": ["counter:material"] if context == "work" else [],
        }
        for context in ("work", "relationship")
    )

    state = resolve_release_primitive_states(mappings, load_release_manifest())["P001"]

    assert state.state == "unknown"


def test_missing_system_evidence_is_non_comparable():
    from destiny_personality.release_semantics import align_release_states

    alignment = align_release_states(_candidate("bazi", "high"), None)

    assert alignment.status == "non_comparable"
    assert alignment.salience_delta == 0
