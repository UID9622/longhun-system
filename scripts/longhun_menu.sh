#!/usr/bin/env bash
# ============================================================
# 龍魂感知层 · 总控菜单（macOS 版 v2.0）
# DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-MENU-MAC-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 适配: macOS(launchd) · faster-whisper + moondream · 兼容 bash3
# 功能: 初始化/状态/排查/更新/卸载/服务控制/语音/视觉/日志/权限修复
# 用法: bash scripts/longhun_menu.sh
# ============================================================
set -euo pipefail
# system_profiler 固定绝对路径（执行环境 PATH 可能缺 /usr/sbin；勿动全局 PATH，否则 python3 解析会漂移）
SPROF="/usr/sbin/system_profiler"
[[ -x "${SPROF}" ]] || SPROF="$(command -v system_profiler 2>/dev/null || true)"

PROJECT_DIR="${HOME}/longhun-system"
SCRIPTS_DIR="${PROJECT_DIR}/scripts"
BIN_DIR="${PROJECT_DIR}/bin"
LOG_DIR="${PROJECT_DIR}/logs"
MEMORY_FILE="${PROJECT_DIR}/.codebuddy/memory/MEMORY.md"
mkdir -p "${LOG_DIR}" "${SCRIPTS_DIR}"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

REQUIRED_SCRIPTS=(
    "install_longhun.sh"
    "status_longhun.sh"
    "troubleshoot_longhun.sh"
    "update_longhun.sh"
    "uninstall_longhun.sh"
)

# ==================== 进度条（bash3 兼容）====================
progress_bar() {
    local msg="${1:-处理中}"
    local steps=12
    echo -ne "  ${CYAN}${msg} ${NC}"
    for ((i=1; i<=steps; i++)); do
        printf "${CYAN}█${NC}"
        sleep 0.05
    done
    echo -e " ${GREEN}✓${NC}"
}

