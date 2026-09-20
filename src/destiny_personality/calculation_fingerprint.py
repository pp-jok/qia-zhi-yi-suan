import hashlib
from pathlib import Path
from typing import Dict, Tuple

from .astrology_table_loader import FILE as ASTROLOGY_TABLE_FILE
from .bazi_table_loader import FILE as BAZI_TABLE_FILE
from .comparison_policy_loader import FILE as COMPARISON_POLICY_FILE
from .config_errors import ConfigError
from .config_loader import ASTROLOGY_FILE, BAZI_FILE, RELATION_FILE, SCORE_FILE
from .node_policy_loader import FILE as NODE_POLICY_FILE
from .vocabulary_loader import FILE as VOCABULARY_FILE


RUNTIME_FILES: Tuple[str, ...] = (
    BAZI_FILE,
    ASTROLOGY_FILE,
    SCORE_FILE,
    RELATION_FILE,
)
CANDIDATE_FILES: Tuple[str, ...] = (
    VOCABULARY_FILE,
    BAZI_TABLE_FILE,
    ASTROLOGY_TABLE_FILE,
    NODE_POLICY_FILE,
    COMPARISON_POLICY_FILE,
)


def _file_sha256(directory: Path, filename: str) -> str:
    path = directory / filename
    if not path.is_file():
        raise ConfigError(
            "CONFIG_GAP",
            "required configuration file is missing during fingerprinting",
            file=filename,
        )
    try:
        content = path.read_bytes()
    except OSError as exc:
        raise ConfigError(
            "CONFIG_PARSE_ERROR",
            "configuration file cannot be read during fingerprinting",
            file=filename,
        ) from exc
    return hashlib.sha256(content).hexdigest()


def build_calculation_bundle_fingerprint(
    candidate_dir: Path,
    runtime_config_dir: Path,
) -> Dict[str, object]:
    scoped_files = {}
    for directory, scope, filenames in (
        (Path(runtime_config_dir), "runtime", RUNTIME_FILES),
        (Path(candidate_dir), "candidate", CANDIDATE_FILES),
    ):
        for filename in filenames:
            scoped_files[f"{scope}/{filename}"] = _file_sha256(
                directory, filename
            )
    ordered_files = {key: scoped_files[key] for key in sorted(scoped_files)}
    canonical = "".join(
        f"{key}:{digest}\n" for key, digest in ordered_files.items()
    ).encode("utf-8")
    return {
        "algorithm": "sha256",
        "bundle_sha256": hashlib.sha256(canonical).hexdigest(),
        "files": ordered_files,
    }
