---
name: longhun-on-translate
description: 龍魂通心译回调族。触发词：沟通·装/真心·口头禅·疑问·童趣词·精准。命中抽屉 1·10·15·38·42·47，走 COG/HUM 主路由。含五彩染色。
version: v1.0
dna: "#龍芯⚡️2026-05-23-ON-TRANSLATE-SKILL-v1.0"
---

# on_translate · 通心译回调族

> **触发词**: 沟通·装/真心·口头禅·疑问·童趣词·精准
> **命中抽屉**: 1·10·15·38·42·47
> **路由**: S2 · PASSIVE
> **含旧 Skill**: 五彩染色

---

## 参数签名

```python
def on_translate(raw_text: str, tone: str, mode: str, persona: str) -> dict:
    """
    通心译主入口
    raw_text: 原始文本
    tone: 语气（直接/温和/正式）
    mode: 模式（技术/日常/文化）
    persona: 当前人格
    """
    pass
```

---

## 五彩染色映射

| 五行 | 色 | 语义区 |
|------|-----|--------|
| 木 | 青/绿 | 生长·通过 |
| 火 | 赤/红 | 爆发·警示 |
| 土 | 黄 | 承载·待定 |
| 金 | 白 | 收敛·主控 |
| 水 | 玄/黑 | 下沉·影子 |

---

## 输出格式

```yaml
translate_result:
  original: <原文>
  translated: <译文>
  tone: <语气>
  wuxing: <五行>
  color: <五色>
  log: AUDIT_LOG log
```

---

## 联动

- 上游: 抽屉词典 Router
- 下游: AUDIT_LOG 唯一账本
- 五彩: wucai_marquee.py

---

☰ 龍🇨🇳魂 ☷
