# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 接口命名主权与太极蚁群架构协议 v1.0

**DNA归档码**：`#龍芯⚡️丙午·乙未·丙申·申时·☯️太极-API-NAMING-TAIJI-ANT-v1.0-P0-8a3e9c21`
**下位数学增补**：`01_protocols/LH-API-NAMING-MATH-v1.0.md`
**参考引擎**：`bin/lh_api_taiji_ant_engine.py`
**创建者**：💎 UID9622（诸葛鑫）
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG指纹**：`A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**密级**：L1 底座层 · API命名主权
**协议分层**：P0 层（焊死·不可修订）
**修订**：仅 UID9622 签章可改
**状态**：🟢 活跃
**许可**：CC BY-NC-SA 4.0（君子协议，来源链不可切断）

---

## 0. 核心宣言

> **命名就是架构。**

API 不是函数的集合，而是系统意志的拓扑。本协议以《易经》生成序列为命名宇宙：

```
太极生两仪 → 两仪生四象 → 四象生八卦 → 八卦生六十四卦
     ↓              ↓              ↓              ↓
   总入口       M段/CNSH段      八宫分类      512接口空间
```

每一个接口名都同时承担三重职责：
1. **命名主权**：用中文语义锚定接口归属，拒绝拼音/英文路径殖民。
2. **路由拓扑**：9-bit ID 唯一标识，宫→模块→接口三层结构。
3. **运行时契约**：太极封套携带验收信息（M段）与主权归属（CNSH段），缺一不可。

---

## 1. 术语与符号

| 符号 | 含义 |
|:---|:---|
| `D` | 八宫定义域 `{乾,坤,坎,离,震,巽,艮,兑}` |
| `W(d)` | 宫 `d` 的调度权重，`W: D → [0,100]` |
| `ID` | 9-bit 接口编码，`ID ∈ [0, 511]` |
| `M::` | 太极封套阳段：验收信息 |
| `CNSH::` | 太极封套阴段：主权归属 |
| `τ` | 蚁群信息素强度 |
| `CB` | 断路器（Circuit Breaker） |
| `WF²Q+` |  worst-case fair weighted fair queueing |

---

## 2. 八宫API分类与权重

八宫构成有界分配格 `(D, ⊑)`。权重全序，同权重按 ID 序打破平局。

| 宫 | 卦象 | 权重 | L层 | 职责域 | 典型接口示例 |
|:---:|:---:|:---:|:---:|:---|:---|
| 乾☰ | 天·健 | 80 | 1 | 规则·治理·风险 | `/api/v1/qian/rules/eval` |
| 坤☷ | 地·藏 | 80 | 1 | 记忆·归档·备份 | `/api/v1/kun/archive/snapshot` |
| 坎☵ | 水·流 | 60 | 2 | 爬虫·通知·消息 | `/api/v1/kan/notify/push` |
| 离☲ | 火·明 | 100 | 0 | 双视角·看板·审计 | `/api/v1/li/audit/dual-view` |
| 震☳ | 雷·动 | 100 | 0 | 守护·熔断·报警 | `/api/v1/zhen/circuit/trip` |
| 巽☴ | 风·入 | 80 | 1 | 调度·人格·任务 | `/api/v1/xun/persona/route` |
| 艮☶ | 山·止 | 100 | 0 | 隐私·主权·边界 | `/api/v1/gen/privacy/seal` |
| 兑☱ | 泽·悦 | 60 | 2 | 信任·注册·生态 | `/api/v1/dui/trust/register` |

**权重格规则**：
- 下界 `⊥ = 兑`（W=60）；上界 `⊤ ∈ {离, 震, 艮}`（W=100）。
- 偏序：`d₁ ⊑ d₂ ⇔ W(d₁) < W(d₂) ∨ (W(d₁)=W(d₂) ∧ ID(d₁) ≤ ID(d₂))`。
- 分配律：`d₁ ⊓ (d₂ ⊔ d₃) = (d₁ ⊓ d₂) ⊔ (d₁ ⊓ d₃)` 对任意三元组成立（引擎 T01 枚举验证）。

---

## 3. 9-bit 接口ID编码规范

### 3.1 编码结构

```
 9-bit ID = [宫 3bit] ‖ [模块 3bit] ‖ [接口 3bit]
