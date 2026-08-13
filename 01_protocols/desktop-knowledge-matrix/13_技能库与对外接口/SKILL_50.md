---
name: longhun-notion-portal
description: "龍魂Notion空间统一入口导航——自动扫描50个页面，按8大类归档（系统核心/数字人/知识库/算法引擎/数据库工具/法律规范/顶刊论文/技术文档），提供本地JSON索引+Markdown导航+Notion入口页面。"
license: CC BY-NC-SA 4.0
metadata:
  version: "5.1"
  dna: "#龍芯⚡️2026-06-26-NOTION-PORTAL-v5.1"
  author: "UID9622"
  language: zh-CN
  triggers:
    - Notion整理
    - Notion入口
    - Notion导航
    - 空间治理
    - 页面归档
    - Notion很乱
    - 帮我整理Notion
---

<!--
君子协议（Zijun Protocol）：
1. 使用时保留DNA追溯链完整
2. 二次修改须标注修订者+时间+摘要
3. 引用须标注六层来源链
六层来源链：L0曾仕强老师 → L1龍魂体系UID9622 → L2Notion空间治理 → L3本地入口 → L4当前会话
-->

# 🌌 龍魂Notion空间统一入口导航 · v5.1

```
#龍芯⚡️2026-06-26-NOTION-PORTAL-v5.1
三色审计: 🟢 50页面归档完成
DNA: #龍芯⚡️2026-06-26-NOTION-PORTAL-v2.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

---

## 1. 快速识别（Trigger Patterns）

当用户说以下话时激活：
- "Notion很乱"
- "帮我整理Notion"
- "Notion入口"
- "页面太乱了"
- "找不到页面"
- "空间治理"

---

## 2. 核心理念（Core Philosophy）

### 入口不是分类，是让水流到该去的地方

> 你的Notion有50个页面，分布在8个类别里。
> 不是页面太多，是没有入口。
> 入口不是做更多分类，是让每个页面都能被找到。

---

## 3. 能力清单（Capability Inventory）

| 能力 | 说明 |
|------|------|
| 自动扫描 | 扫描Notion空间所有页面/数据库 |
| 智能归档 | 按8大类自动分类 |
| 重要度标记 | 🔴核心/🟡重要/🟢补充 |
| 本地索引 | JSON格式本地存储 |
| Markdown导航 | 可阅读的导航文档 |
| Notion入口页 | 在Notion中创建统一入口 |

---

## 4. 使用指引（Usage Guide）

### 4.1 查看本地索引
```bash
# 按类别筛选
cat notion_portal.json | jq '.[] | select(.category=="系统核心")'

# 按状态筛选
cat notion_portal.json | jq '.[] | select(.status | contains("核心"))'

# 搜索关键词
cat notion_portal.json | jq '.[] | select(.title | contains("算法"))'
```

### 4.2 Notion入口页面
- 已创建: 🌌 UID9622 龍魂 Notion 空间 · 统一入口导航 v2.0
- URL: https://www.notion.so/38a7125a9c9f81599505ffcc0cebfd21

---

## 5. 归档结构

```
50个页面 · 8大类
═══════════════════════════════════════════════════

  🔴 系统核心      8个  龍魂心脏（总导航/框架/DNA）
  🤖 数字人        5个  17人格/上下文压缩/身份变量
  📚 知识库        7个  142条CS卡片+45条科技专栏
  ⚙️ 算法引擎      7个  洛书369/不动点/三才/七维
  🛠️ 数据库/工具   7个  DNA库/五行计算器/流水线
  ⚖️ 法律/规范     5个  CNSH法律/君子协议/P0引擎
  📑 顶刊论文       3个  7篇论文规划/白皮书
  📋 技术文档       5个  脚本/API/启动器/归集
  🔮 其他          3个  勋章/知识产权/商业化

═══════════════════════════════════════════════════
```

---

## 6. 输入规范（Input Specification）

| 输入 | 格式 | 示例 |
|------|------|------|
| 新增页面 | JSON | {"id":"...","title":"...","category":"..."} |
| 类别调整 | 字符串 | "从知识库移到算法引擎" |

---

## 7. 输出规范（Output Specification）

| 输出 | 格式 | 路径 |
|------|------|------|
| 索引JSON | JSON | scripts/notion_portal.json |
| 导航Markdown | MD | scripts/notion_portal.md |
| Notion入口页 | Notion Page | https://notion.so/... |

---

## 8. 边界与限制

- 只读索引，不修改Notion页面内容
- 基于标题/关键词自动分类，可能需要人工微调
- 新增页面需手动更新索引

---

## 9. 质量标杆

- 50个页面100%归档
- 8大类覆盖完整
- Notion入口页面可正常访问
- 本地JSON可解析

---

## 10. 关联技能

| 技能 | 关系 | 说明 |
|------|------|------|
| longhun-cs-knowledge-base | 上游 | 142条知识卡片来源 |
| longhun-cn-innovation-kb | 上游 | 45条科技专栏来源 |
| longhun-system | 基础 | DNA追溯+三色审计 |

---

## 11. 版本历史

### v2.0 — 2026-06-26
- 自动扫描50个Notion页面
- 8大类归档
- 创建Notion统一入口页面
- 本地JSON+Markdown双索引

---

## 12. 附录

### 12.1 页面统计
| 指标 | 数值 |
|------|------|
| 总页面 | 50个 |
| 核心 | 28个 |
| 重要 | 19个 |
| 补充 | 3个 |

### 12.2 文件清单
```
longhun-notion-portal/
├── SKILL.md                          # 本文件
└── scripts/
    ├── notion_portal.json            # 50页面索引 (12KB)
    └── notion_portal.md              # Markdown导航 (7KB)
```

---

*DNA: #龍芯⚡️2026-06-26-NOTION-PORTAL-v2.0*
*CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z*
*SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL*
*三色审计: 🟢50页面归档*
*君子协议: CC BY-NC-SA 4.0*

> **「入口不是分类，是让水流到该去的地方。」**
> 50个页面，8大类，28个核心——现在你知道它们在哪了。


---

## 附录：龍魂待整理来源

本技能收录了来自 `/Users/zuimeidedeyihan/龍魂待整理` 的素材：

- **内容**：06-工具脚本（parse_notion.py）
- **中央整合 DNA**：`#龍芯⚡️2026-07-03-LONGHUN-ARCHIVE-INTEGRATION-v1.0`
- **处理方式**：保留原始文件作为 references / examples / scripts，嵌入 DNA 追溯链，与现有能力联动。
