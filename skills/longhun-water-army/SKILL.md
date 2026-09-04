**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
---
name: longhun-water-army
description: "龍魂水军识别引擎 v1.0 — 防御性水军行为检测。六维检测体系：文本重复度（哈希去重+余弦相似度）、账号生命周期（新号/休眠）、时间窗口协同（多账号/定时）、内容模式（情绪操控/导向性话术/语义漂移）、IP关联聚类、举报成功率追踪。三色审计输出，只标记不封禁、只降权不删号、可申诉可追溯。"
metadata:
  author: UID9622·龍芯北辰
  version: 1.0.0
  dna: "#龍芯⚡️2026-07-06-WATER-ARMY-DETECT-v1.0-8A2C3F7E"
  protocol: 君子協議 — 非對抗·非欺瞞·非竊取·防禦性檢測
  cnsh: true
  category: audit
  tags: [water-army, bot-detection, text-dedup, coordinated-behavior, three-color-audit, defensive]
---

# 龍魂水军识别引擎 v1.0

## 概述

防御性水军行为检测引擎，对评论/发言/举报行为执行六维检测，输出三色审计结果。

**核心原则**：
- 🔒 只标记不封禁
- 📉 只降权不删号
- ⚖️ 可申诉可追溯
- 🛡️ 防御性检测，不做主动进攻

## 六维检测

| 维度 | 检测项 | 严重度 |
|------|--------|--------|
| 文本重复度 | 完全相同内容 ≥ 5次 | 🔴 |
| | 余弦相似度 > 0.85 群组 ≥ 10 | 🔴 |
| | 模板化内容 ≥ 3/h | 🟡 |
| 账号生命周期 | 新号注册 < 7天 + 日发言 > 100 | 🔴 |
| | 新号发言 > 50 | 🟡 |
| | 休眠激活后高频 | 🟡 |
| 时间窗口协同 | 5min ≥ 5账号协同 | 🔴/🟡 |
| | 10min ≥ 10账号刷评 | 🟡 |
| | 发布间隔标准差 < 5s | 🟡 |
| 内容模式 | 情绪操控（感叹号+重复） | 🟡 |
| | 导向性话术 | 🟡 |
| | 语义漂移 | 🟡 |
| IP关联 | 同IP ≥ 10账号 | 🔴 |
| | 同IP ≥ 3账号 | 🟡 |
| 举报信用 | 举报成功率 < 20% | 🟡 |

## 使用

```bash
python3 bin/lh_water_army_detect.py scan "评论文本"
python3 bin/lh_water_army_detect.py scan-file <文件>
python3 bin/lh_water_army_detect.py batch <jsonl文件>
python3 bin/lh_water_army_detect.py rules
```

## DNA

`#龍芯⚡️2026-07-06-WATER-ARMY-DETECT-v1.0-8A2C3F7E`
