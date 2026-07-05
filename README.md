<!--#龍芯⚡️2026-07-05-DOC-README-v5.0 -->
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
# 一键启动所有服务
python3 龍魂体系v5-一键启动.py

# 或使用命令行
lh-status        # 查看状态
lh-start         # 启动服务
lh-stop          # 停止服务
```

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

## 📬 Contact · 联系

- **GitHub:** [@UID9622](https://github.com/UID9622)
- **Repository:** [longhun-system](https://github.com/UID9622/longhun-system)

---

*一个人建造。逻辑驱动。AI执行。*
*Built by one person. Powered by logic. Executed by AI.*
