#!/usr/bin/env bash
# ============================================================
# 龍魂感知层 · 一键初始化/依赖修复（macOS 版）
# DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-INSTALL-MAC-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 适配: macOS(launchd) · faster-whisper + Ollama moondream · 零云端
# 用法: bash scripts/install_longhun.sh
# ============================================================
set -euo pipefail

PROJECT_DIR="${HOME}/longhun-system"
BIN_DIR="${PROJECT_DIR}/bin"
PY_MIRROR="https://pypi.tuna.tsinghua.edu.cn/simple"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✓${NC} $*"; }
fail() { echo -e "${RED}✗${NC} $*"; }
warn() { echo -e "${YELLOW}!${NC} $*"; }
info() { echo -e "${CYAN}→${NC} $*"; }

echo "=============================================="
echo " 龍魂感知层 · 一键初始化 (macOS) v2.0"
echo " 时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=============================================="

# 1. 基础工具
echo ""
echo "【1/5 基础工具】"
for tool in python3 ffmpeg brew; do
    if command -v "${tool}" >/dev/null 2>&1; then
        ok "${tool} 可用 ($(command -v "${tool}"))"
    else
        warn "${tool} 缺失"
    fi
done
if ! command -v ffmpeg >/dev/null 2>&1; then
    warn "尝试安装 ffmpeg..."
    brew install ffmpeg 2>&1 | tail -3 || warn "brew 安装 ffmpeg 失败，请手动: brew install ffmpeg"
fi

# 2. Ollama + 视觉模型
echo ""
echo "【2/5 Ollama + 视觉模型 moondream】"
if curl -sf http://localhost:11434/api/tags >/dev/null 2>&1; then
    ok "Ollama 服务在线 (:11434)"
    if curl -sf http://localhost:11434/api/tags 2>/dev/null | grep -q "moondream"; then
        ok "视觉模型 moondream 已就位"
    else
        warn "moondream 未拉取，开始拉取（约1.7GB·本地推理）..."
        ollama pull moondream 2>&1 | tail -3 && ok "moondream 拉取完成" || warn "拉取失败，可稍后手动: ollama pull moondream"
    fi
else
    warn "Ollama 未运行（视觉模块依赖）。启动: brew services start ollama"
    warn "或前台跑: ollama serve &"
fi

# 3. Python 依赖（清代理+清华镜像+PEB668 放行，沿用实测可行方案）
echo ""
echo "【3/5 Python 依赖（语音 faster-whisper + 视觉 requests/Pillow）】"
PY_DEPS=("numpy" "sounddevice" "faster-whisper" "requests" "pillow")
need=""
for pkg in "${PY_DEPS[@]}"; do
    mod="${pkg//-/_}"
    if python3 -c "import ${mod}" >/dev/null 2>&1; then
        ok "${pkg} 已安装"
    else
        warn "${pkg} 缺失 → 待装"
        need="${need} ${pkg}"
    fi
done
if [[ -n "${need}" ]]; then
    info "安装:${need}"
    if env -u all_proxy -u ALL_PROXY -u http_proxy -u HTTP_PROXY -u https_proxy -u HTTPS_PROXY \
        python3 -m pip install --break-system-packages -i "${PY_MIRROR}" ${need} 2>&1 | tail -5; then
        ok "依赖安装完成"
    else
        warn "pip 安装失败。手动执行: python3 -m pip install --break-system-packages -i ${PY_MIRROR} ${need}"
    fi
fi

# 4. 模块自检
echo ""
echo "【4/5 模块自检】"
if [[ -f "${BIN_DIR}/voice_input.py" ]]; then
    if python3 "${BIN_DIR}/voice_input.py" --help >/dev/null 2>&1; then
        ok "语音模块 voice_input.py 正常"
    else
        fail "语音模块启动异常（多半是依赖未装全，见第3步）"
    fi
else
    fail "voice_input.py 缺失（应在 ${BIN_DIR}/）"
fi
if [[ -f "${BIN_DIR}/vision_input.py" ]]; then
    if python3 "${BIN_DIR}/vision_input.py" --help >/dev/null 2>&1; then
        ok "视觉模块 vision_input.py 正常"
    else
        warn "视觉模块启动异常（检查 Ollama 是否已启动）"
    fi
else
    fail "vision_input.py 缺失"
fi

# 5. 权限提示
echo ""
echo "【5/5 系统权限（首次使用需授权一次）】"
echo "  🎤 麦克风:   系统设置 → 隐私与安全性 → 麦克风 → 允许终端"
echo "  🖥 屏幕录制: 系统设置 → 隐私与安全性 → 屏幕录制 → 允许终端"
echo ""
echo "=============================================="
echo " 初始化完成。下一步："
echo "   python3 bin/voice_input.py        # 录音转写"
echo "   lh --voice-in                     # 说话→转写→喂Agent"
echo "   lh --screenshot                   # 截图分析"
echo "   或运行 scripts/longhun_menu.sh 打开总控菜单"
echo "=============================================="
echo "DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-INSTALL-MAC-DONE"
