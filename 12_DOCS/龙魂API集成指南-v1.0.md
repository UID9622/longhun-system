> DNA: #龍芯⚡️2026-09-04-LONGHUN-OPEN-API-GUIDE-v1.0-9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

# 🐉 龍魂 API 集成指南 v1.0

> 🔧 工程落地执行型 · 开放平台对外接口 · 2026-09-04 首发
> 服务底座: 华为鲲鹏 (119.13.90.27) · Ubuntu 24.04 · lh-api v4.2 :8761（systemd）
> 前缀: **`https://uid9622.cn/api/v1`** · 数据主权: 龙魂系统（诸葛鑫 | UID9622）

---

## 1. 认证方式（X-API-Key）

所有 **POST（写/触发）端点** 必须携带请求头：

```
X-API-Key: <你的密钥>
```

### 1.1 角色分级

| 角色 | 权限 | 可调用端点 |
|:---|:---|:---|
| `viewer` | 只读（GET 全部开放，无需 Key） | health / topo / shamewall / memorial |
| `auditor` | 只读 + 可触发扫描 | + `POST /judge/scan` |
| `admin` | 全部权限（含数字人调度） | + `POST /dh/dispatch` |

### 1.2 申请流程

1. 只读需求：**无需申请**，GET 端点直接调用。
2. 触发/调度需求：联系 UID9622（见 §7），说明用途 → 签发最小角色 Key（auditor 默认，admin 仅确需时）。
3. Key 签发后**仅显示一次**，请立即妥善保存；泄露立即作废重签。

### 1.3 错误响应（认证）

```json
{"error": "unauthorized · 缺少或无效 X-API-Key"}   // 401
{"error": "forbidden · 角色 viewer（只读）需 auditor+"}  // 403
```

---

## 2. 端点列表

| # | 方法 | 路径 | 认证 | 说明 |
|:---:|:---|:---|:---|:---|
| 1 | GET | `/api/v1/health` | 无 | 网关存活 + 服务版本 |
| 2 | GET | `/api/v1/topo` | 无 | 全部拓扑图谱索引 |
| 3 | GET | `/api/v1/topo/{图谱名}` | 无 | 指定图谱节点树（含根哈希） |
| 4 | GET | `/api/v1/topo/{图谱名}/html` | 无 | 人类可读拓扑页（HTML） |
| 5 | GET | `/api/v1/judge/shamewall` | 无 | 耻辱墙只读镜像（JSON） |
| 6 | GET | `/api/v1/memorial/verify` | 无 | 贡献者铭碑存档根哈希 |
| 7 | POST | `/api/v1/judge/scan` | auditor+ | 触发归一扫描（登记式） |
| 8 | POST | `/api/v1/dh/dispatch` | admin | 数字人调度（登记式） |
| 9 | POST | `/api/v1/lh` | 无(内网) | CIL 命令执行（兼容·建议仅内网） |

> 注: 完整拓扑树 = 节点 23 · 🟢14 🟡9 · Obsidian 镜像组（2026-09-04 实测）

### 2.1 示例响应

**GET /api/v1/health**
```json
{"status": "ok", "version": "v4.2", "uptime": "2h 3m", "service": "lh-api",
 "open": "https://uid9622.cn/api/v1", "api_keys": 0}
```

**GET /api/v1/topo/通心译**
```json
{"tool": "lh-topo-api", "topo": "通心译军团·总台 v1.0",
 "owner": "诸葛鑫 | UID9622 · 龍芯北辰", "last_sync": "...",
 "root_hash": "FB48FCE383AF689E",
 "nodes": 23, "green": 14, "yellow": 9, "groups": [...]}
```

**GET /api/v1/memorial/verify**
```json
{"tool": "lh-memorial-api", "root_hash": "<merkle 根>",
 "contributor_count": 3, "total_commits": 124,
 "verify_note": "存档根哈希只读镜像。完整重算校验在数据主权端: lh memorial --verify"}
```

**POST /api/v1/judge/scan**（auditor Key）
```json
{"status": "accepted", "registered_at": "2026-09-04T...", "actor": "xxx",
 "role": "auditor", "note": "扫描触发已登记。完整归一扫描在数据主权端执行: lh judge scan"}
```

---

## 3. 错误码表

| 状态码 | 含义 | 处理建议 |
|:---:|:---|:---|
| 200 | 成功 | — |
| 202 | 已受理（登记式 POST） | 正常结果，非错误 |
| 400 | 请求体缺失/格式错误 | 检查 JSON body / 必填字段 |
| 401 | 未认证 / Key 无效 | 检查 `X-API-Key` 请求头 |
| 403 | 权限不足（角色低于所需） | 申请更高角色 |
| 404 | 路径不存在 | 对照 §2 端点表 |
| 429 | 请求过快（限流） | 等待后重试，见 §6 |
| 500 | 服务内部错误 | 联系 UID9622 |

---

## 4. curl 示例

