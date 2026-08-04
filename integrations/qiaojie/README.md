# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🍎 乔接 QiaoJie CLI · 集成文档

> P15 乔前辈出品 · 中英双轨 · 数字根熔断 · Notion+小艺双API桥接

DNA(v∞): `#龍芯⚡️丙午·乙未·癸未·辰时·䷾既济-QIAOJIE-CLI-v1.1`
确认码: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

## 概览

乔接 CLI 是 P15 乔前辈生态的核心 CLI 工具，实现：

- **中英双轨**：中文语义抽屉（随便说）∥ 英文精准指令（二进制）
- **数字根熔断**：每次执行前计算输入的数字根 dr，dr∈{3,9} 熔断，dr=6 待审
- **Notion API 桥接**：搜索 Notion 页面、获取元数据
- **小艺 API 桥接**：通过本地操作台(9622)调用 AI 问答
- **系统健康检查**：检查操作台、人格API、Ollama 在线状态

---

## 安装

```bash
pip install python-dotenv requests
```

配置 Notion Token：
```bash
echo 'NOTION_TOKEN=your_token_here' >> ~/.cnsh/.env
```

---

## 中文指令表

| 你可以说 | 实际执行 | 说明 |
|:---|:---|:---|
| `帮助` / `怎么用` | `help` | 显示帮助 |
| `搜索 <名称>` / `查页面 <名称>` / `找 <名称>` | `search` | Notion页面搜索 |
| `问 <问题>` / `问一下 <问题>` | `ask` | 小艺AI问答 |
| `状态` / `健康` | `status` | 系统健康检查 |
| `同步` | `sync` | 触发全局同步 |
| `时间` / `几点了` | `time` | 显示当前北京时间 |

## 英文指令表

| Command | 说明 |
|:---|:---|
| `help` | Show help |
| `search <name>` | Search Notion page |
| `ask <query>` | Ask XiaoYi AI |
| `status` / `health` | System health check |
| `sync` | Trigger global sync |
| `time` | Current time |

---

## 架构

```
用户输入（中文/英文）
  ├ 数字根计算 → 熔断判定
  │   ├ dr∈{3,9} → 🔴熔断·拒绝
  │   ├ dr=6     → 🟡待审·确认
  │   └ 其他      → 🟢通行
  ├ 语义抽屉匹配 → 命令路由
  │   ├ 搜索指令 → Notion API
  │   ├ 问答指令 → 小艺 API (localhost:9622)
  │   └ 系统指令 → 本地检查
  └ 结果输出 → 中英双语格式化
```

---

## 数值约定

| 约定 | 说明 |
|:---|:---|
| **dr** | 数字根(digital root)，输入文本的Unicode码点求和→反复位数相加至1-9 |
| **熔断 dr∈{3,9}** | 一票否决，拒绝执行 |
| **待审 dr=6** | 标黄，需人工确认 |
| **通行** | 其余数字根，正常执行 |

---

## 依赖

- Python 3.12+
- `requests` (Notion API / 小艺API)
- `python-dotenv` (加载 ~/.cnsh/.env)
- 本地 9622 端口 (操作台API，用于小艺问答)

---

## 金句

> 乔前辈：把复杂变简单 · 你随便说 · 我替你译成机器懂的话 · 跑不了帮你改到跑

🧬 `#龍芯⚡️丙午·乙未·癸未·辰时·䷾既济-QIAOJIE-CLI-v1.1`
