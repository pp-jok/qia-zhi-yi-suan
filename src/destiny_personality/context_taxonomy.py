from dataclasses import dataclass

import yaml

from .candidate_assets import candidate_asset_root


@dataclass(frozen=True)
class CandidateContextTaxonomy:
    contexts: set[str]
    comparison_policy: dict[str, str]


def load_candidate_context_taxonomy() -> CandidateContextTaxonomy:
    path = candidate_asset_root() / "context_taxonomy_v1.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return CandidateContextTaxonomy(
        contexts=set(payload["contexts"]),
        comparison_policy=dict(payload["comparison_policy"]),
    )
