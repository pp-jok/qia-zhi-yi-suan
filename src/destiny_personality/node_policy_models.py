from dataclasses import dataclass


@dataclass(frozen=True)
class AstrologyNodeOutputPolicy:
    included: bool
    phase: str
    aspect_participation: bool
    dignity_participation: bool
    weight_role: str
    time_sensitive: bool


@dataclass(frozen=True)
class AstrologyNodePolicyConfig:
    schema_version: str
    policy_version: str
    methodology_version: str
    vocabulary_version: str
    node_id: str
    output: AstrologyNodeOutputPolicy
