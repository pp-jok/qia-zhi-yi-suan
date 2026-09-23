from test_semantic_mechanism_contract import _candidate


def test_golden_sample_derived_mechanism_is_rejected() -> None:
    from destiny_personality.semantic_mechanisms import (
        validate_semantic_mechanism_candidate,
    )

    findings = validate_semantic_mechanism_candidate(
        _candidate(origin="golden_sample"), {"ER-TEST-001"}
    )

    assert {finding.code for finding in findings} == {
        "GOLDEN_SAMPLE_SEMANTIC_LEAK"
    }
