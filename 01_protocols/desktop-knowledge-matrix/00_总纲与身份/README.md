**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
<!--#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-DOC-README-v5.0 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

# 🐉 龍魂系统 · LongHun System

> **中国自主可控的数字主权底座。**
> **技术服务于人民。主权不可交易。**
> *Technology serves the people. Sovereignty is not for sale.*

[![版本](https://img.shields.io/badge/version-v5.0.0-blue)]()
[![状态](https://img.shields.io/badge/status-Active-green)]()
[![DNA](https://img.shields.io/badge/DNA-Full%20Traceability-orange)]()
[![语言](https://img.shields.io/badge/language-Python%20|%20CNSH-yellow)]()
[![审计](https://img.shields.io/badge/三色审计-🟢%20通过-brightgreen)]()
[![Discussions](https://img.shields.io/badge/Discussions-欢迎讨论-blue)](https://github.com/UID9622/longhun-system/discussions)

> 🚀 **5 分钟上手**: `bash install.sh` → `python3 bin/龍魂体系v5-一键启动.py`
> 
> 📖 [快速入门](./QUICKSTART.md) · 🤝 [参与贡献](./CONTRIBUTING.md) · 💬 [社区讨论](https://github.com/UID9622/longhun-system/discussions)

---
## 📚 文档导航

| 文件 | 内容 |
|------|------|
| 📖 [README.md](./README.md) | 系统介绍（你在看的这个） |
| 📂 [docs/DIRECTORY_INDEX.md](./docs/DIRECTORY_INDEX.md) | 目录结构导航 — 快速找到你要的东西 |
| 🐉 [CNSH-PROTOCOL.md](./CNSH-PROTOCOL.md) | CNSH 中文编程语言完整规范 v2.2 |
| 📜 [CONSTITUTION.md](./CONSTITUTION.md) | 系统宪法 — 根本规则，不可修改 |
| 🤖 [AGENTS.md](./AGENTS.md) | AI 操作手册 — AI Agent 必须遵守的规则 |

> 📊 完整模块清单见 [`docs/DIRECTORY_INDEX.md`](./docs/DIRECTORY_INDEX.md)

---

## 📝 实战文章 · Tutorials

| 文章 | 模块 | 日期 |
|------|------|------|
| 🐉 [lh_deepseek_fixer v5.1 实战](./articles/2026-07-13-deepseek-fixer-v5.1.md) | 道引层 L2 · DeepSeek 自动修复引擎 | 2026-07-13 |
| 📺 [CSDN 发布版](https://uid9622-01.blog.csdn.net/article/details/162820231) | 同上（CSDN 同步） | 2026-07-13 |

---

## 🇨🇳 中文介绍

### 这是什么？

龍魂系统是一套**中国自主可控的数字主权基础设施**，包含：
- 🐉 **CNSH** — 中文原生编程语言（14 章完整规范）
- 🛡️ **三层审计** — 交叉监督 + 三色判定 + DNA 追溯
- ⚖️ **红线熔断** — 内置检测，违反人民数据主权自动阻断
- 🧠 **人格内阁** — 中国式治理决策引擎

当全世界还在讨论如何治理 AI 的时候，龍魂已经在做了。

### 六大核心能力

| 能力 | 说明 |
|------|------|
| 🔒 数据主权 | 中国人数据归中国管，本地存储，不出境 |
| 📝 CNSH 语言 | 中文母语编程，编译到 Python/JS/Rust/C |
| 🛑 红线熔断 | P0-P3 四级红线词组检测，多语言语义等价匹配 |
| 🧬 DNA 追溯 | 每个操作带唯一追溯码，防伪防篡改 |
| 🎨 三色审计 | 🟢通过 / 🟡警告 / 🔴拒绝 实时判定 |
| 🔢 369 数学锚点 | 数字根 + 五行 + 洛书九宫 数学稳定系统 |

### 版本历史

| 版本 | 亮点 |
|------|------|
| **v5.0** | 🧬 CNSH MCP Server 上线 — 13 工具完整语法链 + 统一 pyproject.toml + 红线引擎 v2.0 |
| **v4.2** | 🎛️ 龍魂操作台 MVP v1.1 — 10 项 Skill + 底座能力统一 API |
| **v4.0** | 📱 移动端监控 — 15层体系，AES-256-GCM加密 |
| **v3.1** | ⚡ 第三阶段 — 10项技能完整集成，API < 100ms |

### 快速启动

```bash
# 第一步：一键安装
bash install.sh

# 第二步：启动系统
python3 bin/龍魂体系v5-一键启动.py

# 常用命令
lh status         # 查看状态
lh start          # 启动服务
lh stop           # 停止服务
lh health         # 健康检查
```

> 📖 详细步骤见 [QUICKSTART.md](./QUICKSTART.md)

### MCP Server 启动（让 AI 直接调用 CNSH 工具）

在 MCP 客户端配置中加入：
```json
{
  "mcpServers": {
    "cnsh-syntax": {
      "command": "python3",
      "args": ["integrations/mcp/cnsh_syntax_mcp_server.py"],
      "env": { "PYTHONPATH": "/Users/{你的用户名}/longhun-system" }
    }
  }
}
```

---

## 🌍 English Summary

**LongHun (龍魂) is China's digital sovereignty infrastructure** — an integrated platform for AI governance, Chinese-native programming (CNSH), content creator protection, and data sovereignty.

### Core Capabilities

| Capability | Description |
|-----------|-------------|
| 🔒 Data Sovereignty | Chinese citizens' data stays local, under PRC law |
| 📝 CNSH Language | Chinese-native programming language, compiles to Python/JS/Rust/C |
| 🛑 Redline Fuse | Built-in detection of data sovereignty violations (P0-P3 tiers) |
| 🧬 DNA Traceability | Every operation carries a unique verifiable signature |
| 🎨 Three-Color Audit | 🟢Pass / 🟡Warn / 🔴Reject real-time decisions |
| 🔢 369 Math Anchor | Digital root + Five Elements + Luoshu mathematical system |

**Principle:** Technology serves the people. Sovereignty is not for sale.

---

## 🌏 Vision · 愿景

> *"全世界所有AI，都应该运行在可控的协议上。"*
> *"All AI in the world should run on a controllable protocol."*
> — UID9622，创造者 / Creator

龍魂协议的目标是成为任何AI系统都能采用的治理层——透明、可审计、根植于中国哲学智慧。

The LongHun Protocol is designed to be the governance layer that any AI system can adopt — transparent, auditable, and grounded in Chinese systems thinking (中国哲学).

---

## 👥 贡献者 · Contributors

感谢所有为龍魂系统做出贡献的人！

| 贡献者 | 角色 | 贡献 |
|--------|------|------|
| [UID9622](https://github.com/UID9622) | 创造者 · 架构师 | 全部核心系统 |

> 🏷 想上榜？从 [Good First Issue](https://github.com/UID9622/longhun-system/issues?q=label%3A%22good+first+issue%22) 开始！
> 
> 💬 有任何问题，来 [Discussions](https://github.com/UID9622/longhun-system/discussions) 聊聊。

---

## 🛡️ 维护者 · Maintainers

龍魂系统的核心维护者负责执行[行为准则](./CODE_OF_CONDUCT.md)、组织社区投票、执行熔断机制。

| 维护者 | 角色 | 职责 |
|--------|------|------|
| **UID9622** | 创造者 · 核心维护者 | 红线裁决·架构决策·社区投票组织 |
| （待社区投票增选） | — | — |

> ⚖️ 维护者增选机制：经社区提名 → 投票（2/3 多数通过）→ 名单在此实时更新。
> 
> 📜 治理机制详见：[CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) — 三阶梯决策（社区投票/核心评审/创始人覆写）。

---

## 📬 Contact · 联系

- **GitHub:** [@UID9622](https://github.com/UID9622)
- **Repository:** [longhun-system](https://github.com/UID9622/longhun-system)
- **Discussions:** [社区讨论区](https://github.com/UID9622/longhun-system/discussions)

---

*一个人建造。逻辑驱动。AI执行。社区一起看。*
*Built by one person. Powered by logic. Executed by AI. Watched by community.*
