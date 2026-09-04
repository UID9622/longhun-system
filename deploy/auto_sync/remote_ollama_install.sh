#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 · 华为云 Ollama 服务端一键安装
# DNA: #龍芯⚡️丙午·丙申·乙卯·辰时·䷀乾-REMOTE-OLLAMA-v1.0
#
# 在华为云 ARM64 上：
#   1. 安装 Ollama
#   2. 拉取中文模型 (qwen2.5:7b + deepseek-r1:7b)
#   3. 暴露 11434 端口给本地调用
#   4. systemd 开机自启
#
# 设计：此脚本上传到服务器后直接跑，无需人工交互。
# 同步：本地 sync 自动随 deploy/auto_sync/longhun_sync_worker.sh 推上去。

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

log()   { echo -e "$(date '+%H:%M:%S') $*"; }
ok()    { log "${GREEN}✅${NC} $*"; }
warn()  { log "${YELLOW}⚠️${NC}  $*"; }
fail()  { log "${RED}🔴${NC} $*"; exit 1; }
intro() { echo -e "\n${BOLD}${CYAN}$*${NC}"; }

echo ""
echo "🐉 龍魂 · 华为云 Ollama 安装"
echo "   服务器推理，本地调用。"
echo ""

# ═════════════════════════════════════
# 1. 安装 Ollama
# ═════════════════════════════════════
intro "[1/5] 安装 Ollama ..."

if command -v ollama &>/dev/null; then
    ok "Ollama 已安装: $(ollama --version 2>/dev/null || echo 'unknown')"
else
    log "下载 Ollama (ARM64)..."
    curl -fsSL https://ollama.ai/install.sh | sh
    ok "Ollama 安装完成"
fi

# ═════════════════════════════════════
# 2. 启动服务
# ═════════════════════════════════════
intro "[2/5] 启动 Ollama 服务..."

if curl -s http://localhost:11434/api/tags &>/dev/null; then
    ok "Ollama 服务已在运行"
else
    log "启动 Ollama 守护进程..."
    systemctl start ollama 2>/dev/null || (ollama serve &>/dev/null &)
    sleep 5

    if curl -s http://localhost:11434/api/tags &>/dev/null; then
        ok "Ollama 服务启动成功"
    else
        fail "Ollama 启动失败，请检查: journalctl -u ollama -n 30"
    fi
fi

# ═════════════════════════════════════
# 3. 拉取模型
# ═════════════════════════════════════
intro "[3/5] 拉取中文模型..."

MODELS=(
    "qwen2.5:7b"           # 通义千问 7B — 主力
    "qwen2.5:1.5b"         # 通义千问 1.5B — 极速
    "deepseek-r1:7b"       # DeepSeek 推理
    "nomic-embed-text"      # 嵌入模型
)

for model in "${MODELS[@]}"; do
    if ollama list 2>/dev/null | grep -q "$model"; then
        ok "${model} 已存在"
    else
        log "下载 ${model} ..."
        ollama pull "$model" && ok "${model} 下载完成" || warn "${model} 下载失败（跳过）"
    fi
done

# ═════════════════════════════════════
# 4. 暴露 API 端口
# ═════════════════════════════════════
intro "[4/5] 暴露 Ollama API..."

# 修改监听地址为 0.0.0.0
OLLAMA_SERVICE="/etc/systemd/system/ollama.service"

# 获取当前用户
CURRENT_USER=$(whoami)

# 在 [Service] 段添加 Environment
if systemctl cat ollama &>/dev/null 2>&1; then
    if ! grep -q 'OLLAMA_HOST' /etc/systemd/system/ollama.service 2>/dev/null; then
        log "配置 Ollama 监听 0.0.0.0:11434..."
        mkdir -p /etc/systemd/system/ollama.service.d
        cat > /etc/systemd/system/ollama.service.d/override.conf << 'OVERRIDE'
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
OVERRIDE
    fi
    systemctl daemon-reload
    systemctl restart ollama
    sleep 3
    ok "Ollama 监听 0.0.0.0:11434 (本地 + 内网)"
fi

# ═════════════════════════════════════
# 5. 防火墙放行 (可选，安全组更优先)
# ═════════════════════════════════════
intro "[5/5] 防火墙规则..."

if command -v firewall-cmd &>/dev/null; then
    firewall-cmd --permanent --add-port=11434/tcp 2>/dev/null && \
        firewall-cmd --reload 2>/dev/null && \
        ok "firewalld 11434 已放行" || \
        warn "firewalld 配置跳过"
else
    warn "firewalld 未安装，请在华为云安全组放行 11434 端口"
fi

# ═════════════════════════════════════
# 完成
# ═════════════════════════════════════
echo ""
echo "════════════════════════════════════════"
echo -e "${BOLD}🐉 Ollama 服务端安装完成${NC}"
echo "════════════════════════════════════════"
echo ""
echo "  已安装模型:"
ollama list 2>/dev/null || echo "  (列出失败)"
echo ""
echo "  本地调用方式:"
echo "    curl http://119.13.90.27:11434/api/chat -d '{...}'"
echo "    curl http://这台服务器内网IP:11434/api/generate -d '{...}'"
echo ""
echo "  ⚠️ 请在华为云安全组中放行 11434 端口！"
echo ""
echo "  验证:"
echo "    curl http://119.13.90.27:11434/api/tags"
echo ""

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·乙卯·辰时·䷀乾-CONFIRM-SEAL-remote-ollama-E6B2C7D1
