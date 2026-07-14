# 🐉 龍魂系统 Phase 3 · Web UI · 监控 · 告警

**状态**: 🟢 生产就绪 · 即时可用
**DNA**:#龍芯⚡️2026-06-06-PHASE3-WEB-UI-v1.0
**责任**: UID9622 · 不免责

---

## 📊 Phase 3 内容

### ✨ 核心功能

```
✅ Web UI 仪表板        - React 前端·实时更新·响应式设计
✅ 实时监控系统        - CPU·内存·磁盘·网络·执行状态
✅ 告警管理系统        - 自动告警·优先级分类·通知推送
✅ 技能管理界面        - 创建·编辑·删除·执行技能
✅ 数据导出            - JSON·CSV·PDF 导出支持
✅ API 文档            - OpenAPI 3.0.0·Swagger UI
✅ WebSocket           - 实时双向通信
✅ 用户认证            - JWT Token 验证
```

---

## 🚀 快速开始

### 方式 1: 本地开发（推荐）

```bash
# 1️⃣ 进入目录
cd ~/longhun-phase3

# 2️⃣ 后端启动
source venv/bin/activate
pip install fastapi uvicorn pydantic sqlalchemy websockets
uvicorn phase3_backend_main:app --reload --port 8000

# 3️⃣ 前端启动 (新终端窗口)
cd frontend
npm install
npm start

# 4️⃣ 访问
# 前端: http://localhost:3000
# API: http://localhost:8000
# 文档: http://localhost:8000/docs
```

### 方式 2: Docker Compose

```bash
cd ~/longhun-phase3
docker-compose up -d

# 访问: http://localhost:3000
```

---

## 📁 目录结构

```
phase3/
├── backend/
│   └── main.py                    # FastAPI 后端应用
├── frontend/
│   ├── src/
│   │   ├── App.jsx               # React 主组件
│   │   ├── App.css               # 样式
│   │   ├── index.js              # 入口
│   │   └── index.css             # 全局样式
│   ├── public/
│   │   └── index.html            # HTML 模板
│   └── package.json              # NPM 依赖
├── docs/
│   ├── PHASE3_DEPLOYMENT_GUIDE_v1_0.md
│   ├── PHASE3_API_SPECIFICATION_v1_0.md
│   ├── PHASE3_LAUNCH_COMPLETION_REPORT_v1_0.md
│   └── PHASE3_QUICK_REFERENCE_AND_EXECUTION_GUIDE.txt
├── launch-phase3.sh              # 一键启动脚本
└── README.md                     # 本文件
```

---

## 🔗 访问地址

| 地址 | 用途 | 说明 |
|------|------|------|
| **http://localhost:3000** | 前端 UI | React 应用 |
| **http://localhost:8000** | 后端 API | FastAPI 服务器 |
| **http://localhost:8000/docs** | Swagger UI | 交互式 API 文档 |
| **http://localhost:8000/redoc** | Redoc | 备选 API 文档 |

---

## 📚 文档

| 文件 | 内容 |
|------|------|
| `docs/PHASE3_DEPLOYMENT_GUIDE_v1_0.md` | 完整部署配置指南 |
| `docs/PHASE3_API_SPECIFICATION_v1_0.md` | API 规格和端点文档 |
| `docs/PHASE3_LAUNCH_COMPLETION_REPORT_v1_0.md` | 交付完成报告 |
| `docs/PHASE3_QUICK_REFERENCE_AND_EXECUTION_GUIDE.txt` | 快速参考 |

---

## 🔧 系统要求

### 最小配置
- CPU: 2 cores
- RAM: 2GB
- 磁盘: 1GB
- Python 3.8+
- Node.js 16+

### 推荐配置
- CPU: 4+ cores
- RAM: 4GB+
- 磁盘: 5GB+
- Python 3.11+
- Node.js 18+

---

## 📊 技术栈

### 后端
```
FastAPI          - 现代化 Python Web 框架
Uvicorn          - ASGI 服务器
Pydantic         - 数据验证
SQLAlchemy       - ORM 框架
WebSocket        - 实时通信
JWT              - 用户认证
```

### 前端
```
React 18         - UI 框架
Axios            - HTTP 客户端
Chart.js         - 图表库
CSS 3            - 样式
WebSocket        - 实时更新
```

