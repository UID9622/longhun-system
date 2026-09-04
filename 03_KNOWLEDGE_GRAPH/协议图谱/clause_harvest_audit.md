# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
---
id: clause_harvest_audit
type: clause
title: 收割信号自动审计
layer: L3
dna: "#龍芯⚡️丙午·辛未·乙酉·申时·䷓观-LONGHUN-CLAUSE-HARVEST-AUDIT-1F7A8B4C"
owner: UID9622 · 诸葛鑫（Lucky）
claim: 引擎自动扫描平台内容识别收割信号（PK/倒计时/加成/排名），打分评级，🔴高危进审查，DNA追溯归档。
based_on: [three_color_audit, dragon_vein_trace]
related: [protocol_anti_algorithmic_harvest, clause_no_pk, clause_no_countdown, clause_no_tip_skimming]
immutable: false
created: 丙午·辛未·乙酉
---

# 收割信号自动审计 · v1.0

## 执行说明

本条款由 `bin/lh_anti_algorithmic_harvest.py` 引擎落地执行，不是纸面规则。

**输入**：直播标题/文案/弹幕文本（或 `--demo` 跑内置抖音PK案例）
**信号词典**：
- PK类：比拼 / 连麦 / PK / 对战 / 站队 / 输赢 / 榜一
- 倒计时类：倒计时 / 限时 / 最后 / 秒 / 马上结束
- 加成类：倍数 / 加成 / 3倍 / 翻倍 / 福利
- 排名类：排名 / 上榜 / 热门 / 冲榜 / 推荐
- 抽成类：打赏 / 礼物 / 刷 / 嘉年华

**评级**：命中 0 类 → 🟢安全；1–2 类 → 🟡谨慎；≥3 类 → 🔴高危
**输出**：带 DNA 的审计报告 JSON，写入 `state/threshold_trigger/harvest_audit/` 审计链
**联动**：🔴高危自动进伦理审查队列（复用三色审计 R 值阈值）

## 用户侧保护（引擎可提示）

- 情绪冷却：打赏前强制 30 秒冷静
- 消费透明：实时显示本月已消费/预算
- 时间审计：每日观看时长提醒，超量自动断流

> **DNA**：`#龍芯⚡️丙午·辛未·乙酉·申时·䷓观-LONGHUN-CLAUSE-HARVEST-AUDIT-1F7A8B4C`
> **确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` ✅
