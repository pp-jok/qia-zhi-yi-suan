# Phase 1 Deterministic Chart Calculation Contract Design

> Status: completed development-reference design. Its contracts and guards are
> retained, but the Python backend-injection model is not the Skill runtime.
> Runtime calculation is performed by the agent through the external capability
> protocol defined by the current roadmap.

## 1. 目标

Phase 1 为八字与西方占星确定性命盘计算建立稳定的输入、输出、后端协议和编排契约。它允许后续接入经过产品确认的计算实现，同时确保两套体系隔离、方法版本固定、未知出生时间约束可执行。

本阶段不实现历法、真太阳时、八字排盘或西方星盘数学算法，不访问网络，也不生成 Primitive、人格判断或叙事。

## 2. 设计原则

- 所有业务输入和计算事实均使用不可变 dataclass；
- 所有集合使用 tuple，禁止后端返回可变共享状态；
- 八字与占星后端分别注入，不共享体系内部结果；
- 编排层只传递输入、配置并验证输出契约，不解释命盘；
- 后端必须声明实际使用的方法版本；
- 缺少出生时间时不得生成时柱、Asc、MC 或宫位；
- 任何 Fatal 都中止整个计算，不返回半成品；
- 没有规则依据的字段不以自由字典形式加入事实模型。

## 3. 技术方案

采用 Python 标准库 `typing.Protocol` 定义三个可替换后端：

1. `TimeNormalizer`
2. `BaziChartCalculator`
3. `AstrologyChartCalculator`

`ChartCalculationService` 依赖这些协议而非具体计算库。测试使用小型 fake backend，后续真实算法只需实现协议，不需要修改编排层。

不使用动态插件注册表、依赖注入框架或运行时反射。

## 4. 模块结构

```text
src/destiny_personality/calculation/
├── __init__.py      对外导出 Phase 1 API
├── errors.py        CalculationError 与错误码
├── models.py        输入、标准化时间和两套事实模型
├── protocols.py     三个计算后端 Protocol
└── service.py       编排流程与输出契约校验

tests/
├── test_birth_input_contract.py
├── test_calculation_service.py
├── test_calculation_contract_validation.py
└── test_calculation_failures.py
```

## 5. 输入模型

### 5.1 枚举

```python
class TimeBasis(str, Enum):
    TRUE_SOLAR_TIME = "true_solar_time"
    STANDARD_TIME = "standard_time"


class FactMode(str, Enum):
    STABLE_ONLY = "stable_only"
    TIME_SENSITIVE = "time_sensitive"
```

`TimeBasis` 对应八字方法配置中允许的两种时间口径。`FactMode` 不替产品选择高敏感场景的处理方式，而是要求调用方明确决定只要稳定事实，还是保留带时间敏感性的事实。

### 5.2 BirthInput

```python
@dataclass(frozen=True)
class BirthInput:
    birth_date: date
    birth_time: Optional[time]
    timezone_name: str
    latitude: Decimal
    longitude: Decimal
    time_basis: TimeBasis
    fact_mode: FactMode
```

约束：

- 日期必须是 `date`，不能接受 `datetime`；
- 时间若存在必须是无时区的当地民用时间；
- `timezone_name` 必须是非空字符串，本阶段不验证 IANA 数据库是否包含该名称；
- 纬度范围为 `-90..90`，经度范围为 `-180..180`；
- 经纬度必须为有限 `Decimal`；
- `birth_time is None` 时，`fact_mode` 必须为 `STABLE_ONLY`；
- `STANDARD_TIME` 只有冻结配置允许时才能使用。

调用方必须显式提供 `fact_mode`，编排层不得替产品猜测高时间敏感场景的策略。

## 6. 标准化时间模型

```python
@dataclass(frozen=True)
class NormalizedBirthTime:
    birth_date: date
    historical_civil_time: Optional[datetime]
    local_standard_time: Optional[datetime]
    utc_time: Optional[datetime]
    true_solar_time: Optional[datetime]
    timezone_name: str
    dst_was_applied: Optional[bool]
    time_basis: TimeBasis
    fact_mode: FactMode
    sensitivity_reasons: Tuple[str, ...]
```

