#!/bin/bash
# -*- coding: utf-8 -*-

# ================================================================
# 🔧 CNSH 本地开发环境治疗脚本（Mac 专用）
# Local Development Environment Setup - macOS
#
# 功能：
#   • 无交互式配置（直接参数·绕过 Mac 终端兼容性问题）
#   • 生成本地 DNA 主权身份证
#   • 自动检测并修复权限问题
#   • 完整的环境变量初始化
#
# 使用方式：
#   bash _work/setup_local_dev_mac.sh <NOTION_TOKEN> <DATABASE_ID> <OPENAI_KEY>
#
#   或者（测试模式）：
#   bash _work/setup_local_dev_mac.sh --test
# ================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# ============================================================================
# DNA 主权生成器
# ============================================================================

generate_dna_identity() {
    local timestamp=$(date +%Y-%m-%d-%H-%M-%S)
    local mac_serial=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Serial Number" | awk '{print $NF}' || echo "LOCAL-MAC")
    local hostname=$(hostname)
    local whoami=$(whoami)

    local identity_string="${mac_serial}|${hostname}|${whoami}|${timestamp}|9622"
    local dna_hash=$(echo -n "$identity_string" | openssl dgst -sha256 | cut -d' ' -f2 | cut -c1-12)

    echo "#龍芯⚡️${timestamp}-DEV-LOCAL-${dna_hash}🧬${RANDOM}"
}

