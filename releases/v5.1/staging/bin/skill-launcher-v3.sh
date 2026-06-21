##龍芯⚡️2026-06-21-TOOL-SKILL-LAUNCHER-V3-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  UID9622⚡️2026-06-16-SKILL-LAUNCHER-v3.0-longhun                              ║
# ║  龍芯北辰·诸葛鑫 — 龍魂工具库一键启动脚本（已適配 longhun-system 主幹）           ║
# ║  忠(0.5) > 孝(0.3) > 义(0.2) 排序铁律                                          ║
# ║  确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                              全局配置区
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCRIPT_VERSION="3.0-longhun"
SCRIPT_DATE="2026-06-16"
UID_TAG="UID9622"
DNA_SIGNATURE="${UID_TAG}⚡️${SCRIPT_DATE}-SKILL-LAUNCHER-v${SCRIPT_VERSION}"
CONFIRM_CODE="#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 自動定位 longhun-system 根目錄：本腳本位於 bin/ 下
LAUNCHER_DIR="$(cd "$(dirname "$0")" && pwd)"
if [[ "$(basename "$LAUNCHER_DIR")" == "bin" ]]; then
    LONGHUN_DIR="$(cd "$LAUNCHER_DIR/.." && pwd)"
else
    LONGHUN_DIR="$LAUNCHER_DIR"
fi
ASSETS_DIR="${LONGHUN_DIR}/skills"
HTML_ASSETS_DIR="${ASSETS_DIR}/html-skills"
PY_ASSETS_DIR="${ASSETS_DIR}/py-skills"
LOG_DIR="${LONGHUN_DIR}/logs"
LOG_FILE="${LOG_DIR}/skill-launcher-v3-$(date +%Y%m%d-%H%M%S).log"
PID_FILE="${LOG_DIR}/.skill-launcher-v3.pid"

# 三色审计标记
AUDIT_PASS="🟢通过"
AUDIT_WARN="🟡标记"
AUDIT_BLOCK="🔴阻断"

# 彩色输出定义
CLR_RESET="\033[0m"
CLR_RED="\033[31m"
CLR_GREEN="\033[32m"
CLR_YELLOW="\033[33m"
CLR_BLUE="\033[34m"
CLR_MAGENTA="\033[35m"
CLR_CYAN="\033[36m"
CLR_WHITE="\033[37m"
CLR_BOLD="\033[1m"
CLR_DIM="\033[2m"

# 工具状态追踪数组
declare -A TOOL_STATUS
declare -A TOOL_PID
declare -A TOOL_TYPE
declare -A TOOL_PRIORITY

# 启动模式
MODE="all"            # all | html-only | python-only | single
SINGLE_TOOL=""        # 单工具编号
DRY_RUN=false         # 干运行模式
VERBOSE=false         # 详细输出
NO_BROWSER=false      # 不自动打开浏览器

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                              工具清单定义
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 排序铁律: 忠(0.5) > 孝(0.3) > 义(0.2)
# HTML工具编号 1-5, Python工具编号 6-10

# ---- HTML工具 (1-5) ----
HTML_TOOLS=(
    "1|algorithmic-art|skill-1-algorithmic-art.html|算法艺术生成器|0.5"
    "2|brand-guidelines|skill-2-brand-guidelines.html|龍魂品牌指南|0.5"
    "3|canvas-design|skill-3-canvas-design.html|画布设计工具|0.3"
    "4|doc-coauthoring|skill-4-doc-coauthoring.html|文档协作工具|0.3"
    "5|internal-comms|skill-5-internal-comms.html|内部通讯系统|0.2"
)

# ---- Python工具 (6-10) ----
PYTHON_TOOLS=(
    "6|mcp-builder|skill-6-mcp-builder.py|MCP服务器构建器|0.5"
    "7|skill-creator|skill-7-skill-creator.py|技能创建框架|0.5"
    "8|slack-gif-creator|skill-8-slack-gif-creator.py|Slack GIF生成器|0.3"
    "9|theme-factory|skill-9-theme-factory.py|主题工厂|0.3"
    "10|web-artifacts-builder|skill-10-web-artifacts-builder.py|Web工件构建器|0.2"
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                              核心函数区
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ---- 日志函数 ----
log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local color=""
    local prefix=""

    case "$level" in
        INFO)  color="${CLR_BLUE}";   prefix="[ℹ️ INFO]" ;;
        OK)    color="${CLR_GREEN}";  prefix="[✅ OK  ]" ;;
        WARN)  color="${CLR_YELLOW}"; prefix="[⚠️ WARN]" ;;
        ERROR) color="${CLR_RED}";    prefix="[❌ ERR ]" ;;
        DNA)   color="${CLR_MAGENTA}"; prefix="[🧬 DNA ]" ;;
        STEP)  color="${CLR_CYAN}";   prefix="[⚡ STEP]" ;;
        AUDIT) color="${CLR_CYAN}";   prefix="[📊 AUDIT]" ;;
    esac

    # 控制台输出
    echo -e "${color}${prefix} ${message}${CLR_RESET}"

    # 文件日志
    mkdir -p "${LOG_DIR}"
    echo "[${timestamp}] ${prefix} ${message}" >> "${LOG_FILE}" 2>/dev/null
}

