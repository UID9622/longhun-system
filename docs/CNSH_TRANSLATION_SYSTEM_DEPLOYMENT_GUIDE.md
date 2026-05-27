# 🌐 CNSH 翻译系统 v1.0 完整部署指南

**DNA**: `#龍芯⚡️2026-05-27-CNSH-DEPLOYMENT-GUIDE-v1.0`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`

---

## 📋 目录

1. [快速开始](#快速开始)
2. [本地部署](#本地部署)
3. [Docker 部署](#docker-部署)
4. [Kubernetes 部署](#kubernetes-部署)
5. [配置指南](#配置指南)
6. [使用指南](#使用指南)
7. [故障排查](#故障排查)
8. [维护和升级](#维护和升级)

---

## 快速开始

### 最小化部署（5 分钟）

```bash
# 1. 克隆项目
cd ~/Projects
git clone https://github.com/your-repo/cnsh-translator.git
cd cnsh-translator

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# 3. 安装依赖
pip install -r requirements_cnsh.txt

# 4. 配置环境变量
cp .env.template .env
# 编辑 .env，填入 Notion Token 和 OpenAI API Key

# 5. 运行
chmod +x start_cnsh.sh
./start_cnsh.sh start

# 6. 查看日志
./start_cnsh.sh logs
```

---

## 本地部署

### 前置要求

- Python 3.8+ ✅
- pip 包管理器
- Notion Integration Token
- OpenAI API Key
- macOS/Linux（或 WSL for Windows）

### 详细步骤

#### Step 1: 环境检查

```bash
python3 --version
pip --version
```

#### Step 2: 项目目录

```bash
# 创建项目目录
mkdir -p ~/Projects/cnsh-translator
cd ~/Projects/cnsh-translator

# 从 git 克隆或复制文件
git clone https://github.com/your-repo/cnsh-translator.git
```

#### Step 3: 虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活（macOS/Linux）
source venv/bin/activate

# 激活（Windows PowerShell）
.\venv\Scripts\Activate.ps1

# 激活（Windows CMD）
venv\Scripts\activate.bat
```

#### Step 4: 安装依赖

```bash
# 升级 pip
pip install --upgrade pip

# 安装依赖
pip install -r requirements_cnsh.txt
```

#### Step 5: 配置

```bash
# 创建配置目录
mkdir -p ~/.cnsh/config ~/.cnsh/logs

# 复制环境变量模板
cp .env.template ~/.cnsh/config/.env

# 编辑配置文件
nano ~/.cnsh/config/.env
```

**必填配置**：
```env
NOTION_TOKEN=sk_live_xxx...
DATABASE_ID=xxx...
OPENAI_API_KEY=sk-xxx...
OPENAI_MODEL=gpt-4
```

#### Step 6: 启动

```bash
# 赋予脚本执行权限
chmod +x start_cnsh.sh

# 启动系统
./start_cnsh.sh start

# 查看状态
./start_cnsh.sh status

# 查看日志
./start_cnsh.sh logs
```

#### Step 7: 验证

```bash
# 检查是否成功启动
ps aux | grep cnsh_translator

# 查看日志输出
tail -f ~/.cnsh/logs/cnsh_translator.log

# 预期输出包含：
# ✓ CNSH 完整翻译系统 v1.0
# ✓ 翻译引擎初始化完成
# ✓ 任务队列管理器初始化完成
```

---

## Docker 部署

### Docker 部署（推荐用于生产）

#### 前置要求

- Docker 安装完毕
- Docker Compose（可选）

#### 构建镜像

```bash
# 构建镜像
docker build -f Dockerfile.cnsh -t cnsh-translator:v1.0 .

# 验证镜像
docker images | grep cnsh
```

#### 运行容器

```bash
# 简单运行
docker run -d \
  --name cnsh-translator \
  -v ~/.cnsh/config/.env:/app/.env:ro \
  -v ~/.cnsh/logs:/var/log/cnsh \
  -e LOG_LEVEL=INFO \
  cnsh-translator:v1.0

# 检查运行状态
docker ps | grep cnsh

# 查看日志
docker logs -f cnsh-translator
```

#### 使用 Docker Compose

