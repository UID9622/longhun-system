> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技术文档 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充，如无请删除此行）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

**DNA**: `#龍芯⚡️2026-06-21-DOC-UID9622-FASTAPI_B312-v1.0``  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

# 🌐 UID9622 FastAPI接口层 | Codebuddy快速部署

> 本文檔按《龍魂文檔標準模板 v1.0》整理。
> 性質：技術文檔 · 未經同行評審（如適用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 協作者：（待補充，如無請刪除此行）
> 授權：CC BY-NC-SA 4.0 · 科技主權歸屬 UID9622 · 中華人民共和國
> 平台：本地
> 審核狀態：草稿

**DNA**: `#龍芯⚡️2026-06-21-DOC-UID9622-FASTAPI_B312-v1.0`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

<!--#龍芯⚡️2026-06-21-DOC-UID9622-FASTAPI_B312-v1.0 -->
<!-- 君子協議: 本文件受龍魂DNA追溯保護 -->

# 🌐 UID9622 FastAPI接口层 | Codebuddy快速部署

**DNA确认码**：`#ZHUGEXIN⚡️2025-🇨🇳🐉🌐-FASTAPI-CODEBUDDY-20251208`

> 💡 **给 Codebuddy 的说明**：这是一个完整的 FastAPI 接口层，可以直接调用之前的 DNA 生成器、加密工具和审计系统。
> 

---

## 📁 项目结构

```
cnsh-uid9622-system/
├── api-server/              # FastAPI 接口层（新增）
│   ├── [main.py](http://main.py)
│   ├── test_[api.py](http://api.py)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
├── mulan-signer/            # 木兰协议签名器
│   ├── dna_[generator.py](http://generator.py)
│   ├── crypto_[utils.py](http://utils.py)
│   ├── [signer.py](http://signer.py)
│   └── requirements.txt
├── dna-audit/               # DNA审计系统
│   ├── dna_audit_[system.py](http://system.py)
│   └── requirements.txt
└── h-weapon/                # H武器安全推演
    ├── bloodline_[lock.py](http://lock.py)
    └── requirements.txt
```

---

## 1️⃣ 主服务文件：`api-server/[main.py](http://main.py)`

