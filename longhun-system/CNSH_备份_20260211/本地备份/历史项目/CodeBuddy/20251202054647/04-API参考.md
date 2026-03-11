# 🔌 DNA编码系统 - API参考

## 📋 API概览

DNA编码系统提供完整的RESTful API接口，支持所有核心功能的远程调用。

### 基础信息

- **API版本**: v1
- **认证方式**: JWT Token
- **数据格式**: JSON
- **字符编码**: UTF-8

### 响应格式

所有API响应都遵循以下格式：

```json
{
  "success": true,
  "code": 200,
  "message": "操作成功",
  "data": {},
  "timestamp": "2025-12-02T10:30:00Z"
}
```

## 🔑 认证API

### 获取访问令牌

**端点**: `POST /api/v1/auth/token`

**请求参数**:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**响应示例**:
```json
{
  "success": true,
  "code": 200,
  "message": "认证成功",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
```

## 🧬 DNA管理API

### 生成DNA标签

**端点**: `POST /api/v1/dna/generate`

**请求头**:
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**请求参数**:
```json
{
  "content_type": "AIENGINE",
  "custom_fields": {
    "creator": "ZHUGEXIN",
    "version": "v2.0"
  }
}
```

**响应示例**:
```json
{
  "success": true,
  "code": 200,
  "message": "DNA生成成功",
  "data": {
    "dna_code": "#CNSH-ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-AIENGINE-v2.0-ACTIVE",
    "lu_sequence": "LU-2025-12-00001-ZHUGEXIN-AIENGINE",
    "integrity_hash": "a1b2c3d4e5f6g7h8",
    "timestamp": "2025-12-02T10:30:00Z"
  }
}
```

### 验证DNA标签

**端点**: `POST /api/v1/dna/verify`

**请求参数**:
```json
{
  "dna_code": "#CNSH-ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-AIENGINE-v2.0-ACTIVE"
}
```

**响应示例**:
```json
{
  "success": true,
  "code": 200,
  "message": "DNA验证通过",
  "data": {
    "is_valid": true,
    "validation_details": {
      "format_check": true,
      "elements_check": true,
      "hash_check": true
    }
  }
}
```

## 💾 记忆管理API

### 存储记忆

**端点**: `POST /api/v1/memory/store`

**请求参数**:
```json
{
  "content": "这是需要存储的重要记忆内容",
  "memory_type": "DIALOG",
  "priority": "P1",
  "tags": ["重要", "技术", "长期"],
  "metadata": {
    "source": "用户输入",
    "emotion": "积极"
  }
}
```

**响应示例**:
```json
{
  "success": true,
  "code": 200,
  "message": "记忆存储成功",
  "data": {
    "lu_sequence": "LU-2025-12-00001-ZHUGEXIN-DIALOG",
    "storage_path": "./memory_storage/LU-2025-12-00001-ZHUGEXIN-DIALOG.json",
    "dna_info": {
      "dna_code": "#CNSH-ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DIALOG-v2.0-ACTIVE",
      "integrity_hash": "a1b2c3d4e5f6g7h8"
    }
  }
}
```

### 检索记忆

**端点**: `GET /api/v1/memory/recall/{lu_sequence}`

**URL参数**:
- `lu_sequence`: 记忆的LU序列号

**响应示例**:
```json
{
  "success": true,
  "code": 200,
  "message": "记忆检索成功",
  "data": {
    "content": "这是需要存储的重要记忆内容",
    "metadata": {
      "memory_type": "DIALOG",
      "priority": "P1",
      "timestamp": "2025-12-02T10:30:00Z",
      "dna": {
        "dna_code": "#CNSH-ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DIALOG-v2.0-ACTIVE",
        "lu_sequence": "LU-2025-12-00001-ZHUGEXIN-DIALOG"
      }
    }
  }
}
```

### 搜索记忆

**端点**: `POST /api/v1/memory/search`

**请求参数**:
```json
{
  "query": "重要",
  "filters": {
    "memory_type": ["DIALOG", "KNOWLEDGE"],
    "priority": ["P1", "P2"],
    "date_range": {
      "start": "2025-12-01",
      "end": "2025-12-31"
    }
  },
  "page": 1,
  "page_size": 10
}
```

