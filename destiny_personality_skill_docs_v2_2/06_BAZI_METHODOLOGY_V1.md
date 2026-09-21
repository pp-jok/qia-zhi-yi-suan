# 06 Bazi Methodology v1
## 项目方法约定

> 这是一套产品方法约定，用于保证重复性，并不声称是所有八字流派的唯一标准。

## 1. Calendar Basis

- 使用公历出生日期作为输入；
- 年柱/月柱切换采用节气体系；
- 月柱按“节”切换，不按农历初一，也不按中气切换；
- 历史时区与 DST 必须先还原。

---

## 2. Time Basis

默认模式：

```text
historical civil time
→ remove DST if applicable
→ local standard time
→ true solar time correction
→ determine shichen
```

若用户或调用方明确选择：
`standard_time_mode`

则不使用真太阳时，但必须记录方法差异。

---

## 3. Day Boundary

项目默认：

```text
00:00 local true solar time
```

作为日柱换日边界。

原因：
- 便于与现代历法计算组件统一；
- 必须显式记录，不声称是唯一传统流派。

若未来支持“子初换日”，必须作为另一 methodology version，不能静默切换。

---

## 4. Month Boundary

月柱以节令为界：

```text
立春 寅月
惊蛰 卯月
清明 辰月
立夏 巳月
芒种 午月
小暑 未月
立秋 申月
白露 酉月
寒露 戌月
立冬 亥月
大雪 子月
小寒 丑月
```

---

## 5. Hidden Stems

采用常见藏干表，并明确区分：

- 透干
- 藏干

任何规则不得把“藏”描述成“透”。

---

## 6. Ten Gods

十神全部相对日主计算。

禁止：
- 固定星曜式套用；
- 脱离日主直接判断十神。

---

## 7. Strength Analysis

身强弱至少考虑：

1. 月令季节力量；
2. 生扶日主结构；
3. 克泄耗日主结构；
4. 天干透出；
5. 地支根气；
6. 组合关系对有效性的修饰。

禁止只凭：
- 五行数量；
- 单一日主；
- “缺什么补什么”。

---

## 8. Relations

首版支持：

- 天干五合
- 地支六合
- 三合
- 三会
- 六冲
- 六害
- 三刑
- 自刑（采用常见：辰、午、酉、亥）

不把“同支重复”自动视为自刑。

---

## 9. Personality Scope

核心画像阶段优先使用：

- 日主与身强弱
- 月令
- 印 / 比劫 / 食伤 / 财 / 官杀的显隐与强弱
- 结构性合冲刑害
- 五行气候与流通

暂不把大运流年混入 Core Portrait。

---

## 10. Methodology Version

```text
bazi_methodology_version: bazi-core-v1.0
```
