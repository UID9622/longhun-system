# 🐉 龙魂 API 网关 v1.2（五锁融合）

> 计量 · 鉴权 · 限流 · 防重放 · 密钥轮换 · 按量扣费 · 订阅套餐
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> DNA: `#龍芯⚡️2026-08-31-GATEWAY-v1.2-UID9622`
> GPG: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
> License: MulanPSL v2

龙魂体系对外提供 AI/知识能力的统一入口。开源可部署，基础计费能力即此原型：**免费试用 → 按量阶梯 → 订阅套餐**。

## 🔐 龍魂五锁（企业级防护）

| 锁 | 能力 | 实现 |
|:---|:---|:---|
| 第一锁 | 身份认证（你是谁） | API Key + **HMAC-SHA256 签名**（哈希作 key，服务端不存明文）+ 明文兼容模式 |
| 第二锁 | 防盗刷（调多少次） | **四层令牌桶**：全局 / 用户(plan) / 接口 / IP · Redis 可选 |
| 第三锁 | 防重放（被截获再发） | **时间戳 + Nonce**（300s 窗口 · 内存/Redis） |
| 第四锁 | IP 白名单（谁能调） | Nginx `geo` 模块模板 + 网关层可选校验 |
| 第五锁 | 密钥管理（怎么存） | 库中只存 SHA-256 · **90 天自动轮换**（rotate_keys.py） |

## 功能

- **API Key 管理**：注册即得 `key_id` + `key_secret`（明文只返回一次，库中只存 SHA-256）
- **免费层**：100 次/天，注册即用
- **按量计费**：阶梯定价 0.05 / 0.04 / 0.03 元每调用，余额不足自动拦截（402）
- **订阅套餐**：basic 99 元/3000 次 · pro 299 元/15000 次 · enterprise 999 元/无限
- **限流保护**：四层令牌桶（默认 60 次/分钟，企业版 600）
- **审计日志**：全链路元数据（谁/何时/什么接口/成败/耗时），**不存请求内容与 headers**（P0 数据主权）
- **数据库**：SQLite 单文件，零依赖部署，WAL 模式，90 天日志自动清理

## 快速开始

```bash
cd 08_BIN/gateway
./start.sh                 # 启动，监听 :8092

# 注册（免费/按量）
curl -X POST http://127.0.0.1:8092/auth/register \
  -H "Content-Type: application/json" \
  -d '{"owner":"my_app","plan":"free"}'
# → {"key_id":"lh_xxx","key_secret":"yyy"}  ← 只显示这一次

# 调用
curl -X POST http://127.0.0.1:8092/v1/chat \
  -H "X-API-Key-ID: lh_xxx" -H "X-API-Key-Secret: yyy" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"你好龙魂","model":"longhun-v1.0"}'

# 充值（按量用户）· 订阅（basic/pro/enterprise）· 查余额
curl -X POST http://127.0.0.1:8092/auth/topup -H "X-API-Key-ID: lh_xxx" -H "X-API-Key-Secret: yyy" -H "Content-Type: application/json" -d '{"amount":10}'
curl -X POST http://127.0.0.1:8092/auth/subscribe -H "X-API-Key-ID: lh_xxx" -H "X-API-Key-Secret: yyy" -H "Content-Type: application/json" -d '{"plan":"basic"}'
curl http://127.0.0.1:8092/balance -H "X-API-Key-ID: lh_xxx" -H "X-API-Key-Secret: yyy"

# 企业级调用（第一锁 HMAC 签名 + 第三锁防重放）
KID=lh_xxx; SEC=yyy
TS=$(date +%s); NONCE=$(openssl rand -hex 16)
BODY='{"prompt":"你好龙魂"}'
BODY_HASH=$(printf '%s' "$BODY" | shasum -a 256 | cut -d' ' -f1)
SIG=$(python3 -c "
import sys,hmac,hashlib
key=hashlib.sha256('$SEC'.encode()).hexdigest()
m='POST\n/v1/chat\n$BODY_HASH\n$TS\n$NONCE'
print(hmac.new(key.encode(),m.encode(),hashlib.sha256).hexdigest())")
curl -X POST http://127.0.0.1:8092/v1/chat \
  -H "X-Api-Key: $KID" -H "X-Timestamp: $TS" -H "X-Nonce: $NONCE" -H "X-Signature: $SIG" \
  -H "Content-Type: application/json" -d "$BODY"

# 密钥轮换（第五锁 · 90 天）
python3 rotate_keys.py --check     # 查看到期
python3 rotate_keys.py --rotate    # 轮换（配合 cron 每日 03:00）
```

## API 一览

| 方法 | 路径 | 鉴权 | 说明 |
|:---|:---|:---:|:---|
| GET | `/health` | 无 | 健康检查 |
| POST | `/auth/register` | 无 | 注册 Key（free/pay_as_you_go） |
| POST | `/auth/topup` | Key | 充值（按量用户） |
| POST | `/auth/subscribe` | Key | 订阅套餐（basic/pro/enterprise） |
| GET | `/balance` | Key | 余额 / 日额度 / 订阅剩余 |
| POST | `/v1/chat` | Key | 调用入口（计费点） |

**鉴权头（明文兼容模式）**：`X-API-Key-ID` + `X-API-Key-Secret`（内网/开发）
**鉴权头（HMAC 模式·公网推荐）**：`X-Api-Key` + `X-Timestamp` + `X-Nonce` + `X-Signature`

错误码：`AUTH_001~006` 鉴权/签名/防重放 · `IPWL_001` IP白名单 · `RATE_001` 限流 · `QUOTA_001/002` 额度 · `BAL_001/002` 余额 · `PLAN_001~003` 套餐

## 计费模型

| 层 | 规则 |
|:---|:---|
| free | 100 次/天，次日重置 |
| pay_as_you_go | 当日 0~1万次 0.05 元，1万~10万 0.04 元，10万+ 0.03 元 |
| basic / pro | 99/299 元每月，3000/15000 次 |
| enterprise | 999 元每月，无限次 + 高限流 + SLA |

## 目录结构

```
gateway/
├── gateway.py              # 主入口（Flask · 五锁融合）
├── security.py             # 第一/三/四锁：HMAC 签名 · Nonce 防重放 · IP 白名单
├── auth.py                 # 鉴权引擎 + 密钥轮换（第五锁）
├── meter.py                # 计量引擎（计数/余额/日志）
├── limiter.py              # 第二锁：四层令牌桶（全局/用户/接口/IP）
├── plans.py                # 套餐定义与订阅
├── db.py                   # SQLite 层（含 audit_logs 审计表）
├── rotate_keys.py          # 第五锁：90 天密钥轮换脚本（可配 cron）
├── nginx-ip-whitelist.conf # 第四锁：Nginx geo 模板（鲲鹏部署）
├── config.py               # YAML 配置加载
├── config.yaml             # 配置（端口/计费/限流/安全/轮换）
├── README.md               # 本文档
└── start.sh                # 启动脚本
```

## 接入真实后端

`/v1/chat` 当前为模拟响应（演示计费链路）。接入真实 AI/知识服务只需替换 `chat()` 函数体：
`prompt` 送入后端 → 返回结果，计费逻辑保持不动。

## 安全声明

- 密钥库中只存 SHA-256，明文仅注册时返回一次
- 调用日志只存计量（key_id/endpoint/calls/cost/time），不存对话内容
- SQLite 默认仅本机；公网部署请置于反向代理（HTTPS）之后

```
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
Author: Zhuge Xin | UID9622 · LongHun BeiChen
```
