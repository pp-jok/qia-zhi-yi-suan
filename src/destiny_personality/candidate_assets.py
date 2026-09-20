from pathlib import Path


def candidate_asset_root() -> Path:
    """Resolve checked-out assets first, then package-bundled release assets."""

    source_root = Path(__file__).resolve().parents[2] / "candidates" / "core-profile-v1"
    if source_root.is_dir():
        return source_root
    return Path(__file__).resolve().parent / "candidate_assets" / "core-profile-v1"
