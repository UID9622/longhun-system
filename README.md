# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!--#龍芯⚡️2026-07-05-DOC-README-v5.0 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

# 🐉 龍魂系统 · LongHun System

> **中国自主可控的数字主权底座。**
> **技术服务于人民。主权不可交易。**
> *Technology serves the people. Sovereignty is not for sale.*

[![Version](https://img.shields.io/github/v/release/UID9622/longhun-system?label=版本&color=blue)](https://github.com/UID9622/longhun-system/releases)
[![License](https://img.shields.io/badge/license-MulanPSL%20v2%20%7C%20CC%20BY--NC--SA%204.0-green)](https://github.com/UID9622/longhun-system#%EF%B8%8F-%E5%BC%80%E6%BA%90%E5%8D%8F%E8%AE%AE)
[![CI](https://img.shields.io/github/actions/workflow/status/UID9622/longhun-system/ci.yml?label=CI&color=brightgreen)](https://github.com/UID9622/longhun-system/actions)
[![Python](https://img.shields.io/badge/Python-3.9%2B-yellow?logo=python)](https://www.python.org/)
[![CNSH](https://img.shields.io/badge/CNSH-%E4%B8%AD%E6%96%87%E7%BC%96%E7%A8%8B-orange)](https://github.com/UID9622/longhun-system/tree/orphan_main/cnsh.integrated)
[![Audit](https://img.shields.io/badge/三色审计-🟢_通过-brightgreen)](https://uid9622.cn/)
[![Stars](https://img.shields.io/github/stars/UID9622/longhun-system?style=social)](https://github.com/UID9622/longhun-system/stargazers)

> 🚀 **5 分钟上手**: `bash bin/install.sh` → `python3 bin/龍魂体系v5-一键启动.py`
> 
> 📖 [快速入门](./QUICKSTART.md) · 🤝 [参与贡献](./CONTRIBUTING.md) · 💬 [社区讨论](https://github.com/UID9622/longhun-system/discussions)

> 🏗️ **目录结构 v2.0**（2026-08-04）：核心目录已按编号结构重组（如 `08_BIN/`、`12_DOCS/`）。旧路径（`bin/`、`docs/` 等）仍通过 Symlink 保持兼容，现有命令和链接无需修改。详见 [`docs/DIRECTORY_MAP.md`](./docs/DIRECTORY_MAP.md) 与 [`docs/SYSTEM_STRUCTURE_AUDIT_v1.0.md`](./docs/SYSTEM_STRUCTURE_AUDIT_v1.0.md)。

---

## 🗂️ 仓库速览 · Repository at a Glance

> 一键看清这个仓库的「现在进行时」。所有状态均可在本地复现验证。

| 维度 | 状态 | 验证入口 |
|:---|:---|:---|
| 🏷️ **最新版本** | v5.1.0 · 品牌与国际化完善 | [`CHANGELOG.md`](./CHANGELOG.md) |
| 🧬 **默认分支** | `orphan_main` | GitHub 仓库首页 |
| ✅ **CI 状态** | GitHub Actions 持续集成 | [`.github/workflows/`](./.github/workflows/) |
| 🔐 **GPG 签名** | 全量文件 `.asc` 脱签验证 | 本仓库任意 `.md.asc` / `.py.asc` |
| 🎨 **品牌资产** | 印章风格 Logo / App 图标 / OG 预览 | [`brand/`](./brand/) |
| 🌐 **在线门户** | `10_PORTAL/index.html` 静态站点 | [`portal/`](./portal/) |
| 🖥️ **CNSH IDE** | 基于 FastAPI + Ace Editor 的可交付编辑器 | [`CNSH_IDE.md`](./CNSH_IDE.md) |
| 📊 **学术引用** | CITATION.cff 已配置 | [`CITATION.cff`](./CITATION.cff) |
| 💰 **支持入口** | FUNDING.yml + 此路同行二维码 | [`.github/FUNDING.yml`](./.github/FUNDING.yml) |

---

## 🔐 可验证性 · Verifiability

> 龍魂系统的每一份核心文件都带有 **GPG 脱签签名**（`.asc`），确保内容从提交起未被篡改。

```bash
# 验证任意文件签名（以 README.md 为例）
gpg --verify README.md.asc README.md

# 批量验证当前目录下所有签名
find . -type f -name '*.asc' -not -path './.git/*' | sed 's/\.asc$//' | xargs -I{} gpg --verify {}.asc {}
```

- **签名密钥指纹**: `...SozCbV8`（UID9622）
- **签名策略**: 协议/代码/配置/文档四类文件强制签名，审计日志与临时数据除外
- **验证失败处理**: 参见 [`SECURITY.md`](./SECURITY.md) 的「完整性事件响应」

### 🖥️ 透明看板 · Transparent Dashboard

> **君子协议的可视化契约**：把「德在技术前 · 信息主权不可让渡」从口号变成打开浏览器就能看见的东西。
> **The visual covenant of the Gentlemen's Protocol** — governance events, shame wall, honor wall, shadow AI detection, agent binding, chronicler records and knowledge graph, all real-time.

```bash
./scripts/start_transparent_dashboard.sh          # 本地安全访问 http://127.0.0.1:8080（默认）
./scripts/start_transparent_dashboard.sh 0.0.0.0 8080  # 网络内公开（谨慎）
```

| 模块 | 数据来源 | 意义 |
|:---|:---|:---|
| 📜 治理事件 | `.state/industry_governance/governance.sqlite` | 八大痛点每次评估/执行都有记录 |
| 🚫 耻辱墙 | `shame_wall` | 违规记录永久公开 |
| 🏆 荣誉墙 | `honor_wall` | 贡献者公开表彰 |
| 👤 影子AI检测 | `unauthorized_ai` | 未授权工具检测公开 |
| 🔗 Agent绑定 | `agent_identities` | 法定身份绑定统计 |
| 📜 史官记录 | `~/.longhun/04_AUDIT/*.jsonl` | 系统操作日志 |
| 📚 知识图谱 | `knowledge/graph/graph.json` | 节点/关系统计 |

> 实现：`08_BIN/lh_transparent_dashboard.py`（FastAPI·只读不写回·默认 127.0.0.1）· 测试 `13_TESTS/test_transparent_dashboard.py` · 知识图谱 `03_KNOWLEDGE_GRAPH/03_透明看板_..._TRANSPARENT-DASHBOARD-v1.0.md`

---

## 🏆 揭榜挂帅自检 · Open Source Readiness

> 面向评估方/揭榜挂帅评审的六维自检表。每个维度均提供**可验证入口**。

| 维度 | 状态 | 缺口 → 已补 | 验证入口 |
|:---|:---:|:---|:---|
| 🔬 技术公开可验证 | ✅ | ✅ 复现指南 | [`docs/REPRODUCE.md`](./docs/REPRODUCE.md) |
| 🔄 持续维护 | ✅ | ✅ Issue/PR 流程 | [`CONTRIBUTING.md`](./CONTRIBUTING.md) · [`.github/ISSUE_TEMPLATE/`](./.github/ISSUE_TEMPLATE/) |
| 👥 社区生态 | 🟡 | ✅ 贡献指南 + 使用案例 | [`CONTRIBUTING.md`](./CONTRIBUTING.md) · [`docs/USE_CASES.md`](./docs/USE_CASES.md) |
| 📚 标准化文档 | ✅ | ✅ 系统化技术白皮书 | [`docs/LONGHUN-TECHNICAL-WHITEPAPER-v1.0.md`](./docs/LONGHUN-TECHNICAL-WHITEPAPER-v1.0.md) |
| 📦 第三方可调用 | ✅ | ✅ SDK 可安装（PyPI 已发布） | [`docs/SDK-GUIDE.md`](./docs/SDK-GUIDE.md) · [`sdk/README.md`](./sdk/README.md) |
| 🏗️ 应用案例 | ✅ | ✅ 完整落地案例 | [`docs/CASE_STUDIES.md`](./docs/CASE_STUDIES.md) |

> 🐉 **一键复现**：`bash bin/install.sh` → `lh --help` → `python3 bin/lh_self_heal.py --quick` → `pytest tests/`

---

## 📊 项目规模 · Project Scale

> 数据截止 2026-08-07，可通过下方命令本地复测。

| 指标 | 数量 | 说明 |
|:---|---:|:---|
| 📁 核心目录 | 20+ | `01_protocols/` ~ `25_TASK_ENGINE/` 编号结构 |
| 📝 协议文档 | 185+ | `01_protocols/` 下 `.md` 治理与技术协议 |
| ⚙️ 引擎模块 | 48 | `05_ENGINES/` 下独立引擎/子系统 |
| 🖥️ 门户页面 | 47 | `10_PORTAL/` 静态 HTML 页面 |
| 🧪 测试脚本 | 33 | `13_TESTS/` 单元/集成/回归测试 |
| 🔏 GPG 签名 | 4,000+ | 核心文件 `.asc` 脱签覆盖 |
| 🐍 Python 文件 | 1,700+ | 核心实现（不含下载归档） |
| 📄 Markdown 文件 | 1,500+ | 文档、论文、协议、教程 |

```bash
# 复测命令
find 01_protocols -maxdepth 1 -type f -name '*.md' | wc -l   # 协议数
find 05_ENGINES -maxdepth 2 -type d | wc -l                   # 引擎数
find 10_PORTAL -maxdepth 2 -type f -name '*.html' | wc -l     # 门户页数
find 13_TESTS -type f -name '*.py' | wc -l                    # 测试数
```

---

## 📄 Featured Paper · 行为密码学统一理论

> **[Unified Theory of Behavioral Cryptography v3.0](articles/behavioral-cryptography-unified-theory-v3.0.md)**
> — *Seven-Factor Provenance × Three-Domain Boundary · A Dual-Wing Unified Model*

| | |
|:---|:---|
| 📖 **Paper (Markdown)** | [`articles/behavioral-cryptography-unified-theory-v3.0.md`](articles/behavioral-cryptography-unified-theory-v3.0.md) |
| 🌐 **Paper (HTML)** | [`articles/behavioral-cryptography-unified-theory-v3.0.html`](articles/behavioral-cryptography-unified-theory-v3.0.html) — MathJax rendered, read online |
| 🇨🇳 **论文（中文）** | [`articles/行为密码学-统一框架-v3.0.md`](articles/行为密码学-统一框架-v3.0.md) |
| 🔬 **Engine** | [`04_ENGINES/behavioral_crypto/unified_boundary_engine.py`](04_ENGINES/behavioral_crypto/unified_boundary_engine.py) (~950 lines) |
| 📜 **Protocol** | [`01_protocols/LH-BEHAVIOR-BOUNDARY-PROTOCOL-v1.0.md`](01_protocols/LH-BEHAVIOR-BOUNDARY-PROTOCOL-v1.0.md) |

**Abstract**: A unified mathematical framework that solves content provenance (Who wrote this? — Seven-Factor, joint forgery ~10⁻⁸) and behavioral boundary (Where should this circulate? — A0/A1/A2 three-domain authorization) in one integrated model. Private domain content is mathematically guaranteed audit-exempt; public domain content is full-chain traceable. ~950 lines of Python, empirically verified.

**Keywords**: `#BehavioralCryptography` `#AIGC-Authentication` `#PrivateDomainExemption` `#CrossDomainTracking`

---

## 🖥️ CNSH IDE · 中文编程集成开发环境

> 已交付可独立运行的 CNSH 编辑器，支持纠错 / 编译 / 运行三引擎联动。

```bash
# 本地运行
python3 08_BIN/cnsh_web_ide.py

# 打包为 macOS .app
python3 08_BIN/build_cnsh_app.py
```

| 入口 | 说明 |
|:---|:---|
| 🚀 **运行** | `python3 08_BIN/cnsh_web_ide.py` → http://127.0.0.1:8848 |
| 📦 **打包** | `python3 08_BIN/build_cnsh_app.py --target macos_app` |
| 🧠 **AI 接入** | 本地 Ollama 模型优先 + 国产云厂商可选，零 API 费用 | [`CNSH_IDE.md`](./CNSH_IDE.md) |
| 📖 **交付说明** | [`CNSH_IDE.md`](./CNSH_IDE.md) |
| 🐳 **容器** | [`container/README.md`](./container/README.md) |

---

## 📚 文档导航

### 入门必读
| 文件 | 内容 |
|:---|:---|
| 📖 [README.md](./README.md) | 系统介绍（你在看的这个） |
| 🚀 [INSTALL.md](./INSTALL.md) | 安装指南（Linux/macOS/Windows/Docker） |
| ❓ [docs/FAQ.md](./docs/FAQ.md) | 常见问题 |
| 📔 [docs/GLOSSARY.md](./docs/GLOSSARY.md) | 术语表 |

### 技术文档
| 文件 | 内容 |
|:---|:---|
| 🏗 [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) | 系统架构（Mermaid图） |
| 🔌 [docs/API.md](./docs/API.md) | API文档 |
| 🐉 [CNSH-PROTOCOL.md](./CNSH-PROTOCOL.md) | CNSH 中文编程语言完整规范 v2.2 |
| 🛠 [docs/DEVELOPMENT.md](./docs/DEVELOPMENT.md) | 开发者文档·调试·测试·发布 |
| 🗺 [docs/DIRECTORY_MAP.md](./docs/DIRECTORY_MAP.md) | 目录地图·文件应该放哪里 |
| 📋 [docs/SYSTEM_STRUCTURE_AUDIT_v1.0.md](./docs/SYSTEM_STRUCTURE_AUDIT_v1.0.md) | 系统结构审计与重组方案 |
| 🔬 [docs/REPRODUCE.md](./docs/REPRODUCE.md) | 复现指南（揭榜挂帅） |
| 📚 [docs/LONGHUN-TECHNICAL-WHITEPAPER-v1.0.md](./docs/LONGHUN-TECHNICAL-WHITEPAPER-v1.0.md) | 系统化技术白皮书 v1.0 |
| 📦 [docs/SDK-GUIDE.md](./docs/SDK-GUIDE.md) | SDK 第三方对接指南（pip/npm） |
| 🏗️ [docs/CASE_STUDIES.md](./docs/CASE_STUDIES.md) | 完整落地案例 |
| 💡 [docs/USE_CASES.md](./docs/USE_CASES.md) | 使用案例 |

### 治理与协议
| 文件 | 内容 |
|:---|:---|
| 📜 [GOVERNANCE.md](./GOVERNANCE.md) | 治理模型·三色审计·决策流程 |
| 🤝 [GENTLEMANS_PROTOCOL.md](./GENTLEMANS_PROTOCOL.md) | 君子协议中英文版 |
| 🔒 [PRIVACY_POLICY.md](./PRIVACY_POLICY.md) | 隐私政策 |
| 📋 [TERMS_OF_SERVICE.md](./TERMS_OF_SERVICE.md) | 服务条款 |
| 🛡 [SECURITY.md](./SECURITY.md) | 安全策略 |
| 📜 [CONSTITUTION.md](./CONSTITUTION.md) | 系统宪法·根本规则 |
| 🤖 [AGENTS.md](./AGENTS.md) | AI 操作手册 |

### 社区与贡献
| 文件 | 内容 |
|:---|:---|
| 🤝 [CONTRIBUTING.md](./CONTRIBUTING.md) | 贡献指南·代码规范 |
| 📖 [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) | 社区行为准则 |
| 🗺 [ROADMAP.md](./ROADMAP.md) | 路线图·已完成·进行中·远期 |
| 📝 [CHANGELOG.md](./CHANGELOG.md) | 变更日志 |
| 🌐 [docs/ECOSYSTEM.md](./docs/ECOSYSTEM.md) | 生态系统·MCP·插件 |

> 📊 完整索引见 [`docs/DOCUMENTATION_INDEX.md`](./docs/DOCUMENTATION_INDEX.md)

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
bash bin/install.sh

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
| 🖥️ Transparent Dashboard | Visual covenant of the Gentlemen's Protocol — governance events, shame/honor walls, shadow AI detection, all real-time (`./scripts/start_transparent_dashboard.sh` → http://127.0.0.1:8080) |

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

### 🔗 知识库 & 反向链接

> 龍魂知识分布在多个平台，互为镜像、互相链接。

| 平台 | 链接 | 内容 |
|:---|:---|:---|
| 📓 **Notion 知识库** | [uid9622.notion.site](https://uid9622.notion.site) | 367个数据库·设计文档·引擎注册表·知识图谱·完整知识底座 |
| 📺 **CSDN 博客** | [uid9622-01.blog.csdn.net](https://uid9622-01.blog.csdn.net) | 技术文章·实战教程·知识卡片·公开发布 |
| 🌐 **官方网站** | [uid9622.cn](https://uid9622.cn) | 龍魂系统入口·API文档·健康状态 |
| 📦 **GitHub** | [github.com/UID9622/longhun-system](https://github.com/UID9622/longhun-system) | 源码·协议·引擎·一切开源

---

## 🤝 此路同行 · Support

> **这不是乞讨，是在茫茫数字荒原上，立下一塊路碑。**
> **同行者，自會相認。**

龍魂系统从 2024 年走到今天，没有融资、没有广告、没有平台流量扶持。
每一行代码、每一次修复、每一次熬夜，都是 UID9622 和 AI 兵团一起扛过来的。

如果你认同这个方向——**技术服务于人民，主权不可交易**——可以用实际行动支持我们继续走下去：

| 方式 | 说明 |
|------|------|
| 💰 数字人民币 / 支付宝 | 扫码下方二维码，任意金额均可 |
| ⭐ Star 本项目 | 让更多人看见 |
| 🍴 Fork 并贡献 | 代码、文档、测试、翻译都行 |
| 🗣 参与 Discussions | 你的想法可能成为下一个功能 |

<p align="center">
  <img src="./portal/browser-historian/support-alipay-ecny.jpg" alt="此路同行 - 支付宝 / 数字人民币" width="320">
  <br>
  <strong>此路同行 · 不是赞助，是认领一块路碑</strong>
</p>

**款项用途公开承诺：**
1. 优先用于服务器、域名、证书等基础设施续费
2. 其次用于开源文档、多语言翻译、社区活动
3. 绝不用于任何资本收割、数据贩卖、广告追踪

---

*一个人建造。逻辑驱动。AI执行。社区一起看。*
*Built by one person. Powered by logic. Executed by AI. Watched by community.*