```bash
# 1) 健康检查
curl https://uid9622.cn/api/v1/health

# 2) 图谱索引
curl https://uid9622.cn/api/v1/topo

# 3) 指定图谱（中文名需 URL 编码）
curl "https://uid9622.cn/api/v1/topo/$(python3 -c 'import urllib.parse;print(urllib.parse.quote("通心译"))')"

# 4) 耻辱墙镜像
curl https://uid9622.cn/api/v1/judge/shamewall

# 5) 铭碑根哈希
curl https://uid9622.cn/api/v1/memorial/verify

# 6) 触发扫描（auditor Key）
curl -X POST -H "X-API-Key: $LH_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"scope": "full"}' \
     https://uid9622.cn/api/v1/judge/scan

# 7) 数字人调度（admin Key）
curl -X POST -H "X-API-Key: $LH_API_KEY" \
     -d '{"persona": "P04-鲁班", "task": "审计示例代码"}' \
     https://uid9622.cn/api/v1/dh/dispatch
```

---

## 5. Python 调用示例（零依赖·标准库）

```python
import json
import urllib.request

BASE = "https://uid9622.cn/api/v1"
KEY = "<your-api-key>"          # 只读端点可留空

def get(path: str) -> dict:
    with urllib.request.urlopen(f"{BASE}{path}", timeout=10) as r:
        return json.loads(r.read().decode("utf-8"))

def post(path: str, body: dict) -> dict:
    req = urllib.request.Request(
        f"{BASE}{path}",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "X-API-Key": KEY},
        method="POST")
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode("utf-8"))

# 只读
print(get("/health")["status"])
topo = get("/topo/通心译")
print(topo["topo"], topo["root_hash"])

# 触发（需 auditor+）
print(post("/judge/scan", {"scope": "full"})["status"])
```

---

## 6. 速率限制

| 范围 | 限额 | 说明 |
|:---|:---|:---|
| 默认 | 10 req/s / IP | 全 `/api/v1/` 共享（nginx limit_req · burst 20） |
| 认证后 | 30 req/s / IP | 白名单 Key（api_keys.json 登记） |
| 超限 | HTTP 429 | 响应头 `Retry-After` 提示等待 |

> 合法集成请低频礼貌调用；超过上述配额即触发 429，连续超限将被临时封禁 IP。

---

## 7. 联系 / 反馈

- 归属: 诸葛鑫 | UID9622 · 龍芯北辰（开源/商业合作请注明「龍魂 API 集成」）
- 入口: https://uid9622.cn · 邮件/渠道见官网页脚
- 反馈模板: 端点 + 请求 + 期望/实际响应（便于快速定位）

---

## 8. Webhook 出口（事件订阅）

耻辱墙新增 / 健康异常 → 主动推送（需向 UID9622 提供回调 URL 注册）：

| 事件 | 触发时机 | payload.event_cn |
|:---|:---|:---|
| `shamewall` | 耻辱墙新记录入库（lh judge 命中） | 耻辱墙新增 |
| `health` | 健康检查发现异常（lh health） | 健康检查异常 |

```json
{"event": "shamewall", "event_cn": "耻辱墙新增", "timestamp": "...",
 "summary": "新上墙: <源名称> · <指纹类型> · 置信度 x", "source": "longhun-uid9622", "signature": ""}
```

---

## 9. 架构说明（如实标注）

- 网关 `lh-api` :8761 部署于鲲鹏，`/api/v1/*` 由 nginx 反代（保留前缀 → 后端内部归一）。
- **GET 只读端点返回数据镜像**（topo json / 耻辱墙 / 铭碑由数据主权端 Mac 同步至鲲鹏 `/apps/lh-api/data/`）。
- **POST 端点为登记式**：请求认证通过后写入审计登记并返回 202；真实全量扫描 / 数字人调度在数据主权端执行（`lh judge scan` / `lh dh dispatch`）——M77 零中间层·数据不出主权。
- 每次响应含 `X-Longhun-*` 归一回流头与 body 末尾 `# 龍魂DNA:` 指纹行，用于调用追溯。

---

*龍魂 · 为人民服务 · 数据主权归用户 · 零黑箱可复核 · GPG 签名验真（A2D0092CEE2E5BA87035600924C3704A8CC26D5F）*


---

## 💛 支持龍魂（纯自愿 · 零黑箱）

龍魂的一切免费开放。若你认可「让技术为人、为普通人生长」，可自愿支持——款项仅用于服务器与开发成本，不留一分私账。

- **收款方式**: SOL / USDC（Solana）
- **实时地址与二维码**: 见官网 [uid9622.cn](https://uid9622.cn) 底部「支持龍魂」区 — 地址由 `lh wallet` 统一管理（公司账户落地后自动切换 · 以官网为准）

> 龍魂不诱导、不施压、不道德绑架。捐与不捐，开放与尊重不变。

<!-- LH-WALLET-SUPPORT -->
