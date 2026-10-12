# v0.7.0 产品链路差距分析

## 结论

v0.6.0 的解释与报告层可以消费已资格校验的确定性事实，但它不是一个可由普通出生信息直接运行的产品。`CAPABILITY_GAP` 是当前设计的预期结果，不是偶发部署缺陷。

## 可复核证据

| 链路环节 | 当前实现 | 结果 |
| --- | --- | --- |
| 用户入口 | CLI 只有 `build-interpretive-report FACTS.json --qualification ...` | 无出生信息入口 |
| 计算契约 | `ChartCalculationService` 仅依赖 `TimeNormalizer`、Bazi、Astrology 三个 Protocol | 有边界，没有实现 |
| 运行依赖 | `pyproject.toml` 仅声明 PyYAML | 没有历法、天文或时区计算依赖 |
| Skill 边界 | `execution-boundaries.md` 明确排除 calculator、adapter、runtime 与固定 provider dependency | 特意把关键能力移出产品 |
| 失败策略 | `capability-protocol.md` 要求无合格候选时返回 `CAPABILITY_GAP` | 正常输入必然止步 |
| 资格校验 | facts codec 能绑定指纹、方法版本和资格记录 | 有可复用的正确后段 |

因此，问题不是“让模型补一次排盘”，而是把实际、可追溯的计算能力接入现有事实资格与解释链。

## 根因

早期设计将 Skill 定义为外部能力的编排和审计框架；v0.6 将该框架包装为面向普通用户的产品流程，但没有同时交付可用的本地或已授权远程能力、能力发现实现、出生信息 CLI，或产生资格记录的实现。这使“普通用户只提供出生信息”的文案与可运行边界不一致。

## v0.7 决策

采用本地、确定性、可安装的 provider：

- 八字：`lunar_python==1.4.8`（MIT），提供节气边界的四柱与十神基础数据。
- 西占天文底座：`astronomy-engine==2.1.19`（MIT），提供地心热带黄道经度和恒星时；项目用明确版本的整宫制计算房位、角点、相位及尊贵度。
- 不采用 Swiss Ephemeris/pyswisseph：其 AGPL/商业双许可与本项目 MIT 发布基线不相容，不能在没有购买商业许可或整体改为兼容许可的情况下静默引入。

西占方法随实现升级为 `western-tropical-whole-sign-v1.0`。这是一个显式方法变更，不把整宫制结果伪称为 Placidus；旧的 facts/report 输入仍按其自身方法版本可读，新的出生信息入口只生成新版本事实。

## v0.7 验收口径

用户输入 `1992-07-14 15:30，上海，女` 能在干净环境中完成：规范化、实际本地计算、结构/方法/时间范围校验、产生指纹绑定资格记录、生成标准解释报告和审计工件。任何依赖缺失、地点未知、时间无效或提供者失败都应给出明确错误，不能退化为模型猜测或伪造资格通过。
