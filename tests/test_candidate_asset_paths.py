def test_candidate_asset_root_falls_back_to_package_data_when_not_checked_out(
    monkeypatch, tmp_path
) -> None:
    from destiny_personality import candidate_assets

    installed_module = tmp_path / "site-packages" / "destiny_personality" / "candidate_assets.py"
    packaged_assets = installed_module.parent / "candidate_assets" / "core-profile-v1"
    packaged_assets.mkdir(parents=True)
    monkeypatch.setattr(candidate_assets, "__file__", str(installed_module))

    assert candidate_assets.candidate_asset_root() == packaged_assets
