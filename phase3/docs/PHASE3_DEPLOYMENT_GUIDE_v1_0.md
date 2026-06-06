# 龍魂系統 Phase 3 - 完整部署配置
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
  # 後端服務
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

  # 前端服務
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

  # 數據庫服務
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

## 🐳 後端 Dockerfile

```dockerfile
# Dockerfile (backend)

FROM python:3.11-slim

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用代碼
COPY . .

# 健康檢查
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

# 複製 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 複製構建結果
COPY --from=builder /app/build /usr/share/nginx/html

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
```

---

## 📝 後端 requirements.txt

```
# FastAPI 和 Web 框架
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# 數據庫
sqlalchemy==2.0.23
sqlite3 (built-in)

# 認證與安全
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# WebSocket
websockets==12.0

# 工具
python-dateutil==2.8.2
requests==2.31.0
httpx==0.25.2

# 監控與日誌
prometheus-client==0.19.0
python-json-logger==2.0.7

# 數據分析（用於趨勢分析）
numpy==1.26.2
pandas==2.1.3
scikit-learn==1.3.2

# 導出與文檔
python-docx==0.8.11
openpyxl==3.11.0
reportlab==4.0.8

# 開發工具
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
black==23.12.0
flake8==6.1.0
mypy==1.7.1

# 環境管理
python-dotenv==1.0.0
```

---

## 📝 前端 package.json

```json
{
  "name": "longhun-frontend",
  "version": "3.0.0",
  "description": "龍魂系統 Phase 3 React 前端",
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

## 🚀 快速開始指南

### 方法 1: 使用 Docker Compose（推薦）

```bash
# 1. 克隆倉庫
git clone https://github.com/UID9622/longhun-system.git
cd longhun-system/phase3

# 2. 構建並啟動所有服務
docker-compose up -d

# 3. 查看日誌
docker-compose logs -f backend
docker-compose logs -f frontend

# 4. 訪問應用
# 後端 API: http://localhost:8000
# API 文檔: http://localhost:8000/api/docs
# 前端: http://localhost:3000

# 5. 停止服務
docker-compose down
```

### 方法 2: 本地開發（無 Docker）

#### 後端設置

```bash
# 1. 進入後端目錄
cd backend

# 2. 創建虛擬環境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 運行伺服器
uvicorn main:app --reload
# 訪問: http://localhost:8000/api/docs
```

#### 前端設置

```bash
# 1. 進入前端目錄
cd frontend

# 2. 安裝依賴
npm install

# 3. 啟動開發伺服器
npm start
# 自動打開: http://localhost:3000
```

---

## 📊 系統要求

### 最小配置
- CPU: 2 cores
- RAM: 2GB
- 磁盤: 2GB
- 操作系統: Linux/macOS/Windows

### 推薦配置
- CPU: 4+ cores
- RAM: 4GB+
- 磁盤: 10GB+
- 操作系統: Ubuntu 20.04+ / macOS 10.15+ / Windows 10+

---

## 🔧 常見命令

```bash
# 查看所有容器狀態
docker-compose ps

# 進入後端容器
docker-compose exec backend bash

# 進入前端容器
docker-compose exec frontend sh

# 查看後端日誌
docker-compose logs backend -f

# 重新構建鏡像
docker-compose build --no-cache

# 清理所有數據
docker-compose down -v

# 重启特定服务
docker-compose restart backend
```

---

## 📈 生産部署

### 使用 production profile

```bash
# 啟動包含 Nginx 的生産配置
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
# 生成自簽名證書（開發用）
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# 複製到 ssl/ 目錄
mkdir -p ssl
cp cert.pem key.pem ssl/

# 使用 Let's Encrypt（生産用）
docker run --rm -v /etc/letsencrypt:/etc/letsencrypt \
  certbot/certbot certonly --standalone -d api.longhun-system.com
```

---

## ✅ 驗收檢查清單

部署後請檢查以下項目：

```
[ ] 後端 API 健康檢查通過
    curl http://localhost:8000/api/v1/health

[ ] API 文檔可訪問
    http://localhost:8000/api/docs

[ ] 前端頁面能加載
    http://localhost:3000

[ ] WebSocket 連接正常
    查看瀏覽器控制台是否有連接日誌

[ ] 可以創建技能
    在前端技能管理頁面測試

[ ] 可以查看仪表板
    查看實時監控數據

[ ] 日誌輸出正常
    docker-compose logs backend

[ ] 所有容器健康狀態正常
    docker-compose ps
```

---

## 🐉 DNA 簽章

```
DNA: #龍芯⚡️2026-06-06-PHASE3-DEPLOYMENT-v1.0
責任: UID9622 · 不免責
時間: 2026-06-06 21:25 CST
狀態: 🟢 生産就緒
```

---

**現在可以部署 Phase 3 了！** 🚀
