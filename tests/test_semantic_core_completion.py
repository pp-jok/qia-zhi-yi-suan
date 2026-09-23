import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _approved_mapping_candidate(source_system: str = "bazi") -> dict:
    return {
        "mapping_candidate_id": "MC-TEST-001",
        "source_system": source_system,
        "canonical_fact_requirements": ["fact:test"],
        "semantic_mechanism_refs": ["SMC-APPROVED-001"],
        "primitive_id": "P004",
        "primitive_question": "When and how is concrete action started and advanced?",
        "proposed_direction": {"state": "test_only"},
        "contexts": ["TEST_ONLY"],
        "evidence_root_refs": ["ER-TEST-001"],
        "limitations": ["TEST_ONLY"],
        "legacy_similarity": {"material_equivalence": False},
        "audit_trail": ["audit:test"],
        "review_status": "approved",
    }


def test_mapping_v2_compiles_only_separately_approved_candidate() -> None:
    from destiny_personality.mapping_v2 import compile_mapping_v2_candidate_bundle

    bundle = compile_mapping_v2_candidate_bundle(
        (_approved_mapping_candidate(),),
        approved_mapping_eligible_ids=("SMC-APPROVED-001",),
    )

    assert bundle.status == "candidate_compiled"
    assert bundle.bazi_rules[0]["mapping_candidate_id"] == "MC-TEST-001"
    assert bundle.astrology_rules == ()


def test_mapping_v2_rejects_legacy_contamination_and_direct_fact_path() -> None:
    from destiny_personality.mapping_v2 import validate_mapping_candidate

    candidate = _approved_mapping_candidate()
    candidate["origin"] = "legacy_output"
    candidate["direct_fact_to_primitive"] = True

    findings = validate_mapping_candidate(candidate, ("SMC-APPROVED-001",))

    assert "MAPPING_CANDIDATE_PROHIBITED_ORIGIN" in findings
    assert "MAPPING_CANDIDATE_DIRECT_FACT_TO_PRIMITIVE_PROHIBITED" in findings


def test_semantic_core_source_view_and_explain_are_profile_contained() -> None:
    from destiny_personality.semantic_core import (
        build_semantic_core_candidate,
        explain_semantic_core_item,
        semantic_core_source_view,
    )

    core = build_semantic_core_candidate("profile-test", ())

    assert semantic_core_source_view(core, "mapping") == {
        "profile_ref": "profile-test",
        "stage": "mapping",
        "status": "blocked_by_gate",
        "item_count": 0,
        "containment_status": "profile_refs_only",
    }
    assert explain_semantic_core_item(core, "signature:unknown")["status"] == "not_found"


def test_semantic_core_review_packet_reports_engineering_and_semantic_readiness() -> None:
    from destiny_personality.semantic_core import build_semantic_core_review_packet

    packet = build_semantic_core_review_packet(
        approved_evidence_root_count=2,
        approved_mechanism_count=0,
        mapping_candidate_count=0,
        technical_checks=("PASS",),
    )

    assert packet["engineering_status"] == "ready_for_review"
    assert packet["semantic_readiness"] == "blocked_by_gate"
    assert packet["blockers"] == ("APPROVED_MAPPING_CANDIDATE_REQUIRED",)


def test_cli_exposes_core_source_view_diff_and_review_packet(tmp_path: Path, capsys) -> None:
    from destiny_personality.cli import main
    from destiny_personality.semantic_core import build_semantic_core_candidate
    from destiny_personality.semantic_core_codec import write_semantic_core_candidate

    core_path = tmp_path / "core.json"
    write_semantic_core_candidate(build_semantic_core_candidate("profile-test", ()), core_path)

    assert main(["semantic-core-source-view", str(core_path), "mapping"]) == 0
    assert json.loads(capsys.readouterr().out)["item_count"] == 0
    assert main(["semantic-core-diff", str(core_path), str(core_path)]) == 0
    assert json.loads(capsys.readouterr().out)["changed_categories"] == []
    assert main(["semantic-core-review-packet", str(PROJECT_ROOT)]) == 0
    assert json.loads(capsys.readouterr().out)["semantic_readiness"] == "blocked_by_gate"
    assert main(["validate-mapping-v2", str(PROJECT_ROOT)]) == 0
    assert json.loads(capsys.readouterr().out)["audit"]["candidate_count"] == 0
