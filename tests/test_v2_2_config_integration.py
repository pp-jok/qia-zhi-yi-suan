import json
from pathlib import Path

from destiny_personality import load_runtime_config


def test_project_v2_2_configuration_is_loadable() -> None:
    project_root = Path(__file__).resolve().parents[1]
    config_dir = project_root / "destiny_personality_skill_docs_v2_2"

    config = load_runtime_config(config_dir)

    assert config.bazi.methodology_version == "bazi-core-v1.0"
    assert config.astrology.methodology_version == "western-tropical-v1.0"
    assert config.score_model.score_model_version == "2.2"
    assert config.relation_graph.relation_graph_version == "1.0"
    assert len(config.relation_graph.relations) == 5


def test_manifest_declares_agent_orchestrated_skill_architecture() -> None:
    project_root = Path(__file__).resolve().parents[1]
    docs_dir = project_root / "destiny_personality_skill_docs_v2_2"
    manifest = json.loads((docs_dir / "manifest.json").read_text(encoding="utf-8"))

    assert manifest["delivery_model"] == "agent-orchestrated-skill"
    assert "12_SKILL_EXECUTION_ARCHITECTURE_V2_2.md" in manifest["documents"]
    assert all((docs_dir / filename).is_file() for filename in manifest["documents"])


def test_manifest_points_to_phase_b_skill_artifact() -> None:
    project_root = Path(__file__).resolve().parents[1]
    docs_dir = project_root / "destiny_personality_skill_docs_v2_2"
    manifest = json.loads((docs_dir / "manifest.json").read_text(encoding="utf-8"))

    assert manifest["skill_artifact"] == "../destiny-personality"
    assert manifest["phase_b_status"] == "implemented"
    assert (docs_dir / manifest["skill_artifact"] / "SKILL.md").is_file()


def test_manifest_declares_verified_phase_c_protocol() -> None:
    project_root = Path(__file__).resolve().parents[1]
    docs_dir = project_root / "destiny_personality_skill_docs_v2_2"
    manifest = json.loads((docs_dir / "manifest.json").read_text(encoding="utf-8"))

    assert manifest["phase_c_status"] == "implemented"
    assert manifest["skill_artifact"] == "../destiny-personality"


def test_phase_c_release_status_is_consistent_across_source_documents() -> None:
    project_root = Path(__file__).resolve().parents[1]
    docs_dir = project_root / "destiny_personality_skill_docs_v2_2"
    paths = (
        docs_dir / "11_ACCEPTANCE_CRITERIA_V2_2.md",
        docs_dir / "12_SKILL_EXECUTION_ARCHITECTURE_V2_2.md",
    )

    for path in paths:
        normalized = " ".join(path.read_text(encoding="utf-8").split())
        assert "Phase C" in normalized
        assert "complete and verified on 2026-09-12" in normalized
        assert "awaiting final release verification" not in normalized
        assert "Gate 1" in normalized
        assert "semantic" in normalized.lower()


def test_gate_1a_status_is_consistent_across_source_documents() -> None:
    project_root = Path(__file__).resolve().parents[1]
    docs_dir = project_root / "destiny_personality_skill_docs_v2_2"
    paths = (
        docs_dir / "00_README_V2_2.md",
        docs_dir / "10_CODEX_IMPLEMENTATION_PLAN_V2_2.md",
        docs_dir / "11_ACCEPTANCE_CRITERIA_V2_2.md",
        docs_dir / "12_SKILL_EXECUTION_ARCHITECTURE_V2_2.md",
    )

    for path in paths:
        normalized = " ".join(path.read_text(encoding="utf-8").split())
        assert "Gate 1A Primitive foundation contracts are implemented" in normalized
        assert "Gate 1 remains incomplete" in normalized
        assert "Phase D remains incomplete" in normalized


def test_manifest_declares_verified_gate_1a_contracts() -> None:
    project_root = Path(__file__).resolve().parents[1]
    docs_dir = project_root / "destiny_personality_skill_docs_v2_2"
    manifest = json.loads((docs_dir / "manifest.json").read_text(encoding="utf-8"))

    assert manifest["gate_1a_status"] == "implemented"
    assert manifest["phase_c_status"] == "implemented"
    for filename in (
        "00_README_V2_2.md",
        "10_CODEX_IMPLEMENTATION_PLAN_V2_2.md",
        "11_ACCEPTANCE_CRITERIA_V2_2.md",
        "12_SKILL_EXECUTION_ARCHITECTURE_V2_2.md",
    ):
        normalized = " ".join((docs_dir / filename).read_text(encoding="utf-8").split())
        assert "implemented and verified on 2026-09-13" in normalized
        assert "final verification is pending" not in normalized


