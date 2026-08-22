# DNA: #龍芯⚡️丙午·丙申·甲子·甲戌·䷍大有-CODE-补DNA-4a207718
#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# 🐉 龍魂 · AI身份标识与互认协议引擎 v2.0 部署脚本
# DNA: [[GENERATED_BY_LH_DNA_GENERATOR_V3]]-IDENTITY-DEPLOY-v2.0
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

IDENTITY_DIR="${HOME}/longhun-system/08_BIN/identity"
CONFIG_DIR="${HOME}/.longhun/agent/identity"
BACKUP_DIR="${CONFIG_DIR}/backup/$(date +%Y%m%d_%H%M%S)"
BIN_DIR="${HOME}/bin"

R='\033[0;31m'; G='\033[0;32m'; Y='\033[1;33m'; C='\033[0;36m'; NC='\033[0m'
log_info()  { echo -e "${C}[INFO]${NC}  $*"; }
log_ok()    { echo -e "${G}[OK]${NC}   $*"; }
log_warn()  { echo -e "${Y}[WARN]${NC} $*"; }
log_err()   { echo -e "${R}[ERR]${NC}  $*"; }

# ── 0. 依赖检查 ──
check_deps() {
    log_info "检查依赖..."
    python3 --version >/dev/null 2>&1 || { log_err "未找到 python3"; exit 1; }
    local pyver=$(python3 -c 'import sys; print(sys.version_info[:2] >= (3,9))')
    if [[ "$pyver" != "True" ]]; then
        log_err "需要 Python 3.9+"; exit 1
    fi
    log_ok "Python 版本满足"
}

# ── 1. 备份 ──
backup_old() {
    if [[ -d "$CONFIG_DIR" ]] && [[ -n "$(ls -A "$CONFIG_DIR" 2>/dev/null)" ]]; then
        mkdir -p "$BACKUP_DIR"
        cp -r "${CONFIG_DIR}/." "$BACKUP_DIR/" 2>/dev/null || true
        log_ok "旧配置已备份至 $BACKUP_DIR"
    fi
}

# ── 2. 目录结构 ──
setup_dirs() {
    mkdir -p "$IDENTITY_DIR"
    mkdir -p "$CONFIG_DIR"/{watermarks,indicators,exempt,audit}
    chmod 700 "$CONFIG_DIR"
    log_ok "目录结构创建完成"
}

# ── 3. 复制引擎文件 ──
install_engine() {
    log_info "安装引擎..."
    if [[ -f "${IDENTITY_DIR}/ai_identity.py" ]]; then
        log_ok "ai_identity.py 已就位"
    else
        log_warn "ai_identity.py 未找到，请手动复制到 ${IDENTITY_DIR}/"
    fi
}

# ── 4. 创建入口脚本 ──
install_wrapper() {
    mkdir -p "$BIN_DIR"
    cat > "${BIN_DIR}/lh-identity" << 'EOF'
#!/bin/bash
# 🐉 龍魂 · AI身份标识与互认协议入口 v2.0
IDENTITY_DIR="${HOME}/longhun-system/08_BIN/identity"
python3 "${IDENTITY_DIR}/ai_identity.py" "$@"
EOF
    chmod +x "${BIN_DIR}/lh-identity"
    log_ok "入口脚本 lh-identity 创建完成"
}

# ── 5. 创建默认配置 ──
install_defaults() {
    log_info "创建默认配置..."
    cat > "${CONFIG_DIR}/exempt_list.json" << 'EOF'
{
  "exempt_uids": ["UID9622"],
  "comment": "本地主权豁免列表，只有 UID9622 可修改"
}
EOF
    chmod 600 "${CONFIG_DIR}/exempt_list.json"
    log_ok "默认豁免配置创建完成"
}

# ── 6. 测试 ──
run_tests() {
    log_info "运行单元测试..."
    if [[ -f "${IDENTITY_DIR}/ai_identity.py" ]]; then
        if python3 "${IDENTITY_DIR}/ai_identity.py" --test >/dev/null 2>&1; then
            log_ok "ai_identity.py 测试通过 (12项锚点)"
        else
            log_err "ai_identity.py 测试失败"; exit 1
        fi
    fi
}

# ── 主流程 ──
main() {
    echo -e "${C}"
    echo "═══════════════════════════════════════════════════════════════"
    echo "  🐉 龍魂AI身份标识与互认协议引擎 v2.0 部署脚本"
    echo "═══════════════════════════════════════════════════════════════"
    echo -e "${NC}"
    check_deps
    backup_old
    setup_dirs
    install_engine
    install_wrapper
    install_defaults
    run_tests
    echo ""
    log_ok "🐉 部署完成！"
    echo ""
    echo "使用方法:"
    echo "  lh-identity --version              # 查看版本"
    echo "  lh-identity --inject '内容'        # 注入水印"
    echo "  lh-identity --detect '内容'        # 检测AI标识"
    echo "  lh-identity --recognize '源' '目标' # 互认检测"
    echo "  lh-identity --stats                # 查看统计"
    echo "  lh-identity --exempt               # 查看豁免列表"
    echo ""
    echo "环境变量:"
    echo "  export LONGHUN_LOCAL_SOVEREIGNTY=true  # 开启本地豁免"
}

main "$@"
