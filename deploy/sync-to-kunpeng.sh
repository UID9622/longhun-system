#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 · rsync 搬迁同步脚本
# 依赖: connect-kunpeng.sh 已有密钥配置
# DNA: #龍芯⚡️2026-07-06-KUNPENG-SYNC-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LONGHUN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/.kunpeng_config"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'
log()  { echo -e "$(date '+%H:%M:%S') $*"; }
ok()   { log "${GREEN}✅${NC} $*"; }
warn() { log "${YELLOW}⚠️${NC}  $*"; }
fail() { log "${RED}🔴${NC} $*"; exit 1; }
info() { log "${CYAN}▶${NC}  $*"; }

load_config() {
    [[ -f "$CONFIG_FILE" ]] || fail "请先执行: bash deploy/connect-kunpeng.sh config"
    source "$CONFIG_FILE"
}

ssh_cmd() {
    ssh -p "${KUNPENG_SSH_PORT}" -i "${KUNPENG_KEY}" \
        -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 \
        "${KUNPENG_USER}@${KUNPENG_MGMT_IP}" "$@"
}

EXCLUDES=(
    ".git/" "__pycache__/" "*.pyc" "*.pyo" ".mypy_cache/" ".pytest_cache/"
    ".venv/" "venv/" "env/" "node_modules/" ".next/" "dist/" "build/"
    ".vscode/" ".idea/" ".DS_Store" "logs/" "*.log" "*.tmp" "*.swp"
    "*.dSYM/" "*.app/" ".master_key" "*.pem" "*.key" "*.asc"
    "*.db" "*.sqlite" "*.sqlite3"
    "deploy/.kunpeng_config" "deploy/.kunpeng_auth" "backups/"
)

build_excludes() {
    local args=()
    for p in "${EXCLUDES[@]}"; do args+=("--exclude=$p"); done
    printf '%s\n' "${args[@]}"
}

dry_run() {
    info "干运行 — 预览将传输的文件:"
    local ex=()
    while IFS= read -r line; do ex+=("$line"); done < <(build_excludes)
    rsync -avzn --delete "${ex[@]}" \
        -e "ssh -p ${KUNPENG_SSH_PORT} -i ${KUNPENG_KEY} -o StrictHostKeyChecking=accept-new" \
        "${LONGHUN_ROOT}/" "${KUNPENG_USER}@${KUNPENG_MGMT_IP}:${KUNPENG_DEPLOY_PATH}/" \
        | head -80
}

do_sync() {
    info "全量同步 → ${KUNPENG_USER}@${KUNPENG_MGMT_IP}:${KUNPENG_DEPLOY_PATH}/"
    ssh_cmd "mkdir -p ${KUNPENG_DEPLOY_PATH}"

    local ex=()
    while IFS= read -r line; do ex+=("$line"); done < <(build_excludes)
    rsync -avz --progress --delete --force "${ex[@]}" \
        -e "ssh -p ${KUNPENG_SSH_PORT} -i ${KUNPENG_KEY} -o StrictHostKeyChecking=accept-new" \
        "${LONGHUN_ROOT}/" "${KUNPENG_USER}@${KUNPENG_MGMT_IP}:${KUNPENG_DEPLOY_PATH}/"

    ssh_cmd "find ${KUNPENG_DEPLOY_PATH}/bin -name '*.sh' -exec chmod +x {} \\;" 2>/dev/null || true
    ssh_cmd "find ${KUNPENG_DEPLOY_PATH}/scripts -name '*.sh' -exec chmod +x {} \\;" 2>/dev/null || true
    ok "同步完成"
}

main() {
    load_config
    case "${1:-}" in
        dry|preview) dry_run ;;
        full|sync|--sync) do_sync ;;
        *) echo "用法: dry | full" ;;
    esac
}

main "$@"
