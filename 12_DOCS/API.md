# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · API 文档

> DNA: `#龍芯⚡️丙午·乙未·丙午·甲午·䷳艮为山-API-DOCS-v1.0-UID9622`
> 最后更新: 2026-07-31
> API 版本: v2.0.0
> 基础 URL: `https://uid9622.cn` | `http://localhost:9622`

---

## 概述

龍魂省电 API 为全球 AI 提供确定性任务执行能力。

**省电原理**：
- 大模型推理一个任务 2-10s，耗电 0.5-2 kWh
- 调用本 API 执行相同任务 < 100ms，耗电 ≈ 0
- **省电率: 99.98%**

**两种模式**：
- **同步模式**（默认）: POST /run 阻塞等待返回完整结果
- **异步模式**（需 Redis）: POST /run async_mode=true → 返回 task_id → GET /task/{id} 轮询

---

## 认证

| 方式 | 说明 |
|:---|:---|
| 无认证 | 默认允许匿名访问（`api_user=anonymous`） |
| Bearer Token | 设置环境变量 `LH_API_KEY` 后，需在 `Authorization` header 中传入 `Bearer <key>` |
| X-API-User | 可选 header，标识调用者身份 |

```bash
# 无认证
curl -X POST http://localhost:9622/run \
  -H "Content-Type: application/json" \
  -d '{"trigger":"健康检查"}'

# Bearer Token 认证
curl -X POST http://localhost:9622/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{"trigger":"健康检查"}'
```

---

## 端点列表

### 1. GET /health

健康检查。

**响应** `200 OK`:
```json
{
  "status": "ok",
  "version": "2.0.0",
  "dna": "#龍芯⚡️丙午·乙未·丙午·甲午·䷳艮为山-API-a1b2c3d4",
  "redis": false,
  "db": false,
  "async_supported": false
}
```

### 2. POST /run

执行确定性任务。

**请求体**:
| 字段 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| trigger | string | ✅ | 触发词，如"健康检查"、"签名"、"对齐检查" |
| args | string[] | ❌ | 额外参数，默认 [] |
| timeout | int | ❌ | 超时秒数 (1-600)，默认 300 |
| async_mode | bool | ❌ | 是否异步执行，默认 false（需 Redis） |

**同步模式响应** `200 OK`:
```json
{
  "status": "success",
  "stdout": "健康检查通过 ✅\n所有服务正常运行",
  "stderr": "",
  "duration": 0.045,
  "exit_code": 0,
  "dna": "#龍芯⚡️丙午·乙未·丙午·甲午·䷳艮为山-API-a1b2c3d4"
}
```

**异步模式响应** `200 OK`:
```json
{
  "status": "pending",
  "task_id": "a_1722400000_abc123",
  "message": "任务已提交，通过 GET /task/a_1722400000_abc123 轮询结果"
}
```

**错误响应**:
```json
// 400 Bad Request - 参数错误
{
  "detail": [
    {
      "loc": ["body", "trigger"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}

// 503 Service Unavailable - Redis不可用（异步模式）
{
  "detail": "异步模式需要 Redis。请使用不带 --redis 参数启动，或先安装 Redis。"
}
```

### 3. GET /task/{task_id}

查询异步任务状态。

**路径参数**:
| 参数 | 类型 | 说明 |
|:---|:---|:---|
| task_id | string | 异步任务ID |

**响应**:
```json
// 已完成
{
  "task_id": "a_1722400000_abc123",
  "status": "finished",
  "result": {
    "status": "success",
    "stdout": "对齐检查通过",
    "duration": 0.123,
    "exit_code": 0,
    "dna": "#龍芯⚡️..."
  }
}

// 执行中
{
  "task_id": "a_1722400000_abc123",
  "status": "started"
}

// 排队中
{
  "task_id": "a_1722400000_abc123",
  "status": "queued"
}

// 失败
{
  "task_id": "a_1722400000_abc123",
  "status": "failed",
  "error": "执行超时（>300s）"
}

// 未找到 (404)
{
  "detail": "任务未找到"
}
```

### 4. GET /triggers

获取所有可用触发词列表。

**响应** `200 OK`:
```json
{
  "total": 10,
  "triggers": [
    "健康检查",
    "签名",
    "对齐检查",
    "更新索引",
    "同步鲲鹏",
    "审计",
    "GPG签名",
    "记忆召回",
    "反虚伪",
    "备份"
  ],
  "commands": {
    "健康检查": "lh --trigger 健康检查",
    "签名": "lh --trigger 签名",
    "对齐检查": "lh --trigger 对齐"
  }
}
```

### 5. GET /stats

计费/用量统计（省电积分）。需要 SQLAlchemy。

**响应** `200 OK`:
```json
{
  "total_requests": 1523,
  "total_duration": 456.78,
  "avg_duration": 0.3,
  "success_rate": 0.985,
  "pending": 2,
  "by_user": {
    "anonymous": 1500,
    "uid9622": 23
  },
  "tip": "省电积分 = total_duration（秒）= 节省的大模型推理时间"
}
```

### 6. GET /openapi.json

返回 OpenAPI 3.0 规范文档。AI 可自动发现接口。

### 7. GET /

API 首页，文本格式的快速参考。

---

## AI 集成指南

### 步骤 1：自动发现接口
```bash
curl http://localhost:9622/openapi.json | jq .
```

### 步骤 2：查看可用能力
```bash
curl http://localhost:9622/triggers | jq .
```

### 步骤 3：执行任务
```bash
curl -X POST http://localhost:9622/run \
  -H "Content-Type: application/json" \
  -d '{"trigger":"健康检查"}' | jq .
```

### Python 示例
```python
import httpx

async def run_trigger(trigger: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://localhost:9622/run",
            json={"trigger": trigger}
        )
        return resp.json()

result = await run_trigger("健康检查")
print(result["stdout"])
```

---

## 启动服务

```bash
# 轻量模式（同步执行，无外部依赖）
python3 bin/lh_api_server.py --port 9622

# 或使用 lh 命令
lh --api

# 增强模式（Redis + 异步队列 + 计费）
python3 bin/lh_api_server.py --port 9622 --redis redis://localhost:6379/0

# Docker 部署
docker-compose -f docker/docker-compose.api.yml up -d
```

---

## 错误码汇总

| 状态码 | 含义 |
|:---|:---|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 缺少认证信息 |
| 403 | API Key 无效 |
| 404 | 任务未找到 |
| 500 | 服务器内部错误 |
| 503 | 服务不可用（如Redis未启动） |

---

## 速率限制

目前无速率限制。如有滥用，将根据实际情况添加限制。请合理使用。

---

## OpenAPI 规范

完整 OpenAPI 3.0 规范文件: [docs/openapi.json](./docs/openapi.json)

---

> 🐉 **省的不是电，是大模型不该烧的算力。**
