# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 分布式节点体系 v2.0

> DNA: `#龍芯⚡️丙午·辛未·乙酉·卯时·䷅讼-DISTRIBUTED-NODE-v2.0`
> 融合自: `longhun-complete` 节点管理体系
> 创建: 丙午·辛未·乙酉 (2026-07-17)

## 架构

```
                  ┌──────────────────────┐
                  │   龍魂注册中心 v2.0    │
                  │  registry_server.py   │
                  │    端口: 9623         │
                  │  (华为云 / 本地Mac)    │
                  └──────────┬───────────┘
                             │ 心跳上报（只传用量，不传内容）
           ┌─────────────────┼─────────────────┐
           │                 │                 │
     ┌─────┴─────┐    ┌─────┴─────┐    ┌─────┴─────┐
     │  节点 A   │    │  节点 B   │    │  节点 C   │
     │  (Mac)    │    │  (鲲鹏)   │    │  (战友机)  │
     │  9622     │    │  9622     │    │  9622     │
     └───────────┘    └───────────┘    └───────────┘
```

## 文件清单

| 目录 | 文件 | 功能 |
|:---|:---|:---|
| `deploy/longhun-registry/` | `registry_server.py` | 注册中心 v2.0 |
| | `start_registry.sh` | 注册中心启动器 |
| `deploy/longhun-node/` | `node_heartbeat.py` | 心跳上报器 v2.0 |
| | `node_audit.py` | 质量审计器 v2.0 (P0-P4) |
| | `longhun-node-install.sh` | 一键部署脚本 |
| `docker/` | `longhun-node.Dockerfile` | 节点容器镜像 |

## 快速部署（3步）

### Step 1: 启动注册中心

```bash
cd data/sources
./lh_launch.sh registry-start
# 或指定端口: ./lh_launch.sh registry-start 9623
```

### Step 2: 启动本机节点

```bash
./lh_launch.sh node-start http://localhost:9623
```

### Step 3: 查看全局状态

```bash
./lh_launch.sh registry-stats
./lh_launch.sh registry-nodes
```

## 节点审计

```bash
# 单次审计
./lh_launch.sh node-audit

# 守护模式（每小时一次）
./lh_launch.sh node-audit-daemon
```

## Docker 部署节点

```bash
# 一键部署
./lh_launch.sh node-install

# 或手动
export REGISTRY_URL=http://your-server:9623
bash deploy/longhun-node/longhun-node-install.sh
```

## 原则

- **只传用量，不传内容** — 心跳只上报文件数、存储大小、请求次数
- **DNA签章** — 每条记录带SHA256哈希，不可篡改
- **数据主权** — 所有数据留在节点本地，注册中心只存索引
- **透明审计** — 任何人可验证节点质量