# ---- 横幅显示 ----
show_banner() {
    echo -e "${CLR_CYAN}${CLR_BOLD}"
    cat << 'BANNER'
╔══════════════════════════════════════════════════════════════════════════════╗
║   ███████╗██╗  ██╗██╗██╗     ██╗     ██╗      █████╗ ██╗   ██╗███╗   ██╗   ║
║   ██╔════╝██║ ██╔╝██║██║     ██║     ██║     ██╔══██╗██║   ██║████╗  ██║   ║
║   ███████╗█████╔╝ ██║██║     ██║     ██║     ███████║██║   ██║██╔██╗ ██║   ║
║   ╚════██║██╔═██╗ ██║██║     ██║     ██║     ██╔══██║██║   ██║██║╚██╗██║   ║
║   ███████║██║  ██╗██║███████╗███████╗███████╗██║  ██║╚██████╔╝██║ ╚████║   ║
║   ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║   龍芯北辰·诸葛鑫 — 龍魂工具库一键启动器 v3.0                                 ║
║   忠(0.5) > 孝(0.3) > 义(0.2) 排序铁律                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
BANNER
    echo -e "${CLR_RESET}"
    log DNA "${DNA_SIGNATURE}"
    log DNA "${CONFIRM_CODE}"
    echo ""
}

