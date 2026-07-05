<!-- #龍芯⚡️2026-06-29-CNSH-EDITOR-README-v0.2 -->

# 🌐 CNSH 中文编辑器纠错引擎

基于 `cnsh-editor-rules-v2.0.md` 实现的实战引擎，覆盖老大最痛的**翻译避坑**与**智能修复**场景。

## 已落地规则

| 类别 | 数量 | 代表性规则 |
|---|---|---|
| 01 标点纠错 | 10 | 中英标点转换、顿号、书名号、省略号、破折号 |
| 02 空格规则 | 14 | 中英/中数空格、标点前空格、连续空格压缩 |
| 10 翻译避坑 | 9 | 引号/括号语境、英文冒号空格、列表符号空格 |
| 11 CNSH 特殊语法 | 1 | 中文关键词保留标记 |
| 12 智能修复 | 4 | 句末补句号、标题空格、列表空格、空行压缩 |
| **合计** | **39** | 文档 370 条，覆盖率 10.5% |

## 使用

```bash
# 单句纠错
.venv_longhun_math/bin/python scripts/cnsh_editor_correct.py "我喜欢AI技术,2024年发展很好." --json

# 文件纠错
.venv_longhun_math/bin/python scripts/cnsh_editor_correct.py input.md --file --output output.md
```

## 安全设计

- 自动保护 ```` ``` ```` 代码块、行内代码 `` `code` ``、URL、邮箱，不误改。
- 内置三色审计：检测未闭合引号/括号、潜在 XSS/SQL 注入向量。

## CNSH 卡片

`cnsh-editor-rules.card.json`