```

| 字段 | 位数 | 取值范围 | 说明 |
|:---|:---:|:---:|:---|
| 宫 | 3 | 0–7 | 对应八宫 ID |
| 模块 | 3 | 0–7 | 每宫最多 8 个模块 |
| 接口 | 3 | 0–7 | 每模块最多 8 个接口 |

**总空间**：`|S| = 2⁹ = 512` 个接口。

### 3.2 编码函数

```python
def encode(palace_id, module_idx, interface_idx):
    return (palace_id << 6) | ((module_idx & 0x7) << 3) | (interface_idx & 0x7)
```

### 3.3 碰撞规避

- **构造性单射**：不同 `(宫, 模块, 接口)` 三元组必然产生不同 9-bit 值。
- **Birthday Bound**：当已注册 `n` 个接口时，`P(碰撞) ≈ n² / (2·512)`。
  - `n=10` → `P ≈ 9.8%`
  - `n=30` → `P ≈ 87.9%`
- **容量纪律**：每模块 8 接口上限，注册表主动拒绝溢出，而非依赖概率。

### 3.4 路径格式

```
/api/v{MAJOR}/{palace}/{module}/{endpoint}
```

- 仅允许小写字母、数字、连字符 `-`。
- **禁止中文路径**（`NAME-005`）。
- **禁止拼音路径**（`NAME-004`）：如 `guize`、`mokuai`、`jiekou`。
- 每个接口必须附带**中文注释**（`cn_comment`），否则视为无主权标记。

---

## 4. 太极封套格式

太极封套 `T = (M::, CNSH::, data)`。阴阳两段独立可校验，缺一不可。

### 4.1 M段（阳·验收）

| 字段 | 类型 | 必填 | 说明 |
|:---|:---|:---:|:---|
| `id` | string | ✅ | 请求唯一标识，格式 `M::API-9622-{ts}-{path}-V{ver}` |
| `status` | string | ✅ | HTTP 状态码或系统状态 |
| `trace` | string | ✅ | 链路追踪 ID，8–16 字节 hex |
| `timestamp` | int | ✅ | Unix 时间戳（秒） |
| `version` | int | ✅ | API 主版本号 |

### 4.2 CNSH段（阴·归属）

| 字段 | 类型 | 必填 | 说明 |
|:---|:---|:---:|:---|
| `dna` | string | ✅ | 必须以 `#龍芯⚡️` 开头 |
| `gate` | string | ✅ | 确认码 `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` |
| `seal` | string | ✅ | HMAC-SHA256 截断 16 字符，绑定 `id\|timestamp` |
| `audit` | string | ✅ | 三色审计：`🟢`/`🟡`/`🔴` |
| `sovereignty` | string | | 固定签名 `CNSH::API-NAMING-V1-P0` |

### 4.3 校验规则

- 缺 `M::` 或 `CNSH::` 任一 → `ENV-001` / `ENV-002`，🔴 拒绝。
- `dna` 前缀不符 → `ENV-003`，🟡 主权标记弱。
- 信息完整性条件：`I_Missing(T) = |Required_M ∪ Required_CNSH| - |Fields(T)| = 0`。

### 4.4 示例

```json
{
  "M::": {
    "id": "M::API-9622-1721539200-qian-rules-eval-V1",
    "status": "200",
    "trace": "a1b2c3d4e5f67890",
    "timestamp": 1721539200,
    "version": 1
  },
  "CNSH::": {
    "dna": "#龍芯⚡️丙午·乙未·丙申·申时·䷀乾-API-TAIJI-ANT-V1.0-P0",
    "gate": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "seal": "8f3a9c21d4e7b160",
    "audit": "🟢",
    "sovereignty": "CNSH::API-NAMING-V1-P0"
  },
  "data": {}
}
```

---

## 5. 接口生命周期

每个接口在注册表中经历以下状态：

