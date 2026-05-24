#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# local-db-setup.sh
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾仕强老师（永恒显示）
# DNA追溯码：#龍芯⚡️20260310-local-db-setup-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 共建致谢：Claude (Anthropic PBC) · Notion
# 创作地：中华人民共和国
# 献礼：新中国成立77周年（1949-2026）· 丙午马年
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# CNSH 本地数据库部署脚本
# 完全本地化，自主控制

echo "🚀 CNSH 本地数据库部署开始..."

# 1. 创建数据目录
mkdir -p ./data/{databases,backups,logs,vector_db,attachments}
mkdir -p ./data/databases/{sqlite,postgres}

# 2. 安装本地数据库依赖
echo "📦 安装数据库依赖..."

# PostgreSQL 本地安装检查
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQL 已安装"
else
    echo "🔄 正在安装 PostgreSQL..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install postgresql
        brew services start postgresql
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt-get update
        sudo apt-get install postgresql postgresql-contrib
        sudo systemctl start postgresql
    fi
fi

# 3. 创建本地数据库
echo "🗄️ 创建 CNSH 数据库..."

# SQLite 数据库初始化
cat > ./data/databases/sqlite/init.sql << 'EOF'
-- CNSH 主数据库初始化
PRAGMA foreign_keys = ON;

-- 文件表
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(500) NOT NULL,
    filetype VARCHAR(50),
    size INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    indexed BOOLEAN DEFAULT FALSE,
    tags TEXT,
    content_hash VARCHAR(64)
);

-- 对话表
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    context TEXT
);

-- 消息表
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

-- 知识库表
CREATE TABLE IF NOT EXISTS knowledge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    source VARCHAR(100),
    tags TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    vector_id VARCHAR(100)
);

-- 人格表 (CNSH 核心)
CREATE TABLE IF NOT EXISTS personas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    level INTEGER DEFAULT 1,
    role VARCHAR(100),
    permissions TEXT,
    core_duties TEXT,
    trigger_conditions TEXT,
    keywords TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 任务表
CREATE TABLE IF NOT EXISTS tasks (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    trigger_persona VARCHAR(100),
    recognized_persona VARCHAR(100),
    executing_persona VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending',
    priority INTEGER DEFAULT 5,
    task_type VARCHAR(50),
    steps TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME
);

