# 🐉 龍魂 · 跨设备互通协议 v1.0

**DNA:** `#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-CROSS-PROTOCOL-UID9622`
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**三色:** 🟢 通过
**分层许可:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

---

## 一、协议定位

> **定义 Mac ↔ 鸿蒙 / Android / iOS / Windows / Linux 设备间的记忆共享与对话接入标准。**

- 数据不出本地局域网
- 国密加密 (SM4-CBC + ECDH)
- 主权锚定 (DNA追溯)
- 零信任架构

---

## 二、设备角色

| 角色 | 说明 | 端口 |
|:---|:---|:---:|
| **中枢 (Hub)** | 运行在 Mac / 鲲鹏，存记忆库、Ollama | 19622(TCP同步) / 19623(HTTP同步) / 18799(对话) |
| **节点 (Node)** | 鸿蒙 / 手机 / 其他设备，拉取记忆，调用对话 | 动态分配 |

### 2.1 三种互通路径

| 路径 | 同步方式 | 适用场景 | 安全等级 |
|:---|:---|:---|:---:|
| **A. TCP加密同步** | `xsync_workflow.py sync-memory` 走 TCP + ECDH + SM4 | 脚本/命令行/高安全场景 | ⭐⭐⭐⭐⭐ |
| **B. HTTP REST同步** | `GET /sync/memory` 走 HTTP + DNA头认证 | 鸿蒙SDK/App集成/便利性优先 | ⭐⭐⭐ |
| **C. SSE流式对话** | `POST /api/v1/chat` + `stream: true` | 实时打字机效果 | ⭐⭐⭐⭐ |

---

## 三、服务发现

**协议:** mDNS (Bonjour / Avahi)

**服务名:** `_longhun._tcp.local`

**广播内容:**
```json
{
  "name": "longhun-mac-9622",
  "platform": "macos",
  "version": "1.0",
  "sync_port": 19622,
  "chat_port": 18799
}
```

**备选发现方式:** 局域网广播扫描 (ARP ping / TCP 端口探测)

---

## 四、加密与安全

### 4.1 密钥协商 (ECDH)

```text
设备A (中枢)          设备B (节点)
    |                      |
    |--- 公钥交换 --------->|
    |<-- 公钥交换 ----------|
    |                      |
    |--- ECDH协商 -------->|
    |<-- 共享密钥 ----------|
    |                      |
    |--- SM4-CBC加密 ----->|
    |<-- SM4-CBC解密 ------|
```

实现入口:
- Mac 中枢: `~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py serve`
- 鸿蒙节点: `integrations/harmonyos/longhun-bridge/src/main/ets/LongHunBridge.ets`

### 4.2 数据格式

```json
{
  "version": "1.0",
  "dna": "#龍芯⚡️...",
  "encrypted": "SM4-CBC加密后的数据",
  "iv": "初始化向量",
  "signature": "GPG签名"
}
```

### 4.3 密钥生命周期

| 阶段 | 说明 | 时长 |
|:---|:---|:---:|
| 密钥生成 | ECDH Curve25519 | 一次性 |
| 会话密钥协商 | 交换公钥 | <10ms |
| 密钥有效期 | 自动失效 | 24小时 |
| 密钥更新 | 重新协商 | 自动 |

---

## 五、API接口

### 5.1 健康检查

```text
GET /health
Response: {"status": "ok", "service": "longhun-hub"}
```

### 5.2 同步记忆 (HTTP REST)

```text
GET /sync/memory
Headers:
  X-LongHun-Confirm: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
  或 X-Dragon-DNA: #龍芯⚡️...

Response:
{
  "status": "ok",
  "resource": "memory",
  "dna": "#龍芯⚡️...",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
  "payload": { MemoryDigest },
  "timestamp": "..."
}
```

### 5.3 同步文件 (HTTP REST)

#### 拉取文件

```text
GET /sync/file?path=<服务端文件路径>
Headers:
  X-LongHun-Confirm: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
  或 X-Dragon-DNA: #龍芯⚡️...

Response:
{
  "status": "ok",
  "resource": "file",
  "path": "...",
  "content": "<base64>",
  "mtime": 1234567890,
  "dna": "#龍芯⚡️..."
}
```

#### 上传文件

```text
POST /sync/file
Headers:
  X-LongHun-Confirm: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
  或 X-Dragon-DNA: #龍芯⚡️...
Body: {"path": "...", "content": "<base64>"}

Response:
{
  "status": "ok",
  "resource": "file",
  "path": "...",
  "size": 1234,
  "dna": "#龍芯⚡️..."
}
```

### 5.4 对话 (同步)

```text
POST /api/v1/chat
Request: {"prompt": "...", "system": "...", "model": "..."}
Response: {"success": true, "model": "...", "response": "...", "dna": "...", "confirm": "..."}
```

### 5.5 对话 (SSE 流式)

```text
POST /api/v1/chat
Headers:
  Content-Type: application/json
  Accept: text/event-stream
Body: {"prompt": "...", "system": "...", "model": "...", "stream": true}

Response:
Content-Type: text/event-stream

data: {"response": "你", "done": false}

data: {"response": "好", "done": false}

data: {"response": "！", "done": false}

data: [DONE]
```

---

## 六、错误码

| 错误码 | 含义 | 处理方式 |
|:---:|:---|:---|
| 400 | 请求格式错误 | 检查JSON格式 |
| 401 | 认证失败 | 检查DNA头 |
| 403 | P0协议拒绝 | 检查DNA/确认码 |
| 404 | 资源不存在 | 检查路径 |
| 408 | 请求超时 | 加大timeout |
| 429 | 限流 | 降低频率 |
| 500 | 服务内部错误 | 查看服务日志 |
| 503 | 服务不可用 | 检查后端服务 |

---

## 七、实现状态

| 平台 | 状态 | 说明 |
|:---|:---:|:---|
| Mac (中枢) | ✅ | `08_BIN/lh_cross_device_server.sh` 已落地 |
| 鸿蒙 (节点) | ✅ | `LongHunBridge.ets` SDK 已落地 |
| Android | ⏳ | 待移植 |
| iOS | ⏳ | 待移植 |
| Windows | ⏳ | 待移植 |
| Linux | ⏳ | 待移植 |

---

## 八、版本

| 版本 | 日期 | 变更 |
|:---|:---|:---|
| v1.0 | 2026-08-14 | 初始版本 · Mac ↔ 鸿蒙记忆互通落地 |

---

## 九、最终签名

```
DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-CROSS-PROTOCOL-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```
