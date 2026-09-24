import json
from pathlib import Path

import pytest


def test_role_policy_is_enforced_by_authoritative_mapping_eligibility(tmp_path: Path) -> None:
    from destiny_personality.semantic_authority import load_mapping_eligible_semantic_mechanisms

    root = tmp_path / "semantic-mechanisms-v1"
    root.mkdir()
    (root / "semantic_evidence_root_registry_v1.yaml").write_text("schema_version: semantic-evidence-root-registry-v1\nroots: []\n", encoding="utf-8")
    assert load_mapping_eligible_semantic_mechanisms(root, {"PRIMARY_EVIDENCE": {"mapping_origin": True}}).mechanisms == ()


def test_synthetic_policy_drives_complete_nonzero_pipeline() -> None:
    from destiny_personality.semantic_pipeline import build_semantic_core_from_approved_mapping

    core = build_semantic_core_from_approved_mapping(
        "profile:test",
        ({"mapping_candidate_id": "MAP-1", "primitive_id": "P001", "proposed_direction": {"state": "supported_high"}, "semantic_mechanism_refs": ["SMC-1"], "evidence_root_refs": ["ER-1"], "canonical_fact_requirements": ["fact:1"]},),
        {
            "signature": {"rules": [{"signature_id": "SIG-1", "required_primitive_ids": ["P001"]}]},
            "dynamic": {"rules": [{"dynamic_id": "DYN-1", "required_signature_ids": ["SIG-1"]}]},
            "theme": {"rules": [{"theme_id": "THEME-1", "required_dynamic_ids": ["DYN-1"]}]},
            "archetype": {"rules": [{"archetype_id": "ARCH-1", "required_theme_ids": ["THEME-1"]}]},
        },
    )

    assert core["stage_statuses"]["primitive_v2"] == "available"
    assert core["signatures"][0]["signature_id"] == "SIG-1"
    assert core["dynamics"][0]["dynamic_id"] == "DYN-1"
    assert core["fate_themes"][0]["theme_id"] == "THEME-1"
    assert core["archetype"]["archetype_id"] == "ARCH-1"


def test_promotion_requires_bound_decision_artifact_and_persisted_record(tmp_path: Path) -> None:
    from destiny_personality.semantic_promotion import promote_from_decision, rollback_from_record

    decision = tmp_path / "decision.json"
    decision.write_text('{"schema_version":"semantic-promotion-decision-v1","decision_id":"D-1","candidate_bundle_ref":"bundle:test","candidate_fingerprint":"abc","decision":"approve_shadow","allowed_stage":"shadow","decision_timestamp":"2026-09-23T00:00:00Z","supersedes":null,"review_refs":["review:1"]}', encoding="utf-8")
    record = tmp_path / "promotion.json"

    promotion = promote_from_decision("active:test", "bundle:test", "abc", decision, ("PASS",), record)
    assert promotion.status == "shadow"
    assert rollback_from_record(record).active_bundle_ref == "active:test"


def test_nonzero_core_explain_diff_and_report_remain_source_contained() -> None:
    from destiny_personality.semantic_pipeline import (
        build_semantic_core_from_approved_mapping,
        build_semantic_report,
        diff_semantic_cores,
        explain_semantic_item,
    )

    core = build_semantic_core_from_approved_mapping(
        "profile:test", ({"mapping_candidate_id": "MAP-1", "primitive_id": "P001", "proposed_direction": {"state": "supported_high"}, "semantic_mechanism_refs": ["SMC-1"], "evidence_root_refs": ["ER-1"], "canonical_fact_requirements": ["fact:1"]},),
        {"signature": {"rules": [{"signature_id": "SIG-1", "required_primitive_ids": ["P001"]}]}, "dynamic": {"rules": []}, "theme": {"rules": []}, "archetype": {"rules": []}},
    )

    explanation = explain_semantic_item(core, "signature:SIG-1")
    assert explanation["source_refs"] == ("P001",)
    report = build_semantic_report(core, "standard-portrait-v1")
    assert report["sections"][0]["source_refs"]
    assert report["sections"][0]["body"]
    assert diff_semantic_cores(core, {**core, "signatures": ()}) == ("signature_change",)


def test_cli_audit_reports_authoritative_eligibility_and_candidate_fingerprints(capsys) -> None:
    from destiny_personality.cli import main

    assert main(["audit-semantic-core", str(Path(__file__).resolve().parents[1])]) == 0
    output = capsys.readouterr().out
    assert "mapping_eligible_mechanism_count" in output
    assert "mapping_v2_candidate_fingerprint" in output
    assert "mapping_v2_runtime_status" in output


