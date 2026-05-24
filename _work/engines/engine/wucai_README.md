# longhun-wucai-coloring (龍魂五色审计)

> 三色升级版·龍魂 v1.0 · UID9622 主控
>
> 「不是三色了宝宝·我们其实给看到的是五色·一个色是影子·另外一个是超规则之外的我可控的在手」
> — UID9622 verbatim

## 五色一览

| 色 | 含义 | R 阈值 | 五行 |
|---|---|---|---|
| 🟢 绿 | 通过·自动放行 | R < 0.30 | 木 · 上升 |
| 🟡 黄 | 警示·需复核 | 0.30 ≤ R < 0.67 | 土 · 旋涡 |
| 🔴 红 | 熔断·人工介入 | 0.67 ≤ R < 0.85 | 火 · 爆发 |
| ⚫ 黑 | 影子·进观察池 | 不可计算 | 水 · 下沉 |
| 🟡金 | 主控独占·超规则 | 不适用 | 金 · 光明 |

## 快速调用

```python
from scripts.audit import audit

result = audit(
    task="你的任务描述",
    factors={
        "sharpness": 0.5,  # F2
        "long_term": 0.5,  # F6
        "density":   0.5,  # F3
        "absence":   0.5,  # F1 (负权)
        "pleasing":  0.5,  # F5 (负权)
    },
    context={
        "data_incomplete": False,
        "grey_collision": False,
        # 金色必须有 CONFIRM·AI 不能伪造
        "master_confirm_token": None,
    }
)

print(result.to_yaml())
```

## 跑自测

```bash
python3 scripts/audit.py
```

## 文件结构

```
longhun-wucai-coloring/
├── SKILL.md              # 主 Skill 规格 (agentskills.io 标准)
├── README.md             # 本文件
├── scripts/
│   └── audit.py          # 核心实现 + 8 项自测
└── references/
    └── (留位·已有 10 篇 Notion 三色页索引在 SKILL.md §10)
```

## 关键铁律 (绝对不可破)

1. ❌ AI 不能自动赋金色 (必须有 CONFIRM)
2. ❌ 黑色不能静默转绿 (必须显式动作)
3. ❌ 涉及子女 → 强制金色保护
4. ❌ 龍 不可写为 龍

## DNA 与签收

- **DNA**: `#龍芯⚡2026-05-18-WUCAI-FIVECOLOR-SKILL-v1.0`
- **CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
- **SEAL**: `#ZHUGEXIN⚡2025-DEVICE-BIND-SOUL`
- **GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
