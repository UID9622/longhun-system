# 龍魂部署架构落地报告 · 本地自检 + 鲲鹏桥接

**DNA**: `#龍芯⚡️丙午·乙未·丁酉·巳时·既济-DEPLOY-BRIDGE-20260727-v1.0`
**执行人**: UID9622 · 龍芯⚡️
**时间**: 2026-07-27T10:15:00+08:00
**任务**: 落地龍魂部署架构：本地自检 + 鲲鹏桥接

---

## 一、本地自检

### 1.1 巡检工具
```bash
python3 bin/lh_patrol.py
```

### 1.2 结果摘要
| 检查项 | 结果 |
|--------|------|
| Git 未提交/修改文件 | 285 个 |
| 潜在敏感信息 | 8 处（均为测试/示例硬编码，非真实密钥） |
| lint 报告 | 0 |
| 核心服务在线 | 2/2（memory-api、persona-api） |
| **红旗** | **1**（潜在敏感信息泄露） |

### 1.3 红旗项明细
8 处潜在敏感信息均位于测试/示例代码中，例如 `hardcoded_secret_1234567890123456`、`test-shield-password-2026` 等。已确认：
- 无真实生产密钥泄露
- 无 SSH 私钥泄露
- 无 Cloud API Key 泄露

**建议**: 后续对这些示例值统一替换为 `REPLACE_ME` 占位符或从环境变量读取。

---

## 二、鲲鹏服务器状态

### 2.1 基础信息
| 项目 | 值 |
|------|-----|
| 主机 | `root@119.13.90.27` |
| 系统 | Ubuntu 6.8.0-100-generic x86_64 |
| 在线时长 | 1 天 9 小时 |
| 负载 | 0.26, 0.25, 0.26 |
| SSH 连接 | ✅ 正常 |

### 2.2 核心服务端口
| 端口 | 服务 | 监听地址 | 状态 |
|------|------|----------|------|
| 11434 | Ollama API | `*` | 🟢 在线 |
| 9627 | 龍魂 Dashboard | `0.0.0.0` | 🟢 在线 |
| 8777 | Nginx 反代 | `0.0.0.0` | 🟢 在线 |
| 8443 | Web 门户 | `0.0.0.0` | 🟢 在线 |
| 8445 | Web 门户（本地） | `127.0.0.1` | 🟢 在线 |
| 9622 | 内网网关 | `127.0.0.1` | 🟢 在线 |
| 9623 | 注册中心 | `127.0.0.1` | 🟢 在线 |
| 8766 | AutoFlow 引擎 | `127.0.0.1` | 🟢 在线 |

### 2.3 Ollama 模型清单
- `kimi-k2.7-code:cloud`
- `longhun:latest`
- `longhun-v1.0:latest`
- `qwen2.5:1.5b`

---

## 三、鲲鹏桥接落地

### 3.1 SSH 隧道（Mac ↔ 鲲鹏）
脚本位置：`~/.longhun/scripts/ssh_tunnel_kunpeng.sh`

已建立隧道映射：

| 本地端口 | 方向 | 远程地址 | 用途 |
|----------|------|----------|------|
| `19623` | → | `127.0.0.1:9623` | 注册中心 |
| `19627` | → | `127.0.0.1:9627` | 龍魂 Dashboard |
| `11435` | → | `127.0.0.1:11434` | **Ollama API（鲲鹏）** |
| `19622` | → | `127.0.0.1:9622` | 内网网关 |
| `19624` | ← | `127.0.0.1:9623` | 反向：Mac 服务→鲲鹏 |

验证结果：
- `curl http://127.0.0.1:11435/api/tags` → HTTP 200 ✅
- `curl http://127.0.0.1:19627/` → HTTP 200 ✅
- `curl http://127.0.0.1:11435/api/generate` → 模型正常生成 ✅

### 3.2 FRP 内网穿透
- 鲲鹏 frps 监听 `*:7000`
- Mac frpc 运行中，配置：`deploy/frpc/frpc.toml`
- 当前已映射：
  - 本地 `8799`（小艺枢纽）→ 鲲鹏公网 `18799`
  - 本地 `18798`（小艺管理）→ 鲲鹏公网 `18798`

验证：
- 鲲鹏本机 `curl http://127.0.0.1:18799/health` → HTTP 200 ✅
- **公网 `119.13.90.27:18799` 不可达** → 华为云安全组未放行 18799，需登录控制台开启

