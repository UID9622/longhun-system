# 龍魂标签体系 | longhun-tags

> DNA: `#龍芯⚡️2026-07-01-LONGHUN-TAG-SYSTEM-v1.0`

## 简介

`longhun-tags` 是龍魂系统的文化标签技能，用中国传统符号替代西方 emoji，
覆盖五行、八卦、甲骨文、二十八星宿四大体系，共 **112 个标签**。

## 快速开始

```bash
python3 scripts/longhun_tags.py
python3 scripts/cnsh_tag_variables.py
```

## 核心能力

- **标签查询**：`get_tag(code)` 支持代码、中文键、组合名
- **分类列表**：`get_wuxing_tags()` / `get_bagua_tags()` / `get_oracle_tags()`
- **多格式渲染**：`render_tag(code, style='html')` 支持 html / md / text / ansi
- **Emoji 解析**：`resolve_emoji(emoji)` 把 🔥✅🚨 等映射为龍魂标签
- **组合验证**：`validate_combo(a, b)` 基于五行生克判断吉凶

## CNSH 变量

在 CNSH 脚本或配置中可直接引用：

```
$五行.金旺
$八卦.乾
$甲骨文.成
$状态.通行
```

变量定义位于 `scripts/cnsh_tag_variables.py`。

## 数据结构

- 五行：`{element, state, symbol, desc, hex, code, usage}`
- 八卦：`{gua, variant, label, state, usage, color}`
- 甲骨文：`{char, category, pinyin, modern, usage, color, tag}`
- 星宿：`{star, beast, position, modern, usage, color, tag}`

## 作者

龍魂系统 · UID9622
