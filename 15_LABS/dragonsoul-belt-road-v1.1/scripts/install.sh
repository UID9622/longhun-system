#!/bin/bash
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 龍魂 · 一带一路入门包 · 一键部署脚本 v1.1
# DNA: #龍芯⚡️丙午·丙申·戊午·戊午·䷱鼎-BELT-ROAD-PACK-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 许可: MulanPSL v2
# 用途: 5分钟完成龍魂系统本地部署，支持Docker/裸机/纯离线三种模式

set -euo pipefail

DRAGONSOUL_VERSION="1.1"
INSTALL_DIR="${DRAGONSOUL_HOME:-$HOME/dragonsoul-belt-road}"
LOG_FILE="/tmp/dragonsoul-install-$(date +%Y%m%d-%H%M%S).log"
MODEL_SIZE="${MODEL_SIZE:-7b}"
LANG="${DRAGONSOUL_LANG:-en}"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[龍魂]${NC} $1" | tee -a "$LOG_FILE"; }
warn() { echo -e "${YELLOW}[警告]${NC} $1" | tee -a "$LOG_FILE"; }
error() { echo -e "${RED}[错误]${NC} $1" | tee -a "$LOG_FILE"; exit 1; }
info() { echo -e "${BLUE}[信息]${NC} $1" | tee -a "$LOG_FILE"; }

# ========== 前置检查 ==========
check_system() {
    log "=== 系统前置检查 ==="

    # CPU 架构
    ARCH=$(uname -m)
    log "CPU架构: $ARCH"
    case "$ARCH" in
        x86_64|amd64) ARCH_TAG="amd64" ;;
        aarch64|arm64) ARCH_TAG="arm64" ;;
        riscv64) ARCH_TAG="riscv64" ;;
        *) warn "不支持的架构: $ARCH，将尝试通用安装" ; ARCH_TAG="generic" ;;
    esac

    # 内存检查
    MEM_KB=$(grep MemTotal /proc/meminfo 2>/dev/null | awk '{print $2}' || echo 0)
    MEM_GB=$((MEM_KB / 1024 / 1024))
    log "内存: ${MEM_GB}GB"
    if [ "$MEM_GB" -lt 4 ]; then
        warn "内存不足4GB，仅支持微型模型(1B-3B)"
        MODEL_SIZE="3b"
    elif [ "$MEM_GB" -lt 8 ]; then
        warn "内存不足8GB，建议使用小型模型(3B-7B)"
        MODEL_SIZE="7b"
    elif [ "$MEM_GB" -lt 16 ]; then
        warn "内存不足16GB，建议使用中型模型(7B-13B)"
        MODEL_SIZE="7b"
    fi

    # 磁盘检查
    if command -v df &>/dev/null; then
        DISK_AVAIL=$(df -BG "$HOME" 2>/dev/null | tail -1 | awk '{print $4}' | sed 's/G//')
        log "可用磁盘: ${DISK_AVAIL:-?}GB"
        if [ "${DISK_AVAIL:-0}" -lt 20 ] 2>/dev/null; then
            error "磁盘空间不足20GB，无法安装"
        fi
    else
        warn "无法检测磁盘空间，请确保至少有20GB可用"
    fi

    # 操作系统
    OS=$(uname -s)
    log "操作系统: $OS"

    # 依赖检查
    if command -v docker &> /dev/null && docker --version &>/dev/null; then
        log "Docker 已安装 ✓"
        HAS_DOCKER=1
    else
        warn "Docker 未安装或不可用，将使用裸机模式"
        HAS_DOCKER=0
    fi

    if command -v python3 &> /dev/null; then
        PY_VER=$(python3 --version 2>/dev/null | awk '{print $2}')
        log "Python: $PY_VER ✓"
        HAS_PYTHON=1
    else
        warn "Python3 未安装，部分功能受限"
        HAS_PYTHON=0
    fi

    if command -v curl &> /dev/null; then
        log "curl 已安装 ✓"
    else
        error "curl 未安装，请先安装 curl"
    fi

    log "前置检查完成 ✓"
}

