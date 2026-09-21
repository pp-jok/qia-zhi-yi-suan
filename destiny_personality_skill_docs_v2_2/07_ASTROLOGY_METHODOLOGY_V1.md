# 07 Western Astrology Methodology v1
## 项目方法约定

> 这是一套产品统一方法，用于重复性，不声称代表所有西方占星流派。

## 1. Core Settings

```text
Zodiac: Tropical
Reference: Geocentric
House System: Placidus
Node: True Node
Coordinates: birthplace geolocation
Time: UTC converted from historical local civil time
```

---

## 2. Core Bodies

首版使用：

- Sun
- Moon
- Mercury
- Venus
- Mars
- Jupiter
- Saturn
- Uranus
- Neptune
- Pluto

Angles：
- Ascendant
- MC

可选：
- True North Node
- Part of Fortune

PoF 不进入核心人格高权重，除非后续专题需要。

---

## 3. Major Aspects

首版只使用：

```text
conjunction 0°
opposition 180°
square 90°
trine 120°
sextile 60°
```

minor aspects 默认关闭。

---

## 4. Base Orbs

用于核心人格判定的默认最大 orb：

```text
conjunction: 8°
opposition: 8°
square: 7°
trine: 7°
sextile: 5°
```

若涉及 Sun / Moon，允许 +1°。

但 Salience 优先级按紧密程度递减：

```text
<=1°   dominant
<=3°   strong
<=5°   moderate
>5°    secondary unless luminary/angle emphasis
```

---

## 5. Angles

行星与 Asc / MC 的 conjunction / opposition / square 可进入核心人格。

默认 orb：

```text
<= 4°
```

---

## 6. Dignity

首版仅使用传统核心尊贵作为 modifier：

- domicile
- detriment
- exaltation
- fall

不单独用 dignity 生成完整人格结论。

---

## 7. House Emphasis

以下可成为强结构：

- Sun / Moon / Mercury / Venus / Mars 所在宫位；
- 3颗及以上行星明显聚集同一宫；
- 角宫（1/4/7/10）聚集。

宫位解释必须服从出生时间稳定性。

---

## 8. Element / Modality

作为背景层，不单独压过紧密相位和核心行星结构。

优先级：

```text
tight personal aspects
> Sun/Moon/Asc
> personal planet placements
> house emphasis
> modality/element
> outer planet background
```

---

## 9. Outer Planets

Uranus / Neptune / Pluto 只有在以下情况提高个体人格权重：

- 与 Sun/Moon/Mercury/Venus/Mars/Asc/MC 紧密主要相位；
- 落角宫并构成明显结构；
- 与个人行星形成重复主题。

否则主要作为背景。

---

## 10. Methodology Version

```text
astrology_methodology_version: western-tropical-v1.0
```
