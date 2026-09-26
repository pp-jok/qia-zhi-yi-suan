from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_rule_gate_is_approved_but_never_mapping_eligible(tmp_path: Path) -> None:
    from destiny_personality.semantic_core import (
        load_semantic_mechanism_role_policy,
        mapping_eligibility_for_role,
    )

    policy = load_semantic_mechanism_role_policy(PROJECT_ROOT)

    assert mapping_eligibility_for_role(policy, "RULE_GATE") == {
        "evidence_admission": True,
        "mapping_origin": False,
        "primitive_direction": False,
        "primitive_state": False,
        "runtime_activation": False,
    }


def test_mapping_and_all_downstream_layers_fail_closed_without_approved_mapping() -> None:
    from destiny_personality.semantic_core import build_semantic_core_candidate

    result = build_semantic_core_candidate(
        profile_ref="candidate-profile-test",
        approved_mapping_candidates=(),
    )

    assert result.mapping_candidates == ()
    assert result.signatures == ()
    assert result.dynamics == ()
    assert result.shadow_mature_forms == ()
    assert result.fate_themes == ()
    assert result.archetype is None
    assert result.stage_statuses == {
        "mapping": "blocked_by_gate",
        "primitive_v2": "blocked_by_gate",
        "signature": "blocked_by_gate",
        "dynamic": "blocked_by_gate",
        "theme": "blocked_by_gate",
        "archetype": "blocked_by_gate",
    }


def test_promotion_requires_decision_and_supports_one_step_rollback() -> None:
    from destiny_personality.semantic_core import (
        promote_semantic_bundle,
        rollback_semantic_bundle,
    )

    blocked = promote_semantic_bundle("active-v1", "candidate-v2", None)
    assert blocked.status == "blocked_by_gate"
    assert blocked.blockers == ("PROMOTION_AUTHORIZATION_REQUIRED",)

    promoted = promote_semantic_bundle("active-v1", "candidate-v2", "PO-DECISION-1")
    assert promoted.status == "shadow"
    assert rollback_semantic_bundle(promoted).active_bundle_ref == "active-v1"


def test_candidate_fingerprints_do_not_change_active_fingerprints() -> None:
    from destiny_personality.semantic_core import build_semantic_core_candidate_fingerprint
    from destiny_personality.core_profile_builder import candidate_semantic_bundle_fingerprint

    before = candidate_semantic_bundle_fingerprint()
    fingerprint = build_semantic_core_candidate_fingerprint(PROJECT_ROOT)

    assert len(fingerprint) == 64
    assert candidate_semantic_bundle_fingerprint() == before


def test_core_audit_explain_diff_and_report_are_contained() -> None:
    from destiny_personality.semantic_core import (
        build_report_plan,
        build_semantic_core_candidate,
        diff_semantic_core_candidates,
        explain_semantic_core_item,
        audit_semantic_core_candidate,
    )

    core = build_semantic_core_candidate("profile-a", ())
    assert audit_semantic_core_candidate(core)["production_promotion"] == "blocked_by_gate"
    assert explain_semantic_core_item(core, "signature:any")["status"] == "not_found"
    assert build_report_plan(core, "standard-portrait-v1").sections == ()
    assert diff_semantic_core_candidates(core, core).changed_categories == ()


def test_future_formation_engines_preserve_valid_zero_output() -> None:
    from destiny_personality.semantic_core import (
        form_archetype,
        form_core_dynamics,
        form_dominant_signatures,
        form_fate_themes,
        form_shadow_mature,
    )

    assert form_dominant_signatures(()) == ()
    assert form_core_dynamics(()) == ()
    assert form_shadow_mature(()) == ()
    assert form_fate_themes(()) == ()
    assert form_archetype(()) is None


def test_cli_audits_candidate_only_semantic_core(capsys) -> None:
    from destiny_personality.cli import main

    assert main(["audit-semantic-core", str(PROJECT_ROOT)]) == 0
    assert "blocked_by_gate" in capsys.readouterr().out


def test_review_packet_never_converts_engineering_pass_into_semantic_approval() -> None:
    from destiny_personality.semantic_core import build_promotion_review_packet

    packet = build_promotion_review_packet("candidate-v2", technical_checks=("PASS",), decision_ref=None)

    assert packet["engineering_status"] == "ready_for_review"
    assert packet["semantic_status"] == "blocked_by_gate"
    assert packet["blockers"] == ("PROMOTION_AUTHORIZATION_REQUIRED",)


def test_cli_exposes_mapping_validation_and_downstream_zero_state(capsys) -> None:
    from destiny_personality.cli import main

    assert main(["validate-mapping-v2", str(PROJECT_ROOT)]) == 0
    assert "blocked_by_gate" in capsys.readouterr().out


def test_cli_exposes_mapping_calibration_and_holdout_gates(capsys) -> None:
    from destiny_personality.cli import main

    assert main(["run-mapping-calibration", str(PROJECT_ROOT)]) == 0
    calibration_output = capsys.readouterr().out
    assert "blocked_by_gate" in calibration_output
    assert "design_set" in calibration_output


def test_cli_refuses_to_register_a_nonpassing_mapping_evaluation(capsys) -> None:
    from destiny_personality.cli import main

    assert main(["run-mapping-calibration", str(PROJECT_ROOT), "--register"]) == 2
    assert "EVALUATION_ARTIFACT_NOT_PASSED" in capsys.readouterr().err


def test_cli_promotion_requires_decision_reference(capsys) -> None:
    from destiny_personality.cli import main

    assert main(["promote-semantic-bundle", "active-v1", "candidate-v2"]) == 0
    assert "PROMOTION_AUTHORIZATION_REQUIRED" in capsys.readouterr().out


def test_legacy_promotion_cli_is_explicitly_simulated(capsys) -> None:
    from destiny_personality.cli import main

    assert main(["promote-semantic-bundle", "active-v1", "candidate-v2", "--decision-ref", "D1"]) == 0
    assert "simulated_shadow" in capsys.readouterr().out


def test_cli_review_packet_and_rollback_are_machine_readable(capsys) -> None:
    from destiny_personality.cli import main

    assert main(["promotion-review-packet", "candidate-v2"]) == 0
    assert "blocked_by_gate" in capsys.readouterr().out
    assert main(["rollback-semantic-bundle", "active-v1", "candidate-v2", "PO-1"]) == 0
    assert "rolled_back" in capsys.readouterr().out
    assert main(["run-mapping-holdout", str(PROJECT_ROOT)]) == 0
    holdout_output = capsys.readouterr().out
    assert "blocked_by_gate" in holdout_output
    assert "holdout_set" in holdout_output
    assert main(["build-signatures", str(PROJECT_ROOT)]) == 0
    assert "blocked_by_gate" in capsys.readouterr().out
