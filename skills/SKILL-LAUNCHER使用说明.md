<!--#龍芯⚡️2026-06-21-DOC-SKILL-LAUNCHER_97F1-v1.0-3 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

# SKILL-LAUNCHER.sh 使用说明

> **DNA签名**: `UID9622⚡️2026-06-16-SKILL-LAUNCHER-v3.0`
>
> **确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
>
> **体系**: 龍芯北辰·诸葛鑫 — 龍魂工具库

---

## 一、概述

`SKILL-LAUNCHER.sh` 是龍魂工具库的一键启动脚本，支持同时或分批启动全部10个工具（5个HTML工具 + 5个Python工具），严格遵循**忠(0.5) > 孝(0.3) > 义(0.2)** 排序铁律。

### 功能特性

| 功能 | 说明 |
|------|------|
| 全平台支持 | macOS / Linux 原生支持 |
| 环境自动检测 | 自动检测Python、浏览器、文件等依赖 |
| 多种启动模式 | 全部启动 / 仅HTML / 仅Python / 单个工具 |
| 优先级排序启动 | 忠(0.5) → 孝(0.3) → 义(0.2) 分批启动 |
| 彩色状态输出 | 三色审计：🟢通过 🟡标记 🔴阻断 |
| 启动日志记录 | 自动生成时间戳日志到 `logs/` 目录 |
| 优雅停止 | 支持 `--stop` 优雅终止所有已启动工具 |
| 健康检查 | 内置8项系统健康检查 |
| 信号处理 | Ctrl+C 安全退出，自动清理子进程 |
| 干运行模式 | `--dry-run` 测试配置不实际启动 |

---

## 二、快速开始

### 2.1 前置要求

- **操作系统**: macOS 10.14+ / Linux (Ubuntu 18.04+/CentOS 7+)
- **Bash**: 4.0+
- **Python**: 3.7+ (Python工具需要)
- **浏览器**: Chrome/Firefox/Safari/Edge (HTML工具需要)

### 2.2 目录结构

```
SKILL-LAUNCHER.sh
assets/
├── skill-1-algorithmic-art.html      # 算法艺术生成器
├── skill-2-brand-guidelines.html     # 龍魂品牌指南
├── skill-3-canvas-design.html        # 画布设计工具
├── skill-4-doc-coauthoring.html      # 文档协作工具
├── skill-5-internal-comms.html       # 内部通讯系统
├── skill-6-mcp-builder.py            # MCP服务器构建器
├── skill-7-skill-creator.py          # 技能创建框架
├── skill-8-slack-gif-creator.py      # Slack GIF生成器
├── skill-9-theme-factory.py          # 主题工厂
└── skill-10-web-artifacts-builder.py # Web工件构建器
logs/                                 # 日志目录 (自动生成)
```

### 2.3 基本使用

```bash
# 赋予执行权限
chmod +x SKILL-LAUNCHER.sh

# 启动全部工具 (默认)
./SKILL-LAUNCHER.sh

# 仅启动HTML工具
./SKILL-LAUNCHER.sh --html-only

# 仅启动Python工具
./SKILL-LAUNCHER.sh --python-only

# 启动指定工具
./SKILL-LAUNCHER.sh --tool 1
./SKILL-LAUNCHER.sh --tool 7

# 启动多个指定工具 (逗号分隔)
./SKILL-LAUNCHER.sh --tool 1,7,9

# 干运行模式 (测试不实际启动)
./SKILL-LAUNCHER.sh --dry-run

# 健康检查
./SKILL-LAUNCHER.sh --health-check

# 查看运行状态
./SKILL-LAUNCHER.sh --status

# 优雅停止所有工具
./SKILL-LAUNCHER.sh --stop

# 显示帮助
./SKILL-LAUNCHER.sh --help
```

---

## 三、命令行参数详解

### 3.1 启动模式参数

| 参数 | 简写 | 说明 |
|------|------|------|
| `--all` | `-a` | 启动全部10个工具 (默认模式) |
| `--html-only` | `-H` | 仅启动5个HTML工具 (编号1-5) |
| `--python-only` | `-P` | 仅启动5个Python工具 (编号6-10) |
| `--tool <编号>` | `-t <编号>` | 启动指定编号的工具，支持逗号分隔多选 |

### 3.2 附加选项参数

| 参数 | 简写 | 说明 |
|------|------|------|
| `--dry-run` | `-d` | 干运行模式，模拟启动流程不实际执行 |
| `--verbose` | `-v` | 详细输出模式，显示更多信息 |
| `--no-browser` | `-n` | 不自动打开浏览器 (仅影响HTML工具) |
| `--stop` | `-s` | 优雅停止所有已启动的工具进程 |
| `--status` | - | 显示当前已启动工具的运行状态 |
| `--health-check` | - | 执行8项系统健康检查 |
| `--help` | `-h` | 显示帮助信息 |
| `--version` | `-V` | 显示版本和DNA签名信息 |

---

## 四、工具清单

### 4.1 HTML工具 (浏览器打开)

