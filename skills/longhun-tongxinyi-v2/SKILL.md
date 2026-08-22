# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
---
name: longhun-tongxinyi-v2
description: >
  龍魂前置翻译技能·通心译 v2.0。基于 20 条语义观察构建七维评估体系，
  实现“先翻译再执行、贴身常驻、意图识别、情绪净化、三色审计”。
  入口命令：python3 scripts/tongxin_gate.py。
  触发关键词：通心译、先翻译再执行、意图识别、情绪净化、Tongxin、v2.0、七维评估。
metadata:
  id: longhun-tongxinyi-v2
  display_name: 龍魂通心译 v2.0
  version: "2.0.0"
  author: UID9622
  dna: "#龍芯⚡️丙午·甲午·丙子·甲午·䷙大畜-LONGHUN-TONGXINYI-v2.0"
  category: internal
  status: active
  entry: "python3 /Users/zuimeidedeyihan/longhun-system/skills/longhun-tongxinyi-v2/scripts/tongxin_gate.py"
  trigger:
    keywords:
      - 通心译
      - 先翻译再执行
      - 意图识别
      - 情绪净化
      - Tongxin
      - v2.0
      - 七维评估
    context: "用户输入进入龍魂系统前的第一层理解、翻译、审计与路由"
    priority: 95
---

# longhun-tongxinyi-v2 | 龍魂前置翻译技能·通心译 v2.0

> **DNA**: `#龍芯⚡️丙午·甲午·丙子·甲午·䷙大畜-LONGHUN-TONGXINYI-v2.0`  
> **父DNA**: `#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGWEN-NLP-v5.0`  
> **CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
> **SEAL**: `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`

---

## 1. 一句话定位

通心译 v2.0 是**语义心意映射引擎**，不是传统翻译模型。
基于 20 条哲学观察构建 7 维可训练评估体系，实现“心意相通，而非字面镜像”。

---

## 2. v2.0 升级点

| 维度 | v1.0 | v2.0 |
|------|------|------|
| 评估 | 三色审计 | 七维评估 + R-Score |
| 架构 | L0-L5 六层 | 三层语义传递（字面/逻辑/心意） |
| 训练 | 无 | 20 条样本 + 哲学输入驱动 |
| 输出 | 意图骨架 | 意图骨架 + 龍魂标签 + 推荐技能 |

---

## 3. 入口命令

```bash
# 门控演示
python3 /Users/zuimeidedeyihan/longhun-system/skills/longhun-tongxinyi-v2/scripts/tongxin_gate.py

# 七维评估器
python3 /Users/zuimeidedeyihan/longhun-system/skills/longhun-tongxinyi-v2/scripts/tongxin_evaluator.py
```

---

## 4. Python API

```python
from tongxin_gate import TongxinyiGate

gate = TongxinyiGate()
result = gate.translate("帮我查一下系统状态")

# result 包含：
#   dna, confidence, recommended_skill
#   L0_原话保留, L1_情绪净化, L2_意图骨架,
#   L3_SAST, L4_三色审计, L5_适配输出,
#   龍魂标签, 七维评估
```

---

## 5. 七维评估

| 维度 | 英文名 | 权重 |
|------|--------|------|
| D1 | 文化负载词 Culture Lexicon | 0.20 |
| D2 | 语义-语法制约 Semantic-Syntax | 0.15 |
| D3 | 古代汉语 Classical Chinese | 0.10 |
| D4 | 语篇完整性 Discourse Integrity | 0.20 |
| D5 | 文明安全 Civilization Safety | 0.15 |
| D6 | 创造性策略 Creative Strategy | 0.10 |
| D7 | 语义精确性 Semantic Precision | 0.10 |

完整规范见 `tongxin_translation_v2_spec.md` 与 `tongxin_notion_update.md`。

---

## 6. 文件清单

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 本文件 |
| `scripts/tongxin_gate.py` | 门控 / L0-L5 翻译 |
| `scripts/tongxin_evaluator.py` | 七维评估器 |
| `scripts/tongxin_train_template.json` | 训练样本模板 |
| `tongxin_translation_v2_spec.md` | v2.0 完整规范 |
| `tongxin_notion_update.md` | Notion 版本摘要 |

---

## 7. DNA 追溯

```
本技能: #龍芯⚡️丙午·甲午·丙子·甲午·䷙大畜-LONGHUN-TONGXINYI-v2.0
父技能: #龍芯⚡️丙午·甲午·戊辰·戊午·䷑蛊-LONGHUN-TONGXINYI-v1.0-WELDED-L0
来源:   /Users/zuimeidedeyihan/Downloads/Kimi_Agent_通心意译模型更新/
作者:   UID9622
```
