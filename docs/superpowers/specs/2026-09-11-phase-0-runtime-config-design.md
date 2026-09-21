# Phase 0 Runtime Configuration Design

> Status: completed development-reference design. Under the confirmed V2.2
> delivery architecture, this Python module is a reference validator, not a
> required Skill runtime. The current roadmap is
> `destiny_personality_skill_docs_v2_2/10_CODEX_IMPLEMENTATION_PLAN_V2_2.md`.

## 1. 目标

为八字 × 西方占星核心画像 Skill V2.2 建立首个可运行、可测试的 Python 基础模块。该模块只负责加载和校验已经冻结的四份运行时配置，为后续确定性命盘计算与推理阶段提供不可变、类型明确的配置对象。

Phase 0 不解释命理或占星含义，不执行人格推理，也不补造文档中尚未提供的规则。

## 2. 范围

本阶段读取以下固定文件名：

- `bazi_methodology_v1.yaml`
- `astrology_methodology_v1.yaml`
- `score_model_v2_2.yaml`
- `primitive_relation_graph_v1.yaml`

本阶段交付：

- Python 3.9+ 的 `src` 包结构；
- 四类配置的不可变 dataclass；
- YAML 安全加载；
- 单文件结构和语义校验；
- 必要的跨配置一致性校验；
- 统一且可机器识别的配置错误；
- `validate-config` 命令行入口；
- 单元测试与当前 V2.2 配置的集成测试。

本阶段明确不包含：

- 历史时区、DST、真太阳时或命盘计算；
- Primitive Ontology 与 Primitive 状态解析；
- Context-Aware Mapping Registry 与 Interaction Rules；
- Evidence Graph、Signature、Core Dynamic 选择；
- 12 维覆盖、Shadow、Mature、Fate、Archetype；
- Narrative Renderer 和 Evaluation Harness。

## 3. 技术选择

- Python：`>=3.9`
- 构建系统：`setuptools`
- YAML：`PyYAML >=6,<7`
- 测试：`pytest >=8,<9`
- 数据模型：标准库 `dataclasses`，全部使用 `frozen=True`
- 路径接口：标准库 `pathlib.Path`

不引入 Pydantic。Phase 0 的配置规模固定且较小，显式校验可以减少依赖，同时让每条冻结规则和错误路径保持可见。

## 4. 模块边界

```text
pyproject.toml
src/destiny_personality/
├── __init__.py          对外导出稳定 API
├── config_errors.py     错误码与 ConfigError
├── config_models.py     不可变配置 dataclass
├── config_loader.py     YAML 读取、校验与 RuntimeConfig 组装
└── cli.py               validate-config 命令
tests/
├── test_config_loader.py
├── test_config_validation.py
├── test_cli.py
└── test_v2_2_config_integration.py
```

每个模块只有一个职责：模型不读取文件，加载器不处理终端输出，CLI 不复制校验逻辑。

## 5. 对外接口

主要 Python API：

```python
def load_runtime_config(config_dir: Path) -> RuntimeConfig:
    """加载并完整校验一个 V2.2 运行时配置目录。"""
```

`RuntimeConfig` 包含：

```python
@dataclass(frozen=True)
class RuntimeConfig:
    bazi: BaziMethodologyConfig
    astrology: AstrologyMethodologyConfig
    score_model: ScoreModelConfig
    relation_graph: PrimitiveRelationGraphConfig
```

加载函数不设置依赖当前工作目录的隐式默认值。调用方必须显式提供配置目录，因此安装后的包不会意外读取文档目录或其他项目文件。

命令行接口：

```text
destiny-personality validate-config PATH
```

成功时输出配置包的四个版本及关系数量，退出码为 `0`。失败时向标准错误输出错误码、配置文件和字段路径，退出码为 `2`。

## 6. 校验规则

### 6.1 通用校验

- 四个固定文件必须存在且是普通文件；
- 使用 `yaml.safe_load`，禁止任意对象构造；
- 每个文档根节点必须是 mapping；
- 必需字段不得缺失；
- 字段类型必须精确符合约定，布尔值不能作为整数接受；
- 未知顶层字段视为配置错误，避免拼写错误被静默忽略。

### 6.2 冻结版本