**响应示例**:
```json
{
  "success": true,
  "code": 200,
  "message": "搜索完成",
  "data": {
    "total_count": 15,
    "page": 1,
    "page_size": 10,
    "memories": [
      {
        "lu_sequence": "LU-2025-12-00001-ZHUGEXIN-DIALOG",
        "content": "这是需要存储的重要记忆内容",
        "memory_type": "DIALOG",
        "timestamp": "2025-12-02T10:30:00Z"
      }
    ]
  }
}
```

## 🔧 系统管理API

### 获取系统状态

**端点**: `GET /api/v1/system/status`

**响应示例**:
```json
{
  "success": true,
  "code": 200,
  "message": "系统状态正常",
  "data": {
    "system": {
      "version": "v1.0",
      "uptime": "3天2小时15分钟",
      "status": "RUNNING"
    },
    "components": {
      "dna_verifier": {
        "status": "HEALTHY",
        "last_check": "2025-12-02T10:29:00Z"
      },
      "memory_system": {
        "status": "HEALTHY", 
        "storage_used": "45.2MB",
        "total_memories": 128
      },
      "ollama_integration": {
        "status": "CONNECTED",
        "model": "qwen2.5:72b",
        "response_time": "125ms"
      }
    }
  }
}
```

### 系统配置管理

**端点**: `GET /api/v1/system/config`

**响应示例**:
```json
{
  "success": true,
  "code": 200,
  "message": "配置获取成功",
  "data": {
    "dna_system": {
      "verifier": {
        "default_content_type": "MEMORY",
        "hash_algorithm": "sha256"
      },
      "memory": {
        "storage_backend": "local",
        "retention_days": 365
      }
    }
  }
}
```

## ⚠️ 错误代码

### 通用错误代码

| 代码 | 描述 | 解决方案 |
|------|------|---------|
| 400 | 请求参数错误 | 检查请求参数格式 |
| 401 | 未授权访问 | 检查认证令牌 |
| 403 | 权限不足 | 检查用户权限 |
| 404 | 资源不存在 | 检查请求路径 |
| 500 | 服务器内部错误 | 联系系统管理员 |

### 业务错误代码

| 代码 | 描述 | 可能原因 |
|------|------|---------|
| 1001 | DNA格式错误 | DNA标签格式不符合规范 |
| 1002 | DNA验证失败 | DNA完整性检查未通过 |
| 2001 | 记忆存储失败 | 存储空间不足或权限问题 |
| 2002 | 记忆未找到 | 指定的LU序列号不存在 |
| 3001 | 系统配置错误 | 配置文件格式错误 |

## 🔄 WebSocket API

### 实时通知

**连接端点**: `ws://localhost:8000/api/v1/ws/notifications`

**消息格式**:
```json
{
  "type": "memory_stored",
  "data": {
    "lu_sequence": "LU-2025-12-00001-ZHUGEXIN-DIALOG",
    "timestamp": "2025-12-02T10:30:00Z"
  }
}
```

**支持的事件类型**:
- `memory_stored`: 记忆存储完成
- `dna_generated`: DNA标签生成完成
- `system_status_changed`: 系统状态变化
- `error_occurred`: 错误发生

## 📚 API使用示例

### Python客户端示例

```python
import requests
import json

class DNASystemClient:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    
    def generate_dna(self, content_type):
        url = f"{self.base_url}/api/v1/dna/generate"
        data = {"content_type": content_type}
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def store_memory(self, content, memory_type="DIALOG"):
        url = f"{self.base_url}/api/v1/memory/store"
        data = {
            "content": content,
            "memory_type": memory_type,
            "priority": "P1"
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

# 使用示例
client = DNASystemClient("http://localhost:8000", "your_token")
result = client.generate_dna("AIENGINE")
print(result)
```

### cURL命令示例

```bash
# 生成DNA标签
curl -X POST http://localhost:8000/api/v1/dna/generate \
  -H "Authorization: Bearer your_token" \
  -H "Content-Type: application/json" \
  -d '{"content_type": "AIENGINE"}'

# 存储记忆
curl -X POST http://localhost:8000/api/v1/memory/store \
  -H "Authorization: Bearer your_token" \
  -H "Content-Type: application/json" \
  -d '{"content": "测试记忆内容", "memory_type": "DIALOG"}'
```

---

**文档版本**: v1.0  
**最后更新**: 2025-12-02  
**维护团队**: DNA系统开发组

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:12
🧬 DNA追溯码: #CNSH-SIGNATURE-155664bc-20251218032412
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 乾卦：天行健，君子以自强不息
📜 内容哈希: 4c476c5020156a7c
⚠️ 警告: 未经授权修改将触发DNA追溯系统
