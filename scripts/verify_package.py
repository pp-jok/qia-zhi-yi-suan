from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile


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


def find_project_wheel(wheelhouse: Path) -> Path:
    project_wheels = tuple(
        wheelhouse.glob("destiny_personality_reference_validator-*.whl")
    )
    if len(project_wheels) != 1:
        raise RuntimeError(
            f"expected one project wheel, found {len(project_wheels)}"
        )
    return project_wheels[0]


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
        project_wheel = find_project_wheel(wheelhouse)

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
                "--no-index",
                "--find-links",
                wheelhouse,
                project_wheel,
            ]
        )
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
                "build_calculation_bundle_fingerprint",
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