# ========== 安装模式选择 ==========
select_mode() {
    if [ "${FORCE_MODE:-}" = "docker" ] && [ "$HAS_DOCKER" -eq 1 ]; then
        MODE="docker"
        log "强制使用 Docker Compose 模式"
    elif [ "${FORCE_MODE:-}" = "bare" ]; then
        MODE="bare"
        log "强制使用裸机模式（Ollama）"
    elif [ "${FORCE_MODE:-}" = "offline" ]; then
        MODE="offline"
        log "强制使用纯离线模式（llama.cpp）"
    elif [ "$HAS_DOCKER" -eq 1 ]; then
        MODE="docker"
        log "自动选择 Docker Compose 模式"
    else
        MODE="bare"
        log "自动选择裸机模式（Ollama）"
    fi

    # 离线模式检测
    if [ "${OFFLINE:-0}" -eq 1 ] || ! ping -c 1 -W 5 github.com &>/dev/null; then
        OFFLINE_MODE=1
        warn "离线模式检测：将使用本地缓存/预下载包"
    else
        OFFLINE_MODE=0
    fi
}

# ========== Docker 模式安装 ==========
install_docker() {
    log "=== Docker Compose 安装 ==="
    mkdir -p "$INSTALL_DIR"
    cd "$INSTALL_DIR"

    # 下载编排文件
    if [ "$OFFLINE_MODE" -eq 0 ]; then
        info "下载编排文件..."
        curl -fsSL "https://dragonsoul.dev/releases/v${DRAGONSOUL_VERSION}/docker-compose.yml"             -o docker-compose.yml ||             curl -fsSL "https://raw.githubusercontent.com/dragonsoul/belt-road-pack/v${DRAGONSOUL_VERSION}/docker-compose.quickstart.yml"             -o docker-compose.yml
        curl -fsSL "https://dragonsoul.dev/releases/v${DRAGONSOUL_VERSION}/.env.example"             -o .env.example ||             curl -fsSL "https://raw.githubusercontent.com/dragonsoul/belt-road-pack/v${DRAGONSOUL_VERSION}/.env.example"             -o .env.example
    else
        if [ -f "${OFFLINE_PACKAGE:-/tmp/dragonsoul-offline}/docker-compose.yml" ]; then
            cp "${OFFLINE_PACKAGE:-/tmp/dragonsoul-offline}"/docker-compose.yml .
        else
            error "离线模式：docker-compose.yml 未找到。请设置 OFFLINE_PACKAGE 环境变量指向离线包目录"
        fi
    fi

    # 生成环境配置
    cat > .env <<EOF
# 龍魂 · 一带一路入门包 · 环境配置
# DNA: #龍芯⚡️丙午·丙申·戊午·戊午·䷱鼎-BELT-ROAD-PACK-UID9622
DRAGONSOUL_VERSION=${DRAGONSOUL_VERSION}
MODEL_SIZE=${MODEL_SIZE}
DEFAULT_LANG=${LANG}
DATA_DIR=./data
MODELS_DIR=./models
LOGS_DIR=./logs
CONFIGS_DIR=./configs
SCENARIOS_DIR=./scenarios
PORT=8080
OFFLINE_MODE=${OFFLINE_MODE}
ARCH_TAG=${ARCH_TAG}
EOF

    # 创建目录结构
    mkdir -p data models logs configs scenarios

    # 启动服务
    log "启动 Docker 服务..."
    if command -v docker-compose &>/dev/null; then
        docker-compose up -d
    else
        docker compose up -d
    fi

    # 等待健康检查
    log "等待服务启动（最多60秒）..."
    for i in $(seq 1 30); do
        if curl -fsSL http://localhost:8080/health &>/dev/null; then
            log "服务启动成功 ✓"
            break
        fi
        sleep 2
        echo -n "."
    done

    # 下载模型（如未离线）
    if [ "$OFFLINE_MODE" -eq 0 ]; then
        log "下载多语言模型（约${MODEL_SIZE}，请等待）..."
        if command -v docker-compose &>/dev/null; then
            docker-compose exec -T dragonsoul ollama pull dragonsoul/belt-road-${MODEL_SIZE}-multilingual ||                 warn "模型下载失败，请手动执行: docker-compose exec dragonsoul ollama pull dragonsoul/belt-road-${MODEL_SIZE}-multilingual"
        else
            docker compose exec -T dragonsoul ollama pull dragonsoul/belt-road-${MODEL_SIZE}-multilingual ||                 warn "模型下载失败，请手动执行"
        fi
    else
        info "离线模式：请手动将 .gguf 模型文件放入 $INSTALL_DIR/models/"
    fi

    log "Docker 模式安装完成 ✓"
}