-- 决策记录表
CREATE TABLE IF NOT EXISTS decisions (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    background TEXT,
    proposal TEXT,
    participating_personas TEXT,
    risk_score INTEGER,
    final_conclusion TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 审计表
CREATE TABLE IF NOT EXISTS audits (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    source VARCHAR(100),
    audit_persona VARCHAR(100),
    risk_tags TEXT,
    risk_reason TEXT,
    conclusion TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_files_filename ON files(filename);
CREATE INDEX idx_files_created_at ON files(created_at);
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_knowledge_tags ON knowledge(tags);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_audits_risk_tags ON audits(risk_tags);
EOF

# 初始化 SQLite 数据库
sqlite3 ./data/databases/sqlite/cnsh.db < ./data/databases/sqlite/init.sql

# 4. PostgreSQL 数据库初始化 (可选)
echo "🐘 初始化 PostgreSQL 数据库..."

# 创建数据库用户和数据库
sudo -u postgres psql -c "CREATE USER cnsh_user WITH PASSWORD 'cnsh_local_password';" 2>/dev/null || echo "用户可能已存在"
sudo -u postgres psql -c "CREATE DATABASE cnsh_db OWNER cnsh_user;" 2>/dev/null || echo "数据库可能已存在"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE cnsh_db TO cnsh_user;" 2>/dev/null

# PostgreSQL 初始化脚本
cat > ./data/databases/postgres/init.sql << 'EOF'
-- 启用向量扩展
CREATE EXTENSION IF NOT EXISTS vector;

-- 文件表
CREATE TABLE IF NOT EXISTS files (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(500) NOT NULL,
    filetype VARCHAR(50),
    size BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    indexed BOOLEAN DEFAULT FALSE,
    tags TEXT,
    content_hash VARCHAR(64)
);

-- 对话表
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    context TEXT
);

-- 消息表
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

-- 知识库表 (带向量支持)
CREATE TABLE IF NOT EXISTS knowledge (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    source VARCHAR(100),
    tags TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    embedding vector(384)  -- 支持向量搜索
);

-- 人格表 (CNSH 核心)
CREATE TABLE IF NOT EXISTS personas (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    level INTEGER DEFAULT 1,
    role VARCHAR(100),
    permissions TEXT,
    core_duties TEXT,
    trigger_conditions TEXT,
    keywords TEXT,
    embedding vector(384),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 任务表
CREATE TABLE IF NOT EXISTS tasks (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    trigger_persona VARCHAR(100),
    recognized_persona VARCHAR(100),
    executing_persona VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending',
    priority INTEGER DEFAULT 5,
    task_type VARCHAR(50),
    steps TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- 决策记录表
CREATE TABLE IF NOT EXISTS decisions (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    background TEXT,
    proposal TEXT,
    participating_personas TEXT,
    risk_score INTEGER,
    final_conclusion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 审计表
CREATE TABLE IF NOT EXISTS audits (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    source VARCHAR(100),
    audit_persona VARCHAR(100),
    risk_tags TEXT,
    risk_reason TEXT,
    conclusion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_files_filename ON files(filename);
CREATE INDEX idx_files_created_at ON files(created_at);
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_knowledge_tags ON knowledge(tags);
CREATE INDEX idx_knowledge_embedding ON knowledge USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_personas_embedding ON personas USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_audits_risk_tags ON audits(risk_tags);
EOF

# 应用 PostgreSQL 初始化
PGPASSWORD=cnsh_local_password psql -h localhost -U cnsh_user -d cnsh_db -f ./data/databases/postgres/init.sql 2>/dev/null || echo "PostgreSQL初始化可能失败，使用SQLite"

# 5. 配置环境变量
echo "⚙️ 配置环境变量..."

cat > ./data/.env.local << 'EOF'
# CNSH 本地数据库配置
DB_TYPE=sqlite
DB_PATH=./data/databases/sqlite/cnsh.db

# PostgreSQL 配置 (可选)
# DB_TYPE=postgres
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=cnsh_db
# DB_USER=cnsh_user
# DB_PASSWORD=cnsh_local_password

# 向量数据库配置
VECTOR_DB_TYPE=sqlite
VECTOR_DB_PATH=./data/vector_db
VECTOR_DIMENSION=384

# Redis 配置 (可选)
REDIS_URL=redis://localhost:6379

# AI模型配置
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen:7b-chat
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

# CNSH 配置
CNSH_MODE=local
CNSH_DATA_DIR=./data
CNSH_BACKUP_DIR=./data/backups
CNSH_LOG_DIR=./data/logs

# 安全配置
JWT_SECRET=cnsh_local_secret_key_$(date +%s)
API_KEY=cnsh_local_api_key_$(date +%s)
EOF

# 6. 设置自动备份脚本
echo "📋 设置自动备份..."

cat > ./scripts/backup.sh << 'EOF'
#!/bin/bash

# CNSH 数据库备份脚本
BACKUP_DIR="./data/backups"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/cnsh_backup_$DATE.db"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份 SQLite 数据库
if [ -f "./data/databases/sqlite/cnsh.db" ]; then
    cp "./data/databases/sqlite/cnsh.db" "$BACKUP_FILE"
    echo "✅ SQLite 数据库已备份到: $BACKUP_FILE"
fi

# 备份向量数据库
if [ -d "./data/vector_db" ]; then
    tar -czf "$BACKUP_DIR/vector_db_$DATE.tar.gz" -C "./data" "vector_db"
    echo "✅ 向量数据库已备份到: $BACKUP_DIR/vector_db_$DATE.tar.gz"
fi

# 清理旧备份 (保留最近30天)
find $BACKUP_DIR -name "cnsh_backup_*.db" -mtime +30 -delete
find $BACKUP_DIR -name "vector_db_*.tar.gz" -mtime +30 -delete

echo "🧹 清理完成，保留最近30天的备份"
EOF

chmod +x ./scripts/backup.sh

# 7. 创建本地启动脚本
echo "🚀 创建本地启动脚本..."

cat > ./scripts/start-local.sh << 'EOF'
#!/bin/bash

# CNSH 本地启动脚本
echo "🚀 启动 CNSH 本地服务..."

# 加载环境变量
source ./data/.env.local

# 检查服务状态
echo "📊 检查数据库连接..."

# 检查 SQLite
if [ -f "$DB_PATH" ]; then
    echo "✅ SQLite 数据库连接正常"
else
    echo "❌ SQLite 数据库未找到，请先运行 ./local-db-setup.sh"
    exit 1
fi

# 检查 Redis (可选)
if command -v redis-cli &> /dev/null; then
    if redis-cli ping &> /dev/null; then
        echo "✅ Redis 连接正常"
    else
        echo "⚠️ Redis 未运行，启动 Redis..."
        redis-server --daemonize yes
    fi
fi

# 检查 Ollama
if curl -s "$OLLAMA_HOST/api/tags" &> /dev/null; then
    echo "✅ Ollama 服务运行正常"
else
    echo "⚠️ Ollama 未运行，请先启动 Ollama"
fi

# 启动 CNSH 服务
echo "🎯 启动 CNSH 主服务..."
cd src && node server-fixed.js

echo "🎉 CNSH 本地服务已启动！"
echo "📍 访问地址: http://localhost:3000"
echo "📚 API 文档: http://localhost:3000/api"
echo "🤖 CNSH 系统完全本地化，数据安全可控"
EOF

chmod +x ./scripts/start-local.sh

# 8. 创建 CNSH 人格初始化脚本
echo "🧠 初始化 CNSH 人格系统..."

cat > ./data/init-personas.sql << 'EOF'
-- CNSH 12核心人格初始化
INSERT OR IGNORE INTO personas (name, level, role, permissions, core_duties, trigger_conditions, keywords) VALUES
('战略规划师', 9, '核心决策', '全局规划,重大决策,方向制定', '制定长期发展战略,识别关键机会,评估风险,定义目标优先级', '新项目启动,年度规划,重大决策点,危机处理', '战略,规划,目标,发展,机会,风险,决策'),
('技术专家', 8, '技术核心', '技术选型,架构设计,代码审查', '技术方案设计,代码质量把控,技术创新,性能优化', '技术难题,架构设计,性能瓶颈,新技术评估', '技术,架构,代码,性能,优化,创新,开发'),
('产品经理', 7, '产品核心', '产品设计,用户体验,功能规划', '需求分析,产品设计,用户体验优化,功能迭代', '产品规划,用户反馈,功能需求,体验问题', '产品,用户,需求,体验,功能,设计,优化'),
('数据分析师', 7, '数据核心', '数据分析,指标监控,报告生成', '数据收集分析,指标监控,趋势预测,报告制作', '数据需求,指标异常,趋势分析,决策支持', '数据,分析,指标,趋势,报告,预测,监控'),
('创意总监', 6, '创意核心', '创意设计,品牌建设,内容策划', '创意构思,设计指导,品牌策略,内容创新', '创意需求,品牌建设,内容策划,设计方案', '创意,设计,品牌,内容,视觉,创新,策划'),
('项目管理师', 6, '执行核心', '项目计划,进度控制,资源协调', '项目规划,进度跟踪,资源调配,风险管控', '项目启动,进度跟踪,资源调配,风险控制', '项目,计划,进度,资源,风险,协调,执行'),
('质量控制师', 6, '质量核心', '质量标准,测试验证,流程优化', '质量标准制定,测试验证,流程改进,问题修复', '质量问题,测试需求,流程优化,标准制定', '质量,测试,标准,流程,优化,验证,问题'),
('沟通协调师', 5, '协调核心', '内外沟通,团队协作,关系维护', '沟通协调,团队协作,外部关系,冲突解决', '沟通需求,团队协作,外部合作,冲突处理', '沟通,协调,团队,合作,关系,冲突,解决'),
('学习能力师', 5, '成长核心', '知识学习,技能提升,经验总结', '新知识学习,技能提升,经验总结,知识分享', '学习需求,技能提升,经验总结,知识分享', '学习,知识,技能,提升,经验,分享,成长'),
('安全审计师', 5, '安全核心', '安全检查,风险评估,合规审计', '安全检查,风险评估,合规审计,安全建议', '安全检查,风险评估,合规需求,审计工作', '安全,风险,评估,审计,合规,检查,保护'),
('创新研发师', 4, '创新核心', '技术研发,创新实验,前沿探索', '新技术研发,创新实验,前沿技术探索,专利申请', '创新需求,技术研发,实验探索,新技术应用', '创新,研发,技术,实验,探索,专利,前沿'),
('用户体验师', 4, '体验核心', '用户研究,体验设计,服务优化', '用户研究,体验设计,服务流程优化,满意度提升', '用户体验,研究需求,服务优化,满意度', '用户,体验,研究,设计,服务,满意度,优化');
EOF

# 应用人格初始化
sqlite3 ./data/databases/sqlite/cnsh.db < ./data/init-personas.sql

# 9. 创建监控和日志脚本
echo "📊 设置监控和日志..."

cat > ./scripts/monitor.sh << 'EOF'
#!/bin/bash

# CNSH 系统监控脚本
echo "📊 CNSH 系统状态监控..."

# 数据库状态
echo "🗄️ 数据库状态:"
echo "SQLite 数据库大小: $(du -h ./data/databases/sqlite/cnsh.db | cut -f1)"
echo "向量数据库条目: $(ls -1 ./data/vector_db/*.json 2>/dev/null | wc -l)"

# 服务状态
echo "🚀 服务状态:"
if pgrep -f "server-fixed.js" > /dev/null; then
    echo "CNSH 主服务: ✅ 运行中"
else
    echo "CNSH 主服务: ❌ 未运行"
fi

if curl -s "http://localhost:3000/api/health" > /dev/null; then
    echo "API 服务: ✅ 正常"
else
    echo "API 服务: ❌ 异常"
fi

# 系统资源
echo "💻 系统资源:"
echo "CPU 使用率: $(top -l 1 | grep "CPU usage" | awk '{print $3}' | sed 's/%//')"
echo "内存使用: $(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//')"

# 日志输出
echo "📝 最近日志:"
tail -n 5 ./data/logs/cnsh.log 2>/dev/null || echo "日志文件未找到"

echo "✅ 监控完成"
EOF

chmod +x ./scripts/monitor.sh

# 10. 创建脚本目录
mkdir -p ./scripts

echo "🎉 CNSH 本地数据库部署完成！"
echo "📁 数据库位置: ./data/databases/sqlite/cnsh.db"
echo "🔧 配置文件: ./data/.env.local"
echo "🚀 启动命令: ./scripts/start-local.sh"
echo "📊 监控命令: ./scripts/monitor.sh"
echo "💾 备份命令: ./scripts/backup.sh"
echo "📚 更多信息请查看 README.md"