# ==================== 一键修复脚本权限 ====================
fix_permissions() {
    echo ""
    echo -e "${BOLD}${CYAN}【一键修复脚本权限】${NC}"
    echo ""
    local fixed=0
    for f in "${SCRIPTS_DIR}"/*.sh; do
        [[ -f "$f" ]] || continue
        if [[ ! -x "$f" ]]; then
            chmod +x "$f" && echo -e "  ${GREEN}✓${NC} 已修复: $(basename "$f")" && fixed=$((fixed + 1))
        fi
    done
    [[ -f "${BIN_DIR}/voice_input.py" ]] && chmod +x "${BIN_DIR}/voice_input.py" 2>/dev/null || true
    [[ -f "${BIN_DIR}/vision_input.py" ]] && chmod +x "${BIN_DIR}/vision_input.py" 2>/dev/null || true
    echo ""
    if [[ ${fixed} -gt 0 ]]; then echo -e "${GREEN}共修复 ${fixed} 个脚本权限${NC}"; else echo -e "${GREEN}所有脚本权限正常${NC}"; fi
    echo ""
    read -p "按回车键返回菜单..."
}

# ==================== 麦克风测试（限时·无 timeout 命令用 python alarm）====================
test_microphone() {
    echo ""
    echo -e "${BOLD}${CYAN}【一键测试麦克风】${NC}"
    echo -e "${DIM}将录音约 15 秒并尝试转写，请对着麦克风说话...${NC}"
    echo ""
    progress_bar "准备录音"

    if [[ ! -f "${BIN_DIR}/voice_input.py" ]]; then
        echo -e "${RED}✗ 找不到 voice_input.py${NC}"
        read -p "按回车键返回..."
        return
    fi
    if ! "${SPROF}" SPAudioDataType 2>/dev/null | grep -qiE "麦克风|microphone|输入|input"; then
        echo -e "${YELLOW}! 未检测到音频输入设备（检查麦克风权限/连接）${NC}"
        read -p "按回车键返回..."
        return
    fi

    echo -e "${YELLOW}提示：15 秒后自动停止。若只见录音未见转写，是模型首次加载慢（small 约150MB）。${NC}"
    echo ""
    python3 - "${BIN_DIR}/voice_input.py" <<'PYEOF'
import sys, signal, subprocess
def handler(sig, frame):
    raise TimeoutError
signal.signal(signal.SIGALRM, handler)
signal.alarm(20)
try:
    subprocess.run([sys.executable, sys.argv[1]])
except TimeoutError:
    print("\n[20 秒限时到，录音已自动结束]")
PYEOF

    echo ""
    echo -e "${GREEN}麦克风测试结束${NC}"
    read -p "按回车键返回菜单..."
}

# ==================== 视觉截图测试 ====================
test_vision() {
    echo ""
    echo -e "${BOLD}${CYAN}【一键测试视觉截图】${NC}"
    echo ""
    progress_bar "正在截图并分析"

    if [[ ! -f "${BIN_DIR}/vision_input.py" ]]; then
        echo -e "${RED}✗ 找不到 vision_input.py${NC}"
        read -p "按回车键返回..."
        return
    fi
    python3 "${BIN_DIR}/vision_input.py" --screenshot "请用简洁中文描述当前屏幕的主要内容和任何异常" || true

    echo ""
    echo -e "${GREEN}视觉测试完成${NC}"
    read -p "按回车键返回菜单..."
}

# ==================== 导出日志打包（无 journalctl → 收集系统信息）====================
export_logs() {
    echo ""
    echo -e "${BOLD}${CYAN}【导出日志打包】${NC}"
    echo ""
    local timestamp
    timestamp=$(date +%Y%m%d_%H%M%S)
    local export_file="${LOG_DIR}/longhun_logs_${timestamp}.tar.gz"

    progress_bar "收集日志"

    {
        echo "=== 龍魂日志导出 ${timestamp} ==="
        echo "用户: $(whoami)"
        echo "主机: $(hostname)"
        echo ""
        echo "=== launchd 龍魂相关 ==="
        launchctl list 2>/dev/null | grep -E "longhun|ollama" || echo "无"
        echo ""
        echo "=== 关键端口 ==="
        for port in 11434 9631 8082; do
            if lsof -i :${port} -sTCP:LISTEN -t >/dev/null 2>&1; then
                echo ":${port} ✅ 监听中"
            else
                echo ":${port} 未监听"
            fi
        done
        echo ""
        echo "=== 感知层模块 ==="
        ls -la "${BIN_DIR}"/voice_input.py "${BIN_DIR}"/vision_input.py 2>/dev/null || echo "模块缺失"
        echo ""
        echo "=== MEMORY.md 末尾 30 行 ==="
        tail -n 30 "${MEMORY_FILE}" 2>/dev/null || echo "无 MEMORY.md"
        echo ""
        echo "=== 音频设备 ==="
        "${SPROF}" SPAudioDataType 2>/dev/null | head -20 || echo "无法读取"
    } > "${LOG_DIR}/export_temp.txt"

    tar -czf "${export_file}" -C "${LOG_DIR}" export_temp.txt 2>/dev/null || true
    rm -f "${LOG_DIR}/export_temp.txt"

    if [[ -f "${export_file}" ]]; then
        echo -e "${GREEN}✓ 日志已打包：${NC}"
        echo -e "  ${export_file}"
        echo -e "文件大小: $(du -h "${export_file}" | cut -f1)"
    else
        echo -e "${RED}打包失败${NC}"
    fi
    echo ""
    read -p "按回车键返回菜单..."
}

# ==================== 界面 ====================
print_header() {
    clear 2>/dev/null || true
    echo -e "${CYAN}${BOLD}"
    echo "╔══════════════════════════════════════════════════════╗"
    echo "║             龍魂感知层 · 总控菜单 v2.0              ║"
    echo "║        DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-MENU-MAC-v2.0        ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "  项目目录 : ${DIM}${PROJECT_DIR}${NC}"
    echo -e "  当前时间 : $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
}

check_scripts() {
    local missing=0
    echo -e "${BOLD}【脚本完整性检查】${NC}"
    for script in "${REQUIRED_SCRIPTS[@]}"; do
        if [[ -f "${SCRIPTS_DIR}/${script}" ]]; then
            if [[ -x "${SCRIPTS_DIR}/${script}" ]]; then
                echo -e "  ${GREEN}✓${NC} ${script}"
            else
                echo -e "  ${YELLOW}!${NC} ${script}  ${YELLOW}(无执行权限)${NC}"
                missing=$((missing + 1))
            fi
        else
            echo -e "  ${RED}✗${NC} ${script}  ${RED}(缺失)${NC}"
            missing=$((missing + 1))
        fi
    done
    if [[ ${missing} -gt 0 ]]; then
        echo -e "\n${YELLOW}发现问题，可按「A」一键修复权限 / 「1」跑初始化${NC}"
    else
        echo -e "  ${GREEN}所有核心脚本完整且可执行${NC}"
    fi
    echo ""
}

show_service_status() {
    echo -e "${BOLD}【服务状态】${NC}"
    if curl -sf http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo -e "  Ollama     : ${GREEN}● 运行中${NC} (:11434)"
    else
        echo -e "  Ollama     : ${RED}○ 已停止${NC} (视觉不可用)"
    fi
    if [[ -f "${HOME}/Library/LaunchAgents/com.longhun.voice.plist" ]]; then
        if launchctl list com.longhun.voice >/dev/null 2>&1; then
            echo -e "  语音守护   : ${GREEN}● 运行中${NC}"
        else
            echo -e "  语音守护   : ${YELLOW}○ 未加载${NC}"
        fi
    else
        echo -e "  语音守护   : ${DIM}未安装（前台可用 lh --voice-in）${NC}"
    fi
    echo ""
}

# 限时语音主测试（菜单 7）
voice_stream() {
    echo -e "${CYAN}→ 启动语音输入（说几句话，静音 1.2 秒自动停止）${NC}"
    python3 - "${BIN_DIR}/voice_input.py" <<'PYEOF'
import sys, signal, subprocess
def handler(sig, frame):
    raise TimeoutError
signal.signal(signal.SIGALRM, handler)
signal.alarm(60)
try:
    subprocess.run([sys.executable, sys.argv[1]])
except TimeoutError:
    print("\n[60 秒限时到，自动结束]")
PYEOF
}

run_script() {
    local script="$1"
    local full_path="${SCRIPTS_DIR}/${script}"
    if [[ ! -f "${full_path}" ]]; then
        echo -e "${RED}✗ 脚本不存在：${script}${NC}"
        read -p "按回车键返回..."
        return 1
    fi
    [[ ! -x "${full_path}" ]] && chmod +x "${full_path}"
    echo -e "${CYAN}→ 正在执行 ${script} ...${NC}"
    echo ""
    bash "${full_path}"
    echo ""
    read -p "按回车键返回菜单..."
}

service_control() {
    while true; do
        clear 2>/dev/null || true
        echo -e "${CYAN}${BOLD}【服务控制 · launchd】${NC}"
        echo ""
        show_service_status
        echo "  1) 重启 Ollama（视觉依赖）"
        echo "  2) 端口监听检查（11434/9631/8082）"
        echo "  3) 语音守护控制（若已安装）"
        echo "  0) 返回主菜单"
        echo ""
        read -p "请选择: " sc
        case $sc in
            1)
                progress_bar "重启 Ollama"
                launchctl kickstart -k "gui/$(id -u)/homebrew.mxcl.ollama" >/dev/null 2>&1 \
                    && echo -e "${GREEN}✓ Ollama 已重启${NC}" \
                    || (brew services restart ollama >/dev/null 2>&1 && echo -e "${GREEN}✓ 已通过 brew 重启${NC}" || echo -e "${RED}重启失败${NC}")
                sleep 1.2
                ;;
            2)
                for port in 11434 9631 8082; do
                    if lsof -i :${port} -sTCP:LISTEN -t >/dev/null 2>&1; then
                        echo -e "  ${GREEN}●${NC} :${port} 监听中"
                    else
                        echo -e "  ${RED}○${NC} :${port} 未监听"
                    fi
                done
                echo ""
                read -p "按回车键返回..."
                ;;
            3)
                local plist_file="${HOME}/Library/LaunchAgents/com.longhun.voice.plist"
                if [[ -f "${plist_file}" ]]; then
                    echo "  1) 加载  2) 卸载  0) 返回"
                    read -p "请选择: " vc
                    case $vc in
                        1) launchctl load "${plist_file}" && echo -e "${GREEN}✓ 已加载${NC}" || echo -e "${RED}失败${NC}"; sleep 1 ;;
                        2) launchctl unload "${plist_file}" && echo -e "${GREEN}✓ 已卸载${NC}" || echo -e "${RED}失败${NC}"; sleep 1 ;;
                        *) : ;;
                    esac
                else
                    echo -e "${YELLOW}语音守护未安装。可用前台模式: lh --voice-in${NC}"
                    read -p "按回车键返回..."
                fi
                ;;
            0) return ;;
            *) echo -e "${RED}无效选项${NC}"; sleep 1 ;;
        esac
    done
}

# ==================== 主循环 ====================
while true; do
    print_header
    check_scripts
    show_service_status

    echo -e "${BOLD}${GREEN}【核心操作】${NC}"
    echo -e "  ${CYAN}1${NC}) 一键初始化 / 依赖修复"
    echo -e "  ${CYAN}2${NC}) 状态检查"
    echo -e "  ${CYAN}3${NC}) 故障排查"
    echo -e "  ${CYAN}4${NC}) 安全更新（带备份+回滚提示）"
    echo -e "  ${CYAN}5${NC}) 卸载（默认冻结归档）"
    echo ""
    echo -e "${BOLD}${GREEN}【服务与运行】${NC}"
    echo -e "  ${CYAN}6${NC}) 服务控制（launchd 启停/端口/日志）"
    echo -e "  ${CYAN}7${NC}) 语音输入测试（限时）"
    echo -e "  ${CYAN}8${NC}) 立即压缩 MEMORY.md"
    echo ""
    echo -e "${BOLD}${GREEN}【测试与工具】${NC}"
    echo -e "  ${CYAN}M${NC}) 一键测试麦克风"
    echo -e "  ${CYAN}V${NC}) 一键测试视觉截图"
    echo -e "  ${CYAN}L${NC}) 导出日志打包"
    echo -e "  ${CYAN}A${NC}) 一键修复脚本权限"
    echo -e "  ${CYAN}9${NC}) 打开项目目录"
    echo -e "  ${CYAN}0${NC}) 退出"
    echo ""
    echo -e "${DIM}──────────────────────────────────────────────────────${NC}"
    read -p "请输入选项: " choice

    case $choice in
        1) run_script "install_longhun.sh" ;;
        2) run_script "status_longhun.sh" ;;
        3) run_script "troubleshoot_longhun.sh" ;;
        4) run_script "update_longhun.sh" ;;
        5) run_script "uninstall_longhun.sh" ;;
        6) service_control ;;
        7) voice_stream; echo ""; read -p "按回车键返回菜单..." ;;
        8)
            progress_bar "压缩 MEMORY"
            if [[ -x "${BIN_DIR}/lh.py" || -f "${BIN_DIR}/lh.py" ]]; then
                python3 "${BIN_DIR}/lh.py" --compress-memory run || true
            else
                echo -e "${RED}✗ lh.py 缺失${NC}"
            fi
            read -p "按回车键返回菜单..."
            ;;
        M|m) test_microphone ;;
        V|v) test_vision ;;
        L|l) export_logs ;;
        A|a) fix_permissions ;;
        9)
            command -v open >/dev/null 2>&1 && open "${PROJECT_DIR}" || echo -e "项目目录: ${PROJECT_DIR}"
            read -p "按回车键返回菜单..."
            ;;
        0)
            echo -e "\n${GREEN}已退出總控菜單。${NC}"
            echo -e "${DIM}DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-MENU-MAC-EXIT${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}无效选项${NC}"
            sleep 1.1
            ;;
    esac
done