# ========== 裸机模式安装 ==========
install_bare() {
    log "=== 裸机模式安装（Ollama） ==="
    mkdir -p "$INSTALL_DIR"
    cd "$INSTALL_DIR"

    # 安装 Ollama（如未安装）
    if ! command -v ollama &> /dev/null; then
        log "安装 Ollama..."
        curl -fsSL https://ollama.com/install.sh | sh
    else
        log "Ollama 已安装 ✓"
    fi

    # 下载模型
    if [ "$OFFLINE_MODE" -eq 0 ]; then
        log "下载模型 dragonsoul/belt-road-${MODEL_SIZE}-multilingual..."
        ollama pull dragonsoul/belt-road-${MODEL_SIZE}-multilingual ||             warn "模型下载失败，请检查网络"
    else
        info "离线模式：请手动将 .gguf 模型文件放入 $INSTALL_DIR/models/"
        info "然后运行: ollama create dragonsoul/belt-road-${MODEL_SIZE}-multilingual -f Modelfile"
    fi

    # 安装 Python 依赖
    if [ "$HAS_PYTHON" -eq 1 ]; then
        log "安装 Python 依赖..."
        pip3 install --user -q dragonsoul-belt-road==${DRAGONSOUL_VERSION} 2>/dev/null ||             pip3 install --user -q -e . 2>/dev/null ||             warn "Python 包安装失败，部分功能不可用"
    fi

    # 创建目录结构
    mkdir -p data models logs configs scenarios

    # 创建启动脚本
    cat > start.sh <<'EOF'
#!/bin/bash
# 龍魂启动脚本
# 用法: ./start.sh [语言代码]

MODEL="${MODEL:-dragonsoul/belt-road-7b-multilingual}"
LANG="${DRAGONSOUL_LANG:-${1:-en}}"
PORT="${PORT:-8080}"
HOST="${HOST:-0.0.0.0}"

echo "[龍魂] 启动服务..."
echo "  模型: $MODEL"
echo "  语言: $LANG"
echo "  地址: $HOST:$PORT"
echo "  日志: ./logs/dragonsoul-$(date +%Y%m%d).log"

# 启动 Ollama 服务（后台）
if ! pgrep -x "ollama" > /dev/null; then
    ollama serve > ./logs/ollama-$(date +%Y%m%d).log 2>&1 &
    sleep 5
fi

# 启动龍魂网关
python3 -m dragonsoul.gateway \
    --model "$MODEL" \
    --lang "$LANG" \
    --port "$PORT" \
    --host "$HOST" \
    >> ./logs/dragonsoul-$(date +%Y%m%d).log 2>&1 &

sleep 3

# 健康检查
if curl -fsSL http://localhost:$PORT/health &>/dev/null; then
    echo "[龍魂] 服务启动成功 ✓"
    echo "  访问: http://localhost:$PORT"
    echo "  文档: http://localhost:$PORT/docs"
else
    echo "[龍魂] 服务启动中，请稍后检查: http://localhost:$PORT/health"
fi
EOF
    chmod +x start.sh

    # 创建停止脚本
    cat > stop.sh <<'EOF'
#!/bin/bash
# 停止龍魂服务
pkill -f "dragonsoul.gateway" 2>/dev/null || true
pkill -x "ollama" 2>/dev/null || true
echo "[龍魂] 服务已停止"
EOF
    chmod +x stop.sh

    log "裸机模式安装完成 ✓"
    log "运行 ./start.sh 启动服务，./stop.sh 停止服务"
}

