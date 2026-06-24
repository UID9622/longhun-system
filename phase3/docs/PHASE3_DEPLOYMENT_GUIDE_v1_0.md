# 龍魂系统 Phase 3 - 完整部署配置
# Longhun System Phase 3 - Complete Deployment Configuration

## 📁 项目结构

```
longhun-phase3/
├── backend/
│  ├── main.py                 # FastAPI 主程序
│  ├── requirements.txt         # Python 依赖
│  ├── Dockerfile              # 后端 Docker 镜像
│  ├── .dockerignore            # Docker 忽略文件
│  └── config.yaml             # 配置文件
├── frontend/
│  ├── src/
│  │  ├── App.jsx              # React 主组件
│  │  ├── App.css              # React 样式
│  │  ├── index.js             # React 入口
│  │  └── index.css            # 全局样式
│  ├── public/
│  │  └── index.html
│  ├── package.json            # Node 依赖
│  ├── Dockerfile              # 前端 Docker 镜像
│  └── .dockerignore
├── docker-compose.yml         # Docker Compose 配置
├── Makefile                   # 便捷命令
└── README.md                  # 项目说明
```

---

## 🐳 Docker Compose 配置

```yaml
# docker-compose.yml

version: '3.8'

services:
  # 后端服务
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: longhun-backend
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
      - LOG_LEVEL=INFO
      - DATABASE_URL=sqlite:///./data/longhun.db
    volumes:
      - ./backend:/app
      - backend_data:/app/data
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    networks:
      - longhun-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 10s
    depends_on:
      - db

  # 前端服务
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: longhun-frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000/api/v1
      - REACT_APP_WS_URL=ws://localhost:8000/ws/v1
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm start
    networks:
      - longhun-network
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000"]
      interval: 10s
      timeout: 5s
      retries: 3

  # 数据库服务
  db:
    image: sqlite:3.44
    container_name: longhun-db
    volumes:
      - db_data:/var/lib/sqlite
    networks:
      - longhun-network

  # Nginx 反向代理（生产环境）
  nginx:
    image: nginx:alpine
    container_name: longhun-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    networks:
      - longhun-network
    depends_on:
      - backend
      - frontend
    profiles:
      - production

volumes:
  backend_data:
  db_data:

networks:
  longhun-network:
    driver: bridge
```

---

## 🐳 后端 Dockerfile

```dockerfile
# Dockerfile (backend)

FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 健康检查
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🐳 前端 Dockerfile

```dockerfile
# Dockerfile (frontend)

# 构建阶段
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# 运行阶段
FROM nginx:alpine

# 复制 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 复制构建结果
COPY --from=builder /app/build /usr/share/nginx/html

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
```

---

## 📝 后端 requirements.txt

```
# FastAPI 和 Web 框架
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# 数据库
sqlalchemy==2.0.23
sqlite3 (built-in)

# 认证与安全
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# WebSocket
websockets==12.0

# 工具
python-dateutil==2.8.2
requests==2.31.0
httpx==0.25.2

# 监控与日志
prometheus-client==0.19.0
python-json-logger==2.0.7

# 数据分析（用于趋势分析）
numpy==1.26.2
pandas==2.1.3
scikit-learn==1.3.2

# 导出与文档
python-docx==0.8.11
openpyxl==3.11.0
reportlab==4.0.8

# 开发工具
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
black==23.12.0
flake8==6.1.0
mypy==1.7.1

# 环境管理
python-dotenv==1.0.0
```

---

## 📝 前端 package.json

```json
{
  "name": "longhun-frontend",
  "version": "3.0.0",
  "description": "龍魂系统 Phase 3 React 前端",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "axios": "^1.6.2",
    "chart.js": "^4.4.0",
    "react-chartjs-2": "^5.2.0",
    "date-fns": "^2.30.0",
    "classnames": "^2.3.2"
  },
  "devDependencies": {
    "@testing-library/react": "^14.1.2",
    "@testing-library/jest-dom": "^6.1.5",
    "@testing-library/user-event": "^14.5.1",
    "prettier": "^3.1.0",
    "eslint": "^8.55.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "lint": "eslint src/",
    "format": "prettier --write src/"
  },
  "eslintConfig": {
    "extends": [
      "react-app"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
```

---

## 🚀 快速开始指南

### 方法 1: 使用 Docker Compose（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/UID9622/longhun-system.git
cd longhun-system/phase3

# 2. 构建并启动所有服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 4. 访问应用
# 后端 API: http://localhost:8000
# API 文档: http://localhost:8000/api/docs
# 前端: http://localhost:3000

# 5. 停止服务
docker-compose down
```

### 方法 2: 本地开发（无 Docker）

#### 后端设置

```bash
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行服务器
uvicorn main:app --reload
# 访问: http://localhost:8000/api/docs
```

#### 前端设置

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm start
# 自动打开: http://localhost:3000
```

---

## 📊 系统要求

### 最小配置
- CPU: 2 cores
- RAM: 2GB
- 磁盘: 2GB
- 操作系统: Linux/macOS/Windows

### 推荐配置
- CPU: 4+ cores
- RAM: 4GB+
- 磁盘: 10GB+
- 操作系统: Ubuntu 20.04+ / macOS 10.15+ / Windows 10+

---

## 🔧 常见命令

```bash
# 查看所有容器状态
docker-compose ps

# 进入后端容器
docker-compose exec backend bash

# 进入前端容器
docker-compose exec frontend sh

# 查看后端日志
docker-compose logs backend -f

# 重新构建镜像
docker-compose build --no-cache

# 清理所有数据
docker-compose down -v

# 重启特定服务
docker-compose restart backend
```

---

## 📈 生产部署

### 使用 production profile

```bash
# 启动包含 Nginx 的生产配置
docker-compose --profile production up -d

# Nginx 配置（nginx.conf）
server {
    listen 80;
    server_name api.longhun-system.com;

    location /api/ {
        proxy_pass http://backend:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### SSL/TLS 配置

```bash
# 生成自签名证书（开发用）
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# 复制到 ssl/ 目录
mkdir -p ssl
cp cert.pem key.pem ssl/

# 使用 Let's Encrypt（生产用）
docker run --rm -v /etc/letsencrypt:/etc/letsencrypt \
  certbot/certbot certonly --standalone -d api.longhun-system.com
```

---

## ✅ 验收检查清单

部署后请检查以下项目：

```
[ ] 后端 API 健康检查通过
    curl http://localhost:8000/api/v1/health

[ ] API 文档可访问
    http://localhost:8000/api/docs

[ ] 前端页面能加载
    http://localhost:3000

[ ] WebSocket 连接正常
    查看浏览器控制台是否有连接日志

[ ] 可以创建技能
    在前端技能管理页面测试

[ ] 可以查看仪表板
    查看实时监控数据

[ ] 日志输出正常
    docker-compose logs backend

[ ] 所有容器健康状态正常
    docker-compose ps
```

---

## 🐉 DNA 签章

```
DNA:#龍芯⚡️2026-06-06-PHASE3-DEPLOYMENT-v1.0
责任: UID9622 · 不免责
时间: 2026-06-06 21:25 CST
状态: 🟢 生产就绪
```

---

**现在可以部署 Phase 3 了！** 🚀