### 3.3 本地服务启动与修复
#### 3.3.1 CNSH 网关（8765）
**问题 1**：启动失败，`~/cnsh/logs` 无法创建（macOS 大小写不敏感，`CNSH` 符号链接冲突）。
**修复**：将 `LOG_DIR` 默认改为 `~/longhun-system/logs/cnsh_gateway`，并支持 `CNSH_LOG_DIR` 环境变量覆盖。

**问题 2**：`DNA_TOKEN` 默认与 xiaoyi_hub 不一致，导致 403。
**修复**：将默认 `DNA_TOKEN` 改为 `LONGHUN-XIAOYI-HUB-8799-v1.0`。

**问题 3**：默认 `OLLAMA_HOST` 指向本地 `11434`，本地无 Ollama。
**修复**：将默认 `OLLAMA_HOST` 改为 `http://localhost:11435`（SSH 隧道→鲲鹏 Ollama）。

**新增端点**：`/api/xiaoyi/ask` 供 8799 小艺枢纽直接调用，内部降级到鲲鹏 Ollama。

验证：
```bash
curl -X POST http://127.0.0.1:8765/api/xiaoyi/ask \
  -H 'Content-Type: application/json' \
  -H 'X-DNA-Token: LONGHUN-XIAOYI-HUB-8799-v1.0' \
  -d '{"query":"你好，请一句话自我介绍"}'
# → HTTP 200，backend: 8765GPT→ollama(鲲鹏)
```

#### 3.3.2 小艺调度枢纽（8799）
**问题**：降级链中 8765GPT URL 为 `/chat`（要求 `message` 字段），Ollama URL 指向本地 `11434`。
**修复**：
- 8765GPT URL 改为 `http://localhost:8765/api/xiaoyi/ask`
- Ollama URL 改为 `http://localhost:11435/api/generate`
- 超时统一改为 60 秒

验证：
```bash
curl -X POST http://127.0.0.1:8799/hub/ask \
  -H 'Content-Type: application/json' \
  -d '{"query":"你好，请一句话自我介绍","format":"v2"}'
# → HTTP 200，backend: 8765GPT，route_trace: 8765GPT(HTTP 200)
```

---

## 四、最终链路验证

### 4.1 端到端调用路径
```
Mac 用户
  → http://127.0.0.1:8799/hub/ask
    → 小艺调度枢纽
      → 8765GPT (localhost:8765/api/xiaoyi/ask)
        → CNSH 网关
          → Ollama (localhost:11435)
            → SSH 隧道
              → 鲲鹏 Ollama (127.0.0.1:11434)
```

### 4.2 验证结果
| 链路 | 状态 |
|------|------|
| Mac → 8799 枢纽 | ✅ HTTP 200 |
| 8799 → 8765 网关 | ✅ HTTP 200 |
| 8765 → 11435 Ollama | ✅ HTTP 200 |
| 11435 → 鲲鹏 11434 | ✅ 模型生成正常 |
| 鲲鹏 Dashboard（19627） | ✅ HTTP 200 |
| 鲲鹏注册中心（19623） | ✅ HTTP 200 |

---

## 五、联动感知扫描

```bash
python3 bin/lh_cross_module_awareness.py --auto-fix
```

扫描结果：
- 自动注册了一批未注册的 bin 脚本
- 自动修复了一批缺少执行权限的脚本
- 发现一个主权适配层文件缺失的警告（`L1_内核层/kernel/masters/mcp_sovereignty_config.py`），标记为 🟡 待处理
- 无 🔴 断点

---

## 六、遗留问题与下一步

1. **华为云安全组 18799 未放行**
   - 现象：公网 `119.13.90.27:18799` 不可达
   - 解决：登录华为云控制台 → 安全组 → 添加入方向规则 TCP 18799

2. ** patrol 红旗：8 处示例敏感信息**
   - 已确认非真实密钥
   - 建议后续统一替换为占位符

3. **9622 操作台 `/api/xiaoyi/ask` 端点不存在**
   - 当前降级链中 8765GPT 已可用，不影响主链路
   - 如需 9622 支持，需补充对应端点

---

## 七、修改文件清单

| 文件 | 修改内容 |
|------|----------|
| `bin/cnsh_gateway.py` | LOG_DIR 默认路径、DNA_TOKEN、OLLAMA_HOST、新增 `/api/xiaoyi/ask` 端点、引入 logging |
| `bin/xiaoyi_hub_8799.py` | 8765GPT URL、Ollama URL、超时时间 |
| `02_執行記錄/patrol_20260727.md` | 自动更新 |
| `02_執行記錄/deploy_bridge_audit_20260727.md` | 本报告 |

---

**三色审计**：🟢 本地自检完成 + 鲲鹏桥接落地 + 端到端验证通过