# ---- 用法说明 ----
show_usage() {
    cat << USAGE
${CLR_BOLD}用法:${CLR_RESET} $(basename "$0") [选项]

${CLR_BOLD}启动模式:${CLR_RESET}
  --all, -a              启动全部10个工具 (默认)
  --html-only, -H        仅启动HTML工具 (1-5)
  --python-only, -P      仅启动Python工具 (6-10)
  --tool, -t <编号>      启动指定编号的单个工具 (1-10)

${CLR_BOLD}附加选项:${CLR_RESET}
  --dry-run, -d          干运行模式，不实际启动任何工具
  --verbose, -v          详细输出模式
  --no-browser, -n       不自动打开浏览器 (HTML工具)
  --stop, -s             优雅停止所有已启动的工具
  --status               显示已启动工具的状态
  --health-check         执行健康检查
  --help, -h             显示此帮助信息
  --version, -V          显示版本信息

${CLR_BOLD}示例:${CLR_RESET}
  $(basename "$0")                     # 启动全部工具
  $(basename "$0") --html-only         # 仅启动HTML工具
  $(basename "$0") --python-only       # 仅启动Python工具
  $(basename "$0") --tool 1            # 仅启动算法艺术生成器
  $(basename "$0") --tool 7,8,9        # 启动指定多个工具
  $(basename "$0") --dry-run           # 干运行测试
  $(basename "$0") --stop              # 停止所有工具

USAGE
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                              环境检测
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

check_environment() {
    log STEP "╔══════════════════════════════════════════╗"
    log STEP "║      环境检测 — 龍魂系统自检               ║"
    log STEP "╚══════════════════════════════════════════╝"

    local env_ok=true

    # ---- 操作系统检测 ----
    local os_type="unknown"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        os_type="macOS"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        os_type="Linux"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        os_type="Windows(兼容)"
    fi
    log INFO "操作系统: ${os_type}"

    # ---- Bash版本检测 ----
    local bash_version="${BASH_VERSION%%[^0-9.]*}"
    log INFO "Bash版本: ${bash_version}"

    # ---- Python检测 ----
    PYTHON_CMD=""
    if command -v python3 &>/dev/null; then
        PYTHON_CMD="python3"
        local py_ver=$($PYTHON_CMD --version 2>&1)
        log OK "Python检测: ${py_ver} ${AUDIT_PASS}"
    elif command -v python &>/dev/null; then
        PYTHON_CMD="python"
        local py_ver=$($PYTHON_CMD --version 2>&1)
        log OK "Python检测: ${py_ver} ${AUDIT_PASS}"
    else
        log WARN "未检测到Python环境 ${AUDIT_WARN}"
        PYTHON_CMD=""
        env_ok=false
    fi

    # ---- 浏览器检测 ----
    BROWSER_CMD=""
    local browsers=("open" "xdg-open" "google-chrome" "chromium" "firefox" "safari" "brave" "edge")
    for browser in "${browsers[@]}"; do
        if command -v "$browser" &>/dev/null; then
            BROWSER_CMD="$browser"
            log OK "浏览器检测: ${browser} 可用 ${AUDIT_PASS}"
            break
        fi
    done
    if [[ -z "$BROWSER_CMD" ]]; then
        log WARN "未检测到可用浏览器 ${AUDIT_WARN}"
        if [[ "$NO_BROWSER" == false && "$MODE" != "python-only" ]]; then
            log WARN "HTML工具将无法自动打开，请手动访问"
        fi
    fi

    # ---- assets目录检测 ----
    if [[ -d "${HTML_ASSETS_DIR}" && -d "${PY_ASSETS_DIR}" ]]; then
        log OK "资源目录: ${HTML_ASSETS_DIR} 与 ${PY_ASSETS_DIR} 存在 ${AUDIT_PASS}"
    else
        log WARN "资源目录不完整 ${AUDIT_WARN}"
        log INFO "期望路径: ${HTML_ASSETS_DIR} 和 ${PY_ASSETS_DIR}"
    fi

    # ---- 工具文件存在性检测 ----
    log INFO ""
    log INFO "工具文件检测:"
    local total_tools=0
    local found_tools=0

    for tool_spec in "${HTML_TOOLS[@]}"; do
        IFS='|' read -r num name filename desc priority <<< "$tool_spec"
        total_tools=$((total_tools + 1))
        local filepath="${HTML_ASSETS_DIR}/${filename}"
        if [[ -f "$filepath" ]]; then
            log OK "  [HTML] #${num} ${name} → ${filename} ${AUDIT_PASS}"
            found_tools=$((found_tools + 1))
        else
            log WARN "  [HTML] #${num} ${name} → ${filename} 未找到 ${AUDIT_WARN}"
        fi
    done

    for tool_spec in "${PYTHON_TOOLS[@]}"; do
        IFS='|' read -r num name filename desc priority <<< "$tool_spec"
        total_tools=$((total_tools + 1))
        local filepath="${PY_ASSETS_DIR}/${filename}"
        if [[ -f "$filepath" ]]; then
            log OK "  [PY]   #${num} ${name} → ${filename} ${AUDIT_PASS}"
            found_tools=$((found_tools + 1))
        else
            log WARN "  [PY]   #${num} ${name} → ${filename} 未找到 ${AUDIT_WARN}"
        fi
    done

    log INFO ""
    log INFO "工具文件: ${found_tools}/${total_tools} 就绪"

    # ---- 端口占用检测 (常见开发端口) ----
    log INFO ""
    log INFO "端口占用检测:"
    local common_ports=(3000 5000 8000 8080 9000)
    for port in "${common_ports[@]}"; do
        if lsof -Pi :"$port" -sTCP:LISTEN -t >/dev/null 2>&1 || \
           netstat -tuln 2>/dev/null | grep -q ":${port} " || \
           ss -tuln 2>/dev/null | grep -q ":${port} "; then
            log WARN "  端口 ${port} 已被占用 ${AUDIT_WARN}"
        else
            log OK "  端口 ${port} 可用 ${AUDIT_PASS}"
        fi
    done

    echo ""
    if [[ "$env_ok" == true ]]; then
        log OK "环境检测完成 ✓ 系统就绪"
    else
        log WARN "环境检测完成 ⚠ 部分依赖缺失"
    fi
    echo ""
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                              参数解析
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --all|-a)
                MODE="all"
                shift
                ;;
            --html-only|-H)
                MODE="html-only"
                shift
                ;;
            --python-only|-P)
                MODE="python-only"
                shift
                ;;
            --tool|-t)
                if [[ -n "$2" && "$2" != --* ]]; then
                    SINGLE_TOOL="$2"
                    MODE="single"
                    shift 2
                else
                    log ERROR "--tool 需要指定工具编号 (1-10)"
                    exit 1
                fi
                ;;
            --dry-run|-d)
                DRY_RUN=true
                log WARN "干运行模式已启用 — 不会实际启动任何工具"
                shift
                ;;
            --verbose|-v)
                VERBOSE=true
                shift
                ;;
            --no-browser|-n)
                NO_BROWSER=true
                shift
                ;;
            --stop|-s)
                graceful_stop
                exit 0
                ;;
            --status)
                show_status
                exit 0
                ;;
            --health-check)
                health_check
                exit 0
                ;;
            --help|-h)
                show_banner
                show_usage
                exit 0
                ;;
            --version|-V)
                echo "SKILL-LAUNCHER v${SCRIPT_VERSION} — ${DNA_SIGNATURE}"
                exit 0
                ;;
            *)
                log ERROR "未知参数: $1"
                show_usage
                exit 1
                ;;
        esac
    done
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                              HTML工具启动
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

