from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
import yaml

import destiny_personality


FILE = "narrative_rules_v1.yaml"


def _data():
    return {
        "schema_version": "narrative-rules-v1",
        "narrative_version": "test-only-narrative-1",
        "ontology_version": "test-only-ontology-1",
        "dimension_policy_version": "test-only-policy-1",
        "sections": ["TEST_ONLY_CORE"],
        "invariants": {
            "complete_ir_required": True,
            "narrative_changes_core_claims": False,
            "unsupported_claims_allowed": False,
            "unknown_may_be_rendered_as_certain": False,
            "secondary_may_be_promoted": False,
            "chart_anchor_required": True,
            "traditional_interpretation_claimed_scientific": False,
        },
        "rules": [{
            "rule_id": "TEST_ONLY_NR1",
            "priority": 10,
            "target_section": "TEST_ONLY_CORE",
            "source_kinds": ["primitive", "core_dynamic"],
            "requires_chart_anchor": True,
            "rendering_constraints": {"test_only_mode": "TEST_ONLY_VALUE"},
            "prohibited_inferences": ["TEST_ONLY_PROHIBITION"],
            "limitations": [],
        }],
    }


@pytest.fixture
def narrative_dir(tmp_path):
    with (tmp_path / FILE).open("w", encoding="utf-8") as stream:
        yaml.safe_dump(_data(), stream, sort_keys=False)
    return tmp_path


def _rewrite(path, mutate):
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    mutate(data)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _error(path, foundation, dimensions, code, field=None):
    with pytest.raises(destiny_personality.ConfigError) as caught:
        destiny_personality.load_narrative_rules(path, foundation, dimensions)
    assert (caught.value.code, caught.value.file, caught.value.field) == (code, FILE, field)


def test_load_narrative_rules_returns_immutable_ordered_rules(narrative_dir, primitive_foundation, dimension_policy):
    loader = getattr(destiny_personality, "load_narrative_rules", None)
    assert callable(loader), "public Narrative Rules loader is missing"
    config = loader(narrative_dir, primitive_foundation, dimension_policy)
    assert config.sections == ("TEST_ONLY_CORE",)
    assert config.rules[0].source_kinds == ("primitive", "core_dynamic")
    assert config.rules[0].rendering_constraints == (("test_only_mode", "TEST_ONLY_VALUE"),)
    with pytest.raises(FrozenInstanceError):
        config.narrative_version = "changed"


def test_missing_narrative_is_gap(tmp_path, primitive_foundation, dimension_policy):
    _error(tmp_path, primitive_foundation, dimension_policy, "CONFIG_GAP")


@pytest.mark.parametrize(("field", "value"), (("schema_version", "v9"), ("ontology_version", "wrong"), ("dimension_policy_version", "wrong")))
def test_versions_match(narrative_dir, primitive_foundation, dimension_policy, field, value):
    _rewrite(narrative_dir / FILE, lambda d: d.__setitem__(field, value))
    _error(narrative_dir, primitive_foundation, dimension_policy, "CONFIG_VERSION_MISMATCH", field)


@pytest.mark.parametrize("invariant", tuple(_data()["invariants"]))
def test_invariants_are_exact(narrative_dir, primitive_foundation, dimension_policy, invariant):
    _rewrite(narrative_dir / FILE, lambda d: d["invariants"].__setitem__(invariant, not d["invariants"][invariant]))
    _error(narrative_dir, primitive_foundation, dimension_policy, "CONFIG_VALUE_ERROR", f"invariants.{invariant}")


@pytest.mark.parametrize(("mutation", "field"), (("unknown_source", "rules.0.source_kinds.0"), ("duplicate_source", "rules.0.source_kinds.1"), ("unknown_section", "rules.0.target_section"), ("no_anchor", "rules.0.requires_chart_anchor"), ("empty_constraints", "rules.0.rendering_constraints"), ("empty_prohibitions", "rules.0.prohibited_inferences")))
def test_rule_guards(narrative_dir, primitive_foundation, dimension_policy, mutation, field):
    def mutate(d):
        rule = d["rules"][0]
        if mutation == "unknown_source": rule["source_kinds"][0] = "claim"
        elif mutation == "duplicate_source": rule["source_kinds"][1] = "primitive"
        elif mutation == "unknown_section": rule["target_section"] = "MISSING"
        elif mutation == "no_anchor": rule["requires_chart_anchor"] = False
        elif mutation == "empty_constraints": rule["rendering_constraints"] = {}
        else: rule["prohibited_inferences"] = []
    _rewrite(narrative_dir / FILE, mutate)
    _error(narrative_dir, primitive_foundation, dimension_policy, "CONFIG_VALUE_ERROR", field)