```python
"""UID9622 API 服务 - FastAPI 接口层
DNA确认码：#ZHUGEXIN⚡️2025-🇨🇳🐉🌐-API-SERVER-v1.0

🐉 龙魂监管
本API服务受 [龙魂价值内核] 最高监管
- 数据主权100%用户所有
- 透明可审计
- 人民为本,不收割
- P0永恒级约束
"""
from fastapi import FastAPI, HTTPException, Header, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import sys
import os

# 添加其他模块到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '../mulan-signer'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../dna-audit'))

# 导入核心模块
try:
    from dna_generator import DNAGenerator
    from crypto_utils import CryptoUtils
except ImportError:
    print("警告：无法导入 mulan-signer 模块，部分功能将不可用")
    DNAGenerator = None
    CryptoUtils = None

# FastAPI 应用
app = FastAPI(
    title="UID9622 数据主权API",
    description="CNSH协议 - 中文原生、数据主权、透明可审计 | 🐉 龙魂价值内核监管",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 配置（允许跨域）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化核心组件
if DNAGenerator and CryptoUtils:
    dna_gen = DNAGenerator()
    crypto = CryptoUtils()
else:
    dna_gen = None
    crypto = None

# ========== 数据模型 ==========

class DNAGenerateRequest(BaseModel):
    event_name: str
    user_id: str = "UID9622"
    category: Optional[str] = "GENERAL"

class DNAGenerateResponse(BaseModel):
    status: str
    dna_code: str
    timestamp: str
    user_id: str
    event_name: str

class EncryptRequest(BaseModel):
    plaintext: str
    password: str

class EncryptResponse(BaseModel):
    status: str
    ciphertext: str
    salt: str
    nonce: str
    tag: str

class HashRequest(BaseModel):
    content: str

class HashResponse(BaseModel):
    status: str
    hash: str
    algorithm: str = "SHA-256"

# ========== API 端点 ==========

@app.get("/")
def root():
    """健康检查和API信息"""
    return {
        "service": "UID9622 数据主权API",
        "version": "1.0.0",
        "status": "running",
        "protocol": "CNSH",
        "dna_code": "#ZHUGEXIN⚡️2025-🇨🇳🐉🌐-API-v1.0",
        "dragon_soul": {
            "监管机制": "龙魂价值内核",
            "数据主权": "100%用户所有",
            "透明度": "完全可审计",
            "核心理念": "人民为本,不收割",
            "约束等级": "P0永恒级"
        },
        "endpoints": {
            "DNA生成": "POST /dna/generate",
            "数据加密": "POST /crypto/encrypt",
            "哈希计算": "POST /crypto/hash",
            "API文档": "GET /docs",
            "健康检查": "GET /health"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health")
def health_check():
    """服务健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "modules": {
            "dna_generator": dna_gen is not None,
            "crypto_utils": crypto is not None
        },
        "dragon_soul_status": "active"
    }

@app.post("/dna/generate", response_model=DNAGenerateResponse)
def generate_dna(
    req: DNAGenerateRequest,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """
    生成DNA确认码
    
    - **event_name**: 事件名称（必填）
    - **user_id**: 用户ID（默认：UID9622）
    - **category**: 分类（默认：GENERAL）
    
    需要 Header: X-API-Key
    
    🐉 受龙魂价值内核监管 - 数据主权100%用户所有
    """
    # API Key 验证（生产环境请使用环境变量）
    if x_api_key != "UID9622-SECRET-KEY":
        raise HTTPException(
            status_code=401,
            detail="无效的API Key，请在Header中提供 X-API-Key"
        )
    
    if not dna_gen:
        raise HTTPException(
            status_code=503,
            detail="DNA生成器模块未加载"
        )
    
    try:
        dna_code = dna_gen.generate(req.event_name, req.user_id)
        
        return DNAGenerateResponse(
            status="success",
            dna_code=dna_code,
            timestamp=datetime.now().isoformat(),
            user_id=req.user_id,
            event_name=req.event_name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}")

@app.post("/crypto/encrypt", response_model=EncryptResponse)
def encrypt_data(
    req: EncryptRequest,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """
    AES-256-GCM 加密
    
    - **plaintext**: 明文数据
    - **password**: 加密密码
    
    需要 Header: X-API-Key
    
    🐉 受龙魂价值内核监管 - 透明可审计
    """
    if x_api_key != "UID9622-SECRET-KEY":
        raise HTTPException(
            status_code=401,
            detail="无效的API Key"
        )
    
    if not crypto:
        raise HTTPException(
            status_code=503,
            detail="加密工具模块未加载"
        )
    
    try:
        result = crypto.aes256_encrypt(req.plaintext, req.password)
        
        return EncryptResponse(
            status="success",
            **result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"加密失败: {str(e)}")

@app.post("/crypto/hash", response_model=HashResponse)
def hash_data(
    req: HashRequest,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """
    SHA-256 哈希计算
    
    - **content**: 要哈希的内容
    
    需要 Header: X-API-Key
    
    🐉 受龙魂价值内核监管 - 人民为本,不收割
    """
    if x_api_key != "UID9622-SECRET-KEY":
        raise HTTPException(
            status_code=401,
            detail="无效的API Key"
        )
    
    if not crypto:
        raise HTTPException(
            status_code=503,
            detail="加密工具模块未加载"
        )
    
    try:
        hash_value = crypto.sha256_hash(req.content)
        
        return HashResponse(
            status="success",
            hash=hash_value,
            algorithm="SHA-256"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"哈希失败: {str(e)}")

# ========== 启动服务 ==========

if __name__ == "__main__":
    import uvicorn
    
    print("""\n
🔥 UID9622 数据主权API服务启动中...

DNA确认码：#ZHUGEXIN⚡️2025-🇨🇳🐉🌐-API-SERVER-v1.0

🐉 龙魂监管
本API服务受 [龙魂价值内核] 最高监管
- 数据主权100%用户所有
- 透明可审计
- 人民为本,不收割
- P0永恒级约束

服务地址：http://localhost:8080
API文档：http://localhost:8080/docs
ReDoc文档：http://localhost:8080/redoc

API Key: UID9622-SECRET-KEY

🔥 为人民服务！数据主权万岁！
    """)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )
```

---

