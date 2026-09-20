from dataclasses import dataclass
from typing import Optional, Tuple

import yaml

from .calculation.models import BaziChartFacts, PillarPosition
from .candidate_assets import candidate_asset_root


@dataclass(frozen=True)
class DayMasterEnvironmentFact:
    day_master_stem: str
    day_master_element: str
    month_branch: str
    season: str
    source_pillars: Tuple[PillarPosition, ...]
    table_ref: str


def derive_candidate_day_master_environment(
    facts: BaziChartFacts,
) -> Optional[DayMasterEnvironmentFact]:
    """Derive only project-table day-stem and month-branch descriptors."""

    table = _load_candidate_environment_table()
    try:
        return DayMasterEnvironmentFact(
            day_master_stem=facts.day_pillar.heavenly_stem,
            day_master_element=table["stem_elements"][facts.day_pillar.heavenly_stem],
            month_branch=facts.month_pillar.earthly_branch,
            season=table["month_branch_seasons"][facts.month_pillar.earthly_branch],
            source_pillars=(PillarPosition.DAY, PillarPosition.MONTH),
            table_ref=table["table_version"],
        )
    except KeyError:
        return None


def _load_candidate_environment_table() -> dict:
    path = candidate_asset_root() / "bazi_day_master_environment_v1.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))
