---
name: longhun-tags
description: >
  龍魂文化标签体系。以五行、八卦、甲骨文、二十八星宿替代西方emoji，
  提供 112 个结构化中文标签。入口命令：python3 scripts/longhun_tags.py。
  支持标签查询、渲染（html/md/text/ansi）、emoji 解析、CNSH 变量映射。
  触发关键词：标签、五行、八卦、甲骨文、龍魂标签、CNSH变量、表情包、星宿。
metadata:
  id: longhun-tags
  display_name: 龍魂标签体系
  version: "1.0.0"
  author: UID9622
  dna: "#龍芯⚡️2026-07-01-LONGHUN-TAG-SYSTEM-v1.0"
  category: internal
  status: active
  trigger:
    keywords:
      - 标签
      - 五行
      - 八卦
      - 甲骨文
      - 龍魂标签
      - CNSH变量
      - 表情包
      - 星宿
    context: "当用户需要查询、渲染或映射龍魂文化标签时触发"
    priority: 80
---

# longhun-tags | 龍魂文化标签体系 v1.0

> **DNA**: `#龍芯⚡️2026-07-01-LONGHUN-TAG-SYSTEM-v1.0`  
> **CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
> **SEAL**: `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`  
> **UID**: 9622 | **版本**: 1.0.0

---

## 1. 一句话定位

用中国传统文化符号（五行、八卦、甲骨文、二十八星宿）替代西方 emoji，
构建 112 个可渲染、可组合、可审计的龍魂标签。

---

## 2. 标签统计

| 体系 | 数量 | 说明 |
|------|------|------|
| 五行 | 20 | 5 元素 × 4 状态（生/旺/休/囚） |
| 八卦 | 24 | 8 卦 × 3 变体（正/反/动） |
| 甲骨文 | 40 | 状态/情绪/功能/等级 四类 |
| 二十八星宿 | 28 | 四象 × 7 宿 |
| **总计** | **112** | |

---

## 3. 入口命令

```bash
# 运行演示
python3 /Users/zuimeidedeyihan/longhun-system/skills/longhun-tags/scripts/longhun_tags.py

# 查询 CNSH 变量
python3 /Users/zuimeidedeyihan/longhun-system/skills/longhun-tags/scripts/cnsh_tag_variables.py
```

---

## 4. Python API

```python
from longhun_tags import LongHunTagSystem

ts = LongHunTagSystem()

# 查询
ts.get_tag("METAL_PEAK")      # 五行标签详情
ts.get_tag("启")              # 甲骨文
ts.get_tag("角")              # 星宿

# 列表
ts.get_wuxing_tags()          # 全部五行
ts.get_bagua_tags()           # 全部八卦
ts.get_oracle_tags()          # 全部甲骨文

# 渲染
ts.render_tag("火·旺", style="html")   # <span style="color:#8B0000" ...>...
ts.render_tag("成", style="md")

# Emoji 解析
ts.resolve_emoji("🔥")        # -> 火·旺
```

---

## 5. CNSH 变量

见 `scripts/cnsh_tag_variables.py`。

示例：
- `$五行.金旺`
- `$八卦.乾`
- `$甲骨文.成`
- `$状态.通行`

---

## 6. 文件清单

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 本文件，技能元数据 |
| `README.md` | 使用说明 |
| `scripts/longhun_tags.py` | 核心标签系统类 |
| `scripts/cnsh_tag_variables.py` | CNSH 变量字典 |
| `data/longhun_emoji_map.json` | emoji 映射表 |

---

## 7. DNA 追溯

```
本技能: #龍芯⚡️2026-07-01-LONGHUN-TAG-SYSTEM-v1.0
来源:   /Users/zuimeidedeyihan/Downloads/Kimi_Agent_通心意译模型更新/longhun_tags.py
作者:   UID9622
```
