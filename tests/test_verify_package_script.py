from pathlib import Path

from scripts.verify_package import copy_project_source, find_project_wheel, project_distribution_name


def test_copy_project_source_excludes_generated_artifacts(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    source_file = project_root / "src" / "example" / "module.py"
    source_file.parent.mkdir(parents=True)
    source_file.write_text("VALUE = 1\n", encoding="utf-8")
    (project_root / "pyproject.toml").write_text(
        "[build-system]\n", encoding="utf-8"
    )

    generated_paths = (
        project_root / "build" / "lib" / "module.py",
        project_root / "dist" / "example.whl",
        project_root / ".pytest_cache" / "README.md",
        project_root / "src" / "example.egg-info" / "SOURCES.txt",
        project_root / "src" / "example" / "__pycache__" / "module.pyc",
    )
    for path in generated_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("generated\n", encoding="utf-8")

    destination = tmp_path / "source-copy"
    copy_project_source(project_root, destination)

    assert (destination / "pyproject.toml").is_file()
    assert (destination / "src" / "example" / "module.py").is_file()
    for path in generated_paths:
        assert not (destination / path.relative_to(project_root)).exists()


def test_find_project_wheel_uses_project_distribution_name(
    tmp_path: Path,
) -> None:
    expected = tmp_path / "qia_zhi_yi_suan_candidate-0.3.5.whl"
    expected.touch()
    (tmp_path / "pyyaml-6.0.3.whl").touch()

    assert find_project_wheel(tmp_path, "qia-zhi-yi-suan-candidate") == expected


def test_project_distribution_name_reads_pyproject_and_normalizes_wheel_name(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "qia-zhi-yi-suan-candidate"\n', encoding="utf-8")

    assert project_distribution_name(tmp_path) == "qia_zhi_yi_suan_candidate"


def test_package_verifier_covers_calculation_contract_public_api_and_cli() -> None:
    script = (Path(__file__).resolve().parents[1] / "scripts" / "verify_package.py").read_text(
        encoding="utf-8"
    )
    for symbol in (
        "load_bazi_deterministic_tables",
        "load_astrology_dignity_table",
        "load_astrology_node_policy",
        "load_fact_comparison_policy",
        "load_calculation_contract_bundle",
        "build_calculation_bundle_fingerprint",
    ):
        assert symbol in script
    assert '"validate-calculation-contracts"' in script
    assert "CONFIG_GAP | canonical_fact_vocabulary_v1.yaml" in script
    assert '"--force-reinstall"' in script


def test_package_verifier_loads_the_packaged_release_manifest() -> None:
    script = (Path(__file__).resolve().parents[1] / "scripts" / "verify_package.py").read_text(
        encoding="utf-8"
    )

    assert "from destiny_personality.release_manifest import" in script
    assert "load_release_manifest" in script
    assert "release-primitive-coverage-v2" in script


def test_release_metadata_declares_version_readme_license_and_assets() -> None:
    root = Path(__file__).resolve().parents[1]
    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8")

    assert 'version = "0.5.0"' in pyproject
    assert 'readme = "README.md"' in pyproject
    assert 'license = {file = "LICENSE"}' in pyproject
    assert '"interpretive_assets/v1/*.yaml"' in pyproject
    assert '"release_assets/v1/*.yaml"' in pyproject


def test_package_verifier_runs_installed_formal_report_smoke_and_binary_audit() -> None:
    script = (Path(__file__).resolve().parents[1] / "scripts" / "verify_package.py").read_text(
        encoding="utf-8"
    )

    for symbol in (
        "build_core_destiny_profile",
        "build_release_report_plan",
        "render_release_report",
        "limited_coverage_unknown_only",
        "assert_no_forbidden_wheel_members",
        ".dylib",
        ".ttf",
        "swisseph",
    ):
        assert symbol in script


def test_release_documentation_and_notices_are_present() -> None:
    root = Path(__file__).resolve().parents[1]
    expected = {
        "README.md": (
            "0.5.0",
            "audited_interpretive",
            "standard-interpretive-v1",
            "concise-interpretive-v1",
            "high",
            "moderate",
            "exploratory",
            "insufficient",
            "出生时间缺失",
        ),
        "CHANGELOG.md": ("0.5.0", "audited_interpretive"),
        "THIRD_PARTY_NOTICES.md": ("PyYAML", "pytest", "Swiss Ephemeris"),
        "docs/architecture/autonomous-release-architecture.md": ("Facts", "Core Destiny Profile", "Report Plan"),
        "docs/release/v0.4.2-release-readiness.md": ("0.4.2", "unknown", "wheel"),
        "docs/reviews/archive/README.md": ("historical", "authoritative"),
    }
    for relative, phrases in expected.items():
        text = (root / relative).read_text(encoding="utf-8")
        for phrase in phrases:
            assert phrase in text