launch_html_tool() {
    local num="$1"
    local name="$2"
    local filename="$3"
    local desc="$4"
    local priority="$5"
    local filepath="${HTML_ASSETS_DIR}/${filename}"

    log STEP "启动HTML工具 #${num} — ${desc} (优先级:${priority})"

    # 文件存在性检查
    if [[ ! -f "$filepath" ]]; then
        TOOL_STATUS[$num]="文件缺失"
        log ERROR "  ${AUDIT_BLOCK} 文件未找到: ${filepath}"
        return 1
    fi

    # 获取绝对路径
    local abs_path
    abs_path=$(cd "$(dirname "$filepath")" && pwd)/$(basename "$filepath")

    if [[ "$DRY_RUN" == true ]]; then
        log INFO "  [干运行] 将打开: ${abs_path}"
        TOOL_STATUS[$num]="干运行"
        return 0
    fi

    if [[ "$NO_BROWSER" == true ]]; then
        log WARN "  ${AUDIT_WARN} --no-browser 已设置，跳过自动打开"
        log INFO "  请手动访问: file://${abs_path}"
        TOOL_STATUS[$num]="手动打开"
        return 0
    fi

    if [[ -z "$BROWSER_CMD" ]]; then
        log WARN "  ${AUDIT_WARN} 无可用浏览器"
        log INFO "  请手动访问: file://${abs_path}"
        TOOL_STATUS[$num]="手动打开"
        return 0
    fi

    # 根据浏览器类型选择打开方式
    case "$BROWSER_CMD" in
        open)
            # macOS
            open "file://${abs_path}" &
            TOOL_PID[$num]=$!
            ;;
        xdg-open)
            # Linux
            xdg-open "file://${abs_path}" &
            TOOL_PID[$num]=$!
            ;;
        *)
            $BROWSER_CMD "file://${abs_path}" &
            TOOL_PID[$num]=$!
            ;;
    esac

    TOOL_STATUS[$num]="已启动"
    TOOL_TYPE[$num]="HTML"
    TOOL_PRIORITY[$num]="$priority"

    log OK "  ${AUDIT_PASS} #${num} ${name} 已在浏览器中打开"

    # 保存PID到PID文件
    echo "html:${num}:${TOOL_PID[$num]}" >> "$PID_FILE"

    return 0
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                              Python工具启动
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

