#!/usr/bin/env bash
# ============================================================
# 龍魂感知层 · 状态检查（macOS 版）
# DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-STATUS-MAC-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 检查: 环境/模块/Ollama/依赖/MEMORY/权限 · 三色标记
# 用法: bash scripts/status_longhun.sh
# ============================================================
set -euo pipefail
# system_profiler 固定绝对路径（执行环境 PATH 可能缺 /usr/sbin；勿动全局 PATH，否则 python3 解析会漂移）
SPROF="/usr/sbin/system_profiler"
[[ -x "${SPROF}" ]] || SPROF="$(command -v system_profiler 2>/dev/null || true)"

PROJECT_DIR="${HOME}/longhun-system"
BIN_DIR="${PROJECT_DIR}/bin"
MEMORY_FILE="${PROJECT_DIR}/.codebuddy/memory/MEMORY.md"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✓${NC} $*"; }
fail() { echo -e "${RED}✗${NC} $*"; }
warn() { echo -e "${YELLOW}!${NC} $*"; }
info() { echo -e "${CYAN}→${NC} $*"; }

TOTAL=0; PASS=0; WARN_N=0; FAIL_N=0
MARK="🟢"

echo "=============================================="
echo " 龍魂感知层 · 状态检查 (macOS) v2.0"
echo " 时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=============================================="

# 1. 基础环境
echo ""
echo "【1. 基础环境】"
for tool in python3 ffmpeg brew; do
    TOTAL=$((TOTAL+1))
    if command -v "${tool}" >/dev/null 2>&1; then ok "${tool} 可用"; PASS=$((PASS+1));
    else warn "${tool} 缺失（brew install ${tool}）"; WARN_N=$((WARN_N+1)); fi
done

# 2. 核心模块
echo ""
echo "【2. 感知层模块】"
for f in voice_input.py vision_input.py; do
    TOTAL=$((TOTAL+1))
    if [[ -f "${BIN_DIR}/${f}" ]]; then ok "${f} 存在"; PASS=$((PASS+1));
    else fail "${f} 缺失"; FAIL_N=$((FAIL_N+1)); fi
done
for f in lh.py memory_compress.py; do
    if [[ -f "${BIN_DIR}/${f}" ]]; then ok "${f} 存在"; else warn "${f} 缺失"; WARN_N=$((WARN_N+1)); fi
done

# 3. 服务（Ollama + 语音守护）
echo ""
echo "【3. 服务状态】"
TOTAL=$((TOTAL+1))
if curl -sf http://localhost:11434/api/tags >/dev/null 2>&1; then
    ok "Ollama 在线 (:11434)"
    if curl -sf http://localhost:11434/api/tags 2>/dev/null | grep -q "moondream"; then
        ok "视觉模型 moondream 就位"
    else
        warn "moondream 未拉取（ollama pull moondream）"; WARN_N=$((WARN_N+1))
    fi
    PASS=$((PASS+1))
else
    warn "Ollama 未运行（视觉不可用）· brew services start ollama"; WARN_N=$((WARN_N+1))
fi
if [[ -f "${HOME}/Library/LaunchAgents/com.longhun.voice.plist" ]]; then
    if launchctl list com.longhun.voice >/dev/null 2>&1; then
        ok "语音守护 com.longhun.voice 已加载"
    else
        warn "语音守护 plist 存在但未加载"; WARN_N=$((WARN_N+1))
    fi
else
    info "语音守护未安装（无 com.longhun.voice.plist · 可前台用 lh --voice-in）"
fi

# 4. Python 依赖
echo ""
echo "【4. 依赖】"
for mod in numpy sounddevice faster_whisper requests PIL; do
    TOTAL=$((TOTAL+1))
    if python3 -c "import ${mod}" >/dev/null 2>&1; then ok "${mod} 可用"; PASS=$((PASS+1));
    else fail "${mod} 缺失（跑 scripts/install_longhun.sh）"; FAIL_N=$((FAIL_N+1)); fi
done
if [[ -d "${HOME}/.cache/huggingface" ]]; then
    ok "Whisper 模型缓存存在 (~/.cache/huggingface)"
else
    warn "Whisper 模型尚未下载（首次转写自动拉取·small 约150MB）"; WARN_N=$((WARN_N+1))
fi

# 5. MEMORY
echo ""
echo "【5. MEMORY 与日志】"
TOTAL=$((TOTAL+1))
if [[ -f "${MEMORY_FILE}" ]]; then
    BYTES=$(wc -c < "${MEMORY_FILE}" | tr -d ' ')
    ok "MEMORY.md 存在 ($((BYTES/1024)) KB)"
    if [[ ${BYTES} -gt 7680 ]]; then warn "超过7.5KB安全线 → lh --compress-memory run"; WARN_N=$((WARN_N+1)); fi
    PASS=$((PASS+1))
else
    warn "MEMORY.md 未找到（${MEMORY_FILE}）"; WARN_N=$((WARN_N+1))
fi

# 6. 音频设备
echo ""
echo "【6. 音频设备】"
TOTAL=$((TOTAL+1))
if "${SPROF}" SPAudioDataType 2>/dev/null | grep -qiE "麦克风|microphone|输入|input"; then
    ok "检测到音频输入设备"
    PASS=$((PASS+1))
else
    warn "未检测到音频输入（检查麦克风权限/设备）"; WARN_N=$((WARN_N+1))
fi

# 7. 汇总
echo ""
echo "=============================================="
if [[ ${FAIL_N} -eq 0 && ${WARN_N} -eq 0 ]]; then
    MARK="🟢"; echo -e " ${MARK} 全绿：${PASS}/${TOTAL} 项通过"
elif [[ ${FAIL_N} -eq 0 ]]; then
    MARK="🟡"; echo -e " ${MARK} 待核：${PASS}/${TOTAL} 通过 · ${WARN_N} 项警告"
else
    MARK="🔴"; echo -e " ${MARK} 红线：${FAIL_N} 项失败 · 请跑 scripts/troubleshoot_longhun.sh"
fi
echo "=============================================="
echo "DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-STATUS-MAC-DONE · ${MARK}"