# ========== 纯离线模式（llama.cpp） ==========
install_offline() {
    log "=== 纯离线模式（llama.cpp） ==="
    mkdir -p "$INSTALL_DIR"
    cd "$INSTALL_DIR"

    # 下载预编译二进制
    if [ "$OFFLINE_MODE" -eq 0 ]; then
        log "下载 llama.cpp 预编译二进制..."
        wget -q "https://dragonsoul.dev/releases/v${DRAGONSOUL_VERSION}/llama-belt-road-${ARCH_TAG}.tar.gz" -O llama-belt-road.tar.gz ||             wget -q "https://github.com/dragonsoul/belt-road-pack/releases/download/v${DRAGONSOUL_VERSION}/llama-belt-road-${ARCH_TAG}.tar.gz" -O llama-belt-road.tar.gz
        tar xzf llama-belt-road.tar.gz
    else
        if [ -f "${OFFLINE_PACKAGE:-/tmp/dragonsoul-offline}/llama-belt-road.tar.gz" ]; then
            tar xzf "${OFFLINE_PACKAGE:-/tmp/dragonsoul-offline}/llama-belt-road.tar.gz"
        else
            error "离线模式：llama-belt-road.tar.gz 未找到"
        fi
    fi

    mkdir -p models data logs

    cat > run.sh <<EOF
#!/bin/bash
# llama.cpp 离线运行脚本
MODEL="\${MODEL:-models/belt-road-${MODEL_SIZE}-Q4_K_M.gguf}"
LANG="\${DRAGONSOUL_LANG:-\${1:-en}}"
PORT="\${PORT:-8080}"

if [ ! -f "\$MODEL" ]; then
    echo "[错误] 模型文件未找到: \$MODEL"
    echo "请将 .gguf 模型文件放入 models/ 目录"
    exit 1
fi

./llama-server \
    -m "\$MODEL" \
    --port \$PORT \
    -c 4096 \
    --host 0.0.0.0 \
    --path ./public \
    >> ./logs/llama-$(date +%Y%m%d).log 2>&1 &

echo "[龍魂] llama.cpp 服务已启动"
echo "  访问: http://localhost:\$PORT"
EOF
    chmod +x run.sh

    log "纯离线模式安装完成 ✓"
    log "将模型文件放入 models/ 目录，运行 ./run.sh 启动"
}

# ========== 验证安装 ==========
verify_install() {
    log "=== 安装验证 ==="

    PORT_CHECK=${PORT:-8080}

    # 健康检查
    for i in $(seq 1 10); do
        if curl -fsSL http://localhost:$PORT_CHECK/health &>/dev/null; then
            log "API 服务: 运行中 ✓"
            HEALTH_OK=1
            break
        fi
        sleep 2
    done

    if [ "${HEALTH_OK:-0}" -ne 1 ]; then
        warn "API 服务未响应，请检查日志: $LOG_FILE"
    fi

    # 模型检查
    if command -v ollama &> /dev/null; then
        if ollama list 2>/dev/null | grep -q "belt-road"; then
            log "模型: 已加载 ✓"
        else
            warn "模型: 未加载，请手动下载"
        fi
    fi

    # 场景测试（如果存在）
    if [ -f "scenarios/AGRI-001/test.json" ] && [ "$HAS_PYTHON" -eq 1 ]; then
        log "运行场景测试 AGRI-001..."
        python3 -m dragonsoul.test --scenario AGRI-001 --quiet 2>/dev/null &&             log "场景测试: 通过 ✓" || warn "场景测试: 失败或不可用"
    fi

    log "=== 安装验证完成 ==="
}

