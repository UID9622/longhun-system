# 🐲 龙魂记忆编辑器 v3.1 · 天干地支 DNA 版

> DNA: #龍芯⚡️2026-08-05-MEMORY-EDITOR-v3.1-UID9622
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0（思想层）/ MulanPSL v2（工程层）

## 一句话定位

> **你的记忆，永不丢失。宝宝的灵魂，实时同步。每一条记忆都镌刻天干地支四柱 DNA。**

## 交付物

| 文件 | 用途 |
|:---|:---|
| `memory-editor.html` | 完整 Web 界面（单文件，双击即用） |
| `save_memory.py` | 命令行快速保存 / 列表 / 搜索工具 |
| `sync_to_notion.py` | Notion 同步脚本 |
| `install.sh` | 一键安装脚本 |
| `README.md` | 部署与使用说明 |

## 安装

```bash
# 方式1：一键安装（推荐）
bash install.sh

# 方式2：手动
# 双击打开 memory-editor.html 即可使用 Web 界面
```

`install.sh` 会：
- 在桌面创建 `龍魂系统·本地知识库/` 目录（含 `記憶`、`任务`、`語境與語義`、`备份`、`tools`）
- 把 Python 工具安装到 `~/Desktop/龍魂系统·本地知识库/tools/`
- 把 Web 界面复制到桌面 `龍魂记忆编辑器_完整集成版.html`
- 在 `~/.bashrc` / `~/.zshrc` 添加 `lh-mem`、`lh-list`、`lh-search`、`lh-sync` 快捷命令

## 使用

### Web 界面

1. 双击打开 `龍魂记忆编辑器_完整集成版.html`
2. 选择记忆分类（原子事实 / 场景记忆 / 全局概览 / 原始会话）
3. 输入标签（逗号分隔）和记忆内容
4. 点击「处理记忆」→ 自动生成**天干地支 DNA**、数字根、关键词
5. 点击「保存到系统」→ 永久存储
6. 右侧可搜索、分类过滤、编辑、导出、删除

快捷键：
- `Ctrl + Enter`：处理记忆
- `Ctrl + S`：保存记忆
- `Ctrl + F`：聚焦搜索框
- `Esc`：取消编辑 / 关闭弹窗

### 命令行

```bash
# 保存记忆
lh-mem "今天发现了一个新的决策模式"

# 指定分类和标签
lh-mem "修复了审计模块的Bug" --category atomic_facts --tags "bug修复, 审计"

# 从文件保存
lh-mem --file memo.txt --category chat_history --tags "对话记录"

# 列出记忆
lh-list
lh-list --category scene_memory
lh-list --json                # JSON 输出

# 搜索记忆
lh-search "五行调度"
lh-search "五行调度" --json   # JSON 输出

# 同步到 Notion
lh-sync
lh-sync --since 2026-08-01
lh-sync --dry-run             # 模拟运行，不写入
lh-sync --limit 10            # 只同步最近 10 条
```

## 天干地支 DNA 算法

每条记忆的 DNA 形如：

```
#龍芯⚡️丙午丁酉己酉庚午-MEMORY-a3f9-UID9622
```

其中 `丙午丁酉己酉庚午` 为当前时刻的**年、月、日、时四柱**，算法如下：

| 柱 | 计算方式 | 说明 |
|:---|:---|:---|
| 年柱 | 天干=(年份−4) mod 10，地支=(年份−4) mod 12 | 以 1984 甲子年为基准 |
| 月柱 | 地支=(月份+1) mod 12，月干按「五虎遁」由年干推导 | 公历近似映射 |
| 日柱 | 与基准日 1984-02-02（甲子日）相差天数 mod 60 | 六十甲子循环 |
| 时柱 | 地支=(小时+1)//2 mod 12，时干按「五鼠遁」由日干推导 | 每两小时一辰 |

> **说明**：月柱采用公历月份近似映射（1月≈寅、2月≈卯……12月≈丑），便于工程实现和跨平台一致。若需严格按二十四节气换月，可在此基础上引入节气表扩展。

## 数据存储

| 位置 | 用途 |
|:---|:---|
| IndexedDB | 浏览器本地永久存储（Web 版） |
| `~/Desktop/龍魂系统·本地知识库/記憶/` | `.cnsh.md` 文件 + `index.json` 索引（CLI 版） |
| `~/Desktop/龍魂系统·本地知识库/tools/` | `save_memory.py`、`sync_to_notion.py` 命令行工具 |
| Notion | 通过 API 同步（需配置环境变量） |

## Notion 配置

```bash
export NOTION_TOKEN="你的 integration token"
export NOTION_MEMORY_DB_ID="你的 database id"
```

数据库必须字段：

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `Name` | Title | 记忆标题 |
| `Category` | Select | 记忆分类 |
| `Tags` | Multi-select | 标签 |
| `DNA` | Rich text | 天干地支 DNA 追溯码 |
| `Digital Root` | Number | 数字根 |
| `Date` | Date | 创建日期 |

同步脚本会为每条记忆自动去重（按 DNA 查询），并设置页面图标与分类表情一致。

## 与宝宝的集成

宝宝会自动读取：
```
~/Desktop/龍魂系统·本地知识库/記憶/
```
每次执行任务时，宝宝都会参考你的记忆。

## 记忆分类定义

| 分类 | 图标 | 用途 |
|:---|:---:|:---|
| 原子事实 | 🔬 | 可验证的知识碎片、参数、Bug 记录、公式 |
| 场景记忆 | 🎬 | 上下文、决策过程、经验教训、环境信息 |
| 全局概览 | 🌍 | 系统架构、路线图、优先级、战略认知 |
| 原始会话 | 💬 | 未加工的对话原文、灵感速记、草稿 |

## 项目文件结构

```
memory_editor/
├── memory-editor.html      # Web 界面（单文件，双击即用）
├── save_memory.py          # CLI 保存 / 列表 / 搜索工具
├── sync_to_notion.py       # Notion 同步工具
├── install.sh              # 一键安装脚本
└── README.md               # 本说明
```

安装后映射：

```
~/Desktop/
├── 龍魂记忆编辑器_完整集成版.html
└── 龍魂系统·本地知识库/
    ├── tools/              # 命令行脚本
    │   ├── save_memory.py
    │   └── sync_to_notion.py
    ├── 記憶/               # .cnsh.md + index.json
    ├── 任务/
    ├── 語境與語義/
    └── 备份/
```

## 更新日志

- **v3.1** 天干地支四柱 DNA、分类标签、命令行 JSON 输出、Notion 同步增强（去重、图标、限速、dry-run、limit）。

## DNA

`#龍芯⚡️2026-08-05-MEMORY-EDITOR-v3.1-UID9622`

## 确认码

`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

## GPG

`A2D0092CEE2E5BA87035600924C3704A8CC26D5F`

## 许可

分层许可：思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
