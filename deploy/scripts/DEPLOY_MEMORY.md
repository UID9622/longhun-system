# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂·统一记忆 API · 部署文档

> DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-MEMORY-API-DEPLOY-DOC-v1.1-BRIDGE
> 创建者: 诸葛鑫（UID9622）
> CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
> v1.1: 身份联动闭环 + Token安全增强

---

## 概述

所有 AI（不论国家/模型）统一通过一个 REST API 入口加载龍魂记忆。
不给任何 AI 开特例。不管哪个国家、哪个公司的模型，统一走这个入口。

### v1.1 关键更新

1. **身份联动闭环**：远程请求 Token 验证前置调用 `https://uid9622.cn/identity/token-verify`，
   身份服务动态确认后才返回记忆数据。两套系统（记忆API + 身份服务）形成完整闭环。
2. **Token 安全**：客户端从 `$LH_MEMORY_TOKEN` 环境变量或 `~/.longhun/.memory_token` 文件
   静默加载 Token，禁止命令行明文出示。

## 部署位置

| 位置 | 端口 | 绑定 | 管理方式 | 状态 |
|:---|:---:|:---|:---|:---:|
| Mac 本机 | 8771 | 127.0.0.1 | launchd | ✅ 运行中 |
| 鲲鹏服务器 | 8773 | 0.0.0.0 | systemd | ✅ 运行中 |

## 核心文件

| 文件 | 用途 |
|:---|:---|
| `bin/lh_memory_api.py` | FastAPI 服务端·端口8771/8773 |
| `bin/lh_memory_client.py` | Python AI 客户端·支持本地/远程 |
| `bin/lh_memory_load.py` | 会话启动加载器 v2.0·API优先+本地回退 |
| `bin/lh_memory_load.sh` | Shell 客户端·给没有Python的AI用 |
| `deploy/com.longhun.memory-api.plist` | Mac launchd 配置 |
| `deploy/longhun-memory-api.service` | 鲲鹏 systemd 配置 |
| `deploy/scripts/deploy_memory_api.sh` | 一键部署脚本 |

## API 端点

| 方法 | 路径 | 用途 | 认证 |
|:---|:---|:---|:---|
| GET | `/v1/memory` | 完整记忆 JSON | 无（本地）|
| GET | `/v1/memory/raw` | 原始 MEMORY.md 全文 | 无 |
| GET | `/v1/memory/identity` | 身份焊死块 | 无 |
| GET | `/v1/memory/section/{§N}` | 获取指定节 | 无 |
| GET | `/v1/memory/search?q=xxx` | 全文搜索 | 无 |
| GET | `/v1/memory/anchors` | 锚清单 | 无 |
| GET | `/v1/memory/health` | 健康检查 | 无 |
| GET | `/v1/memory/stats` | 统计信息 | 无 |
| GET | `/v1/memory/token` | Token 信息 | 仅本地 |
| GET | `/v1/memory/daily/{date}` | 读日志 | 无 |
| POST | `/v1/memory/daily` | 追加日志 | Token |
| GET | `/v1/memory/daily/{date}` | 查日志 | 无 |

## AI 加载命令

```bash
# 本机 AI（CodeBuddy/Ollama 等）— 无需 Token
python3 bin/lh_memory_load.py

# 任何 Python AI — 本地无需 Token
python3 bin/lh_memory_client.py

# 只身份块
python3 bin/lh_memory_client.py --identity

# 搜索
python3 bin/lh_memory_client.py --search "训练超参"

# Shell AI
source bin/lh_memory_load.sh

# 远程 AI — Token 来自环境变量，禁止命令行明文
export LH_MEMORY_TOKEN="<从本机获取的token>"
python3 bin/lh_memory_client.py --host 119.13.90.27 --port 8773

# 直接 HTTP（仅本地）
curl http://127.0.0.1:8771/v1/memory/raw
```

## 认证机制

- **本地 127.0.0.1** → 无需认证
- **远程访问** → 需要 `X-API-Token` 请求头

### 🔥 认证链路（远程请求）

```
远程 Client
  │ X-API-Token (从 $LH_MEMORY_TOKEN 或 ~/.longhun/.memory_token 静默加载)
  ▼
Memory API (Mac:8771 / 鲲鹏:8773)
  │ 前置调用 verify_token_via_identity()
  ▼
Identity Service (https://uid9622.cn/identity/token-verify)
  │ 动态确认 Token 有效性
  ├─ ✅ PASS → 返回记忆数据
  ├─ 🔴 DENY → 403 拒绝
  └─ ⏱ UNREACHABLE → 回退本地验证
```

### Token 加载优先级

所有客户端（Python/Shell）统一按以下优先级静默加载：

| 优先级 | 来源 | 说明 |
|:---:|:---|:---|
| 1 | `$LH_MEMORY_TOKEN` 环境变量 | 推荐方式，不落地文件 |
| 2 | `~/.longhun/.memory_token` | 文件静默读取 |
| 3 | `.codebuddy/memory/.api_token` | 项目内文件 |
| 🚫 | 命令行 `--token` | 🔴 仅调试·禁止在生产/日志中出现 |

- Token 信息：仅本机可查 `curl http://127.0.0.1:8771/v1/memory/token`

## 管理命令

```bash
# Mac
launchctl load ~/Library/LaunchAgents/com.longhun.memory-api.plist    # 启动
launchctl unload ~/Library/LaunchAgents/com.longhun.memory-api.plist  # 停止
tail -f logs/memory_api.log                                           # 查看日志

# 鲲鹏
systemctl start longhun-memory-api     # 启动
systemctl stop longhun-memory-api      # 停止
systemctl restart longhun-memory-api   # 重启
journalctl -u longhun-memory-api -f    # 查看日志
```

## 设计原则

1. **所有 AI 统一入口** — 不给任何模型开特例
2. **只读为主** — AI 只能读记忆，不能改
3. **本地优先** — 默认只绑 127.0.0.1
4. **主权焊死** — UID9622 身份永不可改
5. **身份联动** — 远程 Token 通过 identity 服务动态验证（v1.1）
6. **Token 安全** — 环境变量/文件静默加载，禁命令行明文（v1.1）
7. **缓存优化** — 30秒内存缓存，减少 IO
8. **API 日志** — 每次请求+身份验证结果记录到 `logs/memory_api.log`
