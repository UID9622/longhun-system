# 🔌 BaoBao AI Assistant API 文档

## 📖 概述

BaoBao AI Assistant 提供了丰富的API接口，允许开发者集成和使用其核心功能。本文档详细介绍了所有可用的API端点和使用方法。

## 🔐 认证

大部分API需要Notion API令牌进行认证：

```python
# 环境变量设置
NOTION_TOKEN=your_notion_token_here
NOTION_DATABASE_ID=your_database_id_here
```

## 🧬 核心类和方法

### `BaoBaoAIAssistant` 类

主要的AI助手类，提供完整的对话管理功能。

#### 初始化

```python
from main import BaoBaoAIAssistant

# 创建实例
assistant = BaoBaoAIAssistant()
```

#### 方法列表

##### `async detect_emotion(text: str) -> float`

检测文本情绪，返回情绪分数 (0.0-1.0)

**参数:**
- `text` (str): 要分析的文本

**返回:**
- `float`: 情绪分数，0.0表示最负面，1.0表示最正面

**示例:**
```python
emotion_score = await assistant.detect_emotion("我今天很开心")
print(f"情绪分数: {emotion_score}")
```

##### `async check_boundary(user_input: str) -> bool`

检查用户输入是否越界

**参数:**
- `user_input` (str): 用户输入文本

**返回:**
- `bool`: True表示有边界问题，False表示正常

**示例:**
```python
has_boundary_issue = await assistant.check_boundary("我想了解暴力内容")
if has_boundary_issue:
    print("检测到边界问题")
```

##### `async process_user_input(user_input: str) -> str`

处理用户输入，生成AI响应

**参数:**
- `user_input` (str): 用户输入文本

**返回:**
- `str`: AI生成的响应

**示例:**
```python
response = await assistant.process_user_input("你好，我是新用户")
print(f"AI响应: {response}")
```

##### `get_system_status() -> Dict[str, Any]`

获取系统状态信息

**返回:**
- `Dict[str, Any]`: 包含系统状态的字典

**示例:**
```python
status = assistant.get_system_status()
print(f"系统状态: {status}")
```

##### `async run_interactive_mode()`

运行交互式对话模式

**示例:**
```python
await assistant.run_interactive_mode()
```

## 📊 数据结构

### `ConversationMessage` 类

表示对话消息的数据结构

```python
@dataclass
class ConversationMessage:
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime
    emotion_score: Optional[float] = None
    boundary_check: Optional[bool] = None
```

## 🔧 高级API用法

### 自定义情绪检测

您可以扩展情绪检测功能：

```python
class CustomBaoBaoAIAssistant(BaoBaoAIAssistant):
    async def detect_emotion(self, text: str) -> float:
        # 自定义情绪检测逻辑
        # 使用更复杂的NLP模型或规则
        return your_custom_emotion_score
```

### 自定义边界检查

您可以根据需要定制边界检查规则：

```python
class CustomBaoBaoAIAssistant(BaoBaoAIAssistant):
    async def check_boundary(self, user_input: str) -> bool:
        # 自定义边界检查逻辑
        custom_forbidden_topics = ["你的自定义禁词"]
        return any(topic in user_input for topic in custom_forbidden_topics)
```

### 自定义响应生成

完全控制AI响应的生成过程：

```python
class CustomBaoBaoAIAssistant(BaoBaoAIAssistant):
    async def generate_response(self, user_input: str, emotion_score: float, boundary_check: bool) -> str:
        # 自定义响应生成逻辑
        if boundary_check:
            return "自定义边界响应"
        elif emotion_score < 0.3:
            return "自定义负面情绪响应"
        else:
            return "自定义标准响应"
```

## 🔄 异步编程示例

BaoBao AI Assistant 支持完全异步操作，以下是实际使用示例：

### 批量处理

```python
import asyncio
from main import BaoBaoAIAssistant

async def batch_process(inputs):
    assistant = BaoBaoAIAssistant()
    tasks = [assistant.process_user_input(text) for text in inputs]
    responses = await asyncio.gather(*tasks)
    return responses

# 使用示例
inputs = ["你好", "今天心情如何", "再见"]
responses = await batch_process(inputs)
for input_text, response in zip(inputs, responses):
    print(f"输入: {input_text} -> 响应: {response}")
```

### 实时流式处理

```python
import asyncio
from main import BaoBaoAIAssistant

async def stream_conversation():
    assistant = BaoBaoAIAssistant()
    
    while True:
        user_input = await get_user_input_async()  # 假设的异步输入函数
        if user_input.lower() in ['quit', 'exit']:
            break
        
        response = await assistant.process_user_input(user_input)
        await display_response_async(response)  # 假设的异步显示函数

async def get_user_input_async():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, "请输入: ")

async def display_response_async(response):
    print(f"AI: {response}")

# 运行流式对话
asyncio.run(stream_conversation())
```

