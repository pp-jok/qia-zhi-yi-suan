import json

from destiny_personality.calculation import DeterministicChartFacts


def test_calibration_and_holdout_runners_emit_bound_machine_records(tmp_path, normalized_time, bazi_facts, astrology_facts) -> None:
    from destiny_personality.calibration import run_candidate_calibration, run_candidate_holdout
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi_facts, astrology_facts),
        fact_assurance="capability_reported",
    )
    calibration_path = tmp_path / "calibration.json"
    holdout_path = tmp_path / "holdout.json"

    calibration = run_candidate_calibration({"synthetic-a": profile}, calibration_path)
    holdout = run_candidate_holdout({"synthetic-h": profile}, calibration_path, holdout_path)

    assert calibration.run_status == "pass"
    assert json.loads(calibration_path.read_text(encoding="utf-8"))["case_ids"] == ["synthetic-a"]
    assert holdout.run_status == "pass"
    assert json.loads(holdout_path.read_text(encoding="utf-8"))["calibration_policy_sha256"]
