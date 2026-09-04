# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
---
name: longhun-tags
description: >
  龍魂文化标签体系。以五行、八卦、甲骨文、二十八星宿替代西方emoji，
  提供 112+ 个结构化中文标签。入口命令：python3 scripts/longhun_tags.py。
  支持标签查询、渲染（html/md/text/ansi）、emoji 解析、CNSH 变量映射、
  动态扩展、JSON Schema 校验、CSS 设计令牌与组合标签。
  触发关键词：标签、五行、八卦、甲骨文、龍魂标签、CNSH变量、表情包、星宿。
metadata:
  id: longhun-tags
  display_name: 龍魂标签体系
  version: "1.1.0"
  author: UID9622
  dna: "#龍芯⚡️丙午·甲午·丙子·甲午·䷙大畜-LONGHUN-TAG-SYSTEM-v1.1"
  category: internal
  status: active
  entry: "python3 /Users/zuimeidedeyihan/longhun-system/skills/longhun-tags/scripts/longhun_tags.py"
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

# longhun-tags | 龍魂文化标签体系 v1.1

> **DNA**: `#龍芯⚡️丙午·甲午·丙子·甲午·䷙大畜-LONGHUN-TAG-SYSTEM-v1.1`  
> **CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
> **SEAL**: `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`  
> **UID**: 9622 | **版本**: 1.1.0

---

## 1. 一句话定位

用中国传统文化符号（五行、八卦、甲骨文、二十八星宿）替代西方 emoji，
构建 112+ 个可渲染、可组合、可审计、可扩展的龍魂标签。

---

## 2. 标签统计

| 体系 | 数量 | 说明 |
|------|------|------|
| 五行 | 20 | 5 元素 × 4 状态（生/旺/休/囚） |
| 八卦 | 24 | 8 卦 × 3 变体（正/反/动） |
| 甲骨文 | 40 | 状态/情绪/功能/等级 四类 |
| 二十八星宿 | 28 | 四象 × 7 宿 |
| 扩展标签 | 动态 | 通过 `TagExtensionRegistry` 运行时注册 |
| **总计** | **112+** | |

---

## 3. 入口命令

```bash
# 运行演示
python3 /Users/zuimeidedeyihan/longhun-system/skills/longhun-tags/scripts/longhun_tags.py

# 查询 CNSH 变量
python3 /Users/zuimeidedeyihan/longhun-system/skills/longhun-tags/scripts/cnsh_tag_variables.py

# 渲染演示
python3 /Users/zuimeidedeyihan/longhun-system/cnsh-core/longhun_rendering.py
```

---

## 4. Python API

```python
from longhun_tags import LongHunTagSystem

ts = LongHunTagSystem()

# 查询
ts.get_tag("METAL_PEAK")      # 五行标签详情（含 cultural_note）
ts.get_tag("启")              # 甲骨文（含 oracle_context）
ts.get_tag("角")              # 星宿（含 constellation_myth）

# 列表
ts.get_wuxing_tags()          # 全部五行
ts.get_bagua_tags()           # 全部八卦
ts.get_oracle_tags()          # 全部甲骨文
ts.get_xingxiu_tags()         # 全部星宿

# 渲染
ts.render_tag("火·旺", style="html")   # <span style="color:#8B0000" ...>...
ts.render_tag("成", style="md")
ts.render_tag("水·生", style="ansi")   # 24-bit ANSI 彩色

# 组合标签
from longhun_rendering import render_combo_tag
render_combo_tag("火·旺·告警", style="html")

# Emoji 解析
ts.resolve_emoji("🔥")        # -> 火·旺

# 扩展注册表
ts.extensions.register("custom", "CUSTOM_001", {"label": "自定义", "color": "#123456"})
ts.save("data/longhun_tags_state.json")
ts.load("data/longhun_tags_state.json")
```

---

## 5. CNSH 变量

见 `scripts/cnsh_tag_variables.py`。

示例：
- `$五行.金旺`
- `$八卦.乾`
- `$甲骨文.成`
- `$状态.通行`
- `$文化.金.生克`
- `$文化.木.生成`
- `$视觉.金.旺`
- `$视觉.水.囚`

```python
from cnsh_tag_variables import lookup, cultural_note

lookup("$视觉.火.旺")
cultural_note("$文化.土.生克")
```

---

## 6. 文化解释深度

v1.1 针对 小艺 的设计评审，为每个体系增加了文化注解字段：

| 体系 | 新增字段 | 说明 |
|------|----------|------|
| 五行 | `cultural_note` | 元素本性、生克制化与四时气象 rationale |
| 八卦 | `yi_jing_context` | 卦名本义、自然取象、核心德性 |
| 甲骨文 | `oracle_context` | 甲骨字形来源、本义、现代映射 |
| 二十八星宿 | `constellation_myth` | 四象星官神话与司职 |