- 八字：`bazi-core-v1.0`
- 占星：`western-tropical-v1.0`
- 评分模型：`2.2`
- Primitive Relation Graph：`1.0`

版本不匹配必须失败，不做自动迁移或兼容猜测。

### 6.3 八字配置

校验 calendar、time、month_mapping、relations 和 personality_scope。月份映射必须完整覆盖十二个文档规定的节令，且值与冻结配置完全一致；自刑集合必须为 `辰、午、酉、亥`，不得把普通同支重复扩展为自刑。

### 6.4 占星配置

校验 tropical、geocentric、placidus、true node，核心行星和角点列表、五类主要相位、orb、发光体 bonus、角点 orb、salience 阈值、dignity modifier-only 规则及外行星高权重条件。数值必须非负，salience 阈值必须严格递增。

### 6.5 评分模型

校验 Trait Salience 和 Synthesis Priority 范围均为 `0..4`，核心门槛为 `3`；Evidence Stability 与 Cross-System Relation 的枚举必须与 V2.2 完全一致。四条冻结布尔规则必须保持：validation 不修改 salience、tension 不降低 salience、tension 可提高 priority、unknown 不等于 low。

### 6.6 Primitive Relation Graph

每条关系必须包含合法的 `P` 加三位数字格式 ID 和合法 relation 类型；左右 ID 不得相同；同一无向 Primitive 对不得重复。`potential_tension` 必须提供非空 `dynamic_family`。其他关系允许提供 family，但本阶段不解释其推理含义。

Relation Graph 引用的 Primitive 是否真实存在，需要未来 Primitive Ontology 才能验证。本阶段保留 ID，并且不从 ID 猜测定义。

## 7. 错误模型

所有预期配置错误统一抛出 `ConfigError`，包含：

- `code`：稳定的机器错误码；
- `message`：面向开发者的简洁说明；
- `file`：相关文件名；
- `field`：点号分隔字段路径，没有具体字段时为 `None`。

首版错误码：

- `CONFIG_GAP`：必需文件或必需产品规则缺失；
- `CONFIG_PARSE_ERROR`：YAML 无法解析；
- `CONFIG_TYPE_ERROR`：节点类型错误；
- `CONFIG_VALUE_ERROR`：值或枚举违反冻结规则；
- `CONFIG_VERSION_MISMATCH`：方法或模型版本不匹配；
- `CONFIG_DUPLICATE_RELATION`：关系图存在重复无向边。

底层解析异常不得原样泄漏为不稳定的调用方接口，但可通过异常链保留供调试使用。

## 8. 数据流

```text
调用方提供 config_dir
→ 检查四个固定文件
→ safe_load 为原始 mapping
→ 分文件校验并构造 frozen dataclass
→ 执行跨配置一致性检查
→ 返回 RuntimeConfig
```

任一步失败都立即停止，不返回部分 `RuntimeConfig`。文档规定的 partial portrait 属于后续 Mapping Coverage 降级，不适用于 Phase 0 的基础配置缺失。

## 9. 测试策略

采用严格的 Red-Green-Refactor：先编写最小失败测试并确认因缺少行为而失败，再实现恰好使其通过的代码。

测试分为四层：

1. 正常加载：最小合法配置可转换为预期的不可变对象；
2. 单字段失败：文件缺失、YAML 损坏、根类型错误、字段缺失、类型错误、枚举错误和版本错误均返回精确错误码；
3. 关系图约束：非法 ID、自环、缺少 tension family 和重复无向边均失败；
4. 项目集成：直接加载 `destiny_personality_skill_docs_v2_2`，断言四个版本和当前 5 条关系。

CLI 测试覆盖成功退出码与失败退出码，不依赖网络、系统时间或项目外文件。

## 10. 完成标准

Phase 0 只有在以下条件全部成立时完成：

- `python3 -m pytest` 全部通过且无警告；
- 当前四份 V2.2 YAML 均通过集成校验；
- 修改任一冻结版本会触发 `CONFIG_VERSION_MISMATCH`；
- 删除任一必需文件会触发 `CONFIG_GAP`；
- CLI 对有效和无效目录返回约定退出码；
- 生产代码没有读取 Golden、Calibration、其他项目目录或网络；
- 未实现或暗中补造 Phase 1 之后的业务规则。
