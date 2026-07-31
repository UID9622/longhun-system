#!/bin/bash
# 龍魂本地开源模型 · 一键部署脚本
# deploy_local_models.sh
# DNA: #龍芯⚡️丙午·辛未·DEPLOY-LOCAL-MODELS-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 用途: 部署本地备胎模型（国产网络故障时离线可用）

set -euo pipefail

DNA="#龍芯⚡️丙午·辛未·DEPLOY-LOCAL-MODELS-v1.0"
OLLAMA_HOST="${OLLAMA_HOST:-0.0.0.0}"
OLLAMA_PORT="${OLLAMA_PORT:-11434}"
MODEL_DIR="${HOME}/.ollama/models"

# 模型清单（国产优先）
MODELS=(
    "qwen2:7b"       # 通义千问 7B — 中文首选
    "qwen2:72b"      # 通义千问 72B — 长文本中文（需48GB+显存）
    "deepseek-coder:6.7b"  # DeepSeek Coder — 代码专用
    "llama3:8b"      # Llama3 8B — 备胎
)

log() { echo "[$(date '+%H:%M:%S')] $1"; }
warn() { echo "[WARN] $1"; }

# --- 安装 Ollama ---
install_ollama() {
    if command -v ollama &>/dev/null; then
        log "✅ Ollama 已安装: $(ollama --version 2>&1)"
        return
    fi

    log "安装 Ollama..."
    if curl -fsSL https://ollama.com/install.sh | sh; then
        log "✅ Ollama 安装完成"
    else
        warn "在线安装失败，尝试手动安装..."
        # Linux ARM64 (鲲鹏)
        ARCH=$(uname -m)
        if [ "$ARCH" = "aarch64" ]; then
            log "检测到 ARM64，下载鲲鹏兼容版..."
        fi
        warn "请手动安装: https://ollama.com/download"
        exit 1
    fi
}

# --- 拉取模型 ---
pull_models() {
    log "拉取模型（国产优先）..."

    # 停止已有 ollama（如果用 serve 模式）
    pkill ollama 2>/dev/null || true
    sleep 1

    # 后台启动
    ollama serve &
    sleep 3

    local pulled=0
    for model in "${MODELS[@]}"; do
        log "拉取 $model ..."
        if ollama pull "$model" 2>&1; then
            log "  ✅ $model"
            ((pulled++))
        else
            warn "  ⚠️  $model 拉取失败，跳过"
        fi
    done

    log "共拉取 ${pulled}/${#MODELS[@]} 个模型"
    pkill ollama 2>/dev/null || true
}

# --- 配置 API 服务 ---
setup_service() {
    log "配置 Ollama API 服务..."

    cat > /etc/systemd/system/ollama-longhun.service << SERVICEEOF
[Unit]
Description=Ollama · 龍魂本地模型
After=network.target

[Service]
Type=simple
User=root
Environment="OLLAMA_HOST=${OLLAMA_HOST}:${OLLAMA_PORT}"
Environment="OLLAMA_MODELS=${MODEL_DIR}"
ExecStart=$(which ollama) serve
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICEEOF

    systemctl daemon-reload
    systemctl enable ollama-longhun.service
    systemctl start ollama-longhun.service

    sleep 3
    if systemctl is-active --quiet ollama-longhun.service; then
        log "✅ Ollama 服务已启动 (端口 ${OLLAMA_PORT})"
    else
        warn "Ollama 服务启动失败"
    fi
}

# --- 验证 ---
verify() {
    log "验证模型..."
    sleep 2

    # API 连通性
    if curl -sf "http://localhost:${OLLAMA_PORT}/api/tags" >/dev/null 2>&1; then
        log "✅ API 可达: localhost:${OLLAMA_PORT}"
    else
        warn "API 不可达"
        return
    fi

    # 列出模型
    curl -s "http://localhost:${OLLAMA_PORT}/api/tags" | python3 -c "
import sys,json
data=json.load(sys.stdin)
models=[m['name'] for m in data.get('models',[])]
print(f'  已加载模型: {len(models)} 个')
for m in models:
    print(f'    📦 {m}')
" 2>/dev/null || warn "模型列表获取失败"

    # 快速测试
    log "快速推理测试..."
    TEST_RESULT=$(curl -s "http://localhost:${OLLAMA_PORT}/api/generate" -d '{
        "model": "qwen2:7b",
        "prompt": "龍魂系统测试: 请回复OK",
        "stream": false
    }' 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('response','FAIL')[:20])" 2>/dev/null || echo "N/A")
    log "  测试结果: ${TEST_RESULT}"
}

# --- 主流程 ---
main() {
    echo "============================================"
    echo "  龍魂本地模型 · 一键部署"
    echo "  DNA: ${DNA}"
    echo "  目标: 本地离线备胎模型"
    echo "============================================"
    echo ""

    install_ollama
    pull_models
    setup_service
    verify

    echo ""
    echo "============================================"
    echo "  ✅ 本地模型部署完成！"
    echo ""
    echo "  API: http://localhost:${OLLAMA_PORT}"
    echo "  模型: ${MODELS[*]}"
    echo ""
    echo "  测试命令:"
    echo "    curl http://localhost:${OLLAMA_PORT}/api/generate -d '{\"model\":\"qwen2:7b\",\"prompt\":\"你好\"}'"
    echo "============================================"
}

main "$@"