示例：
- 金：`金曰从革，性收敛肃杀。秋金收敛而春木生发，故金克木……`
- 乾：`name_meaning=健 natural_image=天 virtue=刚健中正，自强不息`
- 启：`甲骨文像以手启户，本义开门，引申为开始、启动。`
- 角：`青龍之角，象征万物萌生，天门初开。`

---

## 7. 视觉统一性

定义标准五行色板并在五行、八卦、星宿中复用：

```json
{
  "金": { "base": "#FFD700", "light": "#FFF8DC", "dark": "#B8860B",
         "peak": "#FFD700", "rest": "#C0C0C0", "trap": "#808080" },
  "木": { "base": "#228B22", "light": "#90EE90", "dark": "#006400",
         "peak": "#006400", "rest": "#8FBC8F", "trap": "#556B2F" },
  "水": { "base": "#1E90FF", "light": "#87CEEB", "dark": "#00008B",
         "peak": "#00008B", "rest": "#4682B4", "trap": "#191970" },
  "火": { "base": "#DC143C", "light": "#FF6347", "dark": "#8B0000",
         "peak": "#8B0000", "rest": "#CD5C5C", "trap": "#800000" },
  "土": { "base": "#8B4513", "light": "#D2B48C", "dark": "#654321",
         "peak": "#8B4513", "rest": "#A0522D", "trap": "#654321" }
}
```

- `data/color_palette.json` 保存规范色板
- 乾、兑同属金，共用 `COLOR_PALETTE["金"]`，避免重复配色
- 五行状态色、八卦主色、CNSH 视觉变量均来自同一色板

---

## 8. 技术扩展性

新增 `TagExtensionRegistry` 支持运行时扩展：

```python
class TagExtensionRegistry:
    def register(self, category, code, data) -> dict
    def validate(self, entry) -> bool
    def export(self, path) -> None
    def load(self, path) -> TagExtensionRegistry
    @property
    def version -> str
```

- `data/tag_schema.json`：扩展条目 JSON Schema
- `LongHunTagSystem.save(path)` / `load(path)`：整系统状态持久化
- 版本元数据：`version=1.1.0`，`last_updated` ISO 8601

---

## 9. CSS / 设计令牌

`data/design_tokens.json` 定义设计令牌，例如：

```
--lh-gold-peak  → #FFD700  金旺态、性能峰值
--lh-water-trap → #191970  水囚态、访问冰封
--lh-radius-sm  → 4px      标签圆角
--lh-font-mono  → ui-monospace, ...
```

`longhun_rendering.py` 提供：
- `render_css_variables()` 生成完整 `:root { ... }` CSS 块
- `render_tag(code, style='ansi')` 输出 24-bit ANSI 彩色
- `render_combo_tag(parts, style='html')` 渲染组合标签

---

## 10. 改进迭代（小艺设计评审落地）

| 小艺建议 | 落地内容 |
|----------|----------|
| 文化解释再深一点 | 五行 `cultural_note`、八卦 `yi_jing_context`、甲骨文 `oracle_context`、星宿 `constellation_myth` |
| 视觉配色统一 | 引入 `COLOR_PALETTE` 标准色板；`color_palette.json`；乾/兑等重复配色归一 |
| 技术扩展与版本 | `TagExtensionRegistry`、JSON Schema、`save/load`、版本与 last_updated |
| 渲染迭代 | 组合标签 `render_combo_tag`、CSS 变量 `render_css_variables`、ANSI 真彩色、设计令牌 |

---

## 11. 文件清单

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 本文件，技能元数据 |
| `README.md` | 使用说明 |
| `scripts/longhun_tags.py` | 核心标签系统类 |
| `scripts/cnsh_tag_variables.py` | CNSH 变量字典 |
| `data/longhun_emoji_map.json` | emoji 映射表 |
| `data/color_palette.json` | 标准五行色板 |
| `data/tag_schema.json` | 扩展条目 JSON Schema |
| `data/design_tokens.json` | CSS/设计令牌 |
| `data/longhun_tags_state.json` | 持久化系统状态（运行时生成） |
| `../../cnsh-core/longhun_rendering.py` | 渲染引擎 |

---

## 12. DNA 追溯

```
本技能: #龍芯⚡️丙午·甲午·丙子·甲午·䷙大畜-LONGHUN-TAG-SYSTEM-v1.1
来源:   /Users/zuimeidedeyihan/Downloads/Kimi_Agent_通心意译模型更新/longhun_tags.py
迭代:   小艺设计评审 v1.1
作者:   UID9622
```
