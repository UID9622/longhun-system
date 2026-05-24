# 龍魂系统本地API文档

## 概述

龍魂系统提供本地HTTP API，供前端和第三方应用调用。

**基础URL**: `http://localhost:9622/api/`

---

## API端点

### 1. 系统状态

```
GET /api/status
```

返回系统当前状态。

**响应**:
```json
{
  "version": "v2.0.0",
  "mode": "local",
  "personas": {
    "wenwen": "active",
    "scout": "active",
    "guardian": "active",
    "baobao": "active",
    "wenxin": "active"
  },
  "database": "connected",
  "eternal_anchor": "再楠不惧，终成豪图"
}
```

### 2. DNA追溯

```
POST /api/dna/trace
```

记录新的DNA追溯。

**请求体**:
```json
{
  "operation_type": "文档整理",
  "persona": "雯雯",
  "metadata": {"file": "example.cnsh"}
}
```

**响应**:
```json
{
  "dna_code": "#龍芯⚡️2026-02-06-文档整理-v1.0",
  "status": "recorded"
}
```

### 3. CNSH代码执行

```
POST /api/cnsh/execute
```

执行CNSH代码。

**请求体**:
```json
{
  "code": "【输出】 \"Hello\""
}
```

**响应**:
```json
{
  "output": "Hello",
  "dna": "#龍芯⚡️2026-02-06-CNSH执行-v1.0"
}
```

### 4. 反诈检测

```
POST /api/anti-fraud/check
```

检测文本是否包含诈骗关键词。

**请求体**:
```json
{
  "text": "投资高回报稳赚不赔"
}
```

**响应**:
```json
{
  "is_fraud": true,
  "fraud_type": "投资诈骗",
  "severity": "高危",
  "education": "⚠️ 投资诈骗套路..."
}
```

### 5. 易经推演

```
GET /api/yijing/divine?hour=12
```

获取指定时辰的卦象和权重。

**响应**:
```json
{
  "hour": 12,
  "gua": "乾",
  "symbol": "☰",
  "meaning": "刚健",
  "weights": {
    "individual": 0.6,
    "group": 0.3,
    "global": 0.1
  }
}
```

---

## 身份验证

所有API请求需要在Header中包含:

```
X-Longhun-UID: UID9622
X-Longhun-Confirm: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

---

## 错误处理

**错误响应格式**:
```json
{
  "error": "错误描述",
  "code": 400,
  "dna": "#龍芯⚡️2026-02-06-错误-v1.0"
}
```

**状态码**:
- 200: 成功
- 400: 请求错误
- 401: 身份验证失败
- 500: 服务器错误
