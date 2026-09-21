# 02 Primitive State Model

## 1. Primitive 不再只有 high

每个 Primitive 必须输出：

```text
supported_high
supported_low
mixed
unknown
```

---

## 2. supported_high

存在足够结构支持该倾向偏高。

---

## 3. supported_low

存在明确的反向结构，且不是因为单纯缺证据。

禁止：

```text
no evidence = supported_low
```

---

## 4. mixed

同一体系或双体系中，存在两股足够强、真实并存的力量。

示例：

```text
structure_need = high
exit_option_need = high
```

这不是矛盾数据，而是 Core Dynamic 候选来源。

---

## 5. unknown

以下任一成立：

- 没有足够映射证据；
- 证据过弱；
- 核心证据受出生时间影响过大；
- 规则库尚未覆盖。

---

## 6. 输出示例

```json
{
  "primitive_id": "P001",
  "state": "supported_high",
  "bazi_salience": 3,
  "astrology_salience": 2,
  "evidence_stability": "high"
}
```

或：

```json
{
  "primitive_id": "P053",
  "state": "unknown"
}
```