| 编号 | 工具名称 | 文件名 | 功能描述 | 优先级 |
|------|---------|--------|---------|--------|
| 1 | algorithmic-art | `skill-1-algorithmic-art.html` | 算法艺术生成器 | 忠(0.5) |
| 2 | brand-guidelines | `skill-2-brand-guidelines.html` | 龍魂品牌指南 | 忠(0.5) |
| 3 | canvas-design | `skill-3-canvas-design.html` | 画布设计工具 | 孝(0.3) |
| 4 | doc-coauthoring | `skill-4-doc-coauthoring.html` | 文档协作工具 | 孝(0.3) |
| 5 | internal-comms | `skill-5-internal-comms.html` | 内部通讯系统 | 义(0.2) |

### 4.2 Python工具 (命令行启动)

| 编号 | 工具名称 | 文件名 | 功能描述 | 优先级 |
|------|---------|--------|---------|--------|
| 6 | mcp-builder | `skill-6-mcp-builder.py` | MCP服务器构建器 | 忠(0.5) |
| 7 | skill-creator | `skill-7-skill-creator.py` | 技能创建框架 | 忠(0.5) |
| 8 | slack-gif-creator | `skill-8-slack-gif-creator.py` | Slack GIF生成器 | 孝(0.3) |
| 9 | theme-factory | `skill-9-theme-factory.py` | 主题工厂 | 孝(0.3) |
| 10 | web-artifacts-builder | `skill-10-web-artifacts-builder.py` | Web工件构建器 | 义(0.2) |

### 4.3 启动顺序

启动严格按照优先级分批执行：

```
第一批 (忠 0.5): #1 → #2 → #6 → #7    [核心工具优先]
第二批 (孝 0.3): #3 → #4 → #8 → #9    [重要工具次之]
第三批 (义 0.2): #5 → #10             [辅助工具最后]
```

---

## 五、输出与日志

### 5.1 控制台输出

脚本使用彩色输出显示状态：

```
[ℹ️ INFO]  信息提示 — 蓝色
[✅ OK  ]  操作成功 — 绿色
[⚠️ WARN]  警告提示 — 黄色
[❌ ERR ]  错误提示 — 红色
[🧬 DNA ]  DNA签名 — 品红色
[⚡ STEP]  执行步骤 — 青色
[📊 AUDIT] 审计标记 — 青色
```

### 5.2 日志文件

日志保存在 `logs/skill-launcher-YYYYMMDD-HHMMSS.log`，包含：
- 时间戳
- 日志级别
- 操作详情
- DNA签名
- 启动统计

### 5.3 PID文件

启动过程中会创建 `logs/.skill-launcher.pid` 记录所有子进程信息，用于：
- 状态查询 (`--status`)
- 优雅停止 (`--stop`)
- 信号清理

---

## 六、健康检查

执行 `./SKILL-LAUNCHER.sh --health-check` 会进行以下8项检查：

| 序号 | 检查项 | 说明 |
|------|--------|------|
| 1 | DNA签名验证 | 验证脚本完整性 |
| 2 | Python环境 | 检测Python3/Python可用性 |
| 3 | 浏览器环境 | 检测系统浏览器 |
| 4 | 资源目录 | 检查assets目录存在性 |
| 5 | 工具文件 | 检查10个工具文件完整性 |
| 6 | 日志系统 | 检查日志目录可写性 |
| 7 | 磁盘空间 | 检查磁盘使用是否超过90% |
| 8 | 网络连接 | 检测外网连通性 |

健康检查结果的判定：
- **80%以上通过** → 🟢系统状态良好
- **50%-80%通过** → 🟡系统部分可用
- **50%以下通过** → 🔴系统需要修复

---

## 七、常见问题

### Q1: 提示"Permission denied"

```bash
chmod +x SKILL-LAUNCHER.sh
```

### Q2: 找不到Python环境

确保已安装Python 3.7+ 且 `python3` 或 `python` 命令可用：

```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt-get install python3

# CentOS/RHEL
sudo yum install python3
```

### Q3: HTML工具没有自动打开浏览器

- 检查系统是否安装了浏览器
- 使用 `--no-browser` 参数跳过自动打开，手动访问文件
- 在WSL等环境中可能需要手动配置浏览器路径

### Q4: 如何查看工具输出

Python工具的输出会自动重定向到日志文件：

```bash
tail -f logs/skill-launcher-*.log
```

### Q5: 停止后工具仍在运行

```bash
# 强制停止所有Python进程
pkill -f "skill-6\|skill-7\|skill-8\|skill-9\|skill-10"

# 或者查找并终止
ps aux | grep skill-
kill -9 <PID>
```

---

## 八、DNA签名与体系规范

### 8.1 DNA签名

```
UID9622⚡️2026-06-16-SKILL-LAUNCHER-v3.0
```

### 8.2 确认码

```
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

### 8.3 排序铁律

所有工具按优先级分三批启动：
- **忠(0.5)**: 核心基础设施工具，最先启动
- **孝(0.3)**: 重要业务工具，第二批启动
- **义(0.2)**: 辅助支持工具，最后启动

### 8.4 CNSH规范

脚本遵循CNSH中文编程规范：
- 注释使用中文
- 变量命名语义化
- 代码结构清晰分层
- 三色审计贯穿全脚本

---

## 九、版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v3.0 | 2026-06-16 | 当前版本，完整10工具支持 |

---

## 十、联系方式

- **体系**: 龍芯北辰·诸葛鑫 — UID9622
- **项目**: 龍魂工具库 SKILL-LAUNCHER
- **签名**: `UID9622⚡️2026-06-16-SKILL-LAUNCHER-v3.0`

---

> *龍魂所至，万技归宗。*
