from pathlib import Path
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile


FORBIDDEN_WHEEL_SUFFIXES = (
    ".so", ".dylib", ".dll", ".pyd", ".ttf", ".otf", ".woff", ".woff2"
)


def run(command, *, cwd=None) -> None:
    subprocess.run([str(part) for part in command], cwd=cwd, check=True)


def _ignore_generated(_directory, names):
    ignored_names = {"build", "dist", ".pytest_cache", "__pycache__"}
    return [
        name
        for name in names
        if name in ignored_names
        or name.endswith(".egg-info")
        or name.endswith(".pyc")
    ]


def copy_project_source(project_root: Path, destination: Path) -> None:
    shutil.copytree(project_root, destination, ignore=_ignore_generated)


def project_distribution_name(project_root: Path) -> str:
    pyproject = (project_root / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^name\s*=\s*["\']([^"\']+)["\']\s*$', pyproject, re.MULTILINE)
    if match is None:
        raise RuntimeError("project distribution name is missing")
    return re.sub(r"[-.]+", "_", match.group(1))


def find_project_wheel(wheelhouse: Path, distribution_name: str) -> Path:
    distribution_name = re.sub(r"[-.]+", "_", distribution_name)
    project_wheels = tuple(
        wheelhouse.glob(f"{distribution_name}-*.whl")
    )
    if len(project_wheels) != 1:
        raise RuntimeError(
            f"expected one project wheel, found {len(project_wheels)}"
        )
    return project_wheels[0]


def assert_no_forbidden_wheel_members(wheel: Path) -> None:
    """Keep calculation engines, native binaries, and font assets out of the wheel."""

    with zipfile.ZipFile(wheel) as archive:
        members = tuple(name.lower() for name in archive.namelist())
    forbidden = tuple(
        name
        for name in members
        if name.endswith(FORBIDDEN_WHEEL_SUFFIXES) or "swisseph" in name
    )
    if forbidden:
        raise RuntimeError("forbidden bundled wheel members: " + ", ".join(forbidden))


def installed_release_smoke_script() -> str:
    return (
        "from datetime import date; from pathlib import Path; import json,tempfile; "
        "from destiny_personality.calculation import "
        "AstrologyChartFacts, BaziChartFacts, BaziPillar, DeterministicChartFacts, "
        "FactMode, NormalizedBirthTime, TimeBasis; "
        "from destiny_personality.core_destiny_profile import build_core_destiny_profile; "
        "from destiny_personality.deterministic_facts_codec import "
        "deterministic_facts_fingerprint,deterministic_facts_to_dict,load_qualified_deterministic_facts; "
        "from destiny_personality.release_manifest import load_release_manifest; "
        "from destiny_personality.release_renderer import render_release_report; "
        "from destiny_personality.report_planner import build_release_report_plan; "
        "pillar = BaziPillar('Jia', 'Zi'); "
        "facts = DeterministicChartFacts("
        "NormalizedBirthTime(date(2000,1,1),None,None,None,None,'UTC',False,"
        "TimeBasis.STANDARD_TIME,FactMode.STABLE_ONLY,('package_smoke',)),"
        "BaziChartFacts('bazi-core-v1.0',pillar,pillar,pillar,None,(),(),()),"
        "AstrologyChartFacts('western-tropical-v1.0',(),(),None,None,(),())); "
        "payload=deterministic_facts_to_dict(facts); "
        "payload.update({'schema_version':'deterministic-facts-v1','fact_mode':'stable_only',"
        "'methodology_versions':{'bazi':'bazi-core-v1.0','astrology':'western-tropical-v1.0'},"
        "'provenance_refs':['package-smoke'],'validation_summary':{'structure':'passed'}}); "
        "qualification={'schema_version':'fact-qualification-v1',"
        "'fact_fingerprint':deterministic_facts_fingerprint(facts),"
        "'qualification_status':'passed','derived_fact_assurance':'capability_reported',"
        "'fact_contract_version':'deterministic-facts-v1',"
        "'methodology_versions':{'bazi':'bazi-core-v1.0','astrology':'western-tropical-v1.0'},"
        "'validation_refs':['package-smoke'],'provenance_refs':['package-smoke'],"
        "'calculation_envelope_refs':['package-smoke'],"
        "'comparison':{'required':False,'status':'not_required'},"
        "'validation_summary':{'structure':'passed','methodology':'passed',"
        "'provenance':'passed','internal_consistency':'passed','time_scope':'passed',"
        "'calculation_config':'not_available'}}; "
        "root=Path(tempfile.mkdtemp()); facts_path=root/'facts.json'; qualification_path=root/'qualification.json'; "
        "facts_path.write_text(json.dumps(payload),encoding='utf-8'); "
        "qualification_path.write_text(json.dumps(qualification),encoding='utf-8'); "
        "qualified=load_qualified_deterministic_facts(facts_path,qualification_path); "
        "manifest = load_release_manifest(); "
        "profile = build_core_destiny_profile(qualified); "
        "assert profile.semantic_model_assurance == 'limited_coverage_unknown_only'; "
        "assert {item.state for item in profile.primitive_states.values()} == {'unknown'}; "
        "plan = build_release_report_plan(profile,'standard-portrait-v1'); "
        "report = render_release_report(profile,plan); "
        "assert report.report['primitive_interpretations'] == (); "
        "assert report.audit_refs"
    )


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    config_dir = project_root / "destiny_personality_skill_docs_v2_2"

    with tempfile.TemporaryDirectory(prefix="destiny-personality-package-") as raw:
        workspace = Path(raw)
        wheelhouse = workspace / "wheelhouse"
        wheelhouse.mkdir()
        source_copy = workspace / "source"
        copy_project_source(project_root, source_copy)

        run(
            [
                sys.executable,
                "-m",
                "pip",
                "wheel",
                ".",
                "--wheel-dir",
                wheelhouse,
            ],
            cwd=source_copy,
        )
        project_wheel = find_project_wheel(
            wheelhouse, project_distribution_name(source_copy)
        )
        assert_no_forbidden_wheel_members(project_wheel)

        venv_dir = workspace / "venv"
        run([sys.executable, "-m", "venv", venv_dir])
        bin_dir = venv_dir / ("Scripts" if os.name == "nt" else "bin")
        python = bin_dir / ("python.exe" if os.name == "nt" else "python")
        cli = bin_dir / (
            "destiny-personality-reference-validate.exe"
            if os.name == "nt"
            else "destiny-personality-reference-validate"
        )

        run(
            [
                python,
                "-m",
                "pip",
                "install",
                "--force-reinstall",
                "--no-index",
                "--find-links",
                wheelhouse,
                project_wheel,
            ]
        )
        run([python, "-c", installed_release_smoke_script()])
        run(
            [
                python,
                "-c",
                "from destiny_personality.calculation import "
                "BirthInput, ChartCalculationService, PillarPosition; "
                "from destiny_personality import "
                "load_astrology_dignity_table, load_astrology_node_policy, "
                "load_bazi_deterministic_tables, "
                "load_calculation_contract_bundle, "
                "load_canonical_fact_vocabulary, "
                "load_fact_comparison_policy; "
                "from destiny_personality.calculation_fingerprint import "
                "build_calculation_bundle_fingerprint; "
                "from destiny_personality.canonical_bazi_relations import "
                "load_canonical_bazi_relation_policy; "
                "from destiny_personality.release_manifest import "
                "load_release_manifest; "
                "load_canonical_bazi_relation_policy(); "
                "manifest = load_release_manifest(); "
                "assert len(manifest.core_primitives) == 6; "
                "assert all(item.resolver_capability == 'unknown' "
                "for item in manifest.core_primitives.values())",
            ]
        )
        run([cli, "validate-config", config_dir])
        calculation_check = subprocess.run(
            [
                cli,
                "validate-calculation-contracts",
                config_dir,
                "--runtime-config-dir",
                config_dir,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if (
            calculation_check.returncode != 2
            or calculation_check.stdout
            or "CONFIG_GAP | canonical_fact_vocabulary_v1.yaml"
            not in calculation_check.stderr
        ):
            raise RuntimeError(
                "installed calculation validator did not preserve the expected "
                "missing-candidate contract"
            )
        semantic_check = subprocess.run(
            [
                cli,
                "validate-semantic-contracts",
                config_dir,
                "--runtime-config-dir",
                config_dir,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if (
            semantic_check.returncode != 2
            or semantic_check.stdout
            or "CONFIG_GAP | primitive_ontology_v1.yaml"
            not in semantic_check.stderr
        ):
            raise RuntimeError(
                "installed semantic validator did not preserve the expected "
                "missing-candidate contract"
            )

    print("package verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
