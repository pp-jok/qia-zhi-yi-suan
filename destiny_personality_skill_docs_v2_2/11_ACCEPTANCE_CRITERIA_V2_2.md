# 11 Acceptance Criteria V2.2

验收标准按阶段累积。完成 Phase B 只需满足 Phase B 标准，不得为了满足
后续发布标准而提前进入尚被 `CONFIG_GAP` 阻塞的语义开发。

状态：Phase B 已完成；Phase C external capability protocol is **complete and
verified on 2026-09-12**。这不表示 Gate 1 已通过、生产计算配置已完整，或任何
semantic phase 已完成。

## Phase B — Delivery Architecture
- Skill 是业务逻辑、执行编排和校验框架
- 实际工具调用由遵循 Skill 的智能体执行
- Skill 不打包第三方确定性计算软件
- Skill 不依赖项目 Python 参考验证器才能运行
- 已有能力优先；安装或连接新能力必须先获得用户授权
- `CONFIG_GAP` 与 `CAPABILITY_GAP` 可区分
- 未经授权不得读取无关本地项目或业务文件
- `SKILL.md` 能独立说明作用域、状态机、门禁和合法停止路径
- 首个失败门决定结果，fatal 后不得继续评估后续门

## Phase C — Deterministic Calculation Protocol
- 每个必需类别至少有一份 capability descriptor 后，才可通过发现门
- 每个适用方法设置都有 `exact` compatibility evidence 后，候选才可通过方法门
- 远程授权按 execution-scoped 管理，且发送字段最小化；不得在报告中复制 credentials
- 必需调用来自 qualified、authorized 候选，且每个 accepted operation 都有 envelope reference
- 历史时区与 DST 正确
- 八字/星盘事实确定性生成
- 方法版本固定
- time sensitivity 可执行
- 每份计算结果包含工具、版本、操作、关键参数和边界警告等 provenance
- 归一化仅允许机械转换，不得推导、修复或补造事实
- 每个 fact packet 独立通过契约校验，并在 tiered confirmation 触发时完成 mandatory comparison
- `audit` 只验证已提供证据，绝不调用、修复或推进阶段
- 外部结果归一化并通过契约校验后才可进入人格推理
- `CONFIG_GAP` 先于能力失败；无候选、授权拒绝后无替代、或强制独立候选不可用为 `CAPABILITY_GAP`
- 全部候选均缺少 exact 证据、冲突冻结方法或返回不同已验证方法版本为 `METHODOLOGY_VERSION_MISMATCH`
- 合格且已授权调用失败并耗尽安全候选后为 `CALCULATION_FATAL`
- 返回或归一化包违约为 `CALCULATION_CONTRACT_ERROR`；跨能力冲突子类型为 `external_result_conflict`

当前 exact deterministic lookup tables、True North Node rule、aliases、
boundary-distance margins 与 comparison tolerances 仍为 `CONFIG_GAP`，因此
不能将上述协议契约的存在误报为生产计算配置完整。

Gate 1A Primitive foundation contracts are implemented and verified on
2026-09-13. Gate 1 remains incomplete and Phase D remains incomplete。真实
Primitive Ontology、State Resolution 业务值及其余语义资产仍必须由项目提供。

Gate 1B Context-Aware Mapping Registry contracts are implemented and verified
on 2026-09-13. The real Mapping Registry values remain absent; Gate 1 remains
incomplete and Phase D remains incomplete.

Gate 1C Dimension Coverage Policy contract is implemented and verified on 2026-09-14.
The real dimension semantics and coverage thresholds remain absent; Gate 1 remains incomplete.

Gate 1D Narrative Rules and Semantic Contract Bundle are implemented and verified on 2026-09-14.
The real Narrative Rules remain absent; Gate 1 and downstream reasoning remain incomplete.

Canonical Fact Vocabulary contract is implemented and verified on 2026-09-14.
The production canonical vocabulary values remain absent. For the strict profile, CALCULATION_CONFIG_CHECKED remains closed. Exact lookup tables, the node rule, boundary margins, and comparison tolerances remain separate configuration gaps.

Calculation Config Framework contracts and aggregate validator are implemented and verified on 2026-09-14.
The production calculation values remain absent. For the strict profile, CALCULATION_CONFIG_CHECKED remains closed. Gate 1 remains incomplete, Phase D remains incomplete, and Phase E remains incomplete. Contract acceptance alone is not project-owner approval of a production fingerprint.

Controlled Inference business-test workflow is implemented and verified on 2026-09-14.
With a qualified external calculation capability, `portrait` may now generate an anchored, disclosed report under the controlled profile. This does not permit language-model chart calculation. Strict production remains blocked by project-owned assets.
The controlled report uses the long-form personality-book format: front matter, prologue, four parts, fifty-six chapter dimensions, finale, and audit appendix.
Each supported chapter must make at least three distinct analytical moves across evidence, mechanism, lived expression, and integration; repetition does not satisfy report depth.
User-approved reference interpretations may enrich controlled reports only as source-qualified supplemental interpretations; they do not override calculated facts, promote assurance, or satisfy strict gates.

## Phase D — Mapping
- Context-Aware Mapping 生效
- 不允许单结构无条件硬映射
- 不允许运行时新增主映射
- Mapping coverage 阈值与 partial-portrait 策略已版本化并冻结

## Phase D — Primitive
- 支持 supported_high / supported_low / mixed / unknown
- 无证据不得自动判 low

## Phase D — Score
- Trait Salience 与 Synthesis Priority 分离
- tension 不互相扣低
- cross-system validation 不直接放大 trait salience

## Phase D — Dynamic
- Relation Graph 参与候选生成
- Pole 有合法来源
- Selection Rule 可执行
- 去重生效

## Phase F — Evaluation and Release
- 未完成校准的阈值标记 provisional，但发布版本中的数值仍固定且不可临场更改
- 支持 ontology-aware similarity
- Golden 与 Production 隔离
- template collapse test 生效

## Phase E — Narrative
- 命盘锚点贯穿
- 不成为数据库 dump
- 不新增 IR 核心判断
- 保留神秘感与宿命张力

---

## Release Blockers

任一出现即停止发布：

- Skill 包含或隐式依赖第三方排盘、星历或历法软件
- Skill 必须依赖项目 Python 包才能执行
- 智能体静默安装软件或连接新服务
- 未取得本次执行针对具体远程接收方的授权即发送出生数据
- 执行报告复制原始敏感 payload 或 credentials
- 确定性事实无工具来源、版本或方法证明
- 外部工具输出未经归一化和校验即进入人格推理
- LLM 自由算盘
- LLM 自由发明 Mapping Rule
- 无证据自动判低
- validation 直接增加 trait salience
- tension 通过扣分被压平
- Dynamic 无 relation/source
- 生产读取 Golden expected
- 出生时间未知仍使用 Asc/House/时柱
- 所有用户趋同为少数人格模板
- Primitive Ontology、Mapping Registry 或 Narrative Rules 缺失却继续严格确定性画像
