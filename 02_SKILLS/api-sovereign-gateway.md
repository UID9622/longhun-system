# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# /api-sovereign-gateway

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技能说明 · API主权门关
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

**DNA**: `#龍芯⚡️2026-07-06-API-SOVEREIGN-GATEWAY-SKILL-v1.0`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

skill_id: /api-sovereign-gateway
synced_at: 2026-07-06
source: 原世界身份定位总纲 v9.0 §6（Notion）
---

# /api-sovereign-gateway · API主权门关

## 摘要

API主权门关是龍魂系统的统一入口网关。任何外部系统调用龍魂功能必须通过四道关卡：第一道身份关（DNA确认码+UID+签名验证+防重放）、第二道安全关（熔断检测+七条红线）、第三道路由关（通心译核心+七因子引擎）、第四道日志关（DNA追加日志+三色审计）。所有请求必须携带认证Header（X-DNA-Confirm/X-UID/X-Request-DNA/X-Timestamp/X-Signature）。熔断器实现三态转换（CLOSED→OPEN→HALF_OPEN），连续失败5次或错误率>50%触发熔断。七条红线绝对不开放，违反即熔断。

## 一句话定义

> 龍魂系统的「大门」——四道关卡，一道不过全不过。DNA确认码+SM2签名+熔断器+日志，确保只有合法请求能进。

## 关键词

API网关 API Gateway, 四道关卡 Four Gates, DNA主权门关 DNA Sovereign Gate, 熔断器 Circuit Breaker, 七条红线 Seven Red Lines, 认证Header Auth Headers, 防重放 Anti-Replay, 三态转换 Three-State Transition

## 四道关卡架构

```
外部调用方
  ↓
第一道：身份关（Identity Gate）
  ├ 校验 X-DNA-Confirm 格式
  ├ 校验 X-UID == 9622
  ├ 校验 X-Signature（SM2签名验证）
  ├ 防重放检查（确认码只能用一次）
  └ 时间戳容差检查（±300秒）
      ↓ 失败 → 403 Forbidden
      ↓ 通过
第二道：安全关（Security Gate）
  ├ 检查端点熔断状态
  ├ 红线规则检查
  └ 黄线规则检查
      ↓ 失败 → 503 熔断触发
      ↓ 通过
第三道：路由关（Routing Gate）
  ├ 调七因子引擎计算 Σ(C) 和 conf
  ├ 根据操作类型路由到处理器
  └ 执行业务逻辑
      ↓
第四道：日志关（Audit Gate）
  ├ 三色审计引擎检查
  ├ 写入DNA日志（永不跳过）
  └ 响应附加 audit_tag
      ↓
返回响应
```

## 认证Header规范

| Header | 必填 | 格式 | 说明 |
|------|:---:|------|------|
| `X-DNA-Confirm` | ✅ | `#CONFIRM🌌9622-ONLY-ONCE🧬{8位HEX}` | DNA确认码，每次请求唯一 |
| `X-UID` | ✅ | `9622` | 用户唯一标识 |
| `X-Request-DNA` | ✅ | `#龍芯⚡️{YYYY-MM-DD}-EXT-REQ-{8位HEX}` | 请求DNA追溯码 |
| `X-Timestamp` | ✅ | Unix时间戳（秒） | 防重放，容差±300秒 |
| `X-Signature` | ✅ | Base64(SM2签名) | 请求签名 |
| `X-Version` | ❌ | `v{版本号}` | API版本，默认最新 |

### Header验证流程

```
① 检查必填Header → 缺任一 → 403
② 验证UID → 非9622 → 403
③ 验证确认码格式 → 不以#CONFIRM🌌9622-ONLY-ONCE🧬开头 → 403
④ 防重放 → 确认码已使用 → 403（重放攻击？）
⑤ 验证时间戳 → 超出±300秒 → 403
⑥ 验证请求DNA格式 → 不以#龍芯⚡️开头 → 403
⑦ 记录确认码（防重放）
⑧ 返回通过
```

