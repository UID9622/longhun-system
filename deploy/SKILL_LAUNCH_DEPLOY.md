# 龍魂技能启动 · 集成部署指南 v1.0

> DNA: #龍芯⚡️丙午·乙未·壬戌·豫-SKILL-LAUNCH-DEPLOY-v1.0
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0

## 一、交付清单

| # | 模块 | 文件 | 端口 | 状态 |
|:---:|:---|:---|:---:|:---:|
| 1 | QiaoJie CLI v2.0 | `integrations/qiaojie/qiaojie_cli.py` | — | ✅ |
| 2 | 8799 枢纽 | `bin/xiaoyi_hub_8799.py` | 8799 | ✅ |
| 3 | 8799 launchd | `deploy/com.uid9622.xiaoyi-hub.plist` | — | ✅ |
| 4 | 观澜 M1 | `bin/lh_guanlan_api.py` (+ /chat) | 8770 | ✅ |
| 5 | 观澜 M1 standalone | `engines/guanlan/guanlan_server.py` | 8770 | ✅ |
| 6 | 观澜 launchd | `deploy/com.longhun.guanlan-m1.plist` | — | ✅ |
| 7 | CNSH 网关扩展 | `bin/cnsh_gateway.py` (+ guanlan路由) | 8765 | ✅ |
| 8 | FRP 服务端 | `deploy/frp/frps.toml` | — | ✅ |
| 9 | FRP 客户端 | `deploy/frp/frpc.toml` | — | ✅ |
| 10 | 集成测试 | `bin/test_integration.py` | — | ✅ |

## 二、架构拓扑

```
qiaojie_cli v2 (CLI)
    │
    ├─→ 8799 枢纽 (POST /hub/ask)
    │       ├─→ 9622操作台 (首选)
    │       ├─→ 8765GPT      (降级1)
    │       └─→ Ollama:11434 (最终降级)
    │
    ├─→ 观澜M1 (POST /chat)  → Ollama:11434 透传
    │
    └─→ Notion搜索 (search)
```

## 三、启动命令

```bash
# 1. QiaoJie CLI (无需启动，按需调用)
python3 integrations/qiaojie/qiaojie_cli.py qc

# 2. 8799 枢纽
launchctl load ~/Library/LaunchAgents/com.longhun.xiaoyi-bridge.plist
# 已更新指向: bin/xiaoyi_hub_8799.py

# 3. 观澜M1
launchctl load ~/Library/LaunchAgents/com.longhun.guanlan-api.plist
# /chat 端点已集成到现有 lh_guanlan_api.py

# 4. CNSH网关 (可选)
python3 bin/cnsh_gateway.py &
# 路由新增: guanlan → :8770/chat 透传
```

## 四、验收清单

```bash
# 快速自检
python3 integrations/qiaojie/qiaojie_cli.py qc

# 全链路
python3 integrations/qiaojie/qiaojie_cli.py selftest

# 全局验收 (13项)
python3 bin/test_integration.py

# 烟测试 (仅核心5项)
python3 bin/test_integration.py --smoke
```

## 五、降级链

| 优先级 | 后端 | 端点 | 说明 |
|:---:|:---|:---|:---|
| 1 | 9622操作台 | localhost:9622/api/xiaoyi/ask | 首选 |
| 2 | 8765GPT | localhost:8765/chat | 次选 |
| 3 | Ollama | localhost:11434/api/generate | 兜底 |

## 六、安全设计

- 一票否决词检测 (3级: 伦理/一票否决/敏感词)
- X-DNA-Token 认证
- 审计日志 (append-only, 线程安全)
- 熔断降级 (dr∈{3,9}→拒绝)
- 本地优先 (首选127.0.0.1, 不上云)
