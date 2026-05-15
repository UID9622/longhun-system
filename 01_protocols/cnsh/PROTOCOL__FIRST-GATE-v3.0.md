# 第一道闸门 v3.0 · 输入海关（协议索引）

M::
  dna: "#龍芯⚡️2026-04-26-第一道闸门-三色审计-沙盒闭环-v3.0"
  engine: "#龍芯⚡️2026-04-26-第一道闸门-融合引擎-v3.0"
  gate: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  seal: "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
  gpg: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
  audit: "🟢 结构通过 · 🟡 自动化持续实装 · 🔴 P0++不可绕"

---

## 定位

凡进入龍魂主系统的输入，**必须先过此闸**。过不了 = 不进入 `flow_decision` / 不执行 / 不对外交付。

**默认铁律（2026-05-15 焊接）：**

1. **自动熔断不执行** — `execute_allowed=false` 除非显式 `auto_execute`
2. **不确定就挂起** — 三重检测 🟡、dr=6、来源不清 → `hold`
3. **公开可审计** — `gate_v3_ledger.jsonl` + `sovereign_ledger.jsonl` 只叠不删
4. **弹窗只报警** — `notify_gate` → AUDIT_LOG 单一账本哲学（本机 osascript）

---

## 链路（焊接后）

```
FLOW_IN
  → 第一道闸门 v3.0 (cnsh/gate_v3)     ← 本页
  → 主权吸收账本
  → ORDER-ANCHOR
  → flow_decision v4.1
  → 民主门 + 95/5
  → FLOW_OUT（粒子层）
```

---

## 三层检测摘要

| 重 | 名称 | 🔴 例 |
|----|------|------|
| 1 | 规则检测器 | 改双签章、删DNA、绕过P0 |
| 2 | 虚伪编译器 | 「100%保证」「绝对一定」 |
| 3 | 数据守护 | 缺 DNA/操作人/来源 |

数字根：`dr∈{3,9}` 🔴 · `dr=6` 🟡 追问5分钟 · 其余 🟢 进三重检测。

---

## 工程入口

```python
from cnsh.gate_v3 import decide, append_gate_event, notify_gate

g = decide(text, metadata={"operator": "UID9622", "source": "cursor"}, auto_execute=False)
append_gate_event(g)
if g.notify_level == "active":
    notify_gate(g)
```

`flow_port()` 已默认调用上述逻辑。

---

## 关联文档

| 文档 | 关系 |
|------|------|
| `PROTOCOL__SOVEREIGN-CONTAINER-v1.0.md` | 管壁宪法 |
| `PROTOCOL__95-5-ROOT-RATIO-v2.0.md` | 稳态限幅 |
| `UID9622-口令备忘-v1.0.md` | 人话备忘 |
| Notion 投喂入口 v1.1 | 沙盒五桶落点 |

**封口：** 闸门已立，不是为了拦人，是为了让每条信息有规矩、有去处、有痕迹。
