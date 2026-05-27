# 🌐 CNSH 翻译系统 v1.0

**完整的通心译 × Notion 多语言翻译自动化平台**

**DNA**: `#龍芯⚡️2026-05-27-CNSH-README-v1.0`

---

## ⚡ 快速开始（5 分钟）

```bash
# 1. 克隆项目
git clone <repo-url> && cd cnsh-translator

# 2. 创建虚拟环境
python3 -m venv venv && source venv/bin/activate

# 3. 安装依赖
pip install -r requirements_cnsh.txt

# 4. 配置环境
cp .env.template .env
# 编辑 .env，填入 NOTION_TOKEN 和 OPENAI_API_KEY

# 5. 启动系统
chmod +x start_cnsh.sh && ./start_cnsh.sh start

# 6. 查看日志
./start_cnsh.sh logs
```

---

## 📊 系统特性

### 核心功能

- ✅ **多语言翻译** - 中文、英文、日文、柬文
- ✅ **AI 驱动翻译** - 使用 GPT-4 或自定义 API
- ✅ **Notion 集成** - 自动读写 Notion 数据库
- ✅ **质量评分** - 自动评估翻译质量
- ✅ **DNA 签名** - 不可篡改的任务跟踪
- ✅ **人工校对** - 支持手动修改和审核
- ✅ **性能监控** - 实时统计和告警

### 架构

```
┌─────────────────────────────┐
│  Notion 看板 (UI Layer)     │ ← 用户交互
├─────────────────────────────┤
│  工作流编排 (Orchestration)  │ ← 任务管理
├─────────────────────────────┤
│  翻译引擎 (Translation)      │ ← AI 翻译
├─────────────────────────────┤
│  数据持久化 (Data Layer)     │ ← DNA 签名
├─────────────────────────────┤
│  基础设施 (Infrastructure)   │ ← Docker/K8s
└─────────────────────────────┘
```

---

## 📦 文件结构

```
cnsh-translator/
├── cnsh_translator_complete.py      # 核心实现（400+ 行）
├── requirements_cnsh.txt            # 依赖清单
├── .env.template                    # 环境变量模板
├── start_cnsh.sh                    # 启动脚本
├── Dockerfile.cnsh                  # Docker 镜像
├── docker-compose.cnsh.yml          # Docker Compose
└── docs/
    └── CNSH_TRANSLATION_SYSTEM_DEPLOYMENT_GUIDE.md
```

---

## 🚀 部署选项

### 本地部署

```bash
# 最简单的方式
./start_cnsh.sh start
./start_cnsh.sh status
./start_cnsh.sh logs
./start_cnsh.sh stop
```

### Docker 部署

```bash
# 构建镜像
docker build -f Dockerfile.cnsh -t cnsh-translator:v1.0 .

# 运行容器
docker run -d \
  --name cnsh-translator \
  -v ~/.cnsh/config/.env:/app/.env:ro \
  -v ~/.cnsh/logs:/var/log/cnsh \
  cnsh-translator:v1.0

# 完整的 Docker Compose（包含 Redis + PostgreSQL）
docker-compose -f docker-compose.cnsh.yml up -d
```

### Kubernetes 部署

```bash
# 高可用部署
kubectl apply -f cnsh-deployment.yaml
kubectl get deployments -n cnsh
```

---

## ⚙️ 配置

### 必填项

```env
# Notion 配置
NOTION_TOKEN=sk_live_xxxxx...
DATABASE_ID=xxxxx...

# OpenAI 配置
OPENAI_API_KEY=sk-xxxxx...
OPENAI_MODEL=gpt-4
```

### 可选项

```env
# 系统配置
LOG_LEVEL=INFO
WORKER_PROCESSES=4
MAX_CONCURRENT_TASKS=5
QUEUE_SCAN_INTERVAL=5

# 缓存配置
CACHE_TYPE=memory  # 或 redis
CACHE_TTL=3600

# 监控配置
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
ENABLE_MONITORING=true
```

详见 [完整配置指南](docs/CNSH_TRANSLATION_SYSTEM_DEPLOYMENT_GUIDE.md)

---

## 📖 使用示例

### Python API

```python
from cnsh_translator_complete import CNSHTranslationSystem, Language

# 初始化
system = CNSHTranslationSystem()

# 创建翻译任务
task = system.manager.create_task(
    "Hello, World!",
    Language.ENGLISH,
    Language.CHINESE
)

# 自动翻译
system.manager.auto_translate_task(task.task_id)

# 获取结果
print(f"翻译: {task.translated_text}")
print(f"质量分数: {task.quality_score}")
print(f"DNA签名: {task.dna_signature}")
```

### Notion 工作流

