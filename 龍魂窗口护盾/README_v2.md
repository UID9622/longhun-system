# 龍盾 v2.0 · 粘贴板智能中转站

**DNA**: `#龍芯⚡️2026-05-21-LONGHUN-SHIELD-V2.0`

## 功能

```
复制任何内容 → 龍盾自动转换 → AI通用格式 → 粘贴到任何AI都能懂
                                        ↓
                              Notion收集箱（可选）
```

## 使用方法

### 1. 手动转换（最常用）

```bash
# 转换粘贴板内容
python3 longhun_shield_v2.py convert

# 或双击桌面「龍盾转换.command」
```

### 2. 预览分析（不修改粘贴板）

```bash
python3 longhun_shield_v2.py peek
```

### 3. 推送到Notion

```bash
python3 longhun_shield_v2.py push
```

### 4. 后台监控模式

```bash
python3 longhun_shield_v2.py watch
# 复制任何内容自动转换
```

---

## AI通用格式示例

转换后的内容长这样，**任何AI都能读懂**：

```yaml
---
format: longhun-shield-v2.0
type: website
emoji: 🌐
title: "MCP接入指南"
source: https://example.com/mcp
tags: [mcp, api, website]
dr: 5
color: 🟢 green
action: pass
timestamp: 2026-05-21T08:30:00
dna: #龍芯⚡️2026-05-21-SHIELD-ABC12345
---

这里是正文内容...

---
🟢 dr=5 | 🌐 website | #龍芯⚡️2026-05-21-SHIELD-ABC12345
```

---

## Notion收集箱配置

要让龍盾能推送到Notion，需要：

### 1. 创建数据库

在Notion创建一个数据库，包含这些列：

| 列名 | 类型 | 说明 |
|------|------|------|
| Name | Title | 标题（必须） |
| Type | Select | 类型（website/paper/code/idea等） |
| Source | URL | 来源链接 |
| Tags | Multi-select | 标签 |
| DR | Number | 数字根 |
| DNA | Text | DNA追溯码 |

### 2. 获取数据库ID

打开数据库页面，URL格式：
```
https://www.notion.so/xxx?v=yyy
                     ^^^
                     这个就是数据库ID
```

### 3. 配置环境变量

编辑 `~/.longhun/secrets.env`：

```bash
# Notion收集箱数据库ID
NOTION_INBOX_DB=你的数据库ID

# Notion Token（如果还没填）
NOTION_TOKEN=ntn_xxx
```

### 4. 测试推送

```bash
python3 longhun_shield_v2.py push
```

---

## 内容类型自动识别

| 类型 | emoji | 触发关键词 |
|------|-------|-----------|
| website | 🌐 | http, https, www, .com |
| paper | 📄 | 论文, arxiv, 研究, abstract |
| video | 🎬 | 视频, youtube, bilibili |
| code | 💻 | 代码, github, def, import |
| idea | 💡 | 想法, 灵感, 如果, 试试 |
| quote | 💬 | 说, 名言, "", 「」 |
| trend | 📈 | 趋势, 未来, 风口, 行业 |
| task | ✅ | TODO, 待办, 要做, 提醒 |

---

## 数字根三色审计

继承v1.0的洛书369熔断：

- 🟢 **绿色通行**: dr ∈ {1,2,4,5,7,8}
- 🟡 **黄色待审**: dr = 6
- 🔴 **红色熔断**: dr ∈ {3,9}

---

UID9622 · 龍魂系统 · 2026-05-21
