from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from destiny_personality import load_runtime_config


def test_loads_frozen_v2_2_runtime_config(valid_config_dir: Path) -> None:
    config = load_runtime_config(valid_config_dir)

    assert config.bazi.methodology_version == "bazi-core-v1.0"
    assert config.bazi.calendar.day_boundary == "00:00"
    assert config.astrology.methodology_version == "western-tropical-v1.0"
    assert config.astrology.core.zodiac == "tropical"
    assert config.astrology.core.true_node is True
    assert config.score_model.score_model_version == "2.2"
    assert config.relation_graph.relation_graph_version == "1.0"
    assert len(config.relation_graph.relations) == 5
    with pytest.raises(FrozenInstanceError):
        config.bazi.methodology_version = "changed"
