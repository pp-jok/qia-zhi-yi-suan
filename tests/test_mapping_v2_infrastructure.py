from pathlib import Path


def test_mapping_v2_engine_returns_valid_zero_state_when_no_mapping_eligible_mechanisms() -> None:
    from destiny_personality.mapping_v2 import (
        build_fresh_mapping_candidates,
        compile_mapping_v2_candidate_bundle,
        mapping_v2_candidate_fingerprint,
    )

    candidates = build_fresh_mapping_candidates(())
    bundle = compile_mapping_v2_candidate_bundle(candidates)

    assert candidates == ()
    assert bundle.status == "blocked_by_gate"
    assert bundle.bazi_rules == () and bundle.astrology_rules == ()
    assert len(mapping_v2_candidate_fingerprint(Path(__file__).resolve().parents[1])) == 64


def test_mapping_candidate_requires_approved_mapping_eligible_mechanism() -> None:
    from destiny_personality.mapping_v2 import validate_mapping_candidate

    findings = validate_mapping_candidate(
        {
            "mapping_candidate_id": "MC-TEST",
            "semantic_mechanism_refs": ["SMC-1"],
            "primitive_id": "P004",
            "primitive_question": "When and how is concrete action started and advanced?",
        },
        approved_mapping_eligible_ids=(),
    )

    assert findings == ("APPROVED_MAPPING_ELIGIBLE_MECHANISM_REQUIRED",)
