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
# 龍魂系统·API 技术文档 / Longhun System · API Reference

> DNA: #龍芯⚡️2026-09-05-API技术文档-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）· 代码: MulanPSL v2
> 文档版本: v5.2.0
> 三色: 🟢 端口与端点 2026-09-05 netstat/curl 实测

---

## [中文] API 端点文档

### 一、真实监听端口表（2026-09-05 实测）

#### 本机（macOS）
| 地址 | 端口 | 服务 | 说明 |
|---|---|---|---|
| 127.0.0.1 | 8091 | 三重主权 | 主权守护 |
| 0.0.0.0 | 8761 | dh-api | 数字人 API |
| 127.0.0.1 | 8768 | Notion 只读镜像 | Notion MCP 层 |
| 127.0.0.1 | 8970 | 透明审计 | 审计 API |
| 127.0.0.1 | 8971 | 服务控制 | 服务治理 |
| 127.0.0.1 | 9527 | 万年历服务 | 日历+记忆 HTTP（`/api/memory/*`） |
| 127.0.0.1 | 9628 | hash-api | 哈希产权引擎 API |

#### 鲲鹏（uid9622.cn · 华为云）
| 地址 | 端口 | 服务 | 说明 |
|---|---|---|---|
| 0.0.0.0 | 80/443 | nginx + lh-api | 对外主入口（`/api/onboarding/bootstrap` 等） |
| 127.0.0.1 | 8762 | 拓扑/JSON-RPC 网关 | 回环·服务器本机专用 |
| 127.0.0.1 | 8763-8766 | MCP readonly/audit/cal/knowledge-hub | 回环·仅服务器本机 |

> 安全说明：除 80/443 外，鲲鹏 API 全部绑 127.0.0.1 回环，不对外暴露——符合「无后台·零攻击面」P0 原则。

### 二、实测可用端点示例

#### 1) 万年历日历记忆（本机 9527 · 已实测 🟢）
```bash
curl http://127.0.0.1:9527/api/memory/status
# → {"ok": true, "days": 58, "entries": 85, "chain_links": 1, "chain_ok": true, ...}

curl http://127.0.0.1:9527/api/memory/search?q=龍魂     # 记忆检索
curl http://127.0.0.1:9527/api/memory/note              # POST 速记（append-only）
```

#### 2) 入口引导（鲲鹏对外 · P0）
```bash
curl https://uid9622.cn/api/onboarding/bootstrap
# → AI/开发者进门自动拉取规则包（协议: LH-AI-ONBOARDING-v1.0）
```

#### 3) JSON-RPC 网关（本机 8762 或鲲鹏回环 · 已实测 🟢）
```bash
curl http://127.0.0.1:8762/
# → {"jsonrpc": "2.0", "id": null, "error": {"code": -32601, "message": "路径不存在: /health"}}
# 说明：8762 为 JSON-RPC 2.0 分发网关，方法列表见 12_DOCS/JSONRPC.md
```

### 三、标准调用约定（通用）

- 认证/身份：`X-API-Key` + DNA 头（`#龍芯⚡️...`）+ 三色标记（统一账号模型）
- 内容：`Content-Type: application/json`
- 所有写入类 API 要求请求体含 `dna` 字段（追溯链焊死）
- 隐私：请求/日志不落明文密钥，敏感字段自动 `MELTDOWN`

### 四、通用错误码

| 错误码 | 含义 | 处理建议 |
|---|---|---|
| 200 | 成功 | — |
| 400 | 参数错误 | 检查请求体格式 |
| 401 | 未授权 | 检查 API Key / DNA 头 |
| 403 | 权限不足 | 检查角色层级（R1-R5） |
| 404 | 路径不存在 | 核对端点 |
| -32601 | JSON-RPC 方法不存在 | 核对 method 名 |
| 429 | 限流/余额不足 | 稍后重试或充值 |
| 500 | 服务内部错误 | 看 `~/.longhun/logs/` |

### 五、Python 调用示例

```python
import requests

# 1) 万年历记忆状态（本机）
print(requests.get("http://127.0.0.1:9527/api/memory/status", timeout=3).json())
# → {'ok': True, 'days': 58, 'entries': 85, 'chain_ok': True}

# 2) 记忆检索
r = requests.get("http://127.0.0.1:9527/api/memory/search",
                 params={"q": "龍魂"}, timeout=5)
print(r.json())

# 3) JSON-RPC 网关探活
r = requests.post("http://127.0.0.1:8762/",
                  json={"jsonrpc": "2.0", "method": "ping", "params": {}, "id": 1},
                  timeout=3)
print(r.status_code)   # 200 = 网关在线
```

---

## [English] API Reference

**Local (macOS)**: 8091 triple-sovereignty · 8761 dh-api · 8768 notion mirror · 8970 audit · 8971 service control · 9527 calendar-memory HTTP (`/api/memory/status` verified) · 9628 hash-api — all bound to 127.0.0.1 unless noted.

**Kunpeng (uid9622.cn)**: 80/443 public gateway (`/api/onboarding/bootstrap`) · 8762 JSON-RPC/topo gateway · 8763-8766 MCP cluster (loopback only, zero external attack surface).

**Conventions**: `X-API-Key` + DNA header + tri-color mark for unified accounts; write APIs require a `dna` field; no plaintext secrets in requests/logs (auto MELTDOWN).

**Error codes**: 200/400/401/403/404/429/500 + JSON-RPC -32601.

**Python**: use `requests`; verified samples above (`/api/memory/status` → 58 days/85 entries/chain OK).

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
