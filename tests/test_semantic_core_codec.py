from pathlib import Path


def test_semantic_core_codec_round_trips_blocked_candidate(tmp_path: Path) -> None:
    from destiny_personality.semantic_core import build_semantic_core_candidate
    from destiny_personality.semantic_core_codec import load_semantic_core_candidate, write_semantic_core_candidate

    core = build_semantic_core_candidate("profile-codec", ())
    path = tmp_path / "core.json"
    write_semantic_core_candidate(core, path)

    assert load_semantic_core_candidate(path) == core
