def test_signature_and_dynamic_skeletons_remain_disabled() -> None:
    from destiny_personality.formation_skeletons import build_disabled_dynamic_result, build_disabled_signature_result

    signature = build_disabled_signature_result("candidate-test")
    dynamic = build_disabled_dynamic_result("candidate-test")

    assert signature.mode == "disabled" and signature.signatures == ()
    assert dynamic.mode == "disabled" and dynamic.dynamics == ()