def test_pipeline_codec_preserves_nonzero_audit_and_policy_references(tmp_path: Path) -> None:
    from destiny_personality.semantic_pipeline import build_semantic_core_from_approved_mapping, semantic_pipeline_fingerprint
    from destiny_personality.semantic_pipeline_codec import load_pipeline_core, write_pipeline_core

    core = build_semantic_core_from_approved_mapping("profile:test", ({"mapping_candidate_id": "MAP-1", "primitive_id": "P001", "proposed_direction": {"state": "supported_high"}, "semantic_mechanism_refs": ["SMC-1"], "evidence_root_refs": ["ER-1"], "canonical_fact_requirements": ["fact:1"]},), {"signature": {"rules": []}, "dynamic": {"rules": []}, "theme": {"rules": []}, "archetype": {"rules": []}})
    path = tmp_path / "core.json"

    write_pipeline_core(core, {"signature": "TEST-V1"}, path)
    restored = load_pipeline_core(path)

    assert restored["core"] == core
    assert restored["formation_policy_versions"] == {"signature": "TEST-V1"}
    assert len(semantic_pipeline_fingerprint({"signature": "TEST-V1"})) == 64
    assert restored["formation_policy_fingerprint"] == semantic_pipeline_fingerprint({"signature": "TEST-V1"})


def test_pipeline_codec_fingerprint_changes_when_policy_content_changes(tmp_path: Path) -> None:
    from destiny_personality.semantic_pipeline_codec import load_pipeline_core, write_pipeline_core

    core = {"profile_ref": "test"}
    left, right = tmp_path / "left.json", tmp_path / "right.json"
    write_pipeline_core(core, {"signature": {"policy_version": "V1", "rules": ["S1"]}}, left)
    write_pipeline_core(core, {"signature": {"policy_version": "V1", "rules": ["S2"]}}, right)
    assert load_pipeline_core(left)["formation_policy_fingerprint"] != load_pipeline_core(right)["formation_policy_fingerprint"]


def test_authorized_promotion_cli_requires_decision_artifact(tmp_path: Path, capsys) -> None:
    from destiny_personality.cli import main

    with pytest.raises(SystemExit):
        main(["promote-semantic-bundle-authorized", "active:test", "bundle:test", "abc", str(tmp_path / "fake-decision.json")])


def test_build_semantic_core_cli_persists_authoritative_zero_state(tmp_path: Path, capsys) -> None:
    from destiny_personality.cli import main
    from destiny_personality.semantic_pipeline_codec import load_pipeline_core

    output = tmp_path / "semantic-core.json"
    root = Path(__file__).resolve().parents[1]
    assert main(["build-semantic-core", str(root), "profile:test", str(output)]) == 0
    assert output.is_file()
    assert "blocked_by_gate" in capsys.readouterr().out
    persisted = load_pipeline_core(output)
    assert "repository_mapping_v2" in persisted["core"]["audit_trail"]


def test_pipeline_core_is_readable_by_existing_semantic_core_views(tmp_path: Path, capsys) -> None:
    from destiny_personality.cli import main

    root = Path(__file__).resolve().parents[1]
    output = tmp_path / "semantic-core.json"
    assert main(["build-semantic-core", str(root), "profile:test", str(output)]) == 0
    assert main(["semantic-core-source-view", str(output), "mapping"]) == 0
    assert "profile:test" in capsys.readouterr().out


def test_repository_mapping_compilation_uses_authoritative_eligibility_snapshot(tmp_path: Path) -> None:
    from destiny_personality.mapping_v2 import compile_mapping_v2_from_repository

    candidates = tmp_path / "candidates"
    (candidates / "mapping-v2").mkdir(parents=True)
    (candidates / "semantic-mechanisms-v1").mkdir()
    (candidates / "mapping-v2" / "mapping_v2_candidate_registry_v1.yaml").write_text(
        "schema_version: mapping-v2-candidate-registry-v1\nreview_status: candidate_only\ncandidates: []\n",
        encoding="utf-8",
    )
    assert compile_mapping_v2_from_repository(tmp_path).status == "blocked_by_gate"


def test_promotion_technical_gate_requires_passing_bound_records(tmp_path: Path) -> None:
    from destiny_personality.semantic_promotion import validate_technical_records

    calibration = tmp_path / "calibration.json"
    holdout = tmp_path / "holdout.json"
    calibration.write_text('{"run_status":"pass","bundle_fingerprint":"abc"}', encoding="utf-8")
    holdout.write_text('{"run_status":"pass","bundle_fingerprint":"abc"}', encoding="utf-8")

    assert validate_technical_records("abc", calibration, holdout) == ("PASS",)
    holdout.write_text('{"run_status":"fail","bundle_fingerprint":"abc"}', encoding="utf-8")
    assert "HOLDOUT_NOT_PASSED" in validate_technical_records("abc", calibration, holdout)


def test_shadow_diff_exposes_stage_activation_metrics() -> None:
    from destiny_personality.semantic_promotion import shadow_diff_metrics

    active = {"primitive_states": (), "signatures": (), "dynamics": (), "fate_themes": (), "archetype": None}
    candidate = {"primitive_states": ({"state": "unknown"}, {"state": "mixed"}), "signatures": ({"signature_id": "S"},), "dynamics": (), "fate_themes": (), "archetype": None}
    assert shadow_diff_metrics(active, candidate)["signature_count_delta"] == 1
    assert shadow_diff_metrics(active, candidate)["unknown_rate"] == 0.5