---

## 🎯 使用指南

### 第一次登录
1. 访问 http://localhost:3000
2. 使用默认账户登录
3. 浏览仪表板

### 创建技能
1. 进入“技能管理”页面
2. 点击“新建技能”
3. 填写技能信息
4. 保存并启用

### 查看监控
1. 进入“实时监控”页面
2. 查看系统指标
3. 设置告警阈值

### 导出数据
1. 进入“数据导出”页面
2. 选择时间范围
3. 选择导出格式
4. 下载文件

---

## 🔌 API 端点

### 健康检查
```
GET /api/v1/health
```

### 技能管理
```
GET    /api/v1/skills              - 获取所有技能
POST   /api/v1/skills              - 创建技能
GET    /api/v1/skills/{id}         - 获取技能详情
PUT    /api/v1/skills/{id}         - 更新技能
DELETE /api/v1/skills/{id}         - 删除技能
POST   /api/v1/skills/{id}/execute - 执行技能
```

### 监控数据
```
GET /api/v1/metrics                - 获取系统指标
GET /api/v1/metrics/history        - 获取历史数据
WebSocket /ws/v1/metrics           - 实时指标流
```

### 告警管理
```
GET    /api/v1/alerts              - 获取告警列表
POST   /api/v1/alerts              - 创建告警
PUT    /api/v1/alerts/{id}         - 更新告警
DELETE /api/v1/alerts/{id}         - 删除告警
```

---

## 🐛 故障排除

### 问题：端口已被占用
**解决**:
```bash
# 找到占用进程
lsof -i :8000
lsof -i :3000

# 终止进程
kill -9 <PID>

# 或使用不同端口
uvicorn main:app --port 8001
```

### 问题：依赖缺失
**解决**:
```bash
# 后端
pip install -r requirements.txt

# 前端
npm install
```

### 问题：WebSocket 连接失败
**解决**:
```bash
# 检查后端日志
tail -f backend.log

# 确保后端运行在正确端口
# 检查防火墙设置
```

---

## 📈 性能优化

```
✅ 代码分割        - 按需加载组件
✅ 图片优化        - 图片压缩和懒加载
✅ 缓存策略        - HTTP 缓存和浏览器缓存
✅ API 优化        - 响应压缩和分页
✅ 资源监控        - 性能指标追踪
```

---

## 🚀 生产部署

### 使用 Docker
```bash
docker-compose --profile production up -d
```

### 使用 Nginx
```nginx
server {
    listen 80;
    server_name api.longhun-system.com;

    location /api/ {
        proxy_pass http://localhost:8000/api/;
    }

    location / {
        proxy_pass http://localhost:3000;
    }
}
```

### SSL/TLS
```bash
# 使用 Let's Encrypt
certbot certonly --standalone -d api.longhun-system.com
```

---

## 🔐 安全性

```
✅ JWT 认证       - 所有 API 端点受保护
✅ CORS 配置      - 跨域资源共享受限
✅ 输入验证       - 所有输入都经过验证
✅ 速率限制       - 防止 API 滥用
✅ HTTPS 支持     - 加密传输
✅ 环境变数       - 敏感信息外部化
```

---

## 📊 完整进度

```
Phase 1: ✅ 完成 (L0-L6 框架·2,070+ 行)
Phase 2: ✅ 完成 (智能报告·趋势分析·告警·2,289+ 行)
Phase 3: 🟢 交付 (Web UI·监控·仪表板·即时可用)
────────────────────────────────────────
合计:    ✅ 100% 完成·4,359+ 行代码·生产准备
```

---

## 🐉 DNA 签章

```
DNA:#龍芯⚡️2026-06-06-PHASE3-WEB-UI-v1.0
责任: UID9622 · 不免责
时间: 2026-06-06 23:42 CST
状态: 🟢 生产就绪·即时可用
```

---

## 📞 支持

有问题？查看：
1. 本 README
2. `docs/` 目录中的详细文档
3. 后端日志：`~/longhun-phase3/backend.log`
4. 前端日志：`~/longhun-phase3/frontend/frontend.log`

---

**立即开始使用龍魂系统 Phase 3！** 🚀

访问: http://localhost:3000