未知出生时间时，四个 datetime 与 `dst_was_applied` 必须为 `None`。已知出生时间时：

- historical civil、local standard 和 UTC 必须存在；
- historical civil、local standard 与 true solar time 使用无时区的当地钟表时间；
- UTC 必须带时区且 offset 为零；
- 当 `TimeBasis.TRUE_SOLAR_TIME` 时，true solar time 必须存在；
- 当 `TimeBasis.STANDARD_TIME` 时，true solar time 必须为 `None`；
- birth date、timezone name、time basis 与 fact mode 必须和输入一致；
- `sensitivity_reasons` 只承载后端确定性诊断，不改变事实或评分。

## 7. 八字确定性事实

```python
@dataclass(frozen=True)
class BaziPillar:
    heavenly_stem: str
    earthly_branch: str


@dataclass(frozen=True)
class HiddenStemsFact:
    pillar: str
    stems: Tuple[str, ...]


@dataclass(frozen=True)
class TenGodFact:
    subject_ref: str
    ten_god: str


@dataclass(frozen=True)
class BaziRelationFact:
    relation_type: str
    participant_refs: Tuple[str, ...]


@dataclass(frozen=True)
class BaziChartFacts:
    methodology_version: str
    year_pillar: BaziPillar
    month_pillar: BaziPillar
    day_pillar: BaziPillar
    hour_pillar: Optional[BaziPillar]
    hidden_stems: Tuple[HiddenStemsFact, ...]
    ten_gods: Tuple[TenGodFact, ...]
    relations: Tuple[BaziRelationFact, ...]
```

这些字段都是排盘或相对日主的确定性派生事实。身强弱、结构人格含义和五行气候解释属于后续 Independent System Analysis，不进入 Phase 1。

Phase 1 只校验柱、藏干、十神和关系字段的结构完整性与 stable-only 约束。天干、地支、十神以及关系成员引用的完整枚举尚未在项目配置中提供；在正式配置出现前，不由 Codex 自行写入规则常量。

## 8. 西方占星确定性事实

```python
@dataclass(frozen=True)
class AstrologyPlacement:
    body: str
    longitude: Decimal
    sign: str
    degree_in_sign: Decimal
    house: Optional[int]


@dataclass(frozen=True)
class AstrologyAspectFact:
    body_a: str
    body_b: str
    aspect_type: str
    orb: Decimal


@dataclass(frozen=True)
class HouseCusp:
    house: int
    longitude: Decimal


@dataclass(frozen=True)
class DignityFact:
    body: str
    dignity: str


@dataclass(frozen=True)
class AstrologyChartFacts:
    methodology_version: str
    placements: Tuple[AstrologyPlacement, ...]
    aspects: Tuple[AstrologyAspectFact, ...]
    ascendant: Optional[Decimal]
    mc: Optional[Decimal]
    house_cusps: Tuple[HouseCusp, ...]
    dignities: Tuple[DignityFact, ...]
```

相位只允许冻结配置启用的类型；星体、角点、orb 和 dignity 也必须受 RuntimeConfig 约束。Phase 1 校验后端输出是否落在配置许可范围内，但不计算这些值。

输出校验至少包括：

- placement body 必须来自配置 planets，且每个 body 只能出现一次；
- longitude 位于 `[0, 360)`，degree in sign 位于 `[0, 30)`；
- house 若存在必须为 `1..12`；
- aspect 两端必须是不同且已配置的 body，类型必须启用；
- orb 必须非负且不超过对应配置上限，涉及 Sun 或 Moon 时才允许 luminary bonus；
- ascendant、MC 和 house cusp longitude 位于 `[0, 360)`；
- `TIME_SENSITIVE` 模式必须提供 Asc、MC、每个 placement 的 house，以及不重复的 12 个 house cusps；
- dignity body 和 dignity 类型必须来自配置。

## 9. 聚合输出

```python
@dataclass(frozen=True)
class DeterministicChartFacts:
    normalized_time: NormalizedBirthTime
    bazi: BaziChartFacts
    astrology: AstrologyChartFacts
```

禁止提供合并后的跨体系 facts 字典。两套事实只有在后续 Cross-System Synthesizer 才允许对齐。

