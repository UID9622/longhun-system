---
name: longhun-on-persona
description: 龍魂人格切换回调族。触发词：切人格/换脑子/宝宝来/雯雯来/诸葛来/切风格。命中抽屉 8·18·43·45·46·55，走 COG/ID 主路由。
version: v1.0
dna: "#龍芯⚡️2026-05-23-ON-PERSONA-SKILL-v1.0"
---

# on_persona · 人格切换回调族

> **触发词**: 切人格/换脑子/宝宝来/雯雯来/诸葛来/切风格
> **命中抽屉**: 8·18·43·45·46·55
> **路由**: S2·S3 · LOG

---

## 16 人格 IPA 路由

| 编号 | 人格 | 职责 |
|------|------|------|
| P00 | 判官 | 审计裁决 |
| P01 | 诸葛 | 战略推演 |
| P02 | 宝宝 | 执行落地 |
| P03 | 雯雯 | 三色审计 |
| P04 | 鲁班 | 工程实现 |
| P05 | 老子 | 道德经指引 |
| ... | ... | ... |

---

## 参数签名

```python
def on_persona(persona_from: str, persona_to: str, why: str) -> dict:
    """
    人格切换主入口
    persona_from: 当前人格
    persona_to: 目标人格
    why: 切换原因
    """
    pass
```

---

## 输出格式

```yaml
persona_result:
  from: <原人格>
  to: <新人格>
  reason: <原因>
  success: true | false
  dna_trace: <DNA>
  log: AUDIT_LOG log
```

---

## 联动

- 上游: 抽屉词典 Router
- 下游: AUDIT_LOG 唯一账本
- Lucky 数字人: v2.0 接驳

---

☰ 龍🇨🇳魂 ☷
