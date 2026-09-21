from dataclasses import replace

import pytest

import destiny_personality
from destiny_personality.config_models import PrimitiveRelation, PrimitiveRelationGraphConfig
from destiny_personality.mapping_models import MappingRegistryBundle
from destiny_personality.narrative_models import NarrativeRulesConfig


def _narrative(foundation, dimensions):
    return NarrativeRulesConfig("narrative-rules-v1", "test-only-narrative-1", foundation.ontology.ontology_version, dimensions.policy_version, ("TEST_ONLY_CORE",), (), ())


def test_semantic_bundle_loads_components_in_gate_order(monkeypatch, tmp_path, runtime_config, primitive_foundation, dimension_policy):
    import destiny_personality.semantic_bundle as module

    calls = []
    mappings = MappingRegistryBundle(bazi=object(), astrology=object())
    narrative = _narrative(primitive_foundation, dimension_policy)
    monkeypatch.setattr(module, "load_primitive_foundation", lambda path: calls.append("primitive") or primitive_foundation)
    monkeypatch.setattr(module, "load_mapping_registries", lambda path, foundation, runtime: calls.append("mapping") or mappings)
    monkeypatch.setattr(module, "load_dimension_coverage_policy", lambda path, foundation, runtime: calls.append("dimension") or dimension_policy)
    monkeypatch.setattr(module, "load_narrative_rules", lambda path, foundation, dimensions: calls.append("narrative") or narrative)
    graph = PrimitiveRelationGraphConfig("test-only-graph", (PrimitiveRelation("P900", "P900", "reinforcing", None),))
    accepted_runtime = replace(runtime_config, relation_graph=graph)

    loader = getattr(destiny_personality, "load_semantic_contract_bundle", None)
    assert callable(loader), "public semantic contract bundle loader is missing"
    bundle = loader(tmp_path, accepted_runtime)

    assert calls == ["primitive", "mapping", "dimension", "narrative"]
    assert bundle.primitive_foundation is primitive_foundation
    assert bundle.narrative_rules is narrative


def test_unknown_relation_endpoint_is_value_error(monkeypatch, tmp_path, runtime_config, primitive_foundation, dimension_policy):
    import destiny_personality.semantic_bundle as module
    monkeypatch.setattr(module, "load_primitive_foundation", lambda path: primitive_foundation)
    monkeypatch.setattr(module, "load_mapping_registries", lambda *args: MappingRegistryBundle(object(), object()))
    monkeypatch.setattr(module, "load_dimension_coverage_policy", lambda *args: dimension_policy)
    monkeypatch.setattr(module, "load_narrative_rules", lambda *args: _narrative(primitive_foundation, dimension_policy))
    graph = PrimitiveRelationGraphConfig("test-only-graph", (PrimitiveRelation("P900", "P999", "reinforcing", None),))
    accepted_runtime = replace(runtime_config, relation_graph=graph)
    with pytest.raises(destiny_personality.ConfigError) as caught:
        destiny_personality.load_semantic_contract_bundle(tmp_path, accepted_runtime)
    assert (caught.value.code, caught.value.file, caught.value.field) == ("CONFIG_VALUE_ERROR", "primitive_relation_graph_v1.yaml", "relations.0.right")


def test_missing_primitive_asset_wins_before_later_assets(tmp_path, runtime_config):
    with pytest.raises(destiny_personality.ConfigError) as caught:
        destiny_personality.load_semantic_contract_bundle(tmp_path, runtime_config)
    assert (caught.value.code, caught.value.file) == ("CONFIG_GAP", "primitive_ontology_v1.yaml")