def test_authorized_rollback_is_persisted_and_cannot_repeat(tmp_path: Path) -> None:
    from destiny_personality.semantic_promotion import rollback_from_record

    record = tmp_path / "record.json"
    record.write_text('{"schema_version":"semantic-promotion-record-v1","status":"shadow","active_bundle_ref":"active:test","candidate_bundle_ref":"bundle:test","decision_ref":"D-1","rollback_target":"active:test","candidate_fingerprint":"abc","validation_refs":["PASS"]}', encoding="utf-8")
    assert rollback_from_record(record).status == "rolled_back"
    assert json.loads(record.read_text(encoding="utf-8"))["status"] == "rolled_back"
    with pytest.raises(ValueError, match="ROLLBACK_RECORD_INVALID"):
        rollback_from_record(record)


def test_dynamic_policy_metadata_is_retained_as_formed_data() -> None:
    from destiny_personality.semantic_pipeline import build_semantic_core_from_approved_mapping

    core = build_semantic_core_from_approved_mapping(
        "profile:test",
        ({"mapping_candidate_id": "M1", "primitive_id": "P001", "proposed_direction": {"state": "supported_high"}},),
        {"signature": {"rules": [{"signature_id": "S1", "required_primitive_ids": ["P001"]}]}, "dynamic": {"rules": [{"dynamic_id": "D1", "required_signature_ids": ["S1"], "shadow_form": "SH-1", "mature_form": "MT-1"}]}},
    )
    assert core["shadow_mature_forms"] == ({"dynamic_id": "D1", "shadow_form": "SH-1", "mature_form": "MT-1"},)


def test_pipeline_persists_provenance_from_signature_to_facts() -> None:
    from destiny_personality.semantic_pipeline import build_semantic_core_from_approved_mapping, explain_semantic_pipeline_item, semantic_pipeline_source_view

    core = build_semantic_core_from_approved_mapping(
        "profile:test",
        ({"mapping_candidate_id": "M1", "primitive_id": "P001", "proposed_direction": {"state": "supported_high"}, "semantic_mechanism_refs": ["SMC-1"], "evidence_root_refs": ["ER-1"], "canonical_fact_requirements": ["fact:1"]},),
        {"signature": {"rules": [{"signature_id": "S1", "required_primitive_ids": ["P001"]}]}},
    )
    assert ("signature:S1", "formed_from", "primitive:P001") in core["provenance"]["edges"]
    assert ("mapping:M1", "supported_by", "fact:fact:1") in core["provenance"]["edges"]
    assert "fact:fact:1" in explain_semantic_pipeline_item(core, "signature:S1")["provenance_nodes"]
    assert semantic_pipeline_source_view(core, "signature")["item_count"] == 1


def test_primitive_resolver_merges_conflicting_mapping_evidence() -> None:
    from destiny_personality.semantic_pipeline import resolve_primitive_states

    states = resolve_primitive_states((
        {"mapping_candidate_id": "M1", "primitive_id": "P001", "proposed_direction": {"state": "supported_high"}},
        {"mapping_candidate_id": "M2", "primitive_id": "P001", "proposed_direction": {"state": "supported_low"}},
    ), {})
    assert states == ({"primitive_id": "P001", "state": "mixed", "mapping_refs": ("M1", "M2")},)


def test_primitive_resolver_preserves_cross_context_variation_and_ignores_exclusions() -> None:
    from destiny_personality.semantic_pipeline import resolve_primitive_states

    states = resolve_primitive_states((
        {"mapping_candidate_id": "M1", "primitive_id": "P001", "contexts": ["work"], "proposed_direction": {"state": "supported_high"}},
        {"mapping_candidate_id": "M2", "primitive_id": "P001", "contexts": ["relationship"], "proposed_direction": {"state": "supported_low"}},
        {"mapping_candidate_id": "M3", "primitive_id": "P001", "exclusion_matched": True, "proposed_direction": {"state": "supported_low"}},
    ), {})
    assert states[0]["state"] == "context_differentiated"
    assert states[0]["mapping_refs"] == ("M1", "M2")


def test_pipeline_distinguishes_zero_output_from_missing_policy() -> None:
    from destiny_personality.semantic_pipeline import build_semantic_core_from_approved_mapping

    core = build_semantic_core_from_approved_mapping(
        "profile:test",
        ({"mapping_candidate_id": "M1", "primitive_id": "P001", "proposed_direction": {"state": "supported_high"}},),
        {"signature": {"rules": []}},
    )
    assert core["stage_statuses"]["signature"] == "available_zero"
    assert core["stage_statuses"]["dynamic"] == "blocked_by_gate"


def test_mapping_eligibility_snapshot_exposes_hashable_authoritative_ids() -> None:
    from destiny_personality.semantic_authority import MappingEligibilitySnapshot

    snapshot = MappingEligibilitySnapshot(({"candidate_id": "SMC-1"},), "policy:test")
    assert snapshot.mechanism_ids == frozenset({"SMC-1"})
