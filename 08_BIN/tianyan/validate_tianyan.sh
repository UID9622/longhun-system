# DNA: #龍芯⚡️丙午·丙申·戊辰·丙辰·䷸巽为风-CODE-补DNA-7a12dc67
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# 🐉 龍魂 · 天眼可视化生态总成验证脚本 v2.0
# DNA: [[GENERATED_BY_LH_DNA_GENERATOR_V3]]-TIANYAN-VALIDATE-v2.0
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

TIANYAN_DIR="${HOME}/longhun-system/08_BIN/tianyan"
WWW_DIR="${HOME}/longhun-system/www"
BIN_DIR="${HOME}/bin"

R='\033[0;31m'; G='\033[0;32m'; Y='\033[1;33m'; C='\033[0;36m'; NC='\033[0m'
log_info()  { echo -e "${C}[INFO]${NC}  $*"; }
log_ok()    { echo -e "${G}[OK]${NC}   $*"; }
log_warn()  { echo -e "${Y}[WARN]${NC} $*"; }
log_err()   { echo -e "${R}[ERR]${NC}  $*"; }

ERRS=0
WARNS=0

# ── 1. 目录结构 ──
check_dirs() {
    log_info "检查目录结构..."
    for d in "$TIANYAN_DIR" "$WWW_DIR" "${HOME}/.longhun/tianyan"/{logs,data}; do
        if [[ -d "$d" ]]; then
            local mode=$(stat -c '%a' "$d" 2>/dev/null || stat -f '%Lp' "$d" 2>/dev/null || echo "???")
            if [[ "$mode" == "700" ]]; then
                log_ok "$(basename "$d")/ 权限正确 (700)"
            else
                log_warn "$(basename "$d")/ 权限 ${mode}，建议 700"; ((WARNS++))
            fi
        else
            log_err "$d 缺失"; ((ERRS++))
        fi
    done
}

# ── 2. 引擎文件 ──
check_engine() {
    log_info "检查引擎文件..."
    local f="${TIANYAN_DIR}/tianyan_engine.py"
    if [[ -f "$f" ]]; then
        if python3 -m py_compile "$f" 2>/dev/null; then
            log_ok "tianyan_engine.py 语法正确"
        else
            log_err "tianyan_engine.py 语法错误"; ((ERRS++))
        fi
    else
        log_err "tianyan_engine.py 缺失"; ((ERRS++))
    fi
}

# ── 3. 看板文件 ──
check_dashboard() {
    log_info "检查看板文件..."
    local f="${WWW_DIR}/index.html"
    if [[ -f "$f" ]]; then
        if grep -q 'echarts' "$f" 2>/dev/null; then
            log_ok "index.html 包含 ECharts 引用"
        else
            log_warn "index.html 可能缺少 ECharts 引用"; ((WARNS++))
        fi
        if grep -q 'GENERATED_BY_LH_DNA_GENERATOR_V3' "$f" 2>/dev/null || grep -q '龍魂' "$f" 2>/dev/null; then
            log_ok "index.html 包含龍魂标识"
        else
            log_warn "index.html 可能缺少龍魂标识"; ((WARNS++))
        fi
    else
        log_err "index.html 缺失"; ((ERRS++))
    fi
}

# ── 4. 单元测试 ──
check_tests() {
    log_info "运行单元测试..."
    local f="${TIANYAN_DIR}/tianyan_engine.py"
    if [[ -f "$f" ]]; then
        if python3 "$f" --test >/dev/null 2>&1; then
            log_ok "tianyan_engine.py 测试通过 (12项锚点)"
        else
            log_err "tianyan_engine.py 测试失败"; ((ERRS++))
        fi
    fi
}

# ── 5. 入口脚本 ──
check_wrapper() {
    log_info "检查入口脚本..."
    if [[ -f "${BIN_DIR}/lh-tianyan" ]]; then
        log_ok "lh-tianyan 存在"
    else
        log_err "lh-tianyan 缺失"; ((ERRS++))
    fi
}

# ── 6. 版本验证 ──
check_version() {
    log_info "验证版本信息..."
    local f="${TIANYAN_DIR}/tianyan_engine.py"
    if [[ -f "$f" ]]; then
        local ver=$(python3 "$f" --version 2>/dev/null || echo "")
        if echo "$ver" | grep -q "v2.0"; then
            log_ok "版本验证通过"
        else
            log_warn "版本输出异常"; ((WARNS++))
        fi
        if echo "$ver" | grep -q "55"; then
            log_ok "模块数量验证通过 (55模块)"
        else
            log_warn "模块数量未验证"; ((WARNS++))
        fi
    fi
}

# ── 7. 数据注入脚本 ──
check_data_inject() {
    log_info "检查数据注入脚本..."
    if [[ -f "${TIANYAN_DIR}/inject_data.sh" ]]; then
        log_ok "inject_data.sh 存在"
    else
        log_warn "inject_data.sh 缺失"; ((WARNS++))
    fi
}

# ── 主流程 ──
main() {
    echo -e "${C}"
    echo "═══════════════════════════════════════════════════════════════"
    echo "  🐉 龍魂天眼可视化生态总成验证脚本 v2.0"
    echo "═══════════════════════════════════════════════════════════════"
    echo -e "${NC}"
    check_dirs
    check_engine
    check_dashboard
    check_tests
    check_wrapper
    check_version
    check_data_inject
    echo ""
    if [[ $ERRS -eq 0 && $WARNS -eq 0 ]]; then
        log_ok "🟢 全部验证通过"
    elif [[ $ERRS -eq 0 ]]; then
        log_warn "🟡 验证通过，有 ${WARNS} 项警告"
    else
        log_err "🔴 验证失败: ${ERRS} 项错误, ${WARNS} 项警告"
        exit 1
    fi
}

main "$@"