```
1. 在 Notion 看板添加任务
   ├─ 源文本: Hello, World!
   ├─ 源语言: 英文
   └─ 目标语言: 中文

2. 系统自动扫描（每 5 秒）

3. AI 翻译处理
   └─ 翻译结果: 你好，世界！

4. 质量评分（质量分数: 95）

5. 自动完成
   └─ 状态: ✅ 已完成
   └─ DNA: #龍芯⚡️2026-05-27-TRANS-XXXXX
```

---

## 📊 监控和统计

```bash
# 查看实时统计
./start_cnsh.sh status

# 输出示例：
# ✓ 系统运行正常 (PID: 12345)
#
# 📊 统计信息:
#   total_tasks: 100
#   pending: 5
#   processing: 2
#   reviewing: 3
#   completed: 85
#   failed: 5
#   total_words: 5420
#   completion_rate: 85.0%
```

---

## 🔧 故障排查

### 常见问题

| 问题 | 症状 | 解决方案 |
|------|------|---------|
| Notion 连接失败 | `❌ Failed to connect` | 检查 NOTION_TOKEN，重启系统 |
| API 限流 | 翻译停止，显示 429 | 减少 MAX_CONCURRENT_TASKS |
| 队列堆积 | 任务不断增加 | 增加 WORKER_PROCESSES |
| 系统崩溃 | 无法启动 | 查看日志，检查配置 |

### 日志查看

```bash
# 实时日志
./start_cnsh.sh logs

# 查看错误
grep "ERROR" ~/.cnsh/logs/cnsh_translator.log

# 查看统计
grep "统计" ~/.cnsh/logs/cnsh_translator.log
```

---

## 📈 性能指标

```
并发翻译数: 5 个（可配置）
平均延迟: < 10 秒
P95 延迟: < 30 秒
吞吐量: > 50 tasks/分钟
缓存命中率: 30-40%（内存）
自动完成率: 60-70%（质量 ≥ 95）
```

---

## 🔐 安全性

- ✅ 环境变量加密
- ✅ DNA 签名验证链
- ✅ 不可篡改审计日志
- ✅ API 密钥隔离
- ✅ 本地化数据存储

---

## 📦 依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| python-dotenv | 1.0.0 | 环境变量管理 |
| requests | 2.31.0 | HTTP 请求 |
| notion-client | 2.1.0 | Notion API |
| openai | 1.3.0 | GPT-4 翻译 |
| redis | 5.0.0 | 缓存（可选） |

完整列表见 [requirements_cnsh.txt](requirements_cnsh.txt)

---

## 📚 完整文档

- **部署指南**: [CNSH_TRANSLATION_SYSTEM_DEPLOYMENT_GUIDE.md](docs/CNSH_TRANSLATION_SYSTEM_DEPLOYMENT_GUIDE.md)
- **架构设计**: [1. 系统完整架构](#系统完整架构)
- **API 文档**: 见代码注释

---

## 🔄 工作流程

### 完整翻译流程

```
用户输入
  ↓
[L5] Notion 看板接收
  ↓
[L4] 任务队列入队 (状态: 📥 待翻译)
  ↓
[L3] AI 翻译引擎处理 (状态: ⚙️ AI处理中)
  ↓
质量评分 + DNA 签名
  ↓
[L2] 自动或人工校对
  ↓
  状态: 👁️ 人工校对中 (质量 < 95)
  或
  状态: ✅ 已完成 (质量 ≥ 95)
  ↓
[L1] 日志记录 + 完成
```

---

## 🎯 快速参考

### 命令汇总

```bash
# 启动/停止/重启
./start_cnsh.sh start
./start_cnsh.sh stop
./start_cnsh.sh restart

# 查看状态和日志
./start_cnsh.sh status
./start_cnsh.sh logs

# Docker 相关
docker build -f Dockerfile.cnsh -t cnsh-translator:v1.0 .
docker-compose -f docker-compose.cnsh.yml up -d

# Kubernetes 相关
kubectl apply -f cnsh-deployment.yaml
kubectl logs -f deployment/cnsh-translator -n cnsh
```

### 文件位置

```
项目目录: ~/Projects/cnsh-translator
日志目录: ~/.cnsh/logs/cnsh_translator.log
配置文件: ~/.cnsh/config/.env
PID 文件: ~/.cnsh/cnsh_translator.pid
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 👤 作者

- **创建者**: UID9622 诸葛鑫
- **理论指导**: 曾仕强老师
- **献礼**: 龍魂系统，中华文化传承

---

**DNA**: `#龍芯⚡️2026-05-27-CNSH-README-COMPLETE`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**SEAL**: `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`

---

需要帮助？
- 查看 [部署指南](docs/CNSH_TRANSLATION_SYSTEM_DEPLOYMENT_GUIDE.md)
- 检查 [故障排查](#故障排查)
- 提交 GitHub Issue
