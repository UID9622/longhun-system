#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# 🐉 龍魂 · 国际化指令库 v2.0 部署脚本（修复版）
# DNA: #龍芯⚡️丙午·丙申·癸亥·巳时·䷒临-LH-INTL-DEPLOY-v2.0-551e21fc
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
#
# v2.0 审计修复（相对 Kimi 交付版）:
#   🔴 不再创建 ~/bin/lh（与系统 zsh alias lh 冲突抢占）→ 改 ~/bin/lh-intl
#   🔴 install_engine 逻辑断裂（引擎需外部注入）→ 引擎随部署自包含安装
#   🔴 backup_old 全量备份 ~/.longhun（AI归集Hub·49目录）→ 只备份本模块文件
#   🟡 chmod 700 不再作用于整个 ~/.longhun → 只收紧本模块子目录
#   🟡 幂等: 已存在的用户配置/语言包不覆盖（--force 才覆盖）
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LH_BIN="${HOME}/longhun-system/08_BIN"
LH_INTL="${LH_BIN}/lh_intl.py"
LH_I18N="${HOME}/.longhun/i18n"
LH_LOGS="${HOME}/.longhun/logs"
BACKUP_DIR="${HOME}/.longhun/backup/intl/$(date +%Y%m%d_%H%M%S)"
FORCE=0

[[ "${1:-}" == "--force" ]] && FORCE=1

# ── 颜色 ──
R='\033[0;31m'; G='\033[0;32m'; Y='\033[1;33m'; C='\033[0;36m'; NC='\033[0m'
log_info()  { echo -e "${C}[INFO]${NC}  $*"; }
log_ok()    { echo -e "${G}[OK]${NC}   $*"; }
log_warn()  { echo -e "${Y}[WARN]${NC} $*"; }
log_err()   { echo -e "${R}[ERR]${NC}  $*"; }

# ── 0. 依赖检查 ──
check_deps() {
    log_info "检查依赖..."
    command -v python3 >/dev/null 2>&1 || { log_err "未找到 python3"; exit 1; }
    local pyver
    pyver=$(python3 -c 'import sys; print(sys.version_info[:2] >= (3,9))')
    if [[ "$pyver" != "True" ]]; then
        log_err "需要 Python 3.9+"; exit 1
    fi
    log_ok "Python 版本满足"
}

