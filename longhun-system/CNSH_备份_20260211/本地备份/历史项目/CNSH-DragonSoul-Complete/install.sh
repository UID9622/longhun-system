#!/bin/bash

# 🐉 龙魂终端一键安装脚本
# DNA追溯码: #龙芯⚡️2026-01-21-INSTALL-v2.0

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 横幅
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║   🐉 CNSH-DragonSoul-Complete 安装程序                   ║"
echo "║   龙魂终端 + CNSH编辑器 + Notion扩展                     ║"
echo "║                                                          ║"
echo "║   DNA: #龙芯⚡️2026-01-21-INSTALL                         ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# 检测操作系统
print_status "检测操作系统..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
    print_success "检测到 macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
    print_success "检测到 Linux"
else
    print_error "不支持的操作系统: $OSTYPE"
    exit 1
fi

# 检查Python版本
print_status "检查 Python 版本..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 9 ]; then
        print_success "Python $PYTHON_VERSION ✓"
    else
        print_error "需要 Python 3.9+，当前版本: $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "未找到 Python3，请先安装"
    exit 1
fi

# 检查pip
print_status "检查 pip..."
if command -v pip3 &> /dev/null; then
    print_success "pip3 已安装 ✓"
else
    print_warning "pip3 未安装，尝试安装..."
    python3 -m ensurepip --upgrade
fi

# 创建虚拟环境（可选）
print_status "是否创建虚拟环境？(推荐) [Y/n]"
read -r CREATE_VENV

if [[ "$CREATE_VENV" != "n" && "$CREATE_VENV" != "N" ]]; then
    print_status "创建虚拟环境..."
    python3 -m venv .venv
    
    # 激活虚拟环境
    source .venv/bin/activate
    print_success "虚拟环境已创建并激活 ✓"
fi

# 安装Python依赖
print_status "安装 Python 依赖..."
pip3 install -r requirements.txt
print_success "Python 依赖安装完成 ✓"

# 创建必要目录
print_status "创建必要目录..."
mkdir -p ~/.dragonsoul
mkdir -p ~/.dragonsoul/logs
mkdir -p ~/.dragonsoul/backup
print_success "目录创建完成 ✓"

# 创建配置文件
print_status "创建配置文件..."
if [ ! -f "config/config.yaml" ]; then
    mkdir -p config
    cat > config/config.yaml << 'EOF'
# 🐉 龙魂终端配置文件
# DNA: #龙芯⚡️CONFIG

system:
  name: "DragonSoul Terminal"
  version: "2.0"
  owner: "请填写您的用户名"

backends:
  claude:
    enabled: true
    priority: 2
    # api_key: "sk-xxx"  # 请填写您的API Key
    
  deepseek:
    enabled: true
    priority: 3
    # api_key: "sk-xxx"  # 请填写您的API Key
    
  notion:
    enabled: true
    priority: 1
    # api_key: "secret_xxx"  # 请填写您的Notion API Key
    # task_database_id: ""   # 任务数据库ID
    # finance_database_id: ""  # 财务数据库ID

security:
  audit_enabled: true
  dna_tracing: true
  data_encryption: true
  data_sovereignty: "china"

features:
  mac_management: true
  email_automation: false  # 需要额外配置
  finance_tracking: true
  health_monitoring: false  # 需要额外配置
EOF
    print_success "配置文件已创建 ✓"
    print_warning "请编辑 config/config.yaml 填写API密钥"
else
    print_warning "配置文件已存在，跳过"
fi

# 创建环境变量模板
print_status "创建环境变量模板..."
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# 🐉 龙魂终端环境变量
# DNA: #龙芯⚡️ENV

# Claude API
CLAUDE_API_KEY=

# DeepSeek API
DEEPSEEK_API_KEY=

# Notion API
NOTION_API_KEY=
NOTION_TASK_DB=
NOTION_FINANCE_DB=

# 数据主权设置
DATA_SOVEREIGNTY=china
EOF
    print_success "环境变量模板已创建 ✓"
    print_warning "请编辑 .env 文件填写API密钥"
else
    print_warning ".env 文件已存在，跳过"
fi

# 运行测试
print_status "运行安装测试..."
echo ""

# 测试审计引擎
print_status "测试三色审计引擎..."
python3 security-core/audit_engine.py > /dev/null 2>&1 && print_success "三色审计引擎 ✓" || print_warning "三色审计引擎测试失败"

# 测试DNA追溯
print_status "测试DNA追溯系统..."
python3 security-core/dna_tracer.py > /dev/null 2>&1 && print_success "DNA追溯系统 ✓" || print_warning "DNA追溯系统测试失败"

# 测试Mac管理器
print_status "测试Mac管理器..."
python3 dragonsoul-terminal/backend/mac_manager.py > /dev/null 2>&1 && print_success "Mac管理器 ✓" || print_warning "Mac管理器测试失败"

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║   🎉 安装完成！                                          ║"
echo "║                                                          ║"
echo "║   下一步：                                                ║"
echo "║   1. 编辑 config/config.yaml 填写API密钥                 ║"
echo "║   2. 编辑 .env 文件填写环境变量                          ║"
echo "║   3. 运行 python dragonsoul-terminal/backend/main.py     ║"
echo "║                                                          ║"
echo "║   或在 VS Code 中按 Cmd+Shift+B 运行默认任务             ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

print_success "🐉 龙魂终端安装完成！"
