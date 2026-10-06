from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_p006_pilot_records_zero_activation_exit() -> None:
    matrix = (ROOT / "docs/reviews/p006-semantic-bridge-pilot-matrix.md").read_text(
        encoding="utf-8"
    )
    report = (
        ROOT / "docs/reviews/p006-semantic-bridge-pilot-final-report.md"
    ).read_text(encoding="utf-8")

    for candidate in (
        "布置有方",
        "处事有方",
        "治事无规",
        "systematic workers",
        "able to direct business",
        "prone to change their minds",
    ):
        assert candidate in matrix
    assert "P006_BEHAVIORAL_BRIDGE_FAIL_CAPABILITY_OR_TEMPERAMENT_ONLY" in report
    assert "Primary Evidence: `0`" in report
    assert "Active Mapping: `0`" in report
    assert "Formal P006 state: `unknown`" in report


def test_ontology_v3_pilot_is_candidate_only_and_does_not_replace_v2() -> None:
    v2_path = ROOT / "candidates/core-profile-v2/primitive_ontology_v2.yaml"
    v3_path = ROOT / "candidates/core-profile-v3/primitive_ontology_v3.yaml"
    v2 = yaml.safe_load(v2_path.read_text(encoding="utf-8"))
    v3 = yaml.safe_load(v3_path.read_text(encoding="utf-8"))

    assert v2["schema_version"] == "candidate-primitive-ontology-v2"
    assert v3["schema_version"] == "candidate-primitive-ontology-v3"
    assert v3["activation"] == "candidate_only"
    assert v3["runtime_eligible"] is False
    assert v3["replaces"] is None
    assert [item["primitive_id"] for item in v3["primitives"]] == ["TP001"]
    assert v3["primitives"][0]["canonical_name"] == "Task Continuity Process"


def test_ontology_review_declares_systematic_mismatch_and_migration_boundary() -> None:
    review = (
        ROOT / "docs/reviews/core-primitive-ontology-compatibility-review.md"
    ).read_text(encoding="utf-8")
    pilot = (
        ROOT / "docs/reviews/primitive-ontology-v3-task-continuity-pilot.md"
    ).read_text(encoding="utf-8")

    assert "SYSTEMATIC_MISMATCH" in review
    assert "evidence-discovered ontology" in review
    assert "does not replace v2" in pilot
    assert "method-blocked" in pilot
    assert "runtime activation: prohibited" in pilot


def test_final_summary_records_zero_activation_release_classification() -> None:
    summary = yaml.safe_load(
        (
            ROOT
            / "docs/reviews/semantic-bridge-governance-final-summary.yaml"
        ).read_text(encoding="utf-8")
    )

    assert summary["schema_version"] == "semantic-bridge-governance-final-v1"
    assert summary["single_direction_evidence"]["supported"] is True
    assert summary["p006"]["primary_evidence_count"] == 0
    assert summary["p006"]["active_mapping_count"] == 0
    assert summary["p006"]["formal_state"] == "unknown"
    assert summary["formal_non_unknown_primitive_count"] == 0
    assert summary["release"]["version"] == "0.4.2"
    assert summary["release"]["classification"].endswith("NO_FORMAL_ACTIVATION")
