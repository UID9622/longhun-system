#!/usr/bin/env bash
# ============================================================
# 龍魂感知层 · 一键更新（macOS 版 · 先备份→更新→验证→可回滚）
# DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-UPDATE-MAC-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 安全: 自动备份 bin/ + memory/ 到 backups/时间戳 · 更新失败可回滚
# 用法: bash scripts/update_longhun.sh
# ============================================================
set -euo pipefail

PROJECT_DIR="${HOME}/longhun-system"
BIN_DIR="${PROJECT_DIR}/bin"
MEMORY_DIR="${PROJECT_DIR}/.codebuddy/memory"
BACKUP_DIR="${PROJECT_DIR}/backups/$(date +%Y%m%d_%H%M%S)"
PY_MIRROR="https://pypi.tuna.tsinghua.edu.cn/simple"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✓${NC} $*"; }
warn() { echo -e "${YELLOW}!${NC} $*"; }
info() { echo -e "→ $*"; }

echo "=============================================="
echo " 龍魂感知层 · 一键更新 (macOS) v2.0"
echo " 备份目录: ${BACKUP_DIR}"
echo "=============================================="

# 1. 备份
info "创建备份..."
mkdir -p "${BACKUP_DIR}"
[[ -d "${BIN_DIR}" ]] && cp -a "${BIN_DIR}" "${BACKUP_DIR}/" 2>/dev/null || true
[[ -d "${MEMORY_DIR}" ]] && cp -a "${MEMORY_DIR}" "${BACKUP_DIR}/" 2>/dev/null || true
ok "备份完成 → ${BACKUP_DIR}"

# 2. 更新 Python 依赖（可选）
read -p "是否更新 Python 依赖（numpy/sounddevice/faster-whisper 等）？(y/N): " confirm
if [[ "${confirm}" =~ ^[Yy]$ ]]; then
    info "更新 Python 依赖（清代理+清华镜像）..."
    env -u all_proxy -u ALL_PROXY -u http_proxy -u HTTP_PROXY -u https_proxy -u HTTPS_PROXY \
        python3 -m pip install --upgrade --break-system-packages -i "${PY_MIRROR}" \
        numpy sounddevice faster-whisper requests pillow 2>&1 | tail -5 || warn "pip 更新失败（网络或代理问题）"
else
    info "跳过依赖更新"
fi

# 3. 更新模型（可选）
read -p "是否检查/更新视觉模型 moondream？(y/N): " confirm_model
if [[ "${confirm_model}" =~ ^[Yy]$ ]]; then
    info "检查 moondream 模型..."
    if curl -sf http://localhost:11434/api/tags >/dev/null 2>&1; then
        if curl -sf http://localhost:11434/api/tags 2>/dev/null | grep -q "moondream"; then
            ok "moondream 已就位（如需最新版: ollama pull moondream）"
        else
            info "moondream 未拉取，开始拉取..."
            ollama pull moondream 2>&1 | tail -3 || warn "拉取失败"
        fi
    else
        warn "Ollama 未运行，跳过模型检查"
    fi
fi

# 4. 重启相关服务
info "重启 Ollama（如有需要）..."
if curl -sf http://localhost:11434/api/tags >/dev/null 2>&1; then
    ok "Ollama 运行中，无需重启"
else
    brew services restart ollama 2>/dev/null && sleep 2 && ok "Ollama 已重启" || warn "Ollama 未运行/重启失败"
fi

# 5. 验证
info "快速验证..."
[[ -f "${BIN_DIR}/voice_input.py" ]] && ok "voice_input.py 正常" || warn "voice_input.py 异常"
[[ -f "${BIN_DIR}/vision_input.py" ]] && ok "vision_input.py 正常" || warn "vision_input.py 异常"
if python3 -c "import faster_whisper" >/dev/null 2>&1; then ok "faster-whisper 可用"; else warn "faster-whisper 缺失"; fi

echo ""
echo "更新完成。如需回滚："
echo "  cp -a ${BACKUP_DIR}/bin/* ${BIN_DIR}/"
echo "  cp -a ${BACKUP_DIR}/memory/* ${MEMORY_DIR}/"
echo ""
echo "DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-UPDATE-MAC-DONE"