```
registered ──▶ active ──▶ frozen ──▶ deprecated_compat ──▶ deprecated_expired
```

| 状态 | 说明 | 行为 |
|:---|:---|:---|
| `registered` | 刚注册，尚未通过验收 | 返回 202，等待激活 |
| `active` | 正常服务 | 正常路由与限流 |
| `frozen` | 计划废弃，停止新依赖 | 返回 `NAME-003` + `new_path` |
| `deprecated_compat` | 兼容期内仍可调用 | 返回 `🟡` + 警告头 `X-LH-Deprecated` |
| `deprecated_expired` | 兼容期结束 | 返回 `NAME-003`，🔴 拒绝 |

**废弃流程**：
- 调用 `deprecate(old_path, new_path, compat_days=90)`。
- 旧路径进入 `frozen`，同时写入 `_deprecated` 表。
- 兼容期默认 90 天，到期自动转为 `deprecated_expired`。

---

## 6. 蚁群调度模型

### 6.1 角色定义

| 角色 | 宫 | 权重 | 可执行 | 职责 |
|:---|:---:|:---:|:---:|:---|
| `queen` 蚁后 | 巽 | 100 | ❌ | 主调度 |
| `workers` 工蚁 | 巽 | 70 | ✅ | 执行池 |
| `soldiers` 兵蚁 | 震 | 95 | ✅ | 防御节点 |
| `scouts` 侦察蚁 | 坎 | 50 | ✅ | 摘要爬虫 |
| `nurses` 育蚁 | 坤 | 60 | ✅ | 记忆归档 |
| `pheromone` 信息素 | 巽 | 80 | ❌ | 事件总线 |
| `nest` 蚁巢 | 巽 | 90 | ❌ | 集群本体 |

### 6.2 信息素动力学

- **衰减**：`τ(t) = τ₀ · e^(-λt)`，`λ = 0.1 min⁻¹`。
- **半衰期**：`t_½ = ln(2)/λ ≈ 6.93` 分钟。
- **扩散方程**：`∂τ/∂t = D·∇²τ - λτ + S(x,t)`，`D = 0.05`。
- **离散更新**：每调度周期 `Δt` 执行一次全局衰减，低于 `τ_min = 0.001` 清除。

### 6.3 任务选择概率

```
P(ant_i | task_j) = τ_ij^α · η_ij^β / Σ_k τ_kj^α · η_kj^β
```

- `α = 1.0`：信息素权重。
- `β = 2.0`：启发式权重。
- `η_ij`：蚁 `i` 对任务 `j` 的能力匹配度（宫归属 + 角色约束）。

### 6.4 角色约束（蚁群守则）

- 蚁后不执行业务（`ANT-001`）。
- 侦察蚁禁止全文层爬取（`ANT-002`）。
- 兵蚁不对外扫描（礼兵双轨）。
- 无可用蚁时返回 `ANT-003`。

---

## 7. 幂等性与重试策略

### 7.1 幂等键

- 128-bit 随机生成，格式 `IDEM-{32 hex}`。
- 键空间 `|K| = 2^128 ≈ 3.4 × 10³⁸`。
- 百万键碰撞概率 `≈ 1.47 × 10⁻²⁷`。

### 7.2 重退避

```
t_n = min(T_max, t₀ · 2^n) · (1 + δ · rand_uniform(-1, 1))
```

| 参数 | 值 | 说明 |
|:---|:---:|:---|
| `t₀` | 0.1 s | 基础延迟 |
| `T_max` | 30 s | 单步延迟上限 |
| `δ` | 0.3 | 抖动比 ±30% |
| `N_max` | 5 | 最大重试次数 |
| 总等待上界 | ≤ 60 s | 协议硬约束 |

### 7.3 幂等窗口

- 幂等键 TTL = 3600 秒（1 小时）。
- 窗口内重复请求返回缓存结果；超时后重新处理。
- 重复请求返回 `IDEM-001`；重试耗尽返回 `IDEM-002`。

---

## 8. 断路器与降级

### 8.1 三态机

