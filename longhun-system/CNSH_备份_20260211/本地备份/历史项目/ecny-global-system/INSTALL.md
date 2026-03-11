# 🔧 安装指南

## 🚀 快速安装

### 1. 环境要求

**必需软件：**
- Python 3.11+
- Node.js 18+
- Docker 24+
- PostgreSQL 15+
- Redis 7+

### 2. 一键安装脚本

```bash
# 创建项目目录
mkdir ecny-global-system
cd ecny-global-system

# 创建Python虚拟环境
python3.11 -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 创建requirements.txt
cat > requirements.txt << EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
psycopg2-binary==2.9.9
redis==5.0.1
numpy==1.26.2
pandas==2.1.3
python-dotenv==1.0.0
EOF

# 安装Python依赖
pip install -r requirements.txt

# 启动Docker服务
docker-compose up -d

# 运行系统
python backend/app/main.py
```

## 📋 详细安装步骤

### 第一步：环境安装

### 1. 安装Python环境

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
python3.11 --version
```

**macOS:**
```bash
brew install python@3.11
python3.11 --version
```

**Windows:**
```powershell
# 下载并安装Python 3.11
# 官网：https://www.python.org/downloads/
python --version
```

### 2. 安装Node.js

**Ubuntu/Debian:**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
node --version
npm --version
```

**macOS:**
```bash
brew install node@18
node --version
```

**Windows:**
```powershell
# 下载并安装Node.js LTS
# 官网：https://nodejs.org/
```

### 3. 安装Docker

**Ubuntu:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo systemctl start docker
sudo systemctl enable docker
docker --version
```

**macOS:**
```bash
# 下载Docker Desktop for Mac
# 官网：https://www.docker.com/products/docker-desktop/
```

**Windows:**
```powershell
# 下载Docker Desktop for Windows
# 官网：https://www.docker.com/products/docker-desktop/
```

### 第二步：项目配置

```bash
# 克隆项目
git clone <repository-url>
cd ecny-global-system

# 复制环境配置
cp .env.example .env

# 编辑配置文件
nano .env
```

### 第三步：启动服务

#### 方式一：Docker运行（推荐）
```bash
# 启动所有服务
docker-compose up -d

# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
```

#### 方式二：本地开发运行
```bash
# 启动后端
cd backend
source venv/bin/activate
python app/main.py

# 后端将运行在 http://localhost:8000
# API文档：http://localhost:8000/docs
```

## 🧪 测试安装

### 使用curl测试API

```bash
# 健康检查
curl http://localhost:8000/health

# 获取2030年部署计划
curl -X POST http://localhost:8000/api/yijing/deployment \
  -H "Content-Type: application/json" \
  -d '{"year": 2030}'

# 预测10年增长
curl -X POST http://localhost:8000/api/growth/predict \
  -H "Content-Type: application/json" \
  -d '{"years": 10}'
```

### 使用Python测试

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# 测试健康检查
response = requests.get(f"{BASE_URL}/health")
print("健康检查:", response.json())

# 测试部署计划
response = requests.post(
    f"{BASE_URL}/api/yijing/deployment",
    json={"year": 2030}
)
print("2030年部署计划:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 🔧 故障排除

### Q1：pip安装依赖失败
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2：Docker容器无法连接PostgreSQL
```bash
# 检查网络配置
docker network ls
docker network inspect ecny-network
```

### Q3：端口被占用
```yaml
# 修改docker-compose.yml中的端口映射
ports:
  - "8001:8000"  # 将8000改为8001
```

## 📊 验证安装

安装完成后，访问以下地址验证系统是否正常运行：

- **API文档**：http://localhost:8000/docs
- **健康检查**：http://localhost:8000/health
- **系统状态**：http://localhost:8000/

如果所有API都能正常响应，说明安装成功！

---

**DNA确认码**：`#CNSH-INSTALLATION-GUIDE-COMPLETE`

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-14f69c42-20251218032410
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 乾卦：天行健，君子以自强不息
📜 内容哈希: 0f4865dd33ad9b2a
⚠️ 警告: 未经授权修改将触发DNA追溯系统
