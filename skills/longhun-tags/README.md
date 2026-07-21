# 龍魂标签体系 | longhun-tags

> DNA: `#龍芯⚡️2026-07-01-LONGHUN-TAG-SYSTEM-v1.1`  
> 版本: 1.1.0

## 简介

`longhun-tags` 是龍魂系统的文化标签技能，用中国传统符号替代西方 emoji，
覆盖五行、八卦、甲骨文、二十八星宿四大体系，共 **112+ 个标签**。

v1.1 按 小艺 设计评审进行了迭代：深化文化解释、统一视觉配色、支持动态扩展与 CSS 设计令牌。

## 快速开始

```bash
python3 scripts/longhun_tags.py
python3 scripts/cnsh_tag_variables.py
python3 ../../cnsh-core/longhun_rendering.py
```

## 核心能力

- **标签查询**：`get_tag(code)` 支持代码、中文键、组合名
- **分类列表**：`get_wuxing_tags()` / `get_bagua_tags()` / `get_oracle_tags()` / `get_xingxiu_tags()`
- **多格式渲染**：`render_tag(code, style='html')` 支持 html / md / text / **ansi**
- **组合标签**：`render_combo_tag(parts, style='html')` 渲染如 `火·旺·告警`
- **CSS 变量**：`render_css_variables()` 生成 `:root` 自定义属性
- **Emoji 解析**：`resolve_emoji(emoji)` 把 🔥✅🚨 等映射为龍魂标签
- **组合验证**：`validate_combo(a, b)` 基于五行生克判断吉凶
- **动态扩展**：`TagExtensionRegistry` + `save(path)` / `load(path)`

## 文化解释深度

v1.1 为每个标签体系补充了文化注解：

- **五行**：`cultural_note` —— 生克制化与四时气象 rationale
- **八卦**：`yi_jing_context` —— 卦名本义、自然取象、核心德性
- **甲骨文**：`oracle_context` —— 甲骨字形来源、本义、现代映射
- **二十八星宿**：`constellation_myth` —— 四象星官神话

## 视觉统一性

标准五行色板（`data/color_palette.json`）：

| 元素 | 主色 | 旺态 | 囚态 |
|------|------|------|------|
| 金 | `#FFD700` | `#FFD700` | `#808080` |
| 木 | `#228B22` | `#006400` | `#556B2F` |
| 水 | `#1E90FF` | `#00008B` | `#191970` |
| 火 | `#DC143C` | `#8B0000` | `#800000` |
| 土 | `#8B4513` | `#8B4513` | `#654321` |

五行、八卦、CNSH 视觉变量均来自同一色板；乾/兑同金共用金调色板。

## 技术扩展性

- `TagExtensionRegistry.register(category, code, data)` 动态注册标签
- `validate(entry)` 按分类最小字段 + hex 颜色校验
- `export(path)` / `load(path)` 导入导出扩展条目
- `LongHunTagSystem.save(path)` / `load(path)` 持久化整系统状态
- `data/tag_schema.json` 提供 JSON Schema 校验依据

## CSS / 设计令牌

`data/design_tokens.json` 定义 `--lh-*` 令牌：

```
--lh-gold-peak  #FFD700
--lh-wood-birth #90EE90
--lh-water-trap #191970
--lh-fire-rest  #CD5C5C
--lh-radius-sm  4px
```

`render_css_variables()` 可直接生成完整 CSS 变量块供前端消费。

## CNSH 变量

在 CNSH 脚本或配置中可直接引用：

```
$五行.金旺
$八卦.乾
$甲骨文.成
$状态.通行
$文化.金.生克
$文化.木.生成
$视觉.金.旺
$视觉.水.囚
```

变量定义位于 `scripts/cnsh_tag_variables.py`，新增 `cultural_note(var)` helper。

## 数据结构

- 五行：`{element, state, symbol, desc, hex, code, usage, cultural_note}`
- 八卦：`{gua, variant, label, state, usage, color, palette, yi_jing_context}`
- 甲骨文：`{char, category, pinyin, modern, usage, color, tag, oracle_context}`
- 星宿：`{star, beast, position, modern, usage, color, tag, constellation_myth}`

## 改进迭代

按 小艺 设计评审完成：

1. 增加 `cultural_note` / `yi_jing_context` / `oracle_context` / `constellation_myth`
2. 引入 `COLOR_PALETTE` 标准色板，统一五行/八卦/星宿/CNSH 视觉变量
3. 新增 `TagExtensionRegistry`、JSON Schema、版本与状态持久化
4. 渲染层新增组合标签、CSS 变量、ANSI 真彩色、设计令牌

## 作者

龍魂系统 · UID9622
