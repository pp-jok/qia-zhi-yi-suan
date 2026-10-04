from pathlib import Path

import pytest
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CORE_IDS = {"P001", "P002", "P003", "P004", "P005", "P006"}


def test_every_core_primitive_has_terminal_lifecycle_state() -> None:
    from destiny_personality.release_manifest import load_release_manifest

    manifest = load_release_manifest()

    assert set(manifest.core_primitives) == EXPECTED_CORE_IDS
    assert all(
        item.final_status not in {"TODO", "TBD", "PENDING"}
        for item in manifest.core_primitives.values()
    )
    assert all(
        item.resolver_capability == "unknown"
        for item in manifest.core_primitives.values()
    )


def test_core_closures_explicitly_have_zero_active_evidence_and_mappings() -> None:
    from destiny_personality.release_manifest import load_release_manifest

    manifest = load_release_manifest()

    for closure in manifest.core_primitives.values():
        assert closure.primary_evidence_refs == ()
        assert closure.mapping_refs == ()


def test_p004_preserves_its_system_specific_closure_without_resolving_state() -> None:
    from destiny_personality.release_manifest import load_release_manifest

    p004 = load_release_manifest().core_primitives["P004"]

    assert p004.final_status == "CLOSED_SYSTEM_SPECIFIC_RESEARCH"
    assert p004.system_closures == {
        "astrology": "CLOSED_UNDER_CURRENT_HELLENISTIC_METHODOLOGY",
        "bazi": "DEFERRED_WITH_REASON:METHOD_RESEARCH_SATURATED",
    }
    assert p004.resolver_capability == "unknown"


def test_extended_inventory_is_explicitly_empty_and_deferred() -> None:
    from destiny_personality.release_manifest import load_release_manifest

    extended = load_release_manifest().extended_inventory

    assert extended.status == "EMPTY_DEFERRED"
    assert extended.primitive_ids == ()


def test_manifest_loader_fails_closed_for_malformed_coverage(tmp_path: Path) -> None:
    from destiny_personality.release_manifest import load_release_manifest

    malformed = tmp_path / "primitive_coverage_v1.yaml"
    malformed.write_text(
        "schema_version: release-primitive-coverage-v1\ncore_primitives: {}\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="RELEASE_MANIFEST_INVALID"):
        load_release_manifest(malformed)


@pytest.mark.parametrize(
    ("primitive_id", "field", "value"),
    (
        (
            "P001",
            "system_closures",
            {
                "bazi": "CLOSED_UNDER_CURRENT_HELLENISTIC_METHODOLOGY",
                "astrology": "NO_CURRENT_DEFENSIBLE_MAPPING",
            },
        ),
        ("P004", "final_status", "CLOSED_NO_DEFENSIBLE_CONSTRUCT_UNDER_REVIEWED_ASSETS"),
    ),
)
def test_manifest_loader_rejects_tampered_system_closure_semantics(
    tmp_path: Path, primitive_id: str, field: str, value: object
) -> None:
    from destiny_personality.release_manifest import (
        load_release_manifest,
        release_manifest_path,
    )

    payload = yaml.safe_load(release_manifest_path().read_text(encoding="utf-8"))
    payload["core_primitives"][primitive_id][field] = value
    tampered = tmp_path / "primitive_coverage_v1.yaml"
    tampered.write_text(yaml.safe_dump(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="RELEASE_MANIFEST_INVALID"):
        load_release_manifest(tampered)


def test_release_manifest_asset_is_declared_for_wheel_packaging() -> None:
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert '"release_assets/v1/*.yaml"' in pyproject