# ── 1. 只备份本模块会触碰的文件（不整目录备份 ~/.longhun）──
backup_own() {
    local found=0
    mkdir -p "$BACKUP_DIR"
    for f in "${LH_I18N}"/*.json "${HOME}/.longhun/user_prefs.json" "${HOME}/.longhun/user_aliases.json"; do
        if [[ -f "$f" ]]; then
            cp "$f" "$BACKUP_DIR/" 2>/dev/null && found=1
        fi
    done
    if [[ -f "$LH_INTL" ]]; then
        mkdir -p "$BACKUP_DIR/bin"
        cp "$LH_INTL" "$BACKUP_DIR/bin/" 2>/dev/null
        found=1
    fi
    if [[ "$found" -eq 1 ]]; then
        log_ok "旧配置已备份至 $BACKUP_DIR"
    else
        rmdir "$BACKUP_DIR" 2>/dev/null || true
    fi
}

# ── 2. 创建目录结构（只收紧本模块目录, 不动 ~/.longhun 主权限）──
setup_dirs() {
    mkdir -p "$LH_I18N" "$LH_LOGS"
    chmod 700 "$LH_I18N" "$LH_LOGS"
    log_ok "目录结构创建完成 ($LH_I18N)"
}

# ── 3. 安装语言包（幂等: 已存在不覆盖, --force 覆盖）──
install_langpacks() {
    log_info "安装语言包..."
    local target

    target="${LH_I18N}/zh_CN.json"
    if [[ -f "$target" && "$FORCE" -eq 0 ]]; then
        log_ok "zh_CN.json 已存在, 跳过 (--force 覆盖)"
    else
        cat > "$target" << 'PYEOF'
{
  "language_name": "中文",
  "menu_title": "🐉 龍魂系统 · 主菜单",
  "menu_items": {
    "1": {"label": "🔍 搜索", "cmd": "lh search", "desc": "在知识图谱和本地文件中搜索"},
    "2": {"label": "📊 透明看板", "cmd": "lh dashboard", "desc": "查看实时审计与状态"},
    "3": {"label": "🧬 DNA追溯", "cmd": "lh dna", "desc": "生成或验证DNA追溯码"},
    "4": {"label": "🎨 三色审计", "cmd": "lh audit", "desc": "运行三色审计检查"},
    "5": {"label": "📜 史官记录", "cmd": "lh historian", "desc": "查看最近操作日志"},
    "6": {"label": "🚫 耻辱墙", "cmd": "lh shame", "desc": "查看违规记录"},
    "7": {"label": "⚙️ 系统状态", "cmd": "lh status", "desc": "查看系统运行状态"},
    "8": {"label": "💳 良心支付", "cmd": "lh pay", "desc": "支付支持系统发展"},
    "9": {"label": "❓ 帮助", "cmd": "lh help", "desc": "显示帮助信息"},
    "0": {"label": "🚪 退出", "cmd": "exit", "desc": "退出菜单"}
  },
  "prompt": "请选择操作 [0-9] 或输入别名/命令: ",
  "invalid_choice": "无效选择，请重新输入。",
  "language_switch_hint": "切换语言: 输入 'lang:en' 切换为英文",
  "exit_message": "再见！🐉"
}
PYEOF
        chmod 600 "$target"
        log_ok "zh_CN.json 安装完成"
    fi

    target="${LH_I18N}/en_US.json"
    if [[ -f "$target" && "$FORCE" -eq 0 ]]; then
        log_ok "en_US.json 已存在, 跳过 (--force 覆盖)"
    else
        cat > "$target" << 'PYEOF'
{
  "language_name": "English",
  "menu_title": "🐉 Dragon Soul System · Main Menu",
  "menu_items": {
    "1": {"label": "🔍 Search", "cmd": "lh search", "desc": "Search knowledge graph and local files"},
    "2": {"label": "📊 Transparent Dashboard", "cmd": "lh dashboard", "desc": "Live audit & status view"},
    "3": {"label": "🧬 DNA Trace", "cmd": "lh dna", "desc": "Generate or verify DNA trace"},
    "4": {"label": "🎨 Tricolor Audit", "cmd": "lh audit", "desc": "Run tricolor audit"},
    "5": {"label": "📜 Historian Logs", "cmd": "lh historian", "desc": "View recent operation logs"},
    "6": {"label": "🚫 Shame Wall", "cmd": "lh shame", "desc": "View violation records"},
    "7": {"label": "⚙️ System Status", "cmd": "lh status", "desc": "System health overview"},
    "8": {"label": "💳 Conscience Payment", "cmd": "lh pay", "desc": "Support the system"},
    "9": {"label": "❓ Help", "cmd": "lh help", "desc": "Show help information"},
    "0": {"label": "🚪 Exit", "cmd": "exit", "desc": "Exit menu"}
  },
  "prompt": "Select option [0-9] or enter alias/command: ",
  "invalid_choice": "Invalid choice, please try again.",
  "language_switch_hint": "Switch language: type 'lang:zh' for Chinese",
  "exit_message": "Goodbye! 🐉"
}
PYEOF
        chmod 600 "$target"
        log_ok "en_US.json 安装完成"
    fi
}

# ── 4. 写入用户配置（幂等）──
install_configs() {
    local prefs="${HOME}/.longhun/user_prefs.json"
    if [[ ! -f "$prefs" || "$FORCE" -eq 1 ]]; then
        cat > "$prefs" << 'PYEOF'
{
  "language": "auto",
  "default_output": "text",
  "menu_auto_start": true,
  "confirm_code_check": true,
  "log_level": "INFO"
}
PYEOF
        chmod 600 "$prefs"
        log_ok "user_prefs.json 初始化完成"
    else
        log_ok "user_prefs.json 已存在, 保留"
    fi

    local aliases="${HOME}/.longhun/user_aliases.json"
    if [[ ! -f "$aliases" || "$FORCE" -eq 1 ]]; then
        cat > "$aliases" << 'PYEOF'
{
  "s": "lh search",
  "d": "lh dashboard",
  "x": "lh audit",
  "h": "lh historian",
  "sh": "lh shame",
  "st": "lh status",
  "p": "lh pay",
  "q": "exit"
}
PYEOF
        chmod 600 "$aliases"
        log_ok "user_aliases.json 初始化完成"
    else
        log_ok "user_aliases.json 已存在, 保留"
    fi
}

# ── 5. 安装引擎（自包含: 从同目录复制, 不依赖外部注入）──
install_engine() {
    log_info "安装引擎..."
    local src="$SCRIPT_DIR/lh_intl.py"
    if [[ ! -f "$src" ]]; then
        log_err "引擎源文件 $src 不存在"
        exit 1
    fi
    if [[ -f "$LH_INTL" && "$FORCE" -eq 0 ]]; then
        log_ok "引擎已存在: $LH_INTL (--force 覆盖)"
    else
        cp "$src" "$LH_INTL"
        log_ok "引擎安装完成: $LH_INTL"
    fi
    chmod +x "$LH_INTL"
}

# ── 6. 创建 lh-intl 入口（不碰 ~/bin/lh, 避免与系统 alias lh 冲突）──
install_wrapper() {
    local bin_dir="${HOME}/bin"
    mkdir -p "$bin_dir"
    if [[ -e "$LH_INTL" ]]; then
        ln -sfn "$LH_INTL" "${bin_dir}/lh-intl"
        log_ok "入口符号链接 ~/bin/lh-intl → $LH_INTL"
    else
        cat > "${bin_dir}/lh-intl" << 'PYEOF'
#!/bin/bash
exec python3 "${HOME}/longhun-system/08_BIN/lh_intl.py" "$@"
PYEOF
        chmod +x "${bin_dir}/lh-intl"
        log_ok "入口脚本 ~/bin/lh-intl 创建完成"
    fi
}

# ── 7. 运行单元测试 ──
run_tests() {
    log_info "运行单元测试..."
    if python3 "$LH_INTL" test > /tmp/lh_intl_test.log 2>&1; then
        grep -E "Ran [0-9]+ tests|OK" /tmp/lh_intl_test.log | tail -2
        log_ok "全部测试通过"
    else
        tail -20 /tmp/lh_intl_test.log
        log_err "测试失败"; exit 1
    fi
}

# ── 8. 配置校验 ──
run_validation() {
    log_info "运行配置校验..."
    if python3 "$LH_INTL" --validate; then
        log_ok "校验通过"
    else
        log_warn "校验发现警告, 请检查日志"
    fi
}

# ── 主流程 ──
main() {
    echo -e "${C}"
    echo "═══════════════════════════════════════════════════════════════"
    echo "  🐉 龍魂国际化指令库 v2.0 部署脚本（修复版）"
    echo "═══════════════════════════════════════════════════════════════"
    echo -e "${NC}"
    check_deps
    backup_own
    setup_dirs
    install_langpacks
    install_configs
    install_engine
    install_wrapper
    run_tests
    run_validation
    echo ""
    log_ok "🐉 部署完成！输入 'lh-intl' 或 'lh-intl --version' 开始使用"
}

main "$@"
