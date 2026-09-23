def test_renderer_is_contained_by_report_plan_and_never_invents_sections() -> None:
    from destiny_personality.semantic_core import (
        build_report_plan,
        build_semantic_core_candidate,
        render_semantic_core_report,
    )

    core = build_semantic_core_candidate("profile-render", ())
    plan = build_report_plan(core, "dynamic-long-form-v1")
    report = render_semantic_core_report(core, plan)

    assert report.sections == ()
    assert report.containment_status == "profile_refs_only"
    assert report.claim_refs == ()


def test_cli_builds_and_renders_empty_semantic_core_report(tmp_path, capsys) -> None:
    from destiny_personality.cli import main
    from destiny_personality.semantic_core import build_semantic_core_candidate
    from destiny_personality.semantic_core_codec import write_semantic_core_candidate

    core_path = tmp_path / "core.json"
    write_semantic_core_candidate(build_semantic_core_candidate("profile-cli", ()), core_path)
    assert main(["build-report-plan", str(core_path), "standard-portrait-v1"]) == 0
    assert "profile_refs_only" in capsys.readouterr().out
    assert main(["render-report", str(core_path), "standard-portrait-v1"]) == 0
    assert "claim_refs" in capsys.readouterr().out
