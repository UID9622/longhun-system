# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂·精神免疫系统 v1.0

> **不是功能，是一面盾。不是审视灵魂，是接住灵魂。**
>
> DNA: #龍芯⚡️丙午·乙未·丁酉·丙午·䷨损-MENTAL-IMMUNE-v1.0-e8a1f2b3
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0

---

## ⛔ 焊死铁律（写进每一行代码）

| # | 铁律 | 含义 |
|:---:|:---|:---|
| 1 | **纯本地** | 所有输入数据（文字、情绪、行为）绝对不上传服务器，只在用户本地处理 |
| 2 | **匿名化** | 任何共享数据必须是经过聚合、脱敏后的统计信息（k≥5），无法追溯到个人 |
| 3 | **无评判** | 引擎只提供分析和建议，不评判任何情绪，不打"好/坏"标签 |
| 4 | **不建画像** | 不做用户画像，不分析行为动机，不挖掘消费习惯 |
| 5 | **用户可控** | 所有数据存储位置在 `~/.龍魂/mental_immune/`，用户可随时查看、导出、删除 |

---

## 架构总览

```
检测 → 防御 → 排毒 → 巩固 → 共鸣
  🌡️     🛡️     🧘     ⚓      🫂
```

| 引擎 | 文件 | 功能 |
|:---|:---|:---|
| 🌡️ 精神体温计 | `anxiety_detector.py` | L1关键词+L2句式+L3语义 → 焦虑指数0-100 |
| 🛡️ 降噪盾 | `noise_shield.py` | 12面盾牌，根据焦虑类型自动匹配降噪策略 |
| 🧘 排毒向导 | `digital_detox.py` | 离线时间表 + 3分钟呼吸训练 + 替代活动 |
| ⚓ 行为锚 | `behavior_anchor.py` | 发现稳定行为模式，焦虑时提醒回归 |
| 🫂 共鸣墙 | `community_resonance.py` | 匿名聚合统计，k-匿名性保证不可追溯 |

---

## 快速开始

```bash
# 1. 检测情绪
python3 engines/lh_mental_immune/anxiety_detector.py "今天又被卷了，感觉自己好没用"

# 2. 查看降噪盾
python3 engines/lh_mental_immune/noise_shield.py

# 3. 生成排毒方案
python3 engines/lh_mental_immune/digital_detox.py

# 4. 记录行为锚
python3 engines/lh_mental_immune/behavior_anchor.py

# 5. 查看共鸣墙
python3 engines/lh_mental_immune/community_resonance.py
```

## 门户

访问 `portal/mental-immune/index.html` 获得完整可视化体验。

---

## 数据存储

所有数据存储于用户本地：
```
~/.龍魂/mental_immune/
├── anxiety_log.jsonl    # 焦虑检测日志（只存哈希指纹，不存原文）
├── shield_config.json   # 降噪盾配置
├── shield_log.jsonl     # 降噪日志
├── detox_log.jsonl      # 排毒日志
├── behavior_log.jsonl   # 行为签到
├── anchors.json         # 锚点数据
├── resonance_log.jsonl  # 共鸣日志（完全脱敏）
└── resonance_wall.json  # 共鸣墙缓存
```

用户可随时删除 `~/.龍魂/mental_immune/` 目录，不留任何痕迹。
