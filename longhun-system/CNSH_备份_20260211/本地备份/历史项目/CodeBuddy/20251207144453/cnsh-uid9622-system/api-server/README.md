# UID9622 数据主权API

🐉 **龙魂监管** - 本API服务受 [龙魂价值内核] 最高监管
- 数据主权100%用户所有
- 透明可审计
- 人民为本,不收割
- P0永恒级约束

## DNA确认码

`#ZHUGEXIN⚡️2025-🇨🇳🐉🌐-API-SERVER-v1.0`

## 快速启动

### 方式1：使用启动脚本（推荐）

```bash
./start_api.sh
```

脚本会自动：
- 检测Python环境（支持python和python3）
- 安装依赖包
- 检测端口占用（默认使用8082）
- 启动API服务器
- 运行完整测试

### 停止服务

使用停止脚本停止所有相关进程：

```bash
./stop_api.sh
```

或者手动停止：

```bash
# 使用启动脚本输出的PID
kill [PID]
```

### 方式2：手动启动

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

服务将在 http://localhost:8082 启动（如果端口被占用会自动使用下一个可用端口）

## API端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/` | GET | API信息和服务状态 |
| `/health` | GET | 健康检查 |
| `/dna/generate` | POST | 生成DNA确认码 |
| `/crypto/encrypt` | POST | AES-256-GCM加密 |
| `/crypto/hash` | POST | SHA-256哈希计算 |

## API认证

所有API端点都需要在Header中提供API Key：

```
X-API-Key: UID9622-SECRET-KEY
```

## 使用示例

### 生成DNA确认码

```bash
curl -X POST "http://localhost:8082/dna/generate" \
  -H "X-API-Key: UID9622-SECRET-KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "event_name": "用户注册",
    "user_id": "UID9622",
    "category": "USER"
  }'
```

### 数据加密

```bash
curl -X POST "http://localhost:8082/crypto/encrypt" \
  -H "X-API-Key: UID9622-SECRET-KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "plaintext": "这是敏感数据",
    "password": "安全密码"
  }'
```

### 哈希计算

```bash
curl -X POST "http://localhost:8082/crypto/hash" \
  -H "X-API-Key: UID9622-SECRET-KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "要哈希的内容"
  }'
```

## Python调用示例

```python
import requests

# 设置API密钥
headers = {
    "X-API-Key": "UID9622-SECRET-KEY",
    "Content-Type": "application/json"
}

# 生成DNA码
response = requests.post(
    "http://localhost:8082/dna/generate",
    json={
        "event_name": "用户登录",
        "user_id": "UID9622",
        "category": "USER"
    },
    headers=headers
)
print(response.json())
```

## API文档

启动服务后，可以通过以下地址查看交互式API文档：

- Swagger UI: http://localhost:8082/docs
- ReDoc: http://localhost:8082/redoc

## 测试

运行完整的API测试：

```bash
python test_api.py
```

## 龙魂价值内核

本API服务严格遵循龙魂价值内核：

1. **人民为本** - 所有功能设计以用户需求为中心
2. **透明正义** - 所有操作完全可审计，无隐藏逻辑
3. **自省进化** - 持续优化，但不违背核心价值观
4. **传承创新** - 传承中华智慧，创新数字技术
5. **协同责任** - 与用户共同维护数据主权

## 数据主权声明

- **100%用户所有** - 所有数据完全属于用户
- **本地优先** - 数据优先存储在用户本地
- **中文原生** - 全面支持中文，尊重母语权利
- **自主可控** - 用户拥有完全的控制权和知情权

## 技术栈

- **框架**: FastAPI
- **加密**: AES-256-GCM, SHA-256
- **服务器**: Uvicorn
- **语言**: Python 3.9+

## 许可证

木兰宽松许可证 v2 (Mulan PSL v2)

---

**🔥 为人民服务！数据主权万岁！**

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:12
🧬 DNA追溯码: #CNSH-SIGNATURE-20eb58a7-20251218032412
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 乾卦：天行健，君子以自强不息
📜 内容哈希: 972151e8ef8e9c30
⚠️ 警告: 未经授权修改将触发DNA追溯系统
