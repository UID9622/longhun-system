# 龍魂系统·使用指南 / Longhun System · Usage Guide

> DNA: #龍芯⚡️2026-09-05-使用指南-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）· 代码: MulanPSL v2
> 文档版本: v5.2.0
> 三色: 🟢 命令清单 2026-09-05 全部实测可用（控制台 v1.3 · 36 模块 · 120+ 命令）

---

## [中文] 使用指南

### 一、三种入口

| 入口 | 命令 | 适用 |
|---|---|---|
| 终端控制台 | `lh` | 主入口·菜单式操作 |
| 网页控制台 | `lh --console` | 可视化点按操作 |
| 自然语言 | `lh "系统状态如何"` / `lh ask "..."` / `lh chat` / `lh auto` | 说人话自动路由 |

### 二、28 个顶层命令（全部实测可用）

| 命令 | 说明 | 示例 |
|---|---|---|
| `health` | 系统健康检查（22 项引擎） | `lh health --json` |
| `ledger` | 龍魂账法·底层记账（DNA/哈希/见证/三色/耻辱墙） | `lh ledger balance` / `lh ledger add T1 1001 3201 1条 --note 测试` / `lh ledger verify` |
| `calmem` | 日历记忆（多源聚合+哈希链+速记） | `lh calmem status` / `lh calmem search 龍魂` / `lh calmem note 备忘` |
| `digest` | 内容消化（收件箱→分类→归档） | `lh digest` |
| `recap` | 执行复盘可视化 | `lh recap view` / `lh recap generate --cmd topo --rc 0` |
| `session` | 会话记忆（跨会话自动恢复） | `lh session save --task "..."` / `lh session view` |
| `checkpoint` | 断点续接 | `lh checkpoint list` / `lh checkpoint resume` |
| `community` | GitHub 社区聚合（issue/PR 周报） | `lh community status --live` / `lh community weekly` |
| `billing` | API 计费系统 | `lh billing balance` / `lh billing usage --period month` / `lh billing history` |
| `payment` | 支付渠道管理 | `lh payment channels` |
| `reconcile` | 对账审计 | `lh reconcile` |
| `fraud` | 作假行为检测 | `lh fraud scan .` / `lh fraud status` |
| `judge` | 归一审判官·三色判定（M78） | `lh judge <文件>` |
| `gov` | 三色治理（声誉·红线） | `lh gov rules` / `lh gov status` |
| `council` | 无后台审批团（5 席多签） | `lh council list` |
| `pledge` | 用=认=守约 | `lh pledge` |
| `model` | 本地模型统一入口（离线） | `lh model list` / `lh model status` / `lh model run` |
| `topo` | 通心译拓扑（知识图谱） | `lh topo serve` / `lh topo status` |
| `sense` | 统一多模态识别（识别→决策→编排→反馈） | `lh sense <输入>` |
| `search` | 全库搜索 | `lh search <关键词>` |
| `security` | 安全侦查与漏洞引擎 | `lh security scan` / `lh security status` |
| `wallet` | 数字钱包（SOL 自托管·本地） | `lh wallet balance` |
| `codeql` | 代码安全审计（CodeQL） | `lh codeql scan <repo>` |
| `memory` | 跨层记忆 | `lh memory load` / `lh memory status` |
| `skill` | 技能管理 | `lh skill list` |
| `evolve` | 能力演进 | `lh evolve status` |
| `publish` | 发布物管理 | `lh publish list` |
| `workspace-sync` | 工作区/远端同步 | `lh workspace-sync` |

### 三、GitHub 联动（开源协作）

```bash
lh github status           # 仓库/PR 状态
lh github test-perms       # 令牌权限自检（社区钥匙）
lh github-token-hint       # 令牌来源提示
lh fork <repo>             # 分叉同步
```

### 四、核心数据家（本地·数据主权 P0）

| 数据 | 路径 |
|---|---|
| 账本 | `~/.longhun/ledger/`（transactions.jsonl·append-only） |
| 日历记忆 | `~/.longhun/calendar_memory/`（days/ + notes/ + chain.json） |
| 会话上下文 | `~/.longhun/session_context.json` |
| 断点 | `~/.longhun/checkpoints/` |
| 复盘 | `~/.longhun/recap/` |
| 计费 | `~/.longhun/billing/` |
| 耻辱墙 | `~/.longhun/shame_wall/` |

> 离线铁律：核心命令全本地运行，数据不出机；唯一联网可选件 = Notion MCP。

---

## [English] Usage Guide

**Entries**: `lh` (console) · `lh --console` (web console) · natural language `lh "ask anything in Chinese"` / `lh ask` / `lh chat` / `lh auto`

**28 top-level commands (all verified)**:
`health` · `ledger` (DNA accounting) · `calmem` (calendar memory, hash-chained) · `digest` · `recap` · `session` · `checkpoint` · `community` · `billing` · `payment` · `reconcile` · `fraud` · `judge` · `gov` · `council` · `pledge` · `model` (local/offline) · `topo` · `sense` · `search` · `security` · `wallet` · `codeql` · `memory` · `skill` · `evolve` · `publish` · `workspace-sync`

**GitHub**: `lh github status` · `lh github test-perms` · `lh fork`

**Local data (sovereign, never leaves the device)**: ledger / calendar-memory / session / checkpoints / recap / billing under `~/.longhun/`.

---
🐉 2026-09-05 · 丙午年·壬申月·庚戌日 · UID9622 · 🟢



