from pathlib import Path
from shutil import copytree


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_ROOT = PROJECT_ROOT / "candidates" / "semantic-mechanisms-v1"


def test_candidate_mechanism_changes_do_not_change_active_semantic_fingerprint(
    tmp_path: Path,
) -> None:
    from destiny_personality.core_profile_builder import (
        candidate_semantic_bundle_fingerprint,
    )
    from destiny_personality.semantic_mechanisms import (
        build_semantic_mechanism_candidate_fingerprint,
    )

    copied_root = tmp_path / "semantic-mechanisms-v1"
    copytree(CONTRACT_ROOT, copied_root)
    before_active = candidate_semantic_bundle_fingerprint()
    before_candidate = build_semantic_mechanism_candidate_fingerprint(copied_root)
    candidate_dir = copied_root / "mechanism_candidates"
    candidate_dir.mkdir(exist_ok=True)
    (candidate_dir / "SMC-001.yaml").write_text(
        "candidate_id: SMC-001\nreview_status: proposed\n", encoding="utf-8"
    )

    assert candidate_semantic_bundle_fingerprint() == before_active
    assert build_semantic_mechanism_candidate_fingerprint(copied_root) != before_candidate
