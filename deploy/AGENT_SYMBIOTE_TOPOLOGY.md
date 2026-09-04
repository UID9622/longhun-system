# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 · 智能体共生体部署拓扑

> DNA: `#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-AGENT-SYMBIOTE-TOPOLOGY-v1.0`

## 架构原则

```
云端（只触发）  ──→  本地 Mac（主控）  ──→  鲲鹏服务器（生产）
  │                      │                      │
  │ Cloudflare           │ launchd 管理         │ systemd 管理
  │ 隧道代理             │ 全量数据存储          │ 全量数据存储
  │ 不存数据             │ 不依赖云端            │ 不依赖云端
  │ 不持密钥             │ 持全部密钥            │ 持全部密钥
```

## 当前运行状态 (2026-07-06)

### 本地 Mac

| 服务 | 端口 | PID | 管理方式 | 状态 |
|------|------|-----|----------|------|
| **龍魂共生体** | 9627 | launchd | `com.longhun.symbiote` | 🟢 在线 |
| **L1 五人格守护** | - | 74945 | `agent_daemon.py` | 🟢 运行中 |
| CNSH 操作台 | 9622 | launchd | `com.uid9622.longhun888-services` | 🟢 在线 |
| 卦象审计 | 9623 | launchd | `com.longhun.gua-audit` | 🟢 在线 |
| 龍心之语 | 9624 | launchd | `com.longhun.heart-talk` | 🟢 在线 |
| 知识图谱 | 8088 | launchd | `com.longhun.kg-api` | 🟢 在线 |
| 门户服务 | 8777 | launchd | `com.longhun.portal` | 🟢 在线 |

### 云端（仅触发层）

| 入口 | 指向 | 说明 |
|------|------|------|
| `longhun888.com` | Cloudflare Tunnel → `:8777` | 门户代理，数据留本地 |
| 华为云 ECS | Docker 容器 `119.13.90.27` | CNSH Editor API（ARM64 鲲鹏兼容） |

所有 API 密钥、数据库、配置文件 **只存在于本地 Mac 和鲲鹏服务器**，云端不持有任何数据。

### 鲲鹏服务器

- **管理 IP**: `192.168.122.1`（当前不可达）
- **部署路径**: `/opt/longhun-system`
- **部署命令**: `bash deploy/connect-kunpeng.sh deploy`

## 操作命令

```bash
# 共生体
lh symbiote            # 查看共生体状态
http://127.0.0.1:9627/symbiote   # 仪表盘
http://127.0.0.1:9627/           # 3D 神经网络

# Agent 守护
python3 agents/agent_daemon.py status  # 查看五人格状态
python3 agents/agent_daemon.py start   # 启动

# 全系统状态
lh status              # 全部节点状态
lh health              # 健康检查

# 部署到鲲鹏（服务器在线时）
bash deploy/connect-kunpeng.sh deploy
```
