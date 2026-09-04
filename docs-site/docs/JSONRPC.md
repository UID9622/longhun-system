# 龍魂系统·JSON-RPC 接口文档 / Longhun System · JSON-RPC Reference

> DNA: #龍芯⚡️2026-09-05-JSONRPC-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）· 代码: MulanPSL v2
> 文档版本: v5.2.0
> 三色: 🟢 网关与引擎内嵌 RPC 2026-09-05 实测存在

---

## [中文] JSON-RPC 2.0 接口

### 一、两层 JSON-RPC（实测）

| 层 | 位置 | 说明 |
|---|---|---|
| 引擎内嵌 | `lh ledger rpc`（龍魂账法） | 账本子命令 `rpc` 提供 JSON-RPC 调用模式（与 dna/hash/add/verify 并列） |
| 网络网关 | 127.0.0.1:8762（本机/鲲鹏回环） | JSON-RPC 2.0 分发网关·实测返回标准错误帧 |

### 二、引擎内嵌示例（龍魂账法 v1.0）

```bash
# 查看 rpc 模式用法
python3 08_BIN/lh_ledger.py rpc --help

# 典型调用形态（方法 = 账本原子操作）
lh ledger rpc <method> [params...]
# 例：lh ledger rpc balance       → 资产负债权益（恒等式）
#     lh ledger rpc add T1 1001 3201 1条 --note 测试
#     lh ledger rpc verify        → 账本完整性校验
```

### 三、网络网关 8762

```bash
# 探活（任何非法路径返回标准 JSON-RPC 错误帧 = 网关在线）
curl http://127.0.0.1:8762/
# → {"jsonrpc": "2.0", "id": null, "error": {"code": -32601, "message": "路径不存在: /health"}}
```

通用请求格式（JSON-RPC 2.0）：

```json
{"jsonrpc": "2.0", "method": "longhun.<模块>.<方法>", "params": {}, "id": 1}
```

批量调用（Batch）：

```json
[
  {"jsonrpc": "2.0", "method": "longhun.health", "params": {}, "id": 1},
  {"jsonrpc": "2.0", "method": "longhun.ledger.balance", "params": {}, "id": 2}
]
```

### 四、方法命名约定（longhun.*）

- 方法名 = 28 顶层命令映射：`longhun.health` / `longhun.ledger.balance` / `longhun.calmem.status` / `longhun.fraud.scan` ...
- 实际可用方法以网关响应为准（无方法注册表时返回 -32601，核对 `lh <模块> --help`）
- 写操作请求体必须带 `dna` 字段（追溯链）

### 五、返回结构

```json
{"jsonrpc": "2.0", "result": {"ok": true, "triColor": "🟢", ...}, "id": 1}
{"jsonrpc": "2.0", "error": {"code": -32601, "message": "..."}, "id": 1}
```

---

## [English] JSON-RPC 2.0 Interface

Two real layers:
1. **Engine-embedded RPC**: `lh ledger rpc` (part of the 龍魂账法 v1.0 CLI, verified).
2. **Network gateway**: `127.0.0.1:8762` (loopback, returns standard JSON-RPC error frames — verified).

Request format: `{"jsonrpc":"2.0","method":"longhun.<module>.<method>","params":{},"id":1}` — batch arrays supported. Write calls must carry a `dna` field. Method availability is confirmed via gateway response (`-32601` = method not registered).

---
🐉 2026-09-05 · 丙午年·壬申月·庚戌日 · UID9622 · 🟢
