from test_semantic_mechanism_contract import _candidate


def test_material_legacy_equivalence_creates_review_warning() -> None:
    from destiny_personality.semantic_mechanisms import (
        validate_semantic_mechanism_candidate,
    )

    findings = validate_semantic_mechanism_candidate(
        _candidate(
            legacy_similarity={
                "same_source_conditions": True,
                "same_target_primitive": True,
                "same_direction": True,
            }
        ),
        {"ER-TEST-001"},
    )

    assert [(finding.code, finding.severity) for finding in findings] == [
        ("LEGACY_REINTRODUCTION_WARNING", "warning")
    ]