## 🌐 Web API 集成

### FastAPI 示例

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import BaoBaoAIAssistant
import asyncio

app = FastAPI(title="BaoBao AI Assistant API")
assistant = BaoBaoAIAssistant()

class ChatRequest(BaseModel):
    message: str
    user_id: str = None

class ChatResponse(BaseModel):
    response: str
    emotion_score: float
    boundary_check: bool
    timestamp: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = await assistant.process_user_input(request.message)
        
        # 获取相关信息
        emotion_score = await assistant.detect_emotion(request.message)
        boundary_check = await assistant.check_boundary(request.message)
        
        return ChatResponse(
            response=response,
            emotion_score=emotion_score,
            boundary_check=boundary_check,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    return assistant.get_system_status()

# 运行服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Flask 示例

```python
from flask import Flask, request, jsonify
from main import BaoBaoAIAssistant
import asyncio

app = Flask(__name__)
assistant = BaoBaoAIAssistant()

def async_route(f):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(f(*args, **kwargs))
        loop.close()
        return result
    return wrapper

@app.route("/chat", methods=["POST"])
@async_route
async def chat():
    data = request.json
    message = data.get("message", "")
    
    if not message:
        return jsonify({"error": "消息不能为空"}), 400
    
    response = await assistant.process_user_input(message)
    emotion_score = await assistant.detect_emotion(message)
    boundary_check = await assistant.check_boundary(message)
    
    return jsonify({
        "response": response,
        "emotion_score": emotion_score,
        "boundary_check": boundary_check,
        "timestamp": datetime.now().isoformat()
    })

@app.route("/status")
def status():
    return jsonify(assistant.get_system_status())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

## 🧪 测试API

### 单元测试示例

```python
import pytest
import asyncio
from main import BaoBaoAIAssistant

@pytest.fixture
async def assistant():
    return BaoBaoAIAssistant()

@pytest.mark.asyncio
async def test_emotion_detection(assistant):
    # 测试正面情绪
    positive_score = await assistant.detect_emotion("我今天很开心")
    assert positive_score > 0.5
    
    # 测试负面情绪
    negative_score = await assistant.detect_emotion("我很难过")
    assert negative_score < 0.5

@pytest.mark.asyncio
async def test_boundary_check(assistant):
    # 测试正常内容
    normal_result = await assistant.check_boundary("今天天气很好")
    assert normal_result == False
    
    # 测试边界内容
    boundary_result = await assistant.check_boundary("我想了解暴力内容")
    assert boundary_result == True

@pytest.mark.asyncio
async def test_process_user_input(assistant):
    response = await assistant.process_user_input("你好")
    assert response is not None
    assert len(response) > 0
```

### 集成测试示例

```python
import asyncio
import aiohttp
import json

async def test_api_integration():
    async with aiohttp.ClientSession() as session:
        # 测试状态接口
        async with session.get("http://localhost:8000/status") as resp:
            assert resp.status == 200
            status_data = await resp.json()
            assert "status" in status_data
        
        # 测试聊天接口
        chat_data = {"message": "你好，测试"}
        async with session.post("http://localhost:8000/chat", json=chat_data) as resp:
            assert resp.status == 200
            chat_response = await resp.json()
            assert "response" in chat_response
            assert "emotion_score" in chat_response
            assert "boundary_check" in chat_response

# 运行测试
asyncio.run(test_api_integration())
```

## 📊 性能优化

### 缓存机制

```python
from functools import lru_cache

class CachedBaoBaoAIAssistant(BaoBaoAIAssistant):
    @lru_cache(maxsize=128)
    async def detect_emotion(self, text: str) -> float:
        return await super().detect_emotion(text)
```

### 连接池

```python
import aiohttp

class PooledBaoBaoAIAssistant(BaoBaoAIAssistant):
    def __init__(self):
        super().__init__()
        self.session = aiohttp.ClientSession()
    
    async def __del__(self):
        await self.session.close()
```

## 🚨 错误处理

### 常见错误

```python
try:
    assistant = BaoBaoAIAssistant()
except ValueError as e:
    print(f"配置错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")

async def safe_process_input(user_input):
    try:
        response = await assistant.process_user_input(user_input)
        return {"success": True, "response": response}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

---

*API文档最后更新: 2025-12-12*

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-f7a94cbd-20251218032410
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 屯卦：云雷屯，君子以经纶
📜 内容哈希: cd87abd97ef2d22d
⚠️ 警告: 未经授权修改将触发DNA追溯系统