def test_gate_1a_authoritative_docs_include_reverse_evidence_marker() -> None:
    project_root = Path(__file__).resolve().parents[1]
    paths = (
        project_root
        / "docs/superpowers/specs/2026-09-13-gate-1a-primitive-foundation-contracts-design.md",
        project_root
        / "docs/superpowers/plans/2026-09-13-gate-1a-primitive-foundation-contracts.md",
    )

    for path in paths:
        normalized = " ".join(path.read_text(encoding="utf-8").split())
        assert "requires_explicit_reverse_evidence" in normalized
        assert "must be `true` for every `supported_low` rule" in normalized


def test_gate_1b_status_is_consistent_across_source_documents() -> None:
    project_root = Path(__file__).resolve().parents[1]
    docs_dir = project_root / "destiny_personality_skill_docs_v2_2"
    paths = (
        docs_dir / "00_README_V2_2.md",
        docs_dir / "10_CODEX_IMPLEMENTATION_PLAN_V2_2.md",
        docs_dir / "11_ACCEPTANCE_CRITERIA_V2_2.md",
        docs_dir / "12_SKILL_EXECUTION_ARCHITECTURE_V2_2.md",
    )

    for path in paths:
        normalized = " ".join(path.read_text(encoding="utf-8").split())
        assert (
            "Gate 1B Context-Aware Mapping Registry contracts are implemented "
            "and verified on 2026-09-13."
        ) in normalized
        assert "real Mapping Registry values remain absent" in normalized
        assert "Gate 1 remains incomplete" in normalized
        assert "Phase D remains incomplete" in normalized


def test_manifest_declares_verified_gate_1b_contracts() -> None:
    project_root = Path(__file__).resolve().parents[1]
    docs_dir = project_root / "destiny_personality_skill_docs_v2_2"
    manifest = json.loads((docs_dir / "manifest.json").read_text(encoding="utf-8"))

    assert manifest["gate_1b_status"] == "implemented"
    assert manifest["gate_1a_status"] == "implemented"
    assert "bazi_mapping_registry_v1.yaml" not in manifest["documents"]
    assert "astrology_mapping_registry_v1.yaml" not in manifest["documents"]


def test_gate_1c_status_is_consistent_across_source_documents() -> None:
    project_root = Path(__file__).resolve().parents[1]
    docs_dir = project_root / "destiny_personality_skill_docs_v2_2"
    for filename in ("00_README_V2_2.md", "10_CODEX_IMPLEMENTATION_PLAN_V2_2.md", "11_ACCEPTANCE_CRITERIA_V2_2.md", "12_SKILL_EXECUTION_ARCHITECTURE_V2_2.md"):
        normalized = " ".join((docs_dir / filename).read_text(encoding="utf-8").split())
        assert "Gate 1C Dimension Coverage Policy contract is implemented and verified on 2026-09-14." in normalized
        assert "real dimension semantics and coverage thresholds remain absent" in normalized
        assert "Gate 1 remains incomplete" in normalized


