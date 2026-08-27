#!/bin/bash
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 龍魂 · Docker 入口脚本 v1.1
# DNA: #龍芯⚡️丙午·丙申·戊午·戊午·䷱鼎-BELT-ROAD-PACK-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 用途: 容器启动时自动检测环境、加载模型、启动服务

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[龍魂·容器]${NC} $1"; }
warn() { echo -e "${YELLOW}[警告]${NC} $1"; }
error() { echo -e "${RED}[错误]${NC} $1"; exit 1; }

# ========== 环境检测 ==========
detect_env() {
    log "=== 容器环境检测 ==="
    log "架构: $(uname -m)"
    log "CPU: $(nproc) 核"
    log "内存: $(free -h | awk '/^Mem:/ {print $2}')"
    log "模型大小: ${MODEL_SIZE}"
    log "默认语言: ${DEFAULT_LANG}"
    log "离线模式: ${OFFLINE_MODE:-0}"
}

# ========== 模型加载 ==========
load_model() {
    log "=== 模型加载 ==="

    MODEL_FILE="${MODELS_DIR}/belt-road-${MODEL_SIZE}-Q4_K_M.gguf"

    # 检查模型是否存在
    if [ -f "$MODEL_FILE" ]; then
        log "模型已存在: $MODEL_FILE"
        MODEL_LOADED=1
    elif [ "${OFFLINE_MODE:-0}" -eq 1 ]; then
        warn "离线模式：模型文件不存在，跳过加载"
        MODEL_LOADED=0
    else
        log "尝试下载模型..."
        # 🟡 占位：实际应从模型仓库下载
        # curl -fsSL "https://dragonsoul.dev/models/belt-road-${MODEL_SIZE}-Q4_K_M.gguf"         #     -o "$MODEL_FILE" || warn "模型下载失败"
        warn "模型下载功能待实现（🟡 占位）"
        MODEL_LOADED=0
    fi
}

# ========== 启动 llama.cpp 推理服务 ==========
start_llama() {
    if [ "${MODEL_LOADED:-0}" -eq 1 ]; then
        log "启动 llama.cpp 推理服务..."
        llama-server             -m "$MODEL_FILE"             --host ${HOST:-0.0.0.0}             --port 8081             -c 4096             -n 512             --path /app/public             >> /app/logs/llama.log 2>&1 &
        LLAMA_PID=$!
        log "llama.cpp PID: $LLAMA_PID"

        # 等待 llama.cpp 就绪
        for i in $(seq 1 30); do
            if curl -fsSL http://localhost:8081/health &>/dev/null; then
                log "llama.cpp 就绪 ✓"
                return 0
            fi
            sleep 1
        done
        warn "llama.cpp 启动超时，继续启动网关"
    else
        warn "模型未加载，llama.cpp 服务不可用"
    fi
}

# ========== 启动 Python 网关 ==========
start_gateway() {
    log "启动龍魂网关..."

    export LLAMA_API_URL="http://localhost:8081"
    export LLAMA_MODEL_LOADED="${MODEL_LOADED:-0}"

    exec python3 -m dragonsoul.gateway         --host ${HOST:-0.0.0.0}         --port ${PORT:-8080}         --lang ${DEFAULT_LANG:-en}         --model-size ${MODEL_SIZE:-7b}         --data-dir ${DATA_DIR}         --models-dir ${MODELS_DIR}         --scenarios-dir ${SCENARIOS_DIR}
}

# ========== 主流程 ==========
main() {
    log "🌍 龍魂 · 一带一路入门包 · 容器启动 v${DRAGONSOUL_VERSION}"
    log "DNA: #龍芯⚡️丙午·丙申·戊午·戊午·䷱鼎-BELT-ROAD-PACK-UID9622"

    detect_env
    load_model
    start_llama
    start_gateway
}

case "${1:-start}" in
    start) main ;;
    shell) exec /bin/bash ;;
    health) curl -fsSL http://localhost:8080/health || exit 1 ;;
    *) exec "$@" ;;
esac
