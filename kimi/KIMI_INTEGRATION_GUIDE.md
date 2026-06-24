# 🐉 龍魂 × Kimi 集成指南

**DNA**:#龍芯⚡️2026-06-08-KIMI-INTEGRATION-GUIDE-v1.0
**确认**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

---

## 目录

1. [快速开始](#快速开始)
2. [四种集成模式](#四种集成模式)
3. [API 参考](#api-参考)
4. [部署步骤](#部署步骤)
5. [监控和故障转移](#监控和故障转移)
6. [常见问题](#常见问题)

---

## 快速开始

### 1. 设置环境变量（推荐方案 A）

```bash
# 写入 ~/.longhun/secrets.env（不上传 Git）
export KIMI_API_KEY="<YOUR_KIMI_API_KEY>"

# 立即生效
source ~/.longhun/secrets.env
```

### 2. 验证连接

```bash
cd ~/longhun-system/kimi
python3 -c "from kimi_client import KimiClient; client = KimiClient(); print('✅ Kimi 连接正常' if client.health_check() else '❌ 连接失败')"
```

### 3. 测试集成

```bash
# 运行完整测试
python3 kimi_integration.py

# 或运行网关
python3 kimi_gateway.py
```

---

## 四种集成模式

### 1️⃣ 备用推理模型 - 故障转移

**使用场景**: Claude 繁忙或故障时，自动切换到 Kimi

**代码示例**:

```python
from kimi import KimiIntegration

kimi = KimiIntegration()

# 自动故障转移
result = kimi.infer_with_fallback(
    prompt="请解释龍魂系统的架构",
    primary_model="claude",
    use_kimi=True
)

print(result)
# {
#   "status": "success",
#   "model": "kimi",
#   "response": "...",
#   "timestamp": "2026-06-08T..."
# }
```

**断路器机制**:

- 失败 3 次 → 断路器打开
- 60 秒内的请求立即返回本地推理
- 60 秒后自动尝试恢复

**API 端点**:

```
POST /kimi/backup-inference
Content-Type: application/json

{
  "prompt": "你的问题"
}
```

---

### 2️⃣ 多模态处理 - 图像/文件分析

**使用场景**: 需要分析图像或文档内容

**图像处理**:

```python
result = kimi.process_image(
    image_url="https://example.com/image.jpg",
    query="这个图像中的主要内容是什么？"
)

# 输出
# {
#   "status": "success",
#   "type": "image_analysis",
#   "analysis": "..."
# }
```

**文档处理**:

```python
result = kimi.process_document(
    file_path="/path/to/document.pdf",
    query="总结这个文档的核心观点"
)

# 输出
# {
#   "status": "success",
#   "type": "document_analysis",
#   "analysis": "..."
# }
```

**支持格式**:

- 图像: jpg, png, gif
- 文档: pdf, docx, txt
- 最大大小: 50 MB

**API 端点**:

```
POST /kimi/image
Content-Type: application/json

{
  "image_url": "https://...",
  "query": "分析这个图像"
}
```

---

### 3️⃣ 实时对话 - 用户直接交互

**使用场景**: 构建基于 Kimi 的聊天应用

**创建会话**:

```python
# 启动聊天会话
session = kimi.start_realtime_chat(user_id="user_001")

# 输出
# {
#   "session_id": "KIMI-CHAT-user_001-1686...",
#   "status": "active"
# }
```

**发送消息**:

```python
# 在会话中发送消息
result = kimi.send_message(
    session_id="KIMI-CHAT-user_001-1686...",
    user_message="龍魂系统支持什么功能？"
)

# 输出
# {
#   "status": "success",
#   "kimi_response": "...",
#   "timestamp": "2026-06-08T..."
# }
```

**API 端点**:

```
# 启动会话
POST /kimi/chat/start
{
  "user_id": "user_001"
}

# 发送消息
POST /kimi/chat/message
{
  "session_id": "KIMI-CHAT-...",
  "message": "你的消息"
}
```

---

### 4️⃣ Skill 引擎 - 特定集成

**使用场景**: 特定 Skill 使用 Kimi 作为推理引擎

**支持的 Skill**:

- `skill-3-canvas-design` - Canvas 设计工具
- `skill-4-doc-coauthoring` - 文档协作编辑
- `skill-6-mcp-builder` - MCP 服务器构建

**代码示例**:

```python
# 使用 Kimi 帮助设计 Canvas
result = kimi.use_kimi_for_skill(
    skill_id="skill-3-canvas-design",
    skill_input={
        "description": "设计一个现代化的数据仪表板",
        "width": 1200,
        "height": 800,
        "style": "dark"
    }
)

# 输出
# {
#   "status": "success",
#   "skill_id": "skill-3-canvas-design",
#   "kimi_output": "..."
# }
```

**API 端点**:

```
POST /kimi/skill
Content-Type: application/json

{
  "skill_id": "skill-3-canvas-design",
  "input": {
    "description": "...",
    "width": 1200
  }
}
```

---

## API 参考

### 完整端点列表

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| POST | `/kimi/backup-inference` | 备用推理 |
| POST | `/kimi/image` | 图像分析 |
| POST | `/kimi/document` | 文档分析 |
| POST | `/kimi/chat/start` | 启动聊天 |
| POST | `/kimi/chat/message` | 发送消息 |
| POST | `/kimi/skill` | Skill 引擎 |
| GET | `/kimi/report` | 集成报告 |

### 响应格式

所有响应都遵循统一的格式:

```json
{
  "status": "success|failed|fallback|unsupported",
  "timestamp": "2026-06-08T10:30:00",
  "data": {
    "...": "..."
  }
}
```

---

## 部署步骤

### Phase 1: 环境配置（5 分钟）

```bash
# 1. 克隆/更新代码
cd ~/longhun-system

# 2. 设置环境变量
export KIMI_API_KEY="apisk-kimi-..."

# 3. 安装依赖
pip3 install requests flask

# 4. 验证安装
python3 -c "from kimi import KimiClient; print('✅ 安装成功')"
```

### Phase 2: 本地测试（10 分钟）

```bash
# 1. 测试 Kimi 连接
cd ~/longhun-system/kimi
python3 kimi_client.py

# 2. 测试集成框架
python3 kimi_integration.py

# 3. 测试网关（轻量级）
python3 kimi_gateway.py
```

### Phase 3: 与龍魂系统集成（15 分钟）

```bash
# 1. 更新生产部署配置
# 编辑 ~/longhun-system/deployment/production_deployment.py
# 添加 Kimi 集成步骤

# 2. 更新 DEPLOYMENT_RUNBOOK_FOR_TEAM.md
# 添加 Kimi 配置和验收步骤

# 3. 生成部署报告
python3 ~/longhun-system/deployment/production_deployment.py
```

### Phase 4: 监控和验收（10 分钟）

```bash
# 1. 启动监控
tail -f /tmp/longhun-kimi/logs/*.log

# 2. 运行烟雾测试
curl http://localhost:5000/health

# 3. 验证所有端点
python3 tests/test_kimi_gateway.py
```

---

## 监控和故障转移

### 健康检查

```python
kimi = KimiIntegration()

status = kimi.get_health_status()
# {
#   "kimi_api": "🟢 connected",
#   "circuit_breaker": {
#     "state": "CLOSED",
#     "failure_count": 0
#   },
#   "integration_modes": {
#     "backup_model": true,
#     "multimodal": true,
#     "realtime_chat": true,
#     "skill_engine": true
#   }
# }
```

### 断路器状态

```python
breaker = kimi.integration.circuit_breaker

# 3 次失败 → 打开
# 60 秒后 → 尝试恢复
# 1 次成功 → 关闭

print(breaker.status())
# {
#   "state": "CLOSED|OPEN|HALF_OPEN",
#   "failure_count": 0,
#   "last_failure_time": null
# }
```

### 监控指标

- API 连接状态
- 故障转移率
- 平均响应时间
- 错误率
- 会话活跃数

---

## 常见问题

### Q1: API Key 如何安全存储？

**A**: 使用环境变量（方案 A）:

```bash
# 不要在代码中硬编码 key
export KIMI_API_KEY="..."

# 在 Python 中读取
import os
api_key = os.getenv("KIMI_API_KEY")
```

### Q2: 故障转移如何工作？

**A**: 自动断路器机制:

1. 记录失败（网络错误、超时等）
2. 3 次失败后打开断路器
3. 未来 60 秒内的请求直接返回本地推理
4. 60 秒后尝试恢复（半开状态）
5. 成功则关闭，恢复正常

### Q3: 支持哪些文件格式？

**A**: 多模态处理支持:

- **图像**: jpg, png, gif
- **文档**: pdf, docx, txt
- **大小**: 最大 50 MB

### Q4: 响应时间是多少？

**A**: 典型延迟:

- Kimi API 调用: 500-2000 ms
- 多模态处理: 1000-5000 ms
- 故障转移检查: < 100 ms

### Q5: 如何监控集成状态？

**A**: 查看集成报告:

```python
report = kimi.get_integration_report()
print(f"模式启用数: {report['modes_enabled']}")
print(f"最近日志: {report['recent_logs'][-5:]}")
```

---

## 总结

| 模式 | 用途 | API 端点 |
|------|------|---------|
| 1️⃣ 备用推理 | 故障转移 | `/backup-inference` |
| 2️⃣ 多模态 | 图像/文档分析 | `/image`, `/document` |
| 3️⃣ 实时对话 | 用户聊天 | `/chat/start`, `/chat/message` |
| 4️⃣ Skill 引擎 | Skill 集成 | `/skill` |

---

**维护者**: UID9622（诸葛鑫）
**最后更新**: 2026-06-08
**版本**: 1.0.0