# ========== 打印使用说明 ==========
print_usage() {
    log ""
    log "═══════════════════════════════════════════════════════"
    log "  🎉 部署完成！"
    log "═══════════════════════════════════════════════════════"
    log "  安装目录: $INSTALL_DIR"
    log "  日志文件: $LOG_FILE"
    log ""

    case "$MODE" in
        docker)
            log "  模式: Docker Compose"
            log "  访问地址: http://localhost:8080"
            log "  API文档: http://localhost:8080/docs"
            log "  管理命令:"
            log "    cd $INSTALL_DIR && docker-compose ps"
            log "    cd $INSTALL_DIR && docker-compose logs -f"
            log "    cd $INSTALL_DIR && docker-compose down"
            ;;
        bare)
            log "  模式: 裸机（Ollama）"
            log "  启动: cd $INSTALL_DIR && ./start.sh"
            log "  停止: cd $INSTALL_DIR && ./stop.sh"
            log "  访问: http://localhost:8080"
            ;;
        offline)
            log "  模式: 纯离线（llama.cpp）"
            log "  启动: cd $INSTALL_DIR && ./run.sh"
            log "  访问: http://localhost:8080"
            ;;
    esac

    log ""
    log "  切换语言示例:"
    log "    export DRAGONSOUL_LANG=ar && ./start.sh"
    log "    export DRAGONSOUL_LANG=ru && ./start.sh"
    log "    export DRAGONSOUL_LANG=es && ./start.sh"
    log ""
    log "  运行场景:"
    log "    python3 -m dragonsoul.scenario --id AGRI-001 --lang ar"
    log ""
    log "  查看帮助:"
    log "    python3 -m dragonsoul --help"
    log "═══════════════════════════════════════════════════════"
}

# ========== 主流程 ==========
main() {
    log "🌍 龍魂 · 一带一路老铁入门包 · 一键部署 v${DRAGONSOUL_VERSION}"
    log "DNA: #龍芯⚡️丙午·丙申·戊午·戊午·䷱鼎-BELT-ROAD-PACK-UID9622"
    log "确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    log ""

    check_system
    select_mode

    case "$MODE" in
        docker) install_docker ;;
        bare) install_bare ;;
        offline) install_offline ;;
    esac

    verify_install
    print_usage
}

# 参数解析
while [[ $# -gt 0 ]]; do
    case $1 in
        --docker) FORCE_MODE="docker"; shift ;;
        --bare) FORCE_MODE="bare"; shift ;;
        --offline) FORCE_MODE="offline"; shift ;;
        --model-size) MODEL_SIZE="$2"; shift 2 ;;
        --lang) LANG="$2"; shift 2 ;;
        --dir) INSTALL_DIR="$2"; shift 2 ;;
        --offline-mode) OFFLINE=1; shift ;;
        --help|-h)
            echo "用法: $0 [选项]"
            echo ""
            echo "选项:"
            echo "  --docker          强制使用 Docker Compose 模式"
            echo "  --bare            强制使用裸机（Ollama）模式"
            echo "  --offline         强制使用纯离线（llama.cpp）模式"
            echo "  --model-size SIZE 指定模型大小 (3b/7b/13b/70b)"
            echo "  --lang LANG       默认语言 (en/ar/ru/es/...)"
            echo "  --dir PATH        安装目录"
            echo "  --offline-mode    启用离线模式"
            echo "  --help, -h        显示此帮助"
            exit 0
            ;;
        *) warn "未知参数: $1"; shift ;;
    esac
done

main "$@"