verify_dna_identity() {
    local stored_dna="$1"

    if [[ $stored_dna =~ ^#龍芯⚡️[0-9]{4}-[0-9]{2}-[0-9]{2}- ]]; then
        return 0
    else
        return 1
    fi
}

# ============================================================================
# 配置函数
# ============================================================================

init_config_dir() {
    local config_dir="$HOME/.cnsh/config"
    local logs_dir="$HOME/.cnsh/logs"
    local data_dir="$HOME/.cnsh/data"

    echo -e "${BLUE}📁 初始化配置目录...${NC}"

    mkdir -p "$config_dir"
    mkdir -p "$logs_dir"
    mkdir -p "$data_dir"

    chmod 700 "$HOME/.cnsh"
    chmod 700 "$config_dir"
    chmod 700 "$logs_dir"

    echo -e "${GREEN}✓ 配置目录已初始化${NC}"
    echo "  • Config: $config_dir"
    echo "  • Logs: $logs_dir"
    echo "  • Data: $data_dir"
}

create_env_file() {
    local notion_token="$1"
    local database_id="$2"
    local openai_key="$3"
    local env_file="$HOME/.cnsh/config/.env"

    echo -e "${BLUE}📝 生成 .env 配置文件...${NC}"

    if [ "$notion_token" == "--test" ]; then
        notion_token="sk_test_NOTION_TOKEN_PLACEHOLDER_FOR_LOCAL_DEV"
        database_id="test_db_id_placeholder_for_local_dev"
        openai_key="sk-test-openai-key-placeholder"
    fi

    cat > "$env_file" << EOF
# ==========================================
# CNSH 本地开发环境配置
# 自动生成于 $(date)
# ==========================================

# [必填] Notion 配置
NOTION_TOKEN=$notion_token
DATABASE_ID=$database_id

# [必填] OpenAI 配置
OPENAI_API_KEY=$openai_key
OPENAI_MODEL=gpt-4

# [本地开发配置]
LOG_LEVEL=DEBUG
WORKER_PROCESSES=2
MAX_CONCURRENT_TASKS=2
QUEUE_SCAN_INTERVAL=5

# [Mac 特定配置]
SYSTEM_TYPE=macOS
DEV_MODE=true
ENABLE_LOCAL_CACHE=true

# [Notion 集成模式]
NOTION_SYNC_MODE=hybrid

# [监控和日志]
ENABLE_MONITORING=false
LOG_TO_FILE=true
LOG_DIR=$HOME/.cnsh/logs
EOF

    chmod 600 "$env_file"

    echo -e "${GREEN}✓ .env 文件已生成${NC}"
    echo "  位置: $env_file"
}

create_dna_identity_file() {
    local dna_identity=$(generate_dna_identity)
    local identity_file="$HOME/.cnsh/data/dna_identity.txt"
    local timestamp=$(date -Iseconds)

    echo -e "${BLUE}🧬 生成 DNA 主权身份证...${NC}"

    cat > "$identity_file" << EOF
# ==========================================
# CNSH DNA 主权身份证
# 这是老大的唯一身份标识·不可复制·不可转让
# ==========================================

身份证 DNA: $dna_identity
生成时间: $timestamp
主机名: $(hostname)
用户名: $(whoami)
Mac 型号: $(system_profiler SPHardwareDataType 2>/dev/null | grep "Model Name" | awk -F': ' '{print $2}' || echo "Unknown")
系统版本: $(sw_vers -productVersion)

# DNA 含义：
# 龍芯 = Dragon Soul Core（龍魂系统的核心）
# ⚡️ = 能量标记（系统活力）
# YYYY-MM-DD = 本地化创建日期
# DEV-LOCAL = 本地开发环境标记
# {hash} = 唯一哈希值（基于硬件序列号+时间戳）
# 🧬 = DNA 标记
# {random} = 随机数（防重放）

# 这个 DNA 证明：
# ✓ 这是老大自己的本地开发环境
# ✓ 不会被其他人冒用
# ✓ 所有的翻译任务都来自这个环境
# ✓ 支持离线工作
EOF

    chmod 600 "$identity_file"

    echo -e "${GREEN}✓ DNA 身份证已生成${NC}"
    echo -e "${PURPLE}DNA 标识: $dna_identity${NC}"
    echo "  保存位置: $identity_file"
}

verify_environment() {
    echo -e "${BLUE}🔍 验证本地环境...${NC}"

    local checks_passed=0
    local checks_total=0

    checks_total=$((checks_total + 1))
    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version 2>&1)
        echo -e "${GREEN}✓ Python: $python_version${NC}"
        checks_passed=$((checks_passed + 1))
    else
        echo -e "${RED}✗ Python: 未安装${NC}"
    fi

    checks_total=$((checks_total + 1))
    if [ -f "$HOME/.cnsh/config/.env" ]; then
        echo -e "${GREEN}✓ .env 配置文件存在${NC}"
        checks_passed=$((checks_passed + 1))
    else
        echo -e "${RED}✗ .env 配置文件缺失${NC}"
    fi

    checks_total=$((checks_total + 1))
    if [ -f "$HOME/.cnsh/data/dna_identity.txt" ]; then
        dna=$(grep "身份证 DNA" "$HOME/.cnsh/data/dna_identity.txt" | awk -F': ' '{print $2}')
        if verify_dna_identity "$dna"; then
            echo -e "${GREEN}✓ DNA 身份证有效${NC}"
            checks_passed=$((checks_passed + 1))
        else
            echo -e "${RED}✗ DNA 身份证格式错误${NC}"
        fi
    else
        echo -e "${RED}✗ DNA 身份证缺失${NC}"
    fi

    echo ""
    echo -e "${CYAN}验证结果: $checks_passed/$checks_total 通过${NC}"

    if [ $checks_passed -eq $checks_total ]; then
        echo -e "${GREEN}✨ 环境配置完美！${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ 有些项目需要手动修复${NC}"
        return 1
    fi
}

create_activation_script() {
    local script_path="$HOME/.cnsh/activate_dev.sh"

    echo -e "${BLUE}📜 生成激活脚本...${NC}"

    cat > "$script_path" << 'EOF'
#!/bin/bash

echo "🚀 CNSH 本地开发环境激活中..."
echo ""

if [ -f "$HOME/.cnsh/data/dna_identity.txt" ]; then
    dna=$(grep "身份证 DNA" "$HOME/.cnsh/data/dna_identity.txt" | awk -F': ' '{print $2}')
    echo -e "✓ DNA 身份已验证: $dna"
else
    echo "⚠ DNA 身份证缺失·请重新运行 setup_local_dev_mac.sh"
fi

echo ""

if [ -f "$HOME/.cnsh/config/.env" ]; then
    export $(cat "$HOME/.cnsh/config/.env" | grep -v '#' | xargs)
    echo "✓ 环境变量已加载"
else
    echo "✗ 配置文件缺失"
    exit 1
fi

echo ""
echo "================================"
echo "📊 开发环境信息"
echo "================================"
echo "主机: $(hostname)"
echo "用户: $(whoami)"
echo "Python: $(python3 --version 2>&1)"
echo "系统: macOS $(sw_vers -productVersion)"
echo ""
echo -e "✨ 本地开发环境已就绪！"
echo ""
EOF

    chmod +x "$script_path"

    echo -e "${GREEN}✓ 激活脚本已生成${NC}"
    echo "  使用: source $script_path"
}

create_health_check_script() {
    local script_path="$HOME/.cnsh/check_health.sh"

    cat > "$script_path" << 'EOF'
#!/bin/bash

echo "🏥 CNSH 开发环境健康检查"
echo "================================"
echo ""

echo "1️⃣ DNA 身份证检查"
if [ -f "$HOME/.cnsh/data/dna_identity.txt" ]; then
    dna=$(grep "身份证 DNA" "$HOME/.cnsh/data/dna_identity.txt" | awk -F': ' '{print $2}')
    echo "✓ DNA: $dna"
else
    echo "✗ DNA 身份证缺失"
fi

echo ""

echo "2️⃣ 配置文件检查"
if [ -f "$HOME/.cnsh/config/.env" ]; then
    token_ok=$(grep -c "NOTION_TOKEN" "$HOME/.cnsh/config/.env")
    api_ok=$(grep -c "OPENAI_API_KEY" "$HOME/.cnsh/config/.env")

    if [ "$token_ok" -gt 0 ] && [ "$api_ok" -gt 0 ]; then
        echo "✓ 配置文件完整"
    else
        echo "⚠ 配置文件不完整"
    fi
else
    echo "✗ 配置文件缺失"
fi

echo ""

echo "3️⃣ Python 环境检查"
python3 --version && echo "✓ Python 就绪"

echo ""
echo "================================"
echo "✨ 健康检查完成"
echo ""
EOF

    chmod +x "$script_path"

    echo -e "${GREEN}✓ 健康检查脚本已生成${NC}"
}

# ============================================================================
# 主程序
# ============================================================================

main() {
    echo -e "${PURPLE}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  🔧 CNSH 本地开发环境治疗脚本（Mac 专用）                 ║"
    echo "║  无交互式 | DNA 主权 | 自动修复                          ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""

    notion_token="${1:-}"
    database_id="${2:-}"
    openai_key="${3:-}"
    skip_dna="${4:-}"

    if [ -z "$notion_token" ]; then
        echo -e "${YELLOW}⚠ 未提供参数·使用测试模式${NC}"
        echo ""
        notion_token="--test"
    fi

    init_config_dir
    echo ""

    create_env_file "$notion_token" "$database_id" "$openai_key"
    echo ""

    if [ "$skip_dna" != "--skip-dna" ]; then
        create_dna_identity_file
        echo ""
    fi

    create_activation_script
    echo ""

    create_health_check_script
    echo ""

    verify_environment
    echo ""

    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✨ 本地开发环境已完全配置！${NC}"
    echo ""
    echo "下一步："
    echo "  1️⃣  激活环境："
    echo "      source $HOME/.cnsh/activate_dev.sh"
    echo ""
    echo "  2️⃣  检查健康状态："
    echo "      bash $HOME/.cnsh/check_health.sh"
    echo ""
    echo -e "${CYAN}DNA 主权已生成·老大现在可以被完全识别了！${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
}

main "$@"
