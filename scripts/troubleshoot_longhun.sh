#!/usr/bin/env bash
# ============================================================
# 龍魂感知层 · 故障排查（macOS 版）
# DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-TROUBLESHOOT-MAC-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 排查: 环境/文件/服务/进程/音频/权限/日志 → 快速修复
# 用法: bash scripts/troubleshoot_longhun.sh
# ============================================================
set -euo pipefail
# system_profiler 固定绝对路径（执行环境 PATH 可能缺 /usr/sbin；勿动全局 PATH，否则 python3 解析会漂移）
SPROF="/usr/sbin/system_profiler"
[[ -x "${SPROF}" ]] || SPROF="$(command -v system_profiler 2>/dev/null || true)"

PROJECT_DIR="${HOME}/longhun-system"
BIN_DIR="${PROJECT_DIR}/bin"
MEMORY_FILE="${PROJECT_DIR}/.codebuddy/memory/MEMORY.md"
LOG_DIR="${PROJECT_DIR}/logs"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✓${NC} $*"; }
fail() { echo -e "${RED}✗${NC} $*"; }
warn() { echo -e "${YELLOW}!${NC} $*"; }
info() { echo -e "${CYAN}→${NC} $*"; }

echo "=============================================="
echo " 龍魂感知层 · 故障排查 (macOS) v2.0"
echo " 时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=============================================="
echo ""

# 1. 基础环境
echo "【1. 基础环境】"
command -v python3 >/dev/null 2>&1 && ok "python3 可用" || fail "python3 未安装（brew install python3）"
command -v ffmpeg  >/dev/null 2>&1 && ok "ffmpeg 可用"  || warn "ffmpeg 未安装（部分音频格式可能失败）"
command -v brew    >/dev/null 2>&1 && ok "brew 可用"    || warn "brew 未安装"
echo ""

# 2. 核心文件
echo "【2. 核心文件】"
for f in \
    "${BIN_DIR}/voice_input.py" \
    "${BIN_DIR}/vision_input.py" \
    "${BIN_DIR}/lh.py" \
    "${BIN_DIR}/memory_compress.py"
do
    if [[ -f "$f" ]]; then
        ok "$(basename "$f") 存在"
    else
        fail "$(basename "$f") 缺失 → $f"
    fi
done
echo ""

# 3. 服务状态（launchd）
echo "【3. 服务状态】"
if launchctl list | grep -q "homebrew.mxcl.ollama"; then
    ok "Ollama launchd 已加载"
else
    warn "Ollama 未加载（brew services start ollama）"
fi
if curl -sf http://localhost:11434/api/tags >/dev/null 2>&1; then
    ok "Ollama 服务在线 (:11434)"
else
    fail "Ollama 端口 11434 无响应（ollama serve & 或 brew services start ollama）"
fi
if [[ -f "${HOME}/Library/LaunchAgents/com.longhun.voice.plist" ]]; then
    if launchctl list com.longhun.voice >/dev/null 2>&1; then
        ok "语音守护已加载"
    else
        warn "语音守护 plist 存在但未加载（launchctl load ~/Library/LaunchAgents/com.longhun.voice.plist）"
    fi
else
    info "语音守护未安装（前台模式不受影响）"
fi
echo ""

# 4. 进程与资源
echo "【4. 进程】"
if pgrep -f "voice_input.py" >/dev/null 2>&1; then
    ok "语音进程存在"
else
    warn "未检测到语音进程（正常，除非在录音）"
fi
if pgrep -f "ollama" >/dev/null 2>&1; then
    ok "Ollama 进程存在"
else
    warn "Ollama 未运行（视觉联动会受影响）"
fi
echo ""

# 5. 音频设备（macOS: system_profiler）
echo "【5. 音频设备】"
if "${SPROF}" SPAudioDataType 2>/dev/null | grep -qiE "麦克风|microphone|输入|input"; then
    ok "检测到音频输入设备"
    "${SPROF}" SPAudioDataType 2>/dev/null | grep -iE "麦克风|microphone|输入|input" | head -6
else
    fail "未检测到录音设备（检查麦克风权限/连接）"
fi
echo ""

# 6. 系统权限（TCC）
echo "【6. 系统权限】"
info "TCC 数据库: ${HOME}/Library/Application Support/com.apple.TCC/TCC.db"
info "  麦克风:   系统设置 → 隐私与安全性 → 麦克风"
info "  屏幕录制: 系统设置 → 隐私与安全性 → 屏幕录制"
echo ""

# 7. MEMORY 与日志
echo "【7. MEMORY 与日志】"
if [[ -f "${MEMORY_FILE}" ]]; then
    BYTES=$(wc -c < "${MEMORY_FILE}" | tr -d ' ')
    ok "MEMORY.md 存在 ($((BYTES/1024)) KB)"
    if [[ ${BYTES} -gt 7680 ]]; then warn "超过7.5KB安全线 → lh --compress-memory run"; fi
else
    warn "MEMORY.md 未找到（${MEMORY_FILE}）"
fi

echo ""
echo "最近日志（龙魂相关）："
if [[ -d "${LOG_DIR}" ]]; then
    ls -lt "${LOG_DIR}"/*.log 2>/dev/null | head -5 || echo "  ${LOG_DIR} 下暂无 .log"
else
    echo "  日志目录 ${LOG_DIR} 不存在"
fi
if [[ -d "${HOME}/Library/Logs" ]]; then
    ls -lt "${HOME}/Library/Logs"/longhun* 2>/dev/null | head -5 || echo "  ~/Library/Logs 下暂无 longhun* 日志"
fi
echo ""

# 8. 快速修复建议
echo "【8. 快速修复命令】"
echo "  修复依赖:     bash ${PROJECT_DIR}/scripts/install_longhun.sh"
echo "  重启 Ollama:  brew services restart ollama"
echo "  前台测试语音: python3 ${BIN_DIR}/voice_input.py"
echo "  说话→Agent:   lh --voice-in"
echo "  截图分析:     lh --screenshot"
echo "  压缩 MEMORY:  lh --compress-memory run"
echo "  打包日志:     bash ${PROJECT_DIR}/scripts/longhun_menu.sh (选 L)"
echo ""
echo "DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-TROUBLESHOOT-MAC-DONE"
