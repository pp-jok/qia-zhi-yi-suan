from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_empty_mapping_v2_registry_is_a_valid_fail_closed_state() -> None:
    from destiny_personality.mapping_v2 import load_mapping_v2_candidate_registry

    registry = load_mapping_v2_candidate_registry(PROJECT_ROOT)

    assert registry.review_status == "candidate_only"
    assert registry.candidates == ()


def test_mapping_v2_calibration_and_holdout_are_blocked_without_approved_bundle() -> None:
    from destiny_personality.mapping_v2 import (
        run_mapping_v2_calibration,
        run_mapping_v2_holdout,
    )

    assert run_mapping_v2_calibration(()) .status == "blocked_by_gate"
    assert run_mapping_v2_holdout(()) .status == "blocked_by_gate"
