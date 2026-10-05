from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REOPENED_PRIMITIVES = ("P001", "P002", "P003", "P005", "P006")
DEEP_CLOSURE = (
    "CLOSED_AFTER_DEEP_INDEPENDENT_RESEARCH_NO_EXECUTABLE_DIRECT_CONSTRUCT"
)


def _read(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def test_independent_source_corpora_are_auditable() -> None:
    bazi = _read("docs/reviews/semantic-content-bazi-source-corpus.md")
    astrology = _read("docs/reviews/semantic-content-hellenistic-source-corpus.md")

    for title in ("Yuanhai Ziping", "Ditian Sui", "Ziping Zhenquan", "Sanming Tonghui"):
        assert title in bazi
    for marker in ("authority", "access copy", "locator", "traditional_methodology"):
        assert marker in bazi.lower()
    for title in ("Tetrabiblos", "Valens", "Dorotheus"):
        assert title in astrology
    for marker in ("III.13", "authority", "locator", "not empirical"):
        assert marker.lower() in astrology.lower()


def test_every_reopened_primitive_has_deep_matrix_and_report() -> None:
    required_report_sections = (
        "Ontology boundary",
        "Bazi search",
        "Astrology search",
        "Method feasibility",
        "Canonical fact feasibility",
        "Evidence Root",
        "PRIMARY_EVIDENCE",
        "Mapping",
        "Counterevidence",
        "Saturation",
    )
    for primitive_id in REOPENED_PRIMITIVES:
        matrix = _read(f"docs/reviews/primitives/{primitive_id}-deep-construct-matrix.md")
        report = _read(f"docs/reviews/primitives/{primitive_id}-final-research-report.md")
        assert primitive_id in matrix
        assert "Bazi" in matrix
        assert "Astrology" in matrix
        assert "high" in matrix.lower()
        assert "low" in matrix.lower()
        assert "NO_EXECUTABLE_DIRECT_CONSTRUCT" in matrix
        for section in required_report_sections:
            assert section.lower() in report.lower()
        assert "PRIMARY_EVIDENCE: `0`" in report
        assert "Mapping: `0`" in report
        assert DEEP_CLOSURE in report


def test_packaged_v2_manifest_records_stronger_unknown_without_activation() -> None:
    path = (
        PROJECT_ROOT
        / "src/destiny_personality/release_assets/v1/primitive_coverage_v2.yaml"
    )
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))

    assert payload["schema_version"] == "release-primitive-coverage-v2"
    assert set(payload["core_primitives"]) == {
        "P001", "P002", "P003", "P004", "P005", "P006"
    }
    for primitive_id in REOPENED_PRIMITIVES:
        closure = payload["core_primitives"][primitive_id]
        assert closure["final_status"] == DEEP_CLOSURE
        assert closure["resolver_capability"] == "unknown"
        assert closure["primary_evidence_refs"] == []
        assert closure["mapping_refs"] == []
        assert (PROJECT_ROOT / closure["research_report_ref"]).is_file()

    p004 = payload["core_primitives"]["P004"]
    assert p004["final_status"] == "CLOSED_SYSTEM_SPECIFIC_RESEARCH"
    assert p004["system_closures"] == {
        "astrology": "CLOSED_UNDER_CURRENT_HELLENISTIC_METHODOLOGY",
        "bazi": "DEFERRED_WITH_REASON:METHOD_RESEARCH_SATURATED",
    }


def test_formal_release_remains_six_unknown_and_zero_mapping() -> None:
    from destiny_personality.release_manifest import load_release_manifest
    from destiny_personality.release_mapping_bundle import (
        load_active_release_mapping_bundle,
    )
    from destiny_personality.release_semantics import resolve_release_primitive_states

    manifest = load_release_manifest()
    bundle = load_active_release_mapping_bundle()
    states = resolve_release_primitive_states(bundle, manifest)

    assert set(states) == {"P001", "P002", "P003", "P004", "P005", "P006"}
    assert {state.state for state in states.values()} == {"unknown"}
    assert bundle.mappings == ()
    assert all(not closure.primary_evidence_refs for closure in manifest.core_primitives.values())
    assert all(not closure.mapping_refs for closure in manifest.core_primitives.values())
