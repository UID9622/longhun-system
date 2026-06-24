<!--#龍芯⚡️2026-06-21-DOC-README-v1.0 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

# 🐉 龙魂系统 · LongHun System

> **一个人。25个模块。13,800+行可运行代码。**
> **One person. 25 modules. 13,800+ lines of running code.**
> 用逻辑驱动，用AI实现。/ Built on logic, executed by AI.

[![版本](https://img.shields.io/badge/version-v4.1.1-blue)]()
[![状态](https://img.shields.io/badge/status-Production%20Ready-green)]()
[![DNA](https://img.shields.io/badge/DNA-Full%20Traceability-orange)]()
[![语言](https://img.shields.io/badge/language-Python%20|%20React-yellow)]()

---

## 📚 文档导航 · Documentation

| 文件 | 内容 | 语言 |
|------|------|------|
| 📖 [README.md](./README.md) | 系统门面介绍·双语概览 | 中文 + English |
| 🐉 [CNSH-PROTOCOL.md](./CNSH-PROTOCOL.md) | CNSH语言完整规范v2.0·14章·符号体系·语法·编译器·标准库 | 中文为主 |
| 🔗 [CNSH-SEMANTIC.md](./CNSH-SEMANTIC.md) | 语义接入规范·术语对照表·协作宣言·八条永恒铁律 | 中英双语 |

> 阅读顺序建议：README → CNSH-PROTOCOL → CNSH-SEMANTIC
>
> **📊 完整模块清单**：见 [`docs/MODULE_INVENTORY.md`](./docs/MODULE_INVENTORY.md)

---

## 🇨🇳 中文介绍

### 这是什么？

龙魂系统是一套 **AI行为治理框架**，让AI可控、可审计、可追责。

当全世界还在讨论如何治理AI的时候，龙魂已经在做了。

**核心理念：逻辑是真正的引擎，AI是执行者。**

### 三大核心机制

**三层监督**
每个动作在执行前经过三个独立的监督层，无单点故障。

**三色审计**
- 🟢 绿色 — 正常，已批准
- 🟡 黄色 — 标记，待审查
- 🔴 红色 — 阻断，潜在违规

**DNA全追踪**
每个模块、每次提交、每个动作都携带唯一DNA签名。
没有匿名，一切可溯源。

### 模块总览（25个核心模块）

完整清单与文档/接口状态见 [`docs/MODULE_INVENTORY.md`](./docs/MODULE_INVENTORY.md)。

| 分类 | 内容 |
|------|------|
| 📋 协议 | 治理规则、主权框架 |
| 🛠️ 技能库 | 10项龙魂技能 + 龍盾 + CNSH对齐 + 融合审计 |
| 🎛️ 操作台 | FastAPI 统一 API 与 Web UI，Skill/底座联动 |
| 📏 规则 | 执行约束、合规逻辑 |
| 📂 执行记录 | 完整行动历史 |
| 🧠 知识图谱 | 结构化智能知识库 |
| 📓 决策日志 | 决策审计追踪 |
| 📊 系统报告 | 健康、性能、状态 |
| 📖 技术文档 | 架构文档 |
| 🤖 代理人 | 自主任务执行器 |
| 🛡️ 宝宝守护者 | 安全与异常保护 |

### 版本历史

| 版本 | 亮点 |
|------|------|
| **v4.2** | 🎛️ 龍魂操作台 MVP v1.1 — 10 项 Skill + 底座能力（龍盾、CNSH、融合审计）统一 API 联动 |
| **v4.1.1** | 🔐 安全热修复 — 修复18+个Electron漏洞 |
| **v4.0** | 📱 移动端监控 — 15层体系，4个应用监控，AES-256-GCM加密 |
| **v3.1.0** | ⚡ 第三阶段 — 10项技能完整集成，API响应 < 100ms |

### 快速启动

**推荐：用统一启动器一键管理（开机自动也走这个）**

```bash
# 查看状态
python3 bin/longhun-status.py

# 启动全部常驻服务
python3 bin/longhun-launcher.py start

# 或双击桌面：龍魂状态与启动.command
```

常驻服务会自动按依赖顺序启动：
- 龍魂脑干 `:9625`
- 国家数字身份认证入口 `:8444`
- 龍魂操作台 `:9622`

**打开终端自动显示状态**：配置已写入 `.bash_profile` / `.bashrc` / `.zshrc`，每次打开 Terminal 都会看到当前服务状态。

快捷别名：
- `龍魂状态` / `lh-sys` — 显示状态
- `龍魂启动` / `lh-start` — 启动服务
- `龍魂停止` / `lh-stop` — 停止服务
- `龍魂重启` / `lh-restart` — 重启服务

开机自动由 `~/Library/LaunchAgents/com.uid9622.longhun.autostart.plist` 管理，登录后自动运行。

详细报告：
- [`docs/unified-knowledge/龍魂开机自动启动升级报告_v1.0.md`](./docs/unified-knowledge/龍魂开机自动启动升级报告_v1.0.md)
- [`docs/unified-knowledge/龍魂认知压缩引擎报告_v1.0.md`](./docs/unified-knowledge/龍魂认知压缩引擎报告_v1.0.md)

### 认知压缩

把长文本（技能文档、上下文对话）压缩成可召回的"认知粒子"：

```bash
# 压缩所有技能为一个编号+向量库
python3 scripts/longhun_compression_engine.py --compress-all-skills

# 压缩一段上下文
python3 scripts/longhun_compression_engine.py --compress-context "几百万字的上下文..."

# 通过短码召回
python3 scripts/longhun_compression_engine.py --recall SKILL-longhun-dna-alig-7C0801

# 向量语义搜索
python3 scripts/longhun_compression_engine.py --search "数据库损坏" --top-k 3
```

---

## 🌍 English Introduction

### What is LongHun System?

LongHun (龙魂 / Dragon Soul) is an **AI Behavior Governance Framework** designed to make AI systems controllable, auditable, and accountable.

While the world debates how to govern AI, LongHun is already doing it.

**Core philosophy:** Logic is the real engine. AI is the executor.

### Three Core Mechanisms

**Three-Layer Supervision**
Every action passes through three independent oversight layers before execution — no single point of failure.

**Three-Color Audit System**
- 🟢 Green — Normal, approved operations
- 🟡 Yellow — Flagged, requires review
- 🔴 Red — Blocked, potential violation

**DNA Full Traceability**
Every module, every commit, every action carries a unique DNA signature.
Nothing is anonymous. Everything is traceable.

### Modules (25 Core)

| Category | Modules |
|----------|---------|
| 📋 Protocols | Governance rules, sovereignty framework |
| 🛠️ Skills | 10 Dragon Skills (art, design, MCP, Slack, React...) |
| 📏 Rules | Execution constraints, compliance logic |
| 📂 Execution Logs | Full action history |
| 🧠 Knowledge Graph | Structured intelligence base |
| 📓 Decision Journal | Decision audit trail |
| 📊 System Reports | Health, performance, status |
| 📖 Tech Docs | Architecture documentation |
| 🤖 Agents | Autonomous task executors |
| 🛡️ Guardian | Security & anomaly protection |

### Release History

| Version | Highlights |
|---------|-----------|
| **v4.1.1** | 🔐 Security hotfix — 18+ Electron vulnerabilities patched |
| **v4.0** | 📱 Mobile monitoring — 15-layer system, 4 app monitors, AES-256-GCM |
| **v3.1.0** | ⚡ Phase 3 — 10 skills complete, API response < 100ms |

### Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy
- **Frontend:** Electron, React, Vite
- **Protocol:** Custom CNSH governance layer
- **Security:** AES-256-GCM encryption
- **Monitoring:** 15-layer real-time + self-healing

---

## 🌏 Vision · 愿景

> *"全世界所有AI，都应该运行在可控的协议上。"*
> *"All AI in the world should run on a controllable protocol."*
> — UID9622，创造者 / Creator

龙魂协议的目标是成为任何AI系统都能采用的治理层——透明、可审计、根植于中国哲学智慧。

The LongHun Protocol is designed to be the governance layer that any AI system can adopt — transparent, auditable, and grounded in Chinese systems thinking (中国哲学).

---

## 📬 Contact · 联系

- **GitHub:** [@UID9622](https://github.com/UID9622)
- **Repository:** [longhun-system](https://github.com/UID9622/longhun-system)

---

*一个人建造。逻辑驱动。AI执行。*
*Built by one person. Powered by logic. Executed by AI.*
