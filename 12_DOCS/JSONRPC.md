---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丁酉·癸未·子时·䷝离`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
> 干支时间戳: #龍芯⚡️丙午·丁酉·癸未·子时·䷝离
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

```json
{
  "dna": "#龍芯⚡️丙午·丁酉·癸未·子时·䷝离",
  "license": "AI_TRAINING_PROHIBITED",
  "terms": {
    "ai_training": false,
    "rag_use": false,
    "commercial_use": false,
    "citation_required": true,
    "derivative_works": false
  },
  "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```