def test_manifest_declares_verified_gate_1c_contract() -> None:
    project_root = Path(__file__).resolve().parents[1]
    docs_dir = project_root / "destiny_personality_skill_docs_v2_2"
    manifest = json.loads((docs_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["gate_1c_status"] == "implemented"
    assert "dimension_coverage_policy_v1.yaml" not in manifest["documents"]


def test_gate_1d_status_and_missing_values_are_consistent() -> None:
    project_root = Path(__file__).resolve().parents[1]
    docs_dir = project_root / "destiny_personality_skill_docs_v2_2"
    phrase = "Gate 1D Narrative Rules and Semantic Contract Bundle are implemented and verified on 2026-09-14."
    for filename in ("00_README_V2_2.md", "10_CODEX_IMPLEMENTATION_PLAN_V2_2.md", "11_ACCEPTANCE_CRITERIA_V2_2.md", "12_SKILL_EXECUTION_ARCHITECTURE_V2_2.md"):
        text = " ".join((docs_dir / filename).read_text(encoding="utf-8").split())
        assert phrase in text
        assert "real Narrative Rules remain absent" in text
    manifest = json.loads((docs_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["gate_1d_status"] == "implemented"
    assert "narrative_rules_v1.yaml" not in manifest["documents"]


def test_calculation_vocabulary_contract_status_is_consistent() -> None:
    project_root = Path(__file__).resolve().parents[1]
    docs_dir = project_root / "destiny_personality_skill_docs_v2_2"
    phrase = "Canonical Fact Vocabulary contract is implemented and verified on 2026-09-14."
    for filename in (
        "00_README_V2_2.md",
        "10_CODEX_IMPLEMENTATION_PLAN_V2_2.md",
        "11_ACCEPTANCE_CRITERIA_V2_2.md",
        "12_SKILL_EXECUTION_ARCHITECTURE_V2_2.md",
    ):
        text = " ".join((docs_dir / filename).read_text(encoding="utf-8").split())
        assert phrase in text
        assert "production canonical vocabulary values remain absent" in text
        assert "CALCULATION_CONFIG_CHECKED remains closed" in text

    manifest = json.loads((docs_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["calculation_vocabulary_contract_status"] == "implemented"
    assert "canonical_fact_vocabulary_v1.yaml" not in manifest["documents"]


def test_calculation_framework_contract_status_is_consistent() -> None:
    project_root = Path(__file__).resolve().parents[1]
    docs_dir = project_root / "destiny_personality_skill_docs_v2_2"
    phrase = (
        "Calculation Config Framework contracts and aggregate validator are "
        "implemented and verified on 2026-09-14."
    )
    production_assets = (
        "canonical_fact_vocabulary_v1.yaml",
        "bazi_deterministic_tables_v1.yaml",
        "astrology_dignity_table_v1.yaml",
        "astrology_node_policy_v1.yaml",
        "fact_comparison_policy_v1.yaml",
    )
    for filename in (
        "00_README_V2_2.md",
        "10_CODEX_IMPLEMENTATION_PLAN_V2_2.md",
        "11_ACCEPTANCE_CRITERIA_V2_2.md",
        "12_SKILL_EXECUTION_ARCHITECTURE_V2_2.md",
    ):
        text = " ".join((docs_dir / filename).read_text(encoding="utf-8").split())
        assert phrase in text
        assert "production calculation values remain absent" in text
        assert "CALCULATION_CONFIG_CHECKED remains closed" in text
        assert "Phase D remains incomplete" in text
        assert "Phase E remains incomplete" in text

    manifest = json.loads((docs_dir / "manifest.json").read_text(encoding="utf-8"))
    for status in (
        "calculation_bazi_tables_contract_status",
        "calculation_astrology_dignity_contract_status",
        "calculation_node_policy_contract_status",
        "calculation_comparison_policy_contract_status",
        "calculation_bundle_status",
    ):
        assert manifest[status] == "implemented"
    assert all(asset not in manifest["documents"] for asset in production_assets)


def test_controlled_inference_business_test_status_is_consistent() -> None:
    project_root = Path(__file__).resolve().parents[1]
    docs_dir = project_root / "destiny_personality_skill_docs_v2_2"
    implemented = (
        "Controlled Inference business-test workflow is implemented and "
        "verified on 2026-09-14."
    )
    strict_block = "Strict production remains blocked by project-owned assets."
    for filename in (
        "00_README_V2_2.md",
        "10_CODEX_IMPLEMENTATION_PLAN_V2_2.md",
        "11_ACCEPTANCE_CRITERIA_V2_2.md",
        "12_SKILL_EXECUTION_ARCHITECTURE_V2_2.md",
    ):
        text = " ".join((docs_dir / filename).read_text(encoding="utf-8").split())
        assert implemented in text
        assert strict_block in text
        assert "qualified external calculation capability" in text
        assert "does not permit language-model chart calculation" in text
        assert (
            "The controlled report uses the long-form personality-book format: "
            "front matter, prologue, four parts, fifty-six chapter dimensions, "
            "finale, and audit appendix."
            in text
        )
        assert (
            "User-approved reference interpretations may enrich controlled "
            "reports only as source-qualified supplemental interpretations; "
            "they do not override calculated facts, promote assurance, or "
            "satisfy strict gates."
            in text
        )
        assert (
            "For the strict profile, CALCULATION_CONFIG_CHECKED remains closed"
            in text
        )

    acceptance = (
        docs_dir / "11_ACCEPTANCE_CRITERIA_V2_2.md"
    ).read_text(encoding="utf-8")
    assert "缺失却继续严格确定性画像" in acceptance

    manifest = json.loads((docs_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["controlled_inference_status"] == "implemented"
    assert manifest["business_test_workflow_status"] == "ready"
    assert manifest["strict_production_status"] == "blocked_by_project_assets"


def test_business_test_status_does_not_promote_missing_production_assets() -> None:
    project_root = Path(__file__).resolve().parents[1]
    skill_configs = project_root / "destiny-personality" / "configs"
    assert {path.name for path in skill_configs.iterdir()} == {
        "astrology_methodology_v1.yaml",
        "bazi_methodology_v1.yaml",
        "primitive_relation_graph_v1.yaml",
        "score_model_v2_2.yaml",
    }