launch_python_tool() {
    local num="$1"
    local name="$2"
    local filename="$3"
    local desc="$4"
    local priority="$5"
    local filepath="${PY_ASSETS_DIR}/${filename}"

    log STEP "启动Python工具 #${num} — ${desc} (优先级:${priority})"

    # Python环境检查
    if [[ -z "$PYTHON_CMD" ]]; then
        TOOL_STATUS[$num]="Python缺失"
        log ERROR "  ${AUDIT_BLOCK} 未检测到Python环境，无法启动 #${num} ${name}"
        return 1
    fi

    # 文件存在性检查
    if [[ ! -f "$filepath" ]]; then
        TOOL_STATUS[$num]="文件缺失"
        log ERROR "  ${AUDIT_BLOCK} 文件未找到: ${filepath}"
        return 1
    fi

    # 文件可执行权限检查
    if [[ ! -r "$filepath" ]]; then
        log WARN "  ${AUDIT_WARN} 文件无读权限，尝试修复..."
        chmod +r "$filepath" 2>/dev/null || true
    fi

    if [[ "$DRY_RUN" == true ]]; then
        log INFO "  [干运行] 将执行: ${PYTHON_CMD} ${filepath}"
        TOOL_STATUS[$num]="干运行"
        return 0
    fi

    # 切换到assets目录执行，确保相对路径正确
    local work_dir=$(dirname "$filepath")
    local script_name=$(basename "$filepath")

    log INFO "  工作目录: ${work_dir}"
    log INFO "  执行命令: ${PYTHON_CMD} ${script_name}"

    # 后台启动Python工具，捕获输出到日志
    (
        cd "$work_dir" || exit 1
        $PYTHON_CMD "$script_name" >> "${LOG_FILE}" 2>&1 &
        echo $!
    ) > /tmp/.skill_pid_$$_${num}.tmp

    local pid=$(cat /tmp/.skill_pid_$$_${num}.tmp 2>/dev/null)
    rm -f /tmp/.skill_pid_$$_${num}.tmp

    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
        TOOL_PID[$num]=$pid
        TOOL_STATUS[$num]="运行中"
        TOOL_TYPE[$num]="Python"
        TOOL_PRIORITY[$num]="$priority"

        # 短暂等待确认进程存活
        sleep 0.5
        if kill -0 "$pid" 2>/dev/null; then
            log OK "  ${AUDIT_PASS} #${num} ${name} 已启动 (PID:${pid})"
        else
            log WARN "  ${AUDIT_WARN} #${num} ${name} 进程可能已退出"
            TOOL_STATUS[$num]="已退出"
        fi

        # 保存PID到PID文件
        echo "python:${num}:${pid}" >> "$PID_FILE"
    else
        TOOL_STATUS[$num]="启动失败"
        log ERROR "  ${AUDIT_BLOCK} #${num} ${name} 启动失败"
        return 1
    fi

    return 0
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                              优雅停止
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

graceful_stop() {
    log STEP "╔══════════════════════════════════════════╗"
    log STEP "║      优雅停止 — 龍魂工具终止               ║"
    log STEP "╚══════════════════════════════════════════╝"

    if [[ ! -f "$PID_FILE" ]]; then
        log WARN "没有找到PID文件，尝试检测已启动的工具进程..."

        # 尝试从TOOL_PID数组停止
        local stopped=0
        for num in "${!TOOL_PID[@]}"; do
            local pid="${TOOL_PID[$num]}"
            if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
                log INFO "停止工具 #${num} (PID:${pid})..."
                kill "$pid" 2>/dev/null
                sleep 0.5
                if kill -0 "$pid" 2>/dev/null; then
                    kill -9 "$pid" 2>/dev/null
                fi
                stopped=$((stopped + 1))
            fi
        done

        if [[ $stopped -eq 0 ]]; then
            log WARN "没有发现需要停止的进程"
        else
            log OK "已停止 ${stopped} 个工具进程"
        fi
        return 0
    fi

    local stopped=0
    while IFS= read -r line; do
        local type=$(echo "$line" | cut -d: -f1)
        local num=$(echo "$line" | cut -d: -f2)
        local pid=$(echo "$line" | cut -d: -f3)

        if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
            log INFO "停止 ${type}工具 #${num} (PID:${pid})..."

            # 先尝试SIGTERM
            kill "$pid" 2>/dev/null
            sleep 1

            # 如果仍在运行，使用SIGKILL
            if kill -0 "$pid" 2>/dev/null; then
                log WARN "  进程未响应SIGTERM，强制终止..."
                kill -9 "$pid" 2>/dev/null
            fi

            stopped=$((stopped + 1))
        fi
    done < "$PID_FILE"

    # 清理PID文件
    rm -f "$PID_FILE"

    if [[ $stopped -eq 0 ]]; then
        log WARN "没有发现需要停止的进程"
    else
        log OK "已优雅停止 ${stopped} 个工具进程"
    fi

    log OK "龍魂工具已全部停止 ✓"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                              状态显示
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

show_status() {
    log STEP "╔══════════════════════════════════════════╗"
    log STEP "║      状态查询 — 龍魂工具运行状态           ║"
    log STEP "╚══════════════════════════════════════════╝"

    if [[ ! -f "$PID_FILE" ]]; then
        log WARN "没有找到PID文件，暂无工具在运行"
        return 0
    fi

    echo -e "${CLR_BOLD}┌──────┬─────────────────────┬──────────┬─────────────┬──────────┐${CLR_RESET}"
    echo -e "${CLR_BOLD}│ 编号 │ 名称                │ 类型     │ 状态        │ PID      │${CLR_RESET}"
    echo -e "${CLR_BOLD}├──────┼─────────────────────┼──────────┼─────────────┼──────────┤${CLR_RESET}"

    while IFS= read -r line; do
        local type=$(echo "$line" | cut -d: -f1)
        local num=$(echo "$line" | cut -d: -f2)
        local pid=$(echo "$line" | cut -d: -f3)

        # 获取工具名称
        local name=""
        local tool_spec
        for tool_spec in "${HTML_TOOLS[@]}" "${PYTHON_TOOLS[@]}"; do
            IFS='|' read -r tnum tname tfname tdesc tpriority <<< "$tool_spec"
            if [[ "$tnum" == "$num" ]]; then
                name="$tname"
                break
            fi
        done

        # 检查进程状态
        local status_color="${CLR_RED}"
        local status_text="已停止"
        if kill -0 "$pid" 2>/dev/null; then
            status_color="${CLR_GREEN}"
            status_text="运行中"
        fi

        printf "${CLR_BOLD}│${CLR_RESET} %-4s │ %-19s │ %-8s │ ${status_color}%-11s${CLR_RESET} │ %-8s │\n" \
            "$num" "$name" "$type" "$status_text" "$pid"
    done < "$PID_FILE"

    echo -e "${CLR_BOLD}└──────┴─────────────────────┴──────────┴─────────────┴──────────┘${CLR_RESET}"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                              健康检查
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

health_check() {
    log STEP "╔══════════════════════════════════════════╗"
    log STEP "║      健康检查 — 龍魂系统体检               ║"
    log STEP "╚══════════════════════════════════════════╝"

    local checks_passed=0
    local checks_total=0

    # ---- 检查1: 脚本完整性 ----
    checks_total=$((checks_total + 1))
    if [[ -n "$DNA_SIGNATURE" && -n "$CONFIRM_CODE" ]]; then
        log OK "[1/8] DNA签名验证 ${AUDIT_PASS}"
        checks_passed=$((checks_passed + 1))
    else
        log ERROR "[1/8] DNA签名验证 ${AUDIT_BLOCK}"
    fi

    # ---- 检查2: Python环境 ----
    checks_total=$((checks_total + 1))
    if [[ -n "$PYTHON_CMD" ]]; then
        log OK "[2/8] Python环境 ${AUDIT_PASS}"
        checks_passed=$((checks_passed + 1))
    else
        log WARN "[2/8] Python环境 ${AUDIT_WARN} (Python工具将无法启动)"
    fi

    # ---- 检查3: 浏览器环境 ----
    checks_total=$((checks_total + 1))
    if [[ -n "$BROWSER_CMD" ]]; then
        log OK "[3/8] 浏览器环境 ${AUDIT_PASS}"
        checks_passed=$((checks_passed + 1))
    else
        log WARN "[3/8] 浏览器环境 ${AUDIT_WARN} (HTML工具需手动打开)"
    fi

    # ---- 检查4: 资源目录 ----
    checks_total=$((checks_total + 1))
    if [[ -d "$ASSETS_DIR" ]]; then
        log OK "[4/8] 资源目录 ${AUDIT_PASS}"
        checks_passed=$((checks_passed + 1))
    else
        log WARN "[4/8] 资源目录 ${AUDIT_WARN}"
    fi

    # ---- 检查5: 工具文件存在性 ----
    checks_total=$((checks_total + 1))
    local tools_found=0
    local tools_total=0
    for tool_spec in "${HTML_TOOLS[@]}" "${PYTHON_TOOLS[@]}"; do
        IFS='|' read -r num name filename desc priority <<< "$tool_spec"
        tools_total=$((tools_total + 1))
        if [[ -f "${HTML_ASSETS_DIR}/${filename}" || -f "${PY_ASSETS_DIR}/${filename}" ]]; then
            tools_found=$((tools_found + 1))
        fi
    done
    if [[ $tools_found -eq $tools_total ]]; then
        log OK "[5/8] 工具文件 (${tools_found}/${tools_total}) ${AUDIT_PASS}"
        checks_passed=$((checks_passed + 1))
    elif [[ $tools_found -gt 0 ]]; then
        log WARN "[5/8] 工具文件 (${tools_found}/${tools_total}) ${AUDIT_WARN}"
    else
        log ERROR "[5/8] 工具文件 (0/${tools_total}) ${AUDIT_BLOCK}"
    fi

    # ---- 检查6: 日志目录可写 ----
    checks_total=$((checks_total + 1))
    if mkdir -p "$LOG_DIR" 2>/dev/null && touch "$LOG_FILE" 2>/dev/null; then
        log OK "[6/8] 日志系统 ${AUDIT_PASS}"
        checks_passed=$((checks_passed + 1))
    else
        log ERROR "[6/8] 日志系统 ${AUDIT_BLOCK}"
    fi

    # ---- 检查7: 磁盘空间 ----
    checks_total=$((checks_total + 1))
    local disk_usage=$(df "$LAUNCHER_DIR" 2>/dev/null | tail -1 | awk '{print $5}' | tr -d '%')
    # 确保disk_usage是纯数字
    if [[ "$disk_usage" =~ ^[0-9]+$ && "$disk_usage" -lt 90 ]]; then
        log OK "[7/8] 磁盘空间 (${disk_usage}% 已用) ${AUDIT_PASS}"
        checks_passed=$((checks_passed + 1))
    elif [[ "$disk_usage" =~ ^[0-9]+$ ]]; then
        log WARN "[7/8] 磁盘空间 (${disk_usage}% 已用) ${AUDIT_WARN}"
    else
        log WARN "[7/8] 磁盘空间 (无法检测) ${AUDIT_WARN}"
    fi

    # ---- 检查8: 网络连接 ----
    checks_total=$((checks_total + 1))
    if ping -c 1 -W 3 8.8.8.8 >/dev/null 2>&1 || ping -c 1 -W 3 114.114.114.114 >/dev/null 2>&1; then
        log OK "[8/8] 网络连接 ${AUDIT_PASS}"
        checks_passed=$((checks_passed + 1))
    else
        log WARN "[8/8] 网络连接 ${AUDIT_WARN} (离线模式不影响本地工具)"
    fi

    # 汇总
    echo ""
    local pass_rate=$((checks_passed * 100 / checks_total))
    if [[ $pass_rate -ge 80 ]]; then
        log OK "健康检查完成: ${checks_passed}/${checks_total} 通过 (${pass_rate}%)"
        log OK "${AUDIT_PASS} 系统状态: 良好"
    elif [[ $pass_rate -ge 50 ]]; then
        log WARN "健康检查完成: ${checks_passed}/${checks_total} 通过 (${pass_rate}%)"
        log WARN "${AUDIT_WARN} 系统状态: 部分可用"
    else
        log ERROR "健康检查完成: ${checks_passed}/${checks_total} 通过 (${pass_rate}%)"
        log ERROR "${AUDIT_BLOCK} 系统状态: 需要修复"
    fi

    return $((checks_total - checks_passed))
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                              启动主逻辑
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

execute_launch() {
    log STEP "╔══════════════════════════════════════════╗"
    log STEP "║      启动执行 — 龍魂工具启动序列           ║"
    log STEP "╚══════════════════════════════════════════╝"

    # 清除旧PID文件
    rm -f "$PID_FILE"
    touch "$PID_FILE"

    local launched=0
    local failed=0
    local skipped=0

    # ---- 忠(0.5)优先级工具先启动 ----
    log INFO ""
    log INFO "${CLR_BOLD}${CLR_YELLOW}>>> 第一批: 忠(0.5) 优先级 — 核心工具${CLR_RESET}"
    echo ""

    if [[ "$MODE" == "all" || "$MODE" == "html-only" || "$MODE" == "single" ]]; then
        for tool_spec in "${HTML_TOOLS[@]}"; do
            IFS='|' read -r num name filename desc priority <<< "$tool_spec"
            if [[ "$priority" == "0.5" ]]; then
                if [[ "$MODE" == "single" && ",${SINGLE_TOOL}," != *",${num},"* ]]; then
                    continue
                fi
                launch_html_tool "$num" "$name" "$filename" "$desc" "$priority"
                local rc=$?
                if [[ $rc -eq 0 ]]; then
                    launched=$((launched + 1))
                else
                    failed=$((failed + 1))
                fi
                echo ""
            fi
        done
    fi

    if [[ "$MODE" == "all" || "$MODE" == "python-only" || "$MODE" == "single" ]]; then
        for tool_spec in "${PYTHON_TOOLS[@]}"; do
            IFS='|' read -r num name filename desc priority <<< "$tool_spec"
            if [[ "$priority" == "0.5" ]]; then
                if [[ "$MODE" == "single" && ",${SINGLE_TOOL}," != *",${num},"* ]]; then
                    continue
                fi
                launch_python_tool "$num" "$name" "$filename" "$desc" "$priority"
                local rc=$?
                if [[ $rc -eq 0 ]]; then
                    launched=$((launched + 1))
                else
                    failed=$((failed + 1))
                fi
                echo ""
            fi
        done
    fi

    # ---- 孝(0.3)优先级工具 ----
    log INFO ""
    log INFO "${CLR_BOLD}${CLR_CYAN}>>> 第二批: 孝(0.3) 优先级 — 重要工具${CLR_RESET}"
    echo ""

    if [[ "$MODE" == "all" || "$MODE" == "html-only" || "$MODE" == "single" ]]; then
        for tool_spec in "${HTML_TOOLS[@]}"; do
            IFS='|' read -r num name filename desc priority <<< "$tool_spec"
            if [[ "$priority" == "0.3" ]]; then
                if [[ "$MODE" == "single" && ",${SINGLE_TOOL}," != *",${num},"* ]]; then
                    continue
                fi
                launch_html_tool "$num" "$name" "$filename" "$desc" "$priority"
                local rc=$?
                if [[ $rc -eq 0 ]]; then
                    launched=$((launched + 1))
                else
                    failed=$((failed + 1))
                fi
                echo ""
            fi
        done
    fi

    if [[ "$MODE" == "all" || "$MODE" == "python-only" || "$MODE" == "single" ]]; then
        for tool_spec in "${PYTHON_TOOLS[@]}"; do
            IFS='|' read -r num name filename desc priority <<< "$tool_spec"
            if [[ "$priority" == "0.3" ]]; then
                if [[ "$MODE" == "single" && ",${SINGLE_TOOL}," != *",${num},"* ]]; then
                    continue
                fi
                launch_python_tool "$num" "$name" "$filename" "$desc" "$priority"
                local rc=$?
                if [[ $rc -eq 0 ]]; then
                    launched=$((launched + 1))
                else
                    failed=$((failed + 1))
                fi
                echo ""
            fi
        done
    fi

    # ---- 义(0.2)优先级工具最后 ----
    log INFO ""
    log INFO "${CLR_BOLD}${CLR_MAGENTA}>>> 第三批: 义(0.2) 优先级 — 辅助工具${CLR_RESET}"
    echo ""

    if [[ "$MODE" == "all" || "$MODE" == "html-only" || "$MODE" == "single" ]]; then
        for tool_spec in "${HTML_TOOLS[@]}"; do
            IFS='|' read -r num name filename desc priority <<< "$tool_spec"
            if [[ "$priority" == "0.2" ]]; then
                if [[ "$MODE" == "single" && ",${SINGLE_TOOL}," != *",${num},"* ]]; then
                    continue
                fi
                launch_html_tool "$num" "$name" "$filename" "$desc" "$priority"
                local rc=$?
                if [[ $rc -eq 0 ]]; then
                    launched=$((launched + 1))
                else
                    failed=$((failed + 1))
                fi
                echo ""
            fi
        done
    fi

    if [[ "$MODE" == "all" || "$MODE" == "python-only" || "$MODE" == "single" ]]; then
        for tool_spec in "${PYTHON_TOOLS[@]}"; do
            IFS='|' read -r num name filename desc priority <<< "$tool_spec"
            if [[ "$priority" == "0.2" ]]; then
                if [[ "$MODE" == "single" && ",${SINGLE_TOOL}," != *",${num},"* ]]; then
                    continue
                fi
                launch_python_tool "$num" "$name" "$filename" "$desc" "$priority"
                local rc=$?
                if [[ $rc -eq 0 ]]; then
                    launched=$((launched + 1))
                else
                    failed=$((failed + 1))
                fi
                echo ""
            fi
        done
    fi

    # ---- 汇总 ----
    echo ""
    log STEP "╔══════════════════════════════════════════╗"
    log STEP "║      启动汇总 — 龍魂系统状态报告           ║"
    log STEP "╚══════════════════════════════════════════╝"

    echo -e "${CLR_BOLD}┌──────┬─────────────────────┬──────────┬───────────┬──────────┐${CLR_RESET}"
    echo -e "${CLR_BOLD}│ 编号 │ 名称                │ 类型     │ 优先级    │ 状态     │${CLR_RESET}"
    echo -e "${CLR_BOLD}├──────┼─────────────────────┼──────────┼───────────┼──────────┤${CLR_RESET}"

    for tool_spec in "${HTML_TOOLS[@]}" "${PYTHON_TOOLS[@]}"; do
        IFS='|' read -r num name filename desc priority <<< "$tool_spec"
        local type="HTML"
        if [[ "$num" -ge 6 ]]; then
            type="Python"
        fi

        local status="${TOOL_STATUS[$num]}"
        if [[ -z "$status" ]]; then
            status="未启动"
        fi

        local status_color="${CLR_YELLOW}"
        if [[ "$status" == "已启动" || "$status" == "运行中" ]]; then
            status_color="${CLR_GREEN}"
        elif [[ "$status" == "文件缺失" || "$status" == "启动失败" || "$status" == "Python缺失" ]]; then
            status_color="${CLR_RED}"
        fi

        local priority_label="义(0.2)"
        if [[ "$priority" == "0.5" ]]; then
            priority_label="忠(0.5)"
        elif [[ "$priority" == "0.3" ]]; then
            priority_label="孝(0.3)"
        fi

        printf "${CLR_BOLD}│${CLR_RESET} %-4s │ %-19s │ %-8s │ %-9s │ ${status_color}%-8s${CLR_RESET} │\n" \
            "$num" "$name" "$type" "$priority_label" "$status"
    done

    echo -e "${CLR_BOLD}└──────┴─────────────────────┴──────────┴───────────┴──────────┘${CLR_RESET}"

    echo ""
    log INFO "启动统计: 成功=${launched} 失败=${failed} 模式=${MODE}"

    if [[ $failed -eq 0 ]]; then
        log OK "${AUDIT_PASS} 全部工具启动成功!"
    elif [[ $launched -gt 0 ]]; then
        log WARN "${AUDIT_WARN} 部分工具启动成功 (${launched}/$((launched + failed)))"
    else
        log ERROR "${AUDIT_BLOCK} 工具启动失败，请检查环境和日志"
    fi

    log INFO "日志文件: ${LOG_FILE}"

    # 保存汇总到日志
    echo "" >> "$LOG_FILE"
    echo "===== 启动汇总 $(date '+%Y-%m-%d %H:%M:%S') =====" >> "$LOG_FILE"
    echo "模式: ${MODE}" >> "$LOG_FILE"
    echo "成功: ${launched}" >> "$LOG_FILE"
    echo "失败: ${failed}" >> "$LOG_FILE"
    echo "DNA: ${DNA_SIGNATURE}" >> "$LOG_FILE"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                           信号捕获与清理
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cleanup_on_exit() {
    echo ""
    log WARN "接收到退出信号，执行清理..."

    # 停止已启动的Python工具
    for num in "${!TOOL_PID[@]}"; do
        local pid="${TOOL_PID[$num]}"
        if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null
            sleep 0.3
            kill -9 "$pid" 2>/dev/null
        fi
    done

    # 清理PID文件
    rm -f "$PID_FILE"

    log OK "清理完成，龍魂系统已安全退出"
    exit 0
}

# 注册信号处理
trap cleanup_on_exit SIGINT SIGTERM SIGHUP

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                              主入口
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

main() {
    # 解析命令行参数
    parse_arguments "$@"

    # 显示横幅
    show_banner

    # 环境检测
    check_environment

    # 执行启动
    execute_launch

    # 显示尾部信息
    echo ""
    log DNA "${DNA_SIGNATURE}"
    log DNA "启动完成时间: $(date '+%Y-%m-%d %H:%M:%S')"
    log INFO "使用 --stop 参数可优雅停止所有工具"
    log INFO "使用 --status 参数可查看运行状态"
    echo -e "${CLR_GREEN}${CLR_BOLD}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║   龍魂系统启动完毕 — 忠孝义排序已执行                                       ║"
    echo "║   UID9622⚡️龍芯北辰·诸葛鑫                                                ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${CLR_RESET}"
}

# 启动主程序
main "$@"
