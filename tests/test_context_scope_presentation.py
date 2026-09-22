from dataclasses import replace

from destiny_personality.calculation import DeterministicChartFacts, TenGodFact, TenGodSourceKind
from destiny_personality.calculation.models import PillarPosition


def test_compound_context_scope_is_localized_without_internal_fallback(normalized_time, bazi_facts, astrology_facts) -> None:
    from destiny_personality.core_portrait import build_candidate_profile_summary, render_core_standard
    from destiny_personality.core_profile_builder import build_candidate_core_profile

    bazi = replace(
        bazi_facts,
        ten_gods=(
            TenGodFact("resource", "正印", (PillarPosition.YEAR,), TenGodSourceKind.VISIBLE_STEM),
            TenGodFact("authority", "正官", (PillarPosition.MONTH,), TenGodSourceKind.VISIBLE_STEM),
        ),
    )
    profile = build_candidate_core_profile(
        DeterministicChartFacts(normalized_time, bazi, astrology_facts), fact_assurance="capability_reported"
    )
    body = "\n".join(section.body for section in render_core_standard(build_candidate_profile_summary(profile)).sections)

    assert "压力情境" in body
    assert "工作与任务推进" in body
    assert "pressure+work" not in body
    assert "未命名情境" not in body
