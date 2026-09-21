# Phase 1.1 Calculation Contract Hardening Design

> Status: completed development-reference hardening. The resulting Python
> validation code remains useful for development and tests, but is not packaged
> as a required Skill runtime or calculation backend.

## 1. 目标

Phase 1.1 收紧 Phase 1 的确定性计算契约，解决八字派生事实没有可机械验证的柱位来源、`stable_only` 无法拦截已声明时柱来源的漏洞；同时补齐既有边界保护的回归测试，并将过大的编排服务拆成单职责纯校验模块。

本阶段不实现时区、真太阳时、八字或占星计算算法，不进入 Primitive、Mapping、Signature、Dynamic 或 Narrative，不引入项目外业务数据。

## 2. 方案选择

考虑过三种八字事实来源建模方式：

1. **最小柱位来源（采用）**：引入 `PillarPosition` 枚举；藏干直接使用枚举定位，十神和关系增加 `source_pillars`。它只描述“来自哪些柱”，足以执行时间敏感性边界。
2. **完整强类型事实引用**：同时枚举天干、地支、藏干、十神和关系成员。类型更强，但项目尚未提供所需本体与引用语法，实施会越过规则边界。
3. **保留自由字符串并用命名约定推断**：变更小，但依赖字符串前缀或语义解析，无法稳定验证，也会把未冻结语法暗中写入运行时。

采用方案 1，因为它是当前可验证目标所需的最小契约，不预支未来本体设计。

## 3. 八字来源契约

### 3.1 柱位枚举

```python
class PillarPosition(str, Enum):
    YEAR = "year"
    MONTH = "month"
    DAY = "day"
    HOUR = "hour"
```

`PillarPosition` 是结构来源标记，不表达旺衰、十神含义或关系解释。

### 3.2 派生事实

```python
@dataclass(frozen=True)
class HiddenStemsFact:
    pillar: PillarPosition
    stems: Tuple[str, ...]


@dataclass(frozen=True)
class TenGodFact:
    subject_ref: str
    ten_god: str
    source_pillars: Tuple[PillarPosition, ...]


@dataclass(frozen=True)
class BaziRelationFact:
    relation_type: str
    participant_refs: Tuple[str, ...]
    source_pillars: Tuple[PillarPosition, ...]
```

设计约束：

- `HiddenStemsFact.pillar` 从自由字符串改为 `PillarPosition`；
- 每个十神事实和关系事实必须显式声明非空 `source_pillars`；
- `source_pillars` 必须是 tuple，成员必须是精确的 `PillarPosition`，且不得重复；
- `subject_ref`、`participant_refs`、`ten_god`、`relation_type` 暂保留现有字符串契约，直到项目提供正式本体；
- 这是 `0.1.0` 预发布阶段的有意 API 收紧，不保留无来源声明的兼容构造方式。

### 3.3 `stable_only` 规则

当 `fact_mode` 为 `STABLE_ONLY` 时：

- `hour_pillar` 必须为 `None`；
- 任何 `HiddenStemsFact.pillar` 不得为 `HOUR`；
- 任何 `TenGodFact.source_pillars` 不得包含 `HOUR`；
- 任何 `BaziRelationFact.source_pillars` 不得包含 `HOUR`。

这一约束仅保证后端显式报告的来源不含时柱。来源声明是后端契约的权威输出；Phase 1.1 不尝试从自由字符串反推或校验命理语义。

## 4. 校验模块拆分

`ChartCalculationService` 仅保留三个后端的有序调用、异常转换、短路与最终聚合。纯校验转移到：

```text
src/destiny_personality/calculation/validation/
├── __init__.py
├── common.py      共享的契约错误、非空字符串、数值范围校验
├── input.py       BirthInput 与 RuntimeConfig 约束
├── time.py        NormalizedBirthTime 约束
├── bazi.py        BaziChartFacts 与来源约束
└── astrology.py   AstrologyChartFacts 约束
```

对外公开 API 保持 `ChartCalculationService.calculate(...)`。校验函数是包内实现细节，不从顶层 `calculation.__init__` 导出，不新增类层级或验证框架。

## 5. 测试补强

### 5.1 新行为的 TDD

先写并观察失败的测试，再实现：

- `PillarPosition` 的稳定 wire value 和顶层导出；
- 三种派生事实的来源类型、非空性、唯一性校验；
- `STABLE_ONLY` 对藏干、十神和关系时柱来源的拒绝；
- `TIME_SENSITIVE` 对合法时柱来源的接受。

### 5.2 既有防护的特征测试

补齐 Phase 1 已实现但测试证据不完整的边界：

- 重复 placement、aspect 和 dignity；
- 宫头宫位越界、重复、经度越界以及 12 宫不完整；
- 角点相位的配对类型、允许相位和 `angle_orb`；
- astrology 各 tuple 集合及嵌套对象的类型错误。

特征测试会通过一次局部、可恢复的守卫删除实验证明能抓住对应回归，恢复守卫后再运行全量测试。实验性修改不作为最终代码保留。

## 6. 打包验证入口

新增 `scripts/verify_package.py`，作为显式运行的发布前验证：

1. 在系统临时目录创建隔离工作区；
2. 通过 `python -m pip wheel . --wheel-dir <temp>/wheelhouse` 从当前项目构建项目 wheel 和运行时依赖 wheel；
3. 创建临时 venv，使用 `--no-index --find-links` 仅从临时 wheelhouse 安装该项目；
4. 验证安装后的 calculation 公共 API 可导入；
5. 对项目内 `destiny_personality_skill_docs_v2_2` 执行安装后的 `destiny-personality validate-config`。

脚本不删除项目文件，不全局安装包。它不加入默认 pytest，因为 PEP 517 隔离构建可能需要获取 `setuptools>=68`；如当前环境缺失构建依赖，运行前必须获得明确的网络授权。

## 7. 错误与兼容性

- 继续使用 `CALCULATION_CONTRACT_ERROR`，不新增错误码；
- 来源类型、空来源、重复来源与 `stable_only` 时柱泄漏都给出精确 `system="bazi"` 和字段路径；
- 异常转换、后端调用顺序、Fatal 短路以及聚合输出保持不变；
- 旧的 `HiddenStemsFact(pillar="...")` 以及未提供 `source_pillars` 的派生事实属于不合法后端输出，必须升级；
- 项目版本暂不变，版本策略留待可安装算法或稳定对外 API 出现后统一确定。

## 8. 验收标准

- 所有八字派生事实都具有可机械验证的已声明柱位来源；
- `STABLE_ONLY` 不能通过藏干、十神或关系事实夹带时柱来源；
- 既有 Phase 0/1 对外行为除明确的八字模型收紧外保持不变；
- `service.py` 只承担编排，各类契约校验在独立纯函数模块中可单测；
- 新增边界测试覆盖本规范列出的漏缺；
- 全量 pytest、源码模式的配置 CLI 和显式打包验证均成功；
- 无真实命盘算法、无推理规则、无外部业务数据进入 Phase 1.1。