```bash
# 启动全套服务（包括 Redis、PostgreSQL）
docker-compose -f docker-compose.cnsh.yml up -d

# 检查服务状态
docker-compose -f docker-compose.cnsh.yml ps

# 查看日志
docker-compose -f docker-compose.cnsh.yml logs -f cnsh-translator

# 停止服务
docker-compose -f docker-compose.cnsh.yml down
```

#### 环境变量文件

创建 `.env` 文件用于 Docker Compose：

```bash
# .env
NOTION_TOKEN=sk_live_xxx...
DATABASE_ID=xxx...
OPENAI_API_KEY=sk-xxx...
DB_PASSWORD=your_secure_password
```

---

## Kubernetes 部署

### 高可用部署（可选）

#### 创建命名空间

```bash
kubectl create namespace cnsh
```

#### 部署文件

```yaml
# cnsh-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cnsh-translator
  namespace: cnsh
  labels:
    app: cnsh-translator
spec:
  replicas: 2
  selector:
    matchLabels:
      app: cnsh-translator
  template:
    metadata:
      labels:
        app: cnsh-translator
    spec:
      containers:
      - name: translator
        image: cnsh-translator:v1.0
        imagePullPolicy: IfNotPresent
        env:
        - name: NOTION_TOKEN
          valueFrom:
            secretKeyRef:
              name: cnsh-secrets
              key: notion-token
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: cnsh-secrets
              key: openai-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          exec:
            command:
            - python
            - -c
            - "import sys; sys.exit(0)"
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: cnsh-translator-service
  namespace: cnsh
spec:
  selector:
    app: cnsh-translator
  ports:
  - protocol: TCP
    port: 8000
    targetPort: 8000
  type: LoadBalancer
```

#### 创建 Secret

```bash
# 创建 Secret 存储敏感信息
kubectl create secret generic cnsh-secrets \
  --from-literal=notion-token=sk_live_xxx... \
  --from-literal=openai-key=sk-xxx... \
  -n cnsh
```

#### 部署

```bash
# 应用部署
kubectl apply -f cnsh-deployment.yaml

# 查看部署状态
kubectl get deployments -n cnsh
kubectl get pods -n cnsh

# 查看日志
kubectl logs -f -n cnsh deployment/cnsh-translator

# 扩展副本
kubectl scale deployment cnsh-translator --replicas=3 -n cnsh
```

---

## 配置指南

### 环境变量详解

#### 必填项

| 变量名 | 说明 | 示例 |
|-------|------|------|
| `NOTION_TOKEN` | Notion Integration Token | `sk_live_xxx...` |
| `DATABASE_ID` | Notion 数据库 ID | `abc123xyz...` |
| `OPENAI_API_KEY` | OpenAI API 密钥 | `sk-xxx...` |

#### 可选项

| 变量名 | 默认值 | 说明 |
|-------|-------|------|
| `OPENAI_MODEL` | `gpt-4` | 翻译模型 |
| `LOG_LEVEL` | `INFO` | 日志级别 |
| `WORKER_PROCESSES` | `4` | 工作进程数 |
| `MAX_CONCURRENT_TASKS` | `5` | 最大并发数 |
| `QUEUE_SCAN_INTERVAL` | `5` | 队列扫描间隔（秒） |

### 获取 Notion Token

1. 访问 https://www.notion.com/my-integrations
2. 点击「Create new integration」
3. 命名并创建
4. 复制「Internal Integration Token」
5. 在 Notion 数据库中授予访问权限（Share → Add connection）

### 获取 OpenAI API Key

1. 访问 https://platform.openai.com/api-keys
2. 创建新的 API Key
3. 复制并保存到 `.env`

---

## 使用指南

### 命令参考

```bash
# 启动系统
./start_cnsh.sh start

# 停止系统
./start_cnsh.sh stop

# 重启系统
./start_cnsh.sh restart

# 查看状态
./start_cnsh.sh status

# 实时日志
./start_cnsh.sh logs

# 帮助
./start_cnsh.sh help
```

### 工作流程

```
1. Notion 看板添加新任务
   ↓
2. 系统自动扫描（每 5 秒）
   ↓
3. AI 翻译处理
   ↓
4. 质量评分
   ↓
5. 自动发布（≥95 分）或人工校对（<95 分）
   ↓
6. 完成·写回 Notion
```

### 手动翻译任务