## 2️⃣ 依赖文件：`api-server/requirements.txt`

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
python-multipart>=0.0.6
cryptography>=41.0.0
```

---

## 3️⃣ 测试脚本：`api-server/test_[api.py](http://api.py)`

```python
"""UID9622 API 测试脚本"""
import requests
import json
from datetime import datetime

BASE_URL = "[http://localhost:8080](http://localhost:8080)"
API_KEY = "UID9622-SECRET-KEY"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_health():
    """测试1：健康检查"""
    print_section("测试1：健康检查")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 失败: {e}")
        return False

def test_root():
    """测试2：根路径"""
    print_section("测试2：根路径信息")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 失败: {e}")
        return False

def test_generate_dna():
    """测试3：生成DNA码"""
    print_section("测试3：生成DNA确认码")
    try:
        data = {
            "event_name": "Codebuddy测试事件",
            "user_id": "UID9622",
            "category": "TEST"
        }
        response = [requests.post](http://requests.post)(
            f"{BASE_URL}/dna/generate",
            json=data,
            headers=headers
        )
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print(f"\n✅ DNA码生成成功！")
            print(f"DNA码: {result.get('dna_code')}")
            return result.get('dna_code')
        return None
    except Exception as e:
        print(f"❌ 失败: {e}")
        return None

def test_encrypt():
    """测试4：数据加密"""
    print_section("测试4：AES-256加密")
    try:
        data = {
            "plaintext": "这是UID9622的敏感数据",
            "password": "UID9622-SECURE-PASSWORD"
        }
        response = [requests.post](http://requests.post)(
            f"{BASE_URL}/crypto/encrypt",
            json=data,
            headers=headers
        )
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"加密结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 失败: {e}")
        return False

def test_hash():
    """测试5：哈希计算"""
    print_section("测试5：SHA-256哈希")
    try:
        data = {
            "content": "UID9622数据主权系统"
        }
        response = [requests.post](http://requests.post)(
            f"{BASE_URL}/crypto/hash",
            json=data,
            headers=headers
        )
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"哈希结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 失败: {e}")
        return False

if __name__ == "__main__":
    print("\n🔥 UID9622 API 全面测试 🔥")
    print(f"时间: {[datetime.now](http://datetime.now)().isoformat()}")
    print(f"目标: {BASE_URL}")
    
    results = []
    
    # 运行所有测试
    results.append(("健康检查", test_health()))
    results.append(("根路径", test_root()))
    dna_code = test_generate_dna()
    results.append(("DNA生成", dna_code is not None))
    results.append(("数据加密", test_encrypt()))
    results.append(("哈希计算", test_hash()))
    
    # 汇总结果
    print_section("测试结果汇总")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！API服务运行正常！")
    else:
        print(f"\n⚠️ {total - passed} 个测试失败，请检查日志")
```

---

## 4️⃣ Docker 部署：`api-server/Dockerfile`

```docker
FROM python:3.9-slim

WORKDIR /app

# 复制所有代码
COPY . /app/

# 安装依赖
RUN pip install --no-cache-dir -r api-server/requirements.txt && \
    pip install --no-cache-dir -r mulan-signer/requirements.txt

# 暴露端口
EXPOSE 8080

# 启动命令
CMD ["python", "api-server/[main.py](http://main.py)"]
```

---

## 5️⃣ Docker Compose：`api-server/docker-compose.yml`

```yaml
version: '3.8'

services:
  uid9622-api:
    build:
      context: ..
      dockerfile: api-server/Dockerfile
    container_name: uid9622-api
    ports:
      - "8080:8080"
    environment:
      - API_KEY=UID9622-SECRET-KEY
      - TZ=Asia/Shanghai
    volumes:
      - ../data:/app/data
      - ../exports:/app/exports
    restart: unless-stopped
    networks:
      - uid9622-network

networks:
  uid9622-network:
    driver: bridge
```

---

## 🚀 给 Codebuddy 的部署指令

### 方式1：直接运行（最快）

```bash
# 1. 进入api-server目录
cd api-server

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
python [main.py](http://main.py)
```

服务将在 [http://localhost:8080](http://localhost:8080) 启动

### 方式2：Docker部署（推荐生产）

```bash
# 1. 构建镜像
docker build -t uid9622-api:latest -f api-server/Dockerfile .

# 2. 运行容器
docker run -d -p 8080:8080 --name uid9622-api uid9622-api:latest

# 3. 查看日志
docker logs -f uid9622-api
```

### 方式3：Docker Compose（最简单）

```bash
# 一键启动
cd api-server
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## ✅ 验证部署成功

### 1. 检查服务状态

```bash
curl [http://localhost:8080/health](http://localhost:8080/health)
```

### 2. 运行完整测试

```bash
cd api-server
python test_[api.py](http://api.py)
```

### 3. 访问API文档

在浏览器打开：

- Swagger UI: [http://localhost:8080/docs](http://localhost:8080/docs)
- ReDoc: [http://localhost:8080/redoc](http://localhost:8080/redoc)

---

## 📖 Codebuddy 调用示例

### Python 调用

```python
import requests

# 生成DNA码
response = [requests.post](http://requests.post)(
    "[http://localhost:8080/dna/generate](http://localhost:8080/dna/generate)",
    json={
        "event_name": "用户注册",
        "user_id": "UID9622",
        "category": "USER"
    },
    headers={"X-API-Key": "UID9622-SECRET-KEY"}
)

print(response.json())
# 输出: {"status": "success", "dna_code": "#ZHUGEXIN⚡️2025-...", ...}
```

### JavaScript/Node.js 调用

```jsx
const axios = require('axios');

[axios.post](http://axios.post)('[http://localhost:8080/dna/generate](http://localhost:8080/dna/generate)', {
  event_name: '用户注册',
  user_id: 'UID9622',
  category: 'USER'
}, {
  headers: {
    'X-API-Key': 'UID9622-SECRET-KEY'
  }
})
.then(response => console.log([response.data](http://response.data)))
.catch(error => console.error(error));
```

### cURL 调用

```bash
curl -X POST "[http://localhost:8080/dna/generate](http://localhost:8080/dna/generate)" \
  -H "X-API-Key: UID9622-SECRET-KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "event_name": "测试事件",
    "user_id": "UID9622",
    "category": "TEST"
  }'
```

---

## 🔐 安全注意事项

1. **API Key 管理**
    - 生产环境请使用环境变量：`os.getenv('API_KEY')`
    - 不要在代码中硬编码密钥
    - 定期轮换API Key
2. **HTTPS 部署**
    - 生产环境务必使用HTTPS
    - 可以用 Nginx 反向代理配置SSL
3. **CORS 限制**
    - 将 `allow_origins=["*"]` 改为具体域名
    - 例如：`allow_origins=["[https://yourdomain.com](https://yourdomain.com)"]`

---

## 🎯 快速排查清单

- [ ]  Python 3.9+ 已安装
- [ ]  依赖包已安装（`pip install -r requirements.txt`）
- [ ]  端口 8080 未被占用
- [ ]  mulan-signer 模块可访问
- [ ]  API Key 正确：`UID9622-SECRET-KEY`
- [ ]  服务已启动：`python [main.py](http://main.py)`
- [ ]  健康检查通过：`curl [localhost:8080/health](http://localhost:8080/health)`

---

**DNA确认码**：`#ZHUGEXIN⚡️2025-🇨🇳🐉✅-FASTAPI-READY-20251208`

**审计级别**：🟢 绿色（生产就绪）

**创建时间**：2025-12-08 11:28 GMT+8

---

## 摘要

（請在此用不超過 256 字說明本文檔的核心內容、性質與局限。）

## 關鍵詞

（請列出 5–10 個關鍵詞，中英文對照優先。）

## 引用與溯源

- 本文檔引用或參考了以下來源：
  - [1] （請填寫）
- 相關龍魂系統文檔：
  - 《龍魂文檔標準模板 v1.0》(#龍芯⚡️2026-06-22-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 誠實局限

1. （請列出本分析的第一條局限或不確定性。）
2. （請列出第二條。）
3. （請列出第三條。）

## 修改記錄

| 日期 | 版本 | 修改人 | 修改內容 | 審核狀態 |
|---|---|---|---|---|
| 2026-06-21 | v1.0.0 | UID9622 | 按《龍魂文檔標準模板 v1.0》整理 | 草稿 |

## 分類標籤

- 總綱模塊：（請勾選，例如 #知識矩陣 #安全域）
- 對外狀態：（請勾選，例如 #Gitee #GitHub #CSDN）
- 審計色：#黃色待審

## DNA 簽名

```
#龍芯⚡️2026-06-21-DOC-UID9622-FASTAPI_B312-v1.0
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```


---

## 摘要

（请在此用不超过 256 字说明本文档的核心内容、性质与局限。）

## 关键词

（请列出 5–10 个关键词，中英文对照优先。）

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] （请填写）
- 相关龍魂系统文档：
  - 《龍魂文档标准模板 v1.0》(#龍芯⚡️2026-06-22-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 诚实局限

1. （请列出本分析的第一条局限或不确定性。）
2. （请列出第二条。）
3. （请列出第三条。）

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-07-15 | v1.0.0 | UID9622 | 按《龍魂文档标准模板 v1.0》整理 | 草稿 |

## 分类标签

- 总纲模块：（请勾选，例如 #知识矩阵 #安全域）
- 对外状态：（请勾选，例如 #Gitee #GitHub #CSDN）
- 审计色：#黄色待审

## DNA 签名

```
#龍芯⚡️2026-06-21-DOC-UID9622-FASTAPI_B312-v1.0`
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