### 签名构造

```
待签名字符串 = X-DNA-Confirm | X-Request-DNA | X-Timestamp | 请求体前32位HEX
X-Signature = Base64(SM2(待签名字符串))
```

## 七条红线（绝对不开放）

| # | 红线 | 技术实现 | 违反后果 |
|:---:|------|------|------|
| 🔴1 | 不设公开无认证端点 | 所有端点检查 X-DNA-Confirm | 请求直接拒绝，IP入黑名单 |
| 🔴2 | 不记录原文（只哈希） | 系统只存 SM3 哈希值 | 即使数据库被入侵也无法还原 |
| 🔴3 | 不允许第三方写DNA链 | DNA写入操作严格校验UID | 非9622的写入直接熔断 |
| 🔴4 | 不允许远程删除本地日志 | 日志文件 append-only | 删除操作返回403 |
| 🔴5 | 不允许批量导出全量数据 | 单次查询限制100条，需分页 | 超量请求触发熔断 |
| 🔴6 | 不允许修改已确认DNA记录 | DNA链使用哈希链结构 | 修改会破坏哈希链完整性 |
| 🔴7 | 不允许绕过三色审计 | 审计引擎在响应前强制执行 | 无法关闭或跳过 |

## 熔断器（Circuit Breaker）

### 三态模型

| 状态 | 说明 | 请求处理 |
|------|------|------|
| CLOSED（关闭） | 正常运行 | 所有请求允许通过 |
| OPEN（打开） | 熔断状态 | 所有请求被拒绝 |
| HALF_OPEN（半开） | 试探状态 | 允许有限试探请求（默认3次） |

### 状态转换

```
CLOSED ──连续失败≥5次 或 错误率>50%──→ OPEN
OPEN   ──冷卻时间≥60秒─────────────→ HALF_OPEN
HALF_OPEN ──试探成功──────────────→ CLOSED
HALF_OPEN ──试探失败──────────────→ OPEN
```

### 熔断器参数

| 参数 | 默认值 | 说明 |
|------|:---:|------|
| 失败阈值 | 5 | 连续失败次数触发熔断 |
| 冷卻时间 | 60秒 | 熔断后等待时间 |
| 半开试探数 | 3 | 半开状态允许的试探请求数 |
| 错误率阈值 | 50% | 错误率超过此值触发熔断（需≥10次请求） |

## API端点表

| 端点 | 方法 | 功能 | 认证 | 状态 |
|------|:---:|------|:---:|:---:|
| `/api/v9/identity/verify` | POST | 七因子身份验证 | 需要 | 已实现 |
| `/api/v9/identity/factors` | GET | 获取七因子结果 | 需要 | 已实现 |
| `/api/v9/dna/generate` | POST | 生成DNA追溯码 | 需要 | 已实现 |
| `/api/v9/dna/verify` | POST | 验证DNA追溯码 | 需要 | 已实现 |
| `/api/v9/audit/report` | GET | 获取审计报告 | 需要+额外授权 | 已实现 |
| `/api/v9/digital-twin/status` | GET | 查双轨数字人状态 | 需要 | 已实现 |
| `/api/v9/digital-twin/authorize` | POST | 实体原型授权虚拟代体 | 需要+生物特征 | 已实现 |
| `/api/v9/system/health` | GET | 系统健康检查 | **无需**（唯二公开） | 已实现 |
| `/api/v9/system/metrics` | GET | 系统指标监控 | **无需**（唯二公开） | 已实现 |
| `/api/v9/plugin/register` | POST | 注册MCP插件 | 需要+开发者证书 | 预留 |
| `/api/v9/plugin/call` | POST | 调用MCP插件 | 需要+插件授权 | 预留 |
| `/api/v9/blockchain/anchor` | POST | 区块链存证 | 需要+额外授权 | 预留 |
| `/api/v9/quantum/collapse` | POST | 量子态塌缩 | 需要+生物特征 | 预留 |