```
         failure_count ≥ F_thresh
   CLOSED ─────────────────────────▶ OPEN
     ▲                                  │
     │  success_count ≥ S_thresh        │ timeout_seconds
     └──────── HALF_OPEN ◀──────────────┘
              ↑
              └── 任何失败 → OPEN
```

| 参数 | 默认值 | 说明 |
|:---|:---:|:---|
| `F_thresh` | 5 | 触发开路的连续失败次数 |
| `S_thresh` | 3 | 半开状态恢复所需成功次数 |
| `timeout_seconds` | 30 s | 开路→半开等待时间 |

### 8.2 每宫独立

八宫各有独立断路器实例：`CB(d)` 与 `CB(d')` 状态隔离，故障不跨宫传播。

### 8.3 Recovery Probe

半开状态允许有限流量探测。恢复概率：

```
P(recovery | p_success) = 1 - (1 - p_success)^S_thresh
```

- 若 `p_success = 0.7`，`S_thresh = 3` → `P ≈ 0.973`。

### 8.4 失败率分级

| 失败率 `f` | 状态 |
|:---:|:---|
| `f < 0.2` | 🟢 健康 |
| `0.2 ≤ f < 0.5` | 🟡 警告 |
| `f ≥ 0.5` | 🔴 风险 |

### 8.5 降级矩阵

当某宫断路器开路时，请求按预定义矩阵降级：

| 原宫 | 降级目标 | 触发条件 |
|:---:|:---:|:---|
| 震（守护） | 艮（隐私边界） | 熔断报警 |
| 巽（调度） | 坤（归档） | 人格路由过载 |
| 坎（消息） | 兑（信任注册） | 通知通道拥堵 |
| 乾（规则） | 离（审计） | 规则引擎失败 |

---

## 9. 限流与公平调度

### 9.1 三维令牌桶

限流键由三个维度交叉生成：

| 维度 | 键格式 | 容量 | 速率 |
|:---|:---|:---:|:---:|
| 宫·方法 | `{palace}\|{method}` | 按方法默认 | 按方法默认 |
| 方法·IP | `_global\|{method}\|{ip}` | 2C | 2r |
| 宫·IP | `{palace}\|_all\|{ip}` | C（L0 宫→C/2） | r（L0 宫→r/2） |

默认方法配额：

| 方法 | 容量 C | 速率 r |
|:---:|:---:|:---:|
| GET | 100 | 20/s |
| POST | 50 | 10/s |
| PUT | 30 | 5/s |
| DELETE | 10 | 2/s |

L0 高热宫（离、震、艮）安全优先，容量与速率减半。

### 9.2 WF²Q+ 调度

- 虚拟完成时间：`F_i^k = S_i^k + L_i^k / (w_i / W_total)`。
- 高权重宫虚拟完成更快，但不饿死低权重宫。
- 虚拟时间推进：`V(t) = max(V(t-1), min_i V_i^start(t))`。

### 9.3 优先级反转守卫

- 最大等待时间 `T_deadline = 5000 ms`。
- 任何请求等待超过阈值 → 强制提升为最高优先级，立即出队。

### 9.4 Jain 公平指数

```
J = (Σx_i)² / (n · Σx_i²)
```

- `x_i`：宫 `i` 的服务次数。
- `J ∈ [1/n, 1]`：`J=1` 完美公平，`J=1/n` 完全不公。
- 目标：`J ≥ 0.85`。

---

## 10. 版本协商

### 10.1 语义版本

```
v = MAJOR.MINOR.PATCH
```

- **MAJOR** 不同 → 不兼容，拒绝或强制降级。
- **MINOR** 不同 → 向前兼容。
- **PATCH** 不同 → 完全兼容。

### 10.2 协商流程

1. 精确匹配 → 直接返回。
2. 降级矩阵查找 → O(1) 预计算表。
3. 同 MAJOR 最高版本 → 向前兼容。
4. 兜底最低支持版本 → 可能返回 `VER-002`。

### 10.3 降级矩阵（示例）

