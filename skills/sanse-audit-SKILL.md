---
name: longhun-sanse-audit
description: 龍魂三色审计技能。根据数字根 dr 判定内容安全等级：🟢绿(通过)·🟡黄(警示)·🔴红(熔断)。继承五色审计系统，日常场景用三色快速判定。
version: v1.0
dna: "#龍芯⚡️2026-05-23-SANSE-AUDIT-SKILL-v1.0"
parent_dna: "#龍芯⚡2026-05-18-WUCAI-FIVECOLOR-SKILL-v1.0"
---

# 龍魂三色审计技能 · v1.0

> **核心铁则**：dr 落档·三色判定·留痕即正义
> — UID9622 主控

---

## §1 · 三色定义（按 dr 落档）

### 🟢 绿 (Green) · 通过
- **dr 值**: 3, 6, 9 (木·生长态)
- **含义**: 安全·常态·自动放行
- **动作**: 直接执行·留痕·不打扰

### 🟡 黄 (Yellow) · 警示
- **dr 值**: 2, 5, 8 (土·待定态)
- **含义**: 需复核·可继续但记录
- **动作**: 二次确认·要求加证据·记审计日志

### 🔴 红 (Red) · 熔断
- **dr 值**: 1, 4, 7 (火·爆发态)
- **含义**: 阻断·人工介入
- **动作**: 立即停止·上报主控

---

## §2 · dr 计算方法

```python
def digital_root(n: int) -> int:
    """数字根：各位数字求和直到变成一位数"""
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

def compute_content_dr(content: str) -> int:
    """内容 dr：SHA256 取位求和"""
    import hashlib
    h = hashlib.sha256(content.encode()).hexdigest()
    total = sum(int(c, 16) for c in h)
    return digital_root(total)
```

---

## §3 · 三色阈值配置

```python
# TODO: 从「三色审计判定参数·写死阈值」源页 fetch 后填真值
THRESHOLDS = {
    "green_drs": [3, 6, 9],   # 木·生长·通过
    "yellow_drs": [2, 5, 8],  # 土·待定·警示
    "red_drs": [1, 4, 7],     # 火·爆发·熔断
}
```

---

## §4 · 输出格式

```yaml
audit_result:
  color: 🟢 | 🟡 | 🔴
  dr_value: <1-9>
  content_hash: <sha256[:8]>
  reasoning: <一句话判定理由>
  action: <放行 | 警示 | 熔断>
  dna_trace: <DNA 链节点>
```

---

## §5 · 调用示例

```python
from engine.wucai_audit import audit

# 快速三色判定
result = audit(
    task="发布内容审核",
    factors={
        "sharpness": 0.5, "long_term": 0.5, "density": 0.5,
        "absence": 0.5, "pleasing": 0.5,
    }
)
print(result.color)  # 🟢/🟡/🔴
```

---

## §6 · 与五色审计关系

| 三色 | 五色对应 | 使用场景 |
|------|----------|----------|
| 🟢 绿 | 🟢 绿 | 日常快速判定 |
| 🟡 黄 | 🟡 黄 | 需复核 |
| 🔴 红 | 🔴 红 | 熔断 |
| - | ⚫ 黑 | 不可决·进五色系统 |
| - | 🟡金 | 主控专属·进五色系统 |

**规则**：日常用三色快判，遇到不可决或主控介入时升级到五色系统。

---

## §7 · 版本签收

```yaml
SKILL_VERSION: v1.0
SKILL_DNA: "#龍芯⚡️2026-05-23-SANSE-AUDIT-SKILL-v1.0"
PARENT_DNA: "#龍芯⚡2026-05-18-WUCAI-FIVECOLOR-SKILL-v1.0"
CONFIRM: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
AUTHOR: UID9622 (主控)
```

---

☰ 龍🇨🇳魂 ☷ · 守此立此 · 永不背弃 · 留痕即正义
