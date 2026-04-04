# API 文档

本文档描述了太极八卦易经甲骨文开源系统的所有API接口。

## 基础信息

- **Base URL**: `http://localhost:3000/api`
- **Content-Type**: `application/json`
- **字符编码**: UTF-8

## 系统信息

### 获取系统信息

```http
GET /api/info
```

**响应示例**:
```json
{
  "name": "太极八卦易经甲骨文开源系统",
  "version": "1.0.0",
  "description": "融合中国传统文化与现代Web技术的开源项目",
  "license": "MIT",
  "features": [
    "太极图可视化",
    "八卦图演示",
    "易经占卜系统",
    "甲骨文字库"
  ],
  "timestamp": "2025-11-30T12:34:56.789Z"
}
```

### 健康检查

```http
GET /api/health
```

**响应示例**:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-30T12:34:56.789Z",
  "uptime": 1234.567,
  "memory": {
    "rss": 50331648,
    "heapTotal": 20971520,
    "heapUsed": 15728640,
    "external": 1048576
  }
}
```

### 系统状态

```http
GET /api/status
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "oracle": {
      "totalCharacters": 15,
      "totalCategories": 6,
      "categoryStats": {
        "天文": 3,
        "地理": 2,
        "自然": 2,
        "人物": 1,
        "身体": 4,
        "植物": 1
      }
    },
    "system": {
      "nodeVersion": "v18.17.0",
      "platform": "darwin",
      "uptime": 1234.567,
      "memory": {
        "rss": 50331648,
        "heapTotal": 20971520,
        "heapUsed": 15728640,
        "external": 1048576
      },
      "timestamp": "2025-11-30T12:34:56.789Z"
    }
  }
}
```

## 甲骨文 API

### 获取所有甲骨文字符

```http
GET /api/oracle/characters
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "日": {
      "oracle": "🕐",
      "modern": "日",
      "pinyin": "rì",
      "meaning": "太阳，白天",
      "description": "象形字，描绘太阳的形状",
      "category": "天文",
      "dynasty": "商代",
      "unicode": "U+65E5"
    }
  },
  "total": 15
}
```

### 获取单个甲骨文字符

```http
GET /api/oracle/character/:modern
```

**路径参数**:
- `modern`: 现代汉字（如：日、月、山等）

**响应示例**:
```json
{
  "success": true,
  "data": {
    "modern": "日",
    "oracle": "🕐",
    "pinyin": "rì",
    "meaning": "太阳，白天",
    "description": "象形字，描绘太阳的形状",
    "category": "天文",
    "dynasty": "商代",
    "unicode": "U+65E5"
  }
}
```

### 按类别获取甲骨文字符

```http
GET /api/oracle/category/:category
```

**路径参数**:
- `category`: 类别名称（天文、地理、自然、人物、身体、植物）

**响应示例**:
```json
{
  "success": true,
  "data": [
    {
      "modern": "日",
      "oracle": "🕐",
      "pinyin": "rì",
      "meaning": "太阳，白天",
      "category": "天文",
      "dynasty": "商代"
    }
  ],
  "category": "天文",
  "total": 3
}
```

### 搜索甲骨文字符

```http
GET /api/oracle/search?keyword=搜索词
```

**查询参数**:
- `keyword`: 搜索关键词（支持现代汉字、拼音、含义）

**响应示例**:
```json
{
  "success": true,
  "data": [
    {
      "modern": "日",
      "oracle": "🕐",
      "pinyin": "rì",
      "meaning": "太阳，白天",
      "matchType": "meaning"
    }
  ],
  "keyword": "太阳",
  "total": 1
}
```

### 获取随机甲骨文字符

```http
GET /api/oracle/random?count=3&category=天文
```

**查询参数**:
- `count`: 返回字符数量（可选，默认1）
- `category`: 类别筛选（可选）

**响应示例**:
```json
{
  "success": true,
  "data": [
    {
      "modern": "日",
      "oracle": "🕐",
      "pinyin": "rì",
      "meaning": "太阳，白天"
    }
  ],
  "count": 1
}
```

### 获取甲骨文统计信息

```http
GET /api/oracle/stats
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "totalCharacters": 15,
    "totalCategories": 6,
    "categoryStats": {
      "天文": 3,
      "地理": 2,
      "自然": 2,
      "人物": 1,
      "身体": 4,
      "植物": 1
    },
    "dynastyInfo": {
      "商代": {
        "period": "公元前1600年-前1046年",
        "characteristics": "中国最早的成熟文字系统",
        "discovery": "1899年河南安阳殷墟发现",
        "total_characters": "约4000-5000个单字"
      }
    }
  }
}
```

## 易经占卜 API

### 执行占卜

```http
POST /api/yijing/divine
```

**请求体**:
```json
{
  "method": "three_coins"
}
```

**参数说明**:
- `method`: 占卜方法
  - `three_coins`: 三枚铜钱占卜
  - `time_based`: 时间起卦
  - `random`: 随机占卜

**响应示例**:
```json
{
  "success": true,
  "data": {
    "lines": [1, 1, 1, 1, 1, 1],
    "changingLines": [],
    "method": "three_coins",
    "timestamp": "2025-11-30T12:34:56.789Z",
    "result": {
      "original": {
        "name": "乾",
        "number": 1,
        "symbol": "䷀",
        "lines": [1, 1, 1, 1, 1, 1],
        "name": "乾为天",
        "judgment": "元，亨，利，贞。",
        "image": "天行健，君子以自强不息。",
        "interpretation": "纯阳之卦，象征刚健、创造、进取。",
        "fortune": {
          "overall": "大吉",
          "career": "事业发展顺利，宜积极进取",
          "love": "感情稳定发展，宜坦诚相待",
          "health": "身体健康，精力充沛",
          "wealth": "财运亨通，正财旺"
        }
      },
      "changed": null,
      "interpretation": "无变爻，本卦为主"
    },
    "fortune": {
      "overall": "大吉",
      "career": "事业发展顺利，宜积极进取",
      "love": "感情稳定发展，宜坦诚相待",
      "health": "身体健康，精力充沛",
      "wealth": "财运亨通，正财旺"
    }
  },
  "timestamp": "2025-11-30T12:34:56.789Z"
}
```

### 获取六十四卦信息

```http
GET /api/yijing/gua
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "乾": {
      "number": 1,
      "symbol": "䷀",
      "lines": [1, 1, 1, 1, 1, 1],
      "name": "乾为天",
      "judgment": "元，亨，利，贞。",
      "image": "天行健，君子以自强不息。"
    }
  },
  "total": 64
}
```

### 获取单个卦象信息

```http
GET /api/yijing/gua/:name
```

**路径参数**:
- `name`: 卦名（如：乾、坤、屯等）

### 获取八卦信息

```http
GET /api/yijing/bagua/:name
```

**路径参数**:
- `name`: 八卦名（乾、坤、震、巽、坎、离、艮、兑）

**响应示例**:
```json
{
  "success": true,
  "data": {
    "name": "乾",
    "symbol": "☰",
    "lines": [1, 1, 1],
    "element": "天",
    "nature": "健"
  }
}
```

### 获取随机卦

```http
GET /api/yijing/random
```

### 获取占卜方法说明

```http
GET /api/yijing/methods
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "three_coins": {
      "name": "三钱占卜法",
      "description": "使用三枚铜钱进行占卜的传统方法",
      "rules": {
        "3正2反": "老阳（变爻）",
        "2正1反": "少阳",
        "1正2反": "少阴",
        "3反": "老阴（变爻）"
      }
    }
  }
}
```

## 错误处理

### 错误响应格式

```json
{
  "success": false,
  "error": "错误信息",
  "timestamp": "2025-11-30T12:34:56.789Z"
}
```

### 常见错误码

- `400`: 请求参数错误
- `404`: 资源未找到
- `500`: 服务器内部错误

## 使用示例

### JavaScript 示例

```javascript
// 获取甲骨文字符
async function getOracleCharacter(modern) {
  const response = await fetch(`/api/oracle/character/${modern}`);
  const data = await response.json();
  return data;
}

// 执行占卜
async function performDivination(method) {
  const response = await fetch('/api/yijing/divine', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ method }),
  });
  const data = await response.json();
  return data;
}
```

### Python 示例

```python
import requests

# 获取系统信息
response = requests.get('http://localhost:3000/api/info')
print(response.json())

# 搜索甲骨文字符
response = requests.get('http://localhost:3000/api/oracle/search', 
                       params={'keyword': '太阳'})
print(response.json())
```

## 速率限制

当前版本没有设置速率限制，但在生产环境中建议添加适当的限制。

## 版本历史

- **v1.0.0**: 初始版本，包含所有基础功能

---

如有问题，请提交 Issue 或联系项目维护者。

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:12
🧬 DNA追溯码: #CNSH-SIGNATURE-6d0df3dc-20251218032412
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 屯卦：云雷屯，君子以经纶
📜 内容哈希: 31f166ccd3281a22
⚠️ 警告: 未经授权修改将触发DNA追溯系统