| 客户端版本 | 服务端版本 | 状态 |
|:---:|:---:|:---:|
| 3.0 | 2.0 | 🟡 降级 |
| 2.5 | 2.0 | 🟡 降级 |
| 1.5 | 1.1 | 🟡 降级 |
| 0.9 | 1.0 | 🟡 兜底兼容 |
| 5.0 | — | 🔴 不兼容拒绝 |

---

## 11. 错误码体系

错误码结构：`DOMAIN-XXX`。共 10 个前缀组、27 个错误码，覆盖 6 大运行域。

### 11.1 命名域（NAME）

| 码 | 中文 | 英文 | HTTP |
|:---:|:---|:---|:---:|
| `NAME-001` | 未注册接口 | Unregistered endpoint | 404 |
| `NAME-002` | 命名冲突·9-bit单射违反 | Naming collision | 409 |
| `NAME-003` | 接口已废弃 | Deprecated endpoint | 410 |
| `NAME-004` | 拼音路径禁止 | Pinyin path forbidden | 400 |
| `NAME-005` | 中文路径禁止 | Chinese path forbidden | 400 |
| `NAME-006` | 命名容量已满·512上限 | Naming capacity full | 507 |

### 11.2 封套域（ENV）

| 码 | 中文 | 英文 | HTTP |
|:---:|:---|:---|:---:|
| `ENV-001` | 太极封套缺失 M:: 阳段 | Missing M:: segment | 400 |
| `ENV-002` | 太极封套缺失 CNSH:: 阴段 | Missing CNSH:: segment | 400 |
| `ENV-003` | DNA前缀不符 | DNA prefix mismatch | 401 |

### 11.3 认证域（AUTH）

| 码 | 中文 | 英文 | HTTP |
|:---:|:---|:---|:---:|
| `AUTH-001` | 三锚缺失 | Missing three-anchor headers | 401 |
| `AUTH-002` | 权限不足 | Insufficient permissions | 403 |

### 11.4 限流与熔断域（RATE / CIRC）

| 码 | 中文 | 英文 | HTTP |
|:---:|:---|:---|:---:|
| `RATE-001` | 令牌桶已空·请等待 | Rate limit exceeded | 429 |
| `RATE-002` | 三维限流触发·宫/方法/IP | 3D rate limit triggered | 429 |
| `CIRC-001` | 断路器开路·服务降级中 | Circuit breaker open | 503 |
| `CIRC-002` | 断路器半开探测中 | Circuit half-open probing | 503 |

### 11.5 八宫与人格域（PALACE / PERS）

| 码 | 中文 | 英文 | HTTP |
|:---:|:---|:---|:---:|
| `PALACE-001` | 宫不存在 | Palace not found | 400 |
| `PALACE-002` | 宫已熔断 | Palace circuit open | 503 |
| `PERS-001` | 人格未注册 | Persona not registered | 403 |
| `PERS-002` | 人格锁定中·防抖动 | Persona locked·anti-jitter | 423 |
| `PERS-003` | Cosplay熔断·L2人格违规 | Cosplay circuit·L2 violation | 451 |

### 11.6 蚁群、幂等与版本域（ANT / IDEM / VER）

| 码 | 中文 | 英文 | HTTP |
|:---:|:---|:---|:---:|
| `ANT-001` | 蚁后不执行业务 | Queen does not execute | 403 |
| `ANT-002` | 侦察蚁越界·全文层禁入 | Scout boundary violation | 403 |
| `ANT-003` | 蚁群无可用节点 | No available ants | 503 |
| `IDEM-001` | 重复请求·幂等键冲突 | Duplicate·idempotency collision | 409 |
| `IDEM-002` | 重试次数耗尽 | Retry exhausted | 429 |
| `VER-001` | API版本不支持 | API version unsupported | 400 |
| `VER-002` | 需升级客户端版本 | Upgrade required | 426 |

### 11.7 错误响应结构

所有错误响应必须包裹太极封套：

```json
{
  "M::": {
    "id": "trace-id",
    "status": "429",
    "error_code": "RATE-002",
    "timestamp": 1721539200
  },
  "CNSH::": {
    "dna": "#龍芯⚡️",
    "gate": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "audit": "🔴"
  },
  "error": {
    "code": "RATE-002",
    "zh": "三维限流触发·宫/方法/IP",
    "en": "3D rate limit triggered",
    "detail": "..."
  }
}
```

