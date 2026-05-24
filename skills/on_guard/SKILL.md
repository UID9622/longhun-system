---
name: longhun-on-guard
description: 龍魂守门回调族。触发词：触红线/黄线/熔断/审计/隐私/一票否决。命中抽屉 3·12·25·26·27·44，走 RULE 主路由。合并旧 R + Watchdog。
version: v1.0
dna: "#龍芯⚡️2026-05-23-ON-GUARD-SKILL-v1.0"
---

# on_guard · 守门回调族

> **触发词**: 触红线/黄线/熔断/审计/隐私/一票否决
> **命中抽屉**: 3·12·25·26·27·44
> **路由**: S4·S8 · FORCE
> **合并旧 Skill**: R责任系数 + Watchdog三重检测

---

## 三色阈值

| R 值 | 颜色 | 动作 |
|------|------|------|
| R < 0.3 | 🔴 红 | 熔断 |
| 0.3 ≤ R < 0.5 | 🟡 黄 | 警示 |
| 0.5 ≤ R < 0.7 | 🟢 绿 | 通过 |
| R ≥ 0.7 | ⭐ 金 | 龍魂型 |
| R ≥ 0.85 | 🐉 龍 | 超阈值 |

---

## 参数签名

```python
def on_guard(rule_id: str, signal: str, color: str, dna: str) -> dict:
    """
    守门审计主入口
    rule_id: 触发的规则 ID
    signal: 信号（红线/黄线/熔断）
    color: 判定颜色
    dna: DNA 追溯码
    """
    pass
```

---

## 熔断联动

触发 §8.5 极端态四条件时：
1. 立即停止当前操作
2. 上报主控
3. 进金色队列等裁决
4. 写 AUDIT_LOG force_log + 主动弹窗

---

## 联动

- 上游: 抽屉词典 Router
- 下游: AUDIT_LOG 唯一账本 + osascript 弹窗
- 五色审计: wucai_audit.py

---

☰ 龍🇨🇳魂 ☷
