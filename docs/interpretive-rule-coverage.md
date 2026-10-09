# v0.6.0 Interpretive Rule Coverage

## Scope and method

This matrix records the reports actually produced from the 12 qualification-bound
fixtures in `tests/fixtures/interpretive/v060`. Counts are extracted from the
standard reader report and from the matched signals; they are not estimates from
the rule YAML. A topic counts only when it becomes a reader-visible section.

## Topic × system matrix

| Reader topic | Bazi evidence family | Astrology evidence family |
| --- | --- | --- |
| 表达与创造 | 印星表达、食伤输出 | 太阳元素与模式 |
| 思考与学习 | — | 水星元素与模式 |
| 情绪与安全感 | — | 月亮元素与模式 |
| 关系与边界 | 地支关系 | 金星元素与模式 |
| 自主与协作 | 比劫 | — |
| 工作与驱动 | — | 火星元素与模式 |
| 资源与落实 | 财星 | — |
| 责任与压力 | 官杀 | — |
| 成长取向 | — | 木星元素与模式 |
| 边界与长期建设 | — | 土星元素与模式 |
| 生活重心 | — | 太阳宫位（需可用出生时间） |
| 成长张力 | — | 日月主要相位 |
| 表达条件 | — | 太阳先天尊贵 |
| 反复主题 | 同一十神复见 | — |

Across the suite every v3 rule family is exercised: all five Bazi ten-god
families, repetition, branch relations, all seven core-planet sign families,
Sun house, Sun–Moon major aspect, and Sun dignity. The dash means that the
current audited bundle has no rule for that exact system/topic pair; it is not
treated as negative evidence.

The sign-quality families share one bounded value-narrative registry covering
all four elements and all three modalities. Those matched values alter reader
conclusions, mechanisms, likely expressions, directions, and contexts rather
than only appearing in an evidence label.

## Fixture coverage

| Fixture | Reader topics | Bazi signals | Astrology signals | Product role |
| --- | ---: | ---: | ---: | --- |
| bazi-dominated | 7 | 7 | 2 | Five ten-god families, repetition and relation lead; Sun evidence remains visible. |
| astrology-dominated | 11 | 1 | 10 | Seven planets plus house, aspect and dignity lead; wealth evidence anchors Bazi. |
| cross-system-agreement | 10 | 1 | 10 | Food-god output and solar expression independently support the exact `style of expression` / `outward` relationship. |
| cross-system-tension | 11 | 3 | 10 | Reflective seal evidence and outward solar evidence form an explicit two-pole tension. |
| missing-time | 10 | 3 | 9 | Stable-only report omits the Sun-house signal and displays the omission boundary. |
| practical-builder | 12 | 4 | 10 | Wealth/authority, peer agency and earth-sign practical pacing make a delivery-focused but self-directed profile. |
| relational-connector | 11 | 2 | 10 | Peer and branch-relation evidence foreground collaboration and reciprocity. |
| expressive-creator | 10 | 2 | 10 | Food/hurting-officer output and fire-sign expression foreground making and showing. |
| structured-steward | 11 | 2 | 10 | Officer/killing and relation evidence foreground responsibility and structure. |
| reflective-scholar | 10 | 1 | 10 | Seal evidence and water-sign processing foreground absorption and reflection. |
| adaptive-explorer | 11 | 3 | 10 | Peer/output plus air/mutable evidence foreground autonomy and experimentation. |
| boundary-mentor | 12 | 3 | 10 | Authority, resource and relational evidence foreground standards with reciprocity. |

Every normal complete fixture has at least six reader topics and includes
traceable signals from both systems. The missing-time fixture is intentionally
excluded from the complete-chart gate but still carries both systems.
When more than 12 supported topics match, the final standard section merges
the overflow conclusions while retaining every signal and provenance record.