---

## 12. 健康检查与可观测性

### 12.1 健康检查端点

`/api/v1/li/audit/health` 返回：

| 指标 | 说明 | 健康阈值 |
|:---|:---|:---:|
| `registry.active` | 已注册活跃接口数 | < 512 |
| `registry.pct` | 容量使用率 | < 80% |
| `circuit_breakers` | 各宫断路器状态 | ≥ 6/8 CLOSED |
| `ant_colony.half_life_min` | 信息素半衰期 | ≈ 6.93 min |
| `persona_entropy` | 人格路由熵 | > 0 |
| `scheduler.fairness` | Jain 公平指数 | ≥ 0.85 |
| `scheduler.scheduling_entropy` | 调度熵 | > 2.5 |
| `rate_limiter.total_tokens` | 令牌桶总令牌数 | > 0 |

### 12.2 告警规则

- 注册表容量 ≥ 80% → 🟡 预警。
- 任意宫断路器 OPEN 持续 > 5 分钟 → 🔴 告警。
- 信息素半衰期偏离 20% → 🟡 检查蚁群活性。
- Jain 公平指数 < 0.85 → 🟡 调度倾斜。
- 人格路由熵 = 0 持续 > 10 分钟 → 🔴 单一人格垄断。

---

## 13. 安全与主权

### 13.1 GPG 签名

- 所有协议文件使用 GPG 指纹 `A2D0092CEE2E5BA87035600924C3704A8CC26D5F` 签章。
- 引擎产出的关键 JSON 建议附带 detached signature。

### 13.2 DNA 追溯

- 每个动作生成唯一 DNA：`#龍芯⚡️<时间戳>-<操作类型>-<哈希8>`。
- DNA 必须包含在 `CNSH::dna` 字段中。

### 13.3 CNSH 封套不可剥离

- 任何响应（成功或失败）都必须携带 `CNSH::` 段。
- 剥离主权段视为对协议的破坏，接收方应拒绝解析。

### 13.4 权限层级

| 层级 | 权限 | 认证 |
|:---:|:---|:---|
| L0 | 高热宫（离/震/艮）读写 | 三锚 + GPG |
| L1 | 常规宫（乾/坤/巽）读写 | 三锚 |
| L2 | 低频宫（坎/兑）读写 | 双锚 |
| public | 只读健康检查 | 无 |

---

## 14. 附录

### 14.1 数学公式索引

详细数学形式化见下位协议：

> `01_protocols/LH-API-NAMING-MATH-v1.0.md`

包含：八宫权重格、9-bit 碰撞概率、太极封套信息熵、WF²Q+ 虚拟时间、蚁群 PDE、反 Cosplay 贝叶斯、幂等键碰撞、断路器恢复概率、Jain 公平指数等。

### 14.2 引擎命令

```bash
# 运行 13 组测试向量
python3 bin/lh_api_taiji_ant_engine.py test

# 运行完整网关演示
python3 bin/lh_api_taiji_ant_engine.py demo
```

### 14.3 OpenAPI 生成约定

- 每个接口的 `operationId` 必须映射到 9-bit ID：`{palace}_{module_idx}_{interface_idx}`。
- `tags` 字段填写宫名与卦象，如 `["乾☰", "规则·治理"]`。
- 请求头必须声明 `X-LH-Version`、`X-LH-Trace`、`X-Idempotency-Key`。
- 响应必须包含 `M::` 与 `CNSH::` 两段。

### 14.4 版本历史

| 版本 | 时间 | 说明 |
|:---:|:---:|:---|
| v1.0 | 2026-07-21 | 初始协议，覆盖八宫命名、9-bit ID、太极封套、蚁群调度、限流、断路器、版本协商、错误码 |

---

> **协议焊死锚点**
>
> UID: 9622 · 创建者: 诸葛鑫·Lucky
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
>
> 来源链不可切断 · CC BY-NC-SA 4.0