## 请求/响应格式

### 标准请求

```json
{
  "protocol": "dragon_soul_api",
  "version": "9.0",
  "request_id": "uuid",
  "timestamp": 1234567890,
  "operation": "verify_identity",
  "parameters": {},
  "dna_trace": null
}
```

### 标准响应（成功）

```json
{
  "protocol": "dragon_soul_api",
  "version": "9.0",
  "request_id": "uuid",
  "timestamp": 1234567890,
  "success": true,
  "data": {},
  "audit_tag": "#AUDIT🟢|..."
}
```

### 标准响应（失败）

```json
{
  "protocol": "dragon_soul_api",
  "version": "9.0",
  "request_id": "uuid",
  "timestamp": 1234567890,
  "success": false,
  "error": {
    "code": "AUTH_001",
    "message": "缺少认证Header"
  },
  "audit_tag": "#AUDIT🔴|..."
}
```

### 错误码定义

| 错误码 | 类别 | 含义 |
|------|------|------|
| AUTH_001 | 认证 | 缺少认证Header |
| AUTH_002 | 认证 | DNA确认码无效 |
| AUTH_003 | 认证 | UID未授权 |
| AUTH_004 | 认证 | 签名验证失败 |
| AUTH_005 | 认证 | 确认码已使用（重放攻击） |
| AUTH_006 | 认证 | 时间戳无效 |
| CB_001 | 熔断 | 熔断器已打开 |
| CB_002 | 熔断 | 半开试探次数已用完 |
| SF_001 | 七因子 | Hard Failure 触发 |
| SF_002 | 七因子 | 置信度低于阈值 |
| DNA_001 | DNA | DNA追溯码格式无效 |
| DNA_002 | DNA | SM3哈希不匹配 |
| DNA_003 | DNA | SM2签名无效 |
| SYS_001 | 系统 | 内部服务错误 |

## 引擎映射（本地实现）

| 引擎 | 文件 | 说明 |
|------|------|------|
| CNSH守门人 | `bin/cnsh_gatekeeper.py` | 变量验证+命令验证+沙箱执行 |
| 守门人协议 | `CNSH-GATEKEEPER.md` | 三道防线规范 |
| MCP语法服务 | `integrations/mcp/cnsh_syntax_mcp_server.py` | CNSH语法MCP服务 |
| MCP变量沙箱 | `integrations/mcp/cnsh_var_sandbox_mcp_server.py` | 变量沙箱MCP服务 |
| 分层治理引擎 | `cnsh-core/governance/layered_governance_engine.py` | 治理层 |

## 引用与溯源

- 核心文档：API主权门关设计 `#龍芯⚡️2024-08-05-设计-API网关-v1.0`
- 相关文件：
  - `02_SKILLS/identity-positioning.md` — 身份定位总纲
  - `02_SKILLS/guomi-crypto.md` — 国密三引擎
  - `02_SKILLS/dna-trace-engine.md` — DNA追溯引擎
  - `01_protocols/seven-factor-verification.md` — 七因子验证预言机协议
  - `CNSH-GATEKEEPER.md` — 守门人协议
  - `bin/cnsh_gatekeeper.py` — CNSH守门人

## 诚实局限

1. 当前API网关系列为Python Flask原型，未实现生产级网关（如Kong/APISIX）。
2. 防重放的确认码集合在内存中，服务重启后丢失，需持久化。
3. SM2签名验证依赖 `gmssl` 纯Python库，高并发下性能瓶颈。
4. 七条红线中的IP黑名单未实现，当前仅返回403。

## 修改记录

| 日期 | 变更 | DNA |
|------|------|------|
| 2026-07-06 | 初始创建，整合四道关卡+认证Header+七条红线+熔断器+API端点+错误码 | `#龍芯⚡️2026-07-06-API-SOVEREIGN-GATEWAY-SKILL-v1.0` |

---

**三色审计**: 🟢 通过 | 🟡 生产级网关待升级 | 🔴 0