## 10. 后端协议

```python
class TimeNormalizer(Protocol):
    def normalize(
        self,
        birth_input: BirthInput,
        config: RuntimeConfig,
    ) -> NormalizedBirthTime: ...


class BaziChartCalculator(Protocol):
    def calculate(
        self,
        birth_input: BirthInput,
        normalized_time: NormalizedBirthTime,
        methodology: BaziMethodologyConfig,
    ) -> BaziChartFacts: ...


class AstrologyChartCalculator(Protocol):
    def calculate(
        self,
        birth_input: BirthInput,
        normalized_time: NormalizedBirthTime,
        methodology: AstrologyMethodologyConfig,
    ) -> AstrologyChartFacts: ...
```

协议只规定可验证接口，不规定算法来源。未经后续授权，不选择外部计算库或自研算法。

## 11. 编排流程

`ChartCalculationService.calculate(birth_input, runtime_config)` 执行：

```text
校验 BirthInput
→ TimeNormalizer.normalize
→ 校验 NormalizedBirthTime
→ BaziChartCalculator.calculate
→ 校验八字方法版本与事实契约
→ AstrologyChartCalculator.calculate
→ 校验占星方法版本与事实契约
→ 返回 DeterministicChartFacts
```

八字计算结果不得作为占星计算输入，反之亦然。若任一步失败，后续步骤不再执行。

## 12. 未知时间与 stable-only 约束

当 `birth_time is None`：

- `NormalizedBirthTime.fact_mode` 必须为 `STABLE_ONLY`；
- `BaziChartFacts.hour_pillar` 必须为 `None`；
- 所有 Astrology placement 的 `house` 必须为 `None`；
- `ascendant` 与 `mc` 必须为 `None`；
- `house_cusps` 必须为空 tuple；
- 若后端返回任一时间敏感事实，抛出 `CALCULATION_CONTRACT_ERROR`。

当调用方主动选择 `STABLE_ONLY` 时，即便出生时间已知，也执行同样的输出限制。这避免编排层自行判断“哪些边界风险可以接受”。

## 13. 错误模型

```python
class CalculationError(RuntimeError):
    code: str
    message: str
    system: Optional[str]
    field: Optional[str]
```

错误码：

- `BIRTH_INPUT_ERROR`：输入类型、范围或模式组合非法；
- `TIME_NORMALIZATION_ERROR`：时间后端无法确定性标准化；
- `CALCULATION_FATAL`：八字或占星后端计算失败；
- `CALCULATION_CONTRACT_ERROR`：后端输出违反已冻结契约；
- `METHODOLOGY_VERSION_MISMATCH`：输出方法版本与 RuntimeConfig 不同。

编排层保留原异常链，但不给调用方返回部分结果。协议实现主动抛出的 `CalculationError` 原样传播；其他异常包装为对应阶段的稳定错误码。

## 14. 测试策略

使用不包含命理逻辑的 fake 后端进行 TDD：

1. 输入校验：日期/时间类型、空时区、经纬度范围、unknown-time 模式；
2. 编排顺序：normalizer → bazi → astrology；
3. 隔离性：两个 calculator 仅收到各自 methodology；
4. 方法版本：任一后端返回错误版本即失败；
5. stable-only：拒绝时柱、Asc、MC、house 和 house cusp；
6. Fatal：前置阶段失败后，后续后端不执行；
7. 不可变性：聚合输出及全部嵌套集合不可修改；
8. 回归：现有 Phase 0 的 18 个测试必须继续通过。

测试不验证具体柱、星体位置或相位数值是否正确，因为 Phase 1 没有被授权实现这些算法。

## 15. 完成标准

- Phase 1 所有新增测试通过；
- Phase 0 的 18 个测试保持通过；
- 不含真实排盘算法、LLM、Primitive 或 Narrative；
- 不访问网络或项目外业务文件；
- 未知出生时间和主动 stable-only 均无法泄漏时间敏感事实；
- 两套体系的事实对象、方法配置和后端调用保持隔离；
- 任一计算 Fatal 都不会返回部分 `DeterministicChartFacts`。
