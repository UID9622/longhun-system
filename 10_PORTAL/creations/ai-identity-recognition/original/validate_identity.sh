# DNA: #龍芯⚡️丙午·丙申·甲子·甲戌·䷍大有-CODE-补DNA-ef97e828
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# 🐉 龍魂 · AI身份标识与互认协议引擎验证脚本 v2.0
# DNA: [[GENERATED_BY_LH_DNA_GENERATOR_V3]]-IDENTITY-VALIDATE-v2.0
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

IDENTITY_DIR="${HOME}/longhun-system/08_BIN/identity"
CONFIG_DIR="${HOME}/.longhun/agent/identity"
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
    for d in "$IDENTITY_DIR" "$CONFIG_DIR" "${CONFIG_DIR}/watermarks" "${CONFIG_DIR}/indicators" "${CONFIG_DIR}/exempt" "${CONFIG_DIR}/audit"; do
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
    local f="${IDENTITY_DIR}/ai_identity.py"
    if [[ -f "$f" ]]; then
        if python3 -m py_compile "$f" 2>/dev/null; then
            log_ok "ai_identity.py 语法正确"
        else
            log_err "ai_identity.py 语法错误"; ((ERRS++))
        fi
    else
        log_err "ai_identity.py 缺失"; ((ERRS++))
    fi
}

# ── 3. 单元测试 ──
check_tests() {
    log_info "运行单元测试..."
    local f="${IDENTITY_DIR}/ai_identity.py"
    if [[ -f "$f" ]]; then
        if python3 "$f" --test >/dev/null 2>&1; then
            log_ok "ai_identity.py 测试通过 (12项锚点)"
        else
            log_err "ai_identity.py 测试失败"; ((ERRS++))
        fi
    fi
}

# ── 4. 入口脚本 ──
check_wrapper() {
    log_info "检查入口脚本..."
    if [[ -f "${BIN_DIR}/lh-identity" ]]; then
        log_ok "lh-identity 存在"
    else
        log_err "lh-identity 缺失"; ((ERRS++))
    fi
}

# ── 5. 版本验证 ──
check_version() {
    log_info "验证版本信息..."
    local f="${IDENTITY_DIR}/ai_identity.py"
    if [[ -f "$f" ]]; then
        local ver=$(python3 "$f" --version 2>/dev/null || echo "")
        if echo "$ver" | grep -q "v2.0"; then
            log_ok "版本验证通过"
        else
            log_warn "版本输出异常"; ((WARNS++))
        fi
    fi
}

# ── 6. 豁免配置 ──
check_exempt() {
    log_info "检查豁免配置..."
    local f="${CONFIG_DIR}/exempt_list.json"
    if [[ -f "$f" ]]; then
        if grep -q 'UID9622' "$f" 2>/dev/null; then
            log_ok "UID9622 豁免配置正确"
        else
            log_warn "UID9622 未在豁免列表中"; ((WARNS++))
        fi
        local mode=$(stat -c '%a' "$f" 2>/dev/null || stat -f '%Lp' "$f" 2>/dev/null || echo "???")
        if [[ "$mode" == "600" ]]; then
            log_ok "豁免配置权限正确 (600)"
        else
            log_warn "豁免配置权限 ${mode}，建议 600"; ((WARNS++))
        fi
    else
        log_warn "exempt_list.json 缺失"; ((WARNS++))
    fi
}

# ── 主流程 ──
main() {
    echo -e "${C}"
    echo "═══════════════════════════════════════════════════════════════"
    echo "  🐉 龍魂AI身份标识与互认协议引擎验证脚本 v2.0"
    echo "═══════════════════════════════════════════════════════════════"
    echo -e "${NC}"
    check_dirs
    check_engine
    check_tests
    check_wrapper
    check_version
    check_exempt
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