```python
from cnsh_translator_complete import CNSHTranslationSystem, Language

# 初始化系统
system = CNSHTranslationSystem()

# 创建翻译任务
task = system.manager.create_task(
    "Hello, World!",
    Language.ENGLISH,
    Language.CHINESE
)

# 自动翻译
system.manager.auto_translate_task(task.task_id)

# 查看结果
print(f"翻译结果: {task.translated_text}")
print(f"DNA签名: {task.dna_signature}")
```

---

## 故障排查

### 常见问题

#### Q1: Notion 连接失败

```
错误: ❌ Failed to connect to Notion
```

**解决方案**：
- 检查 `NOTION_TOKEN` 是否正确
- 确保数据库在 Notion 中授予了 Integration 访问权限
- 重启系统：`./start_cnsh.sh restart`

#### Q2: OpenAI API 错误

```
错误: ❌ OpenAI API Error: Invalid API key
```

**解决方案**：
- 检查 API Key 是否正确
- 确认 API 配额充足
- 检查网络连接

#### Q3: 队列堆积

```
症状: 任务不断增加，不见减少
```

**解决方案**：
- 增加 `WORKER_PROCESSES`
- 减少 `MAX_CONCURRENT_TASKS`
- 检查 API 配额和速率限制

#### Q4: 系统崩溃

```
错误: ❌ 系统已崩溃
```

**解决方案**：
```bash
# 查看详细错误
tail -50 ~/.cnsh/logs/cnsh_translator.log

# 重启系统
./start_cnsh.sh stop && sleep 2 && ./start_cnsh.sh start

# 清理日志
rm ~/.cnsh/logs/*.log
```

### 日志分析

```bash
# 查看最近错误
grep "ERROR" ~/.cnsh/logs/cnsh_translator.log | tail -20

# 查看性能统计
grep "统计" ~/.cnsh/logs/cnsh_translator.log

# 导出日志用于分析
tar -czf cnsh_logs_$(date +%Y%m%d).tar.gz ~/.cnsh/logs/
```

---

## 维护和升级

### 定期维护

#### 日志轮转

```bash
# 自动轮转日志（Linux）
sudo cat > /etc/logrotate.d/cnsh-translator << EOF
/home/*/.cnsh/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
EOF
```

#### 定期备份

```bash
# 每周备份 Notion 数据库
0 2 * * 0 ~/.cnsh/backup/backup_notion.sh
```

### 版本升级

#### v1.0 → v1.1

```bash
# 1. 备份数据
cp -r ~/.cnsh/logs ~/.cnsh/logs.backup

# 2. 停止系统
./start_cnsh.sh stop

# 3. 更新代码
git pull origin main

# 4. 更新依赖
pip install -r requirements_cnsh.txt --upgrade

# 5. 运行迁移（如有）
python migrate_v1.0_to_v1.1.py

# 6. 重启系统
./start_cnsh.sh start

# 7. 验证
./start_cnsh.sh status
```

---

## 性能优化

### 缓存优化

```env
# 启用 Redis 缓存以提高性能
CACHE_TYPE=redis
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 并发优化

```env
# 根据 CPU 核心数调整
WORKER_PROCESSES=8
MAX_CONCURRENT_TASKS=10
```

### 数据库优化

```env
# 使用 PostgreSQL 替代 SQLite
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql://user:password@localhost:5432/cnsh_db
```

---

## 最终检查清单

- [ ] Python 3.8+ 已安装
- [ ] 虚拟环境已创建
- [ ] 依赖已安装
- [ ] .env 文件已配置
- [ ] Notion Integration Token 已获取
- [ ] OpenAI API Key 已获取
- [ ] 日志目录已创建
- [ ] 系统已启动
- [ ] 日志正常输出
- [ ] Notion 数据库已连接
- [ ] AI 翻译引擎正常工作

---

## 支持和反馈

- **文档**: https://docs.cnsh.local
- **问题**: GitHub Issues
- **讨论**: GitHub Discussions
- **邮件**: support@cnsh.local

---

**DNA**: `#龍芯⚡️2026-05-27-CNSH-DEPLOYMENT-GUIDE-COMPLETE`
**创建时间**: 2026-05-27
**版本**: v1.0
**作者**: UID9622 诸葛鑫
