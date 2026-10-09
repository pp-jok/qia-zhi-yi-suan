import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
READINESS_PATH = ROOT / "docs" / "v0.6.0-product-readiness.md"


def skill_product_flow() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "destiny-personality" / "SKILL.md", ROOT / "README.md")
    )


def load_readiness_summary() -> dict:
    text = READINESS_PATH.read_text(encoding="utf-8")
    match = re.search(
        r"<!-- readiness-summary:start -->\s*```yaml\s*(.*?)\s*```\s*"
        r"<!-- readiness-summary:end -->",
        text,
        flags=re.DOTALL,
    )
    assert match, "missing machine-readable readiness summary"
    summary = yaml.safe_load(match.group(1))
    assert isinstance(summary, dict)
    return summary


def test_birth_input_uses_provider_or_returns_capability_gap() -> None:
    flow = skill_product_flow()

    required_steps = (
        "Normal users supply birth information only",
        "Discover an available calculation/qualification provider",
        "Invoke the provider with the normalized birth input",
        "return `CAPABILITY_GAP`",
    )
    assert all(step in flow for step in required_steps)
    assert flow.index(required_steps[0]) < flow.index(required_steps[1])
    assert flow.index(required_steps[1]) < flow.index(required_steps[2])
    assert flow.index(required_steps[1]) < flow.index(required_steps[3])
    assert "Do not ask the user for facts JSON" in flow
    assert "Do not free-form calculate" in flow


def test_v060_readiness_machine_summary_is_complete() -> None:
    summary = load_readiness_summary()

    assert summary["schema_version"] == "v0.6.0-product-readiness-v1"
    assert summary["release_version"] == "0.6.0"
    assert summary["release_ready"] is True
    assert summary["product_status"] == "internal_test_product"
    assert summary["workflow"] == {
        "normal_user_input": "birth_information_only",
        "provider_boundary": "calculation_and_qualification",
        "unavailable_provider_result": "CAPABILITY_GAP",
        "facts_json_interface": "internal_only",
        "free_form_calculation": "forbidden",
    }
    assert summary["compatibility"]["v0_5_strict_routes_retained"] is True
    assert summary["quality_gates"] == {
        "full_pytest": "pass",
        "wheel_build": "pass",
        "interpretive_assets_in_wheel": True,
        "ci_matrix_defined": True,
    }
