# 🗺️ 龍魂系统目录地图 · DIRECTORY_MAP

> **DNA:** `#龍芯⚡️丙午·丙申·庚戌·䷙大畜-DIRECTORY-MAP-v1.0-UID9622`
> **创建者:** 诸葛鑫（UID9622）
> **协议:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

---

## 目录设计原则

龍魂系统采用**编号前缀 + 语义命名**的混合目录结构：

- **编号目录**（如 `01_protocols/`、`08_BIN/`）用于稳定、高频访问的核心资产。
- **语义目录**（如 `brand/`、`articles/`）用于跨模块的共享资源。
- **Symlink** 用于兼容旧路径（如 `bin -> 08_BIN`、`docs -> 12_DOCS`），旧命令和链接无需修改。

---

## 📂 核心目录一览

| 目录 | 说明 | 典型内容 |
|:---|:---|:---|
| `01_protocols/` | 协议层 | 治理协议、技术规范、君子协议、隐私政策等 `.md` |
| `02_SKILLS/` | 技能层 | Kimi / Claude / MCP 技能定义与实现 |
| `03_KNOWLEDGE_GRAPH/` | 知识图谱 | 本体定义、实体关系、图数据 |
| `03_LAYERS/` | 分层架构 | L0-L9 系统分层实现 |
| `04_ENGINES/` | 引擎层（旧） | 行为密码学、洛书、三才等引擎 |
| `04_SERVICES/` | 服务层 | 独立微服务、API 服务 |
| `05_ENGINES/` | 引擎层（新） | 统一引擎目录，含 48+ 独立引擎/子系统 |
| `06_HOUTU_OS/` | 后土 OS | 操作系统级模块、进程管理、资源调度 |
| `07_AUDIT/` | 审计层 | 三色审计、DNA 对齐、审计报告 |
| `08_BIN/` | 可执行脚本 | 一键启动、CLI 命令、运维脚本 |
| `09_TOOLS/` | 工具集 | 数据导出、算法检测、价格审计等 |
| `10_PORTAL/` | 门户层 | 静态 HTML 门户页面（47+ 页面） |
| `12_DOCS/` | 文档层 | 架构、API、开发、FAQ、术语表等 |
| `13_TESTS/` | 测试层 | 单元测试、集成测试、回归测试 |
| `20_CONFIG/` | 配置层 | 环境配置、特征库、策略配置 |

---

## 🔗 Symlink 兼容说明

为兼容旧路径和既有命令，根目录保留以下符号链接：

| Symlink | 指向 | 说明 |
|:---|:---|:---|
| `bin` | `08_BIN/` | 旧命令入口 |
| `docs` | `12_DOCS/` | 旧文档入口 |
| `engines` | `05_ENGINES/` | 旧引擎入口 |
| `tests` | `13_TESTS/` | 旧测试入口 |
| `tools` | `09_TOOLS/` | 旧工具入口 |
| `portal` | `10_PORTAL/` | 旧门户入口 |
| `knowledge-graph` | `03_KNOWLEDGE_GRAPH/` | 旧知识图谱入口 |
| `services` | `04_SERVICES/` | 旧服务入口 |
| `backend` | `04_SERVICES/` | 后端服务别名 |

> 新开发建议直接使用编号目录；旧脚本和外部链接通过 Symlink 继续工作。

---

## 🌳 应用/生态目录

| 目录 | 说明 |
|:---|:---|
| `apps/` | 应用示例与 MVP |
| `brand/` | Logo、图标、印章、OG 预览等品牌资产 |
| `articles/` | 论文、实战文章、发布说明 |
| `papers/` | 学术论文与白皮书 |
| `reports/` | 审计报告、数据报表、运行报告 |
| `public-content/` | 对外发布的统一内容 |
| `digital_humans/` | 数字人模块 |
| `longhun-core/` | 龍魂核心库 |
| `integrations/` | 第三方集成（MCP、Kimi、Notion 等） |
| `deploy/` | 部署脚本与配置 |
| `docker/` | Docker 镜像与编排 |
| `mobile/` / `ios/` / `android/` / `harmonyos/` | 移动端与鸿蒙端代码 |
| `web/` / `web_apps/` | Web 端与在线应用 |

---

## 🧪 开发支持目录

| 目录 | 说明 |
|:---|:---|
| `.github/` | GitHub Actions、Issue 模板、FUNDING |
| `.githooks/` | Git 钩子 |
| `.devcontainer/` | VS Code Dev Container 配置 |
| `config/` | 运行时配置 |
| `scripts/` | 辅助脚本 |
| `experiments/` | 实验性代码 |
| `archive/` | 归档资料 |
| `backup/` | 备份策略与数据 |

---

## 🎯 文件放置速查

| 我要放... | 应该放到... |
|:---|:---|
| 新的治理协议 | `01_protocols/` |
| 新的 AI 技能 | `02_SKILLS/` |
| 新的核心引擎 | `05_ENGINES/` |
| 新的 CLI 命令 | `08_BIN/` |
| 新的可运行工具 | `09_TOOLS/` |
| 新的门户页面 | `10_PORTAL/` |
| 新的技术文档 | `12_DOCS/` |
| 新的测试脚本 | `13_TESTS/` |
| 新的配置项 | `20_CONFIG/` |
| 新的论文/文章 | `articles/` 或 `papers/` |
| 新的品牌素材 | `brand/` |
| 新的审计报告 | `reports/` |

---

## 📊 规模参考（2026-08-07）

```bash
# 协议数
find 01_protocols -maxdepth 1 -type f -name '*.md' | wc -l

# 引擎数
find 05_ENGINES -maxdepth 2 -type d | wc -l

# 门户页数
find 10_PORTAL -maxdepth 2 -type f -name '*.html' | wc -l

# 测试数
find 13_TESTS -type f -name '*.py' | wc -l
```

---

> 🐉 **目录是骨架，协议是血脉，代码是肌肉。** 放对位置，才能跑得远。
