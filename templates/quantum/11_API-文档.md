# DNA: #龍芯⚡️2026-08-31-QUANTUM-TEMPLATE-11-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# 来源: Notion「🧬 量子模板引擎」库


## 🎯 模板定位

面向开发者的标准化 API 接口文档模板——无论是开源项目、科研平台还是商业 API，都能快速生成专业文档，并支持多语言国际化。


---


## 📄 API 文档模板


```markdown
# [API名称] API 文档 | [API Name] Documentation

**版本 / Version:** v1.0.0  
**Base URL:** `https://api.example.com/v1`  
**最后更新 / Last Updated:** YYYY-MM-DD  
**DNA追溯:** #龍芯⚡️YYYY-MM-DD-API名-v1.0

---

## 概述 | Overview

**中文：** [一段话描述API的用途、能力和适用场景]

**English:** [One paragraph: what this API does, its capabilities, and use cases]

## 认证 | Authentication

### API Key 认证
```

GET /endpoint HTTP/1.1

Host: api.example.com

Authorization: Bearer YOUR_API_KEY

Content-Type: application/json


```javascript

获取API Key / Get API Key: [注册链接]

---

## 通用规范 | General Conventions

| 项目 | 规范 |
|---|---|
| 协议 | HTTPS only |
| 数据格式 | JSON (`Content-Type: application/json`) |
| 字符编码 | UTF-8 |
| 时间格式 | ISO 8601 (`2026-08-31T18:00:00Z`) |
| 分页 | `?page=1&limit=20` |
| 限流 | 100 次/分钟（默认）|

---

## 接口列表 | Endpoints

### POST /analyze

**功能：** 分析输入数据并返回结果  
**描述：** Analyze input data and return results

#### 请求 / Request

```

POST /v1/analyze HTTP/1.1

Host: api.example.com

Authorization: Bearer YOUR_API_KEY

Content-Type: application/json

{

}


```javascript

**请求参数 / Request Parameters:**

| 字段 | 类型 | 必填 | 说明 / Description |
|---|---|---|---|
| `input` | string | ✅ | 输入内容 / Input content (max 10000 chars) |
| `lang` | string | ❌ | 语言代码 / Language code (default: `zh-CN`) |
| `options.mode` | string | ❌ | 运行模式 / Mode: `fast`\|`accurate` (default: `fast`) |
| `options.threshold` | float | ❌ | 阈值 / Threshold: 0.0–1.0 (default: `0.8`) |

#### 响应 / Response

**成功响应 (200 OK):**
```

{

}


```javascript

**响应字段 / Response Fields:**

| 字段 | 类型 | 说明 |
|---|---|---|
| `code` | int | 状态码（0=成功）|
| `data.result` | string | 分析结果 |
| `data.confidence` | float | 置信度 0.0–1.0 |
| `data.processing_time_ms` | int | 处理耗时(ms) |
| `data.request_id` | string | 请求唯一ID（用于排查问题）|

---

### GET /status

**功能：** 查询服务状态 / Check service status

```

GET /v1/status HTTP/1.1

Host: api.example.com

Authorization: Bearer YOUR_API_KEY


```javascript

**响应：**
```

{

}


```javascript

---

## 错误码 | Error Codes

| HTTP状态码 | code | 说明 / Description | 解决方案 |
|---|---|---|---|
| 400 | 1001 | 参数缺失 / Missing parameter | 检查必填参数 |
| 400 | 1002 | 参数格式错误 / Invalid format | 检查字段类型 |
| 401 | 2001 | API Key无效 / Invalid API key | 重新获取API Key |
| 429 | 3001 | 超出限流 / Rate limit exceeded | 降低请求频率 |
| 500 | 5000 | 服务器内部错误 / Server error | 联系支持 |

**错误响应示例：**
```

{

}


```javascript

---

## SDK 示例 | SDK Examples

### Python
```

import requests

def analyze(input_text, api_key, lang="zh-CN"):

result = analyze("Hello World", api_key="YOUR_KEY")

print(result["data"]["result"])


```javascript

### JavaScript (Node.js)
```

const axios = require('axios');

async function analyze(inputText, apiKey, lang = 'zh-CN') {

}

analyze('Hello World', 'YOUR_KEY').then(r => console.log(r.data.result));


```javascript

### curl
```

curl -X POST https://api.example.com/v1/analyze \


```javascript

```


---


## 🌍 API文档国际化（通义翻译提示词）


```javascript
请将以下API文档翻译为[英文/日文/西班牙文]。
规则：
1. HTTP方法(GET/POST/PUT/DELETE/PATCH)不翻译
2. 字段名(input/output/code/message等)不翻译
3. 代码示例块不翻译
4. JSON示例中的字段名不翻译，注释可翻译
5. 保持Markdown表格格式
6. 使用开发者友好的简洁语言
[粘贴文档内容]
```


---

> 💬 DNA： #龍芯⚡️2026-08-31-API接口文档模板-v1.0-UID9622