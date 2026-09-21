from dataclasses import replace


def test_derives_day_master_environment_from_day_stem_and_month_branch(bazi_facts) -> None:
    from destiny_personality.day_master_environment import (
        derive_candidate_day_master_environment,
    )

    result = derive_candidate_day_master_environment(bazi_facts)

    assert result.day_master_stem == "庚"
    assert result.day_master_element == "metal"
    assert result.month_branch == "午"
    assert result.season == "summer"
    assert result.table_ref == "candidate-bazi-day-master-environment-v1"


def test_returns_no_environment_when_project_table_cannot_describe_the_chart(bazi_facts) -> None:
    from destiny_personality.calculation.models import BaziPillar
    from destiny_personality.day_master_environment import (
        derive_candidate_day_master_environment,
    )

    unmapped_facts = replace(
        bazi_facts,
        day_pillar=BaziPillar("未知", bazi_facts.day_pillar.earthly_branch),
    )

    assert derive_candidate_day_master_environment(unmapped_facts) is None
