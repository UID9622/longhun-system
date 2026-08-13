#!/usr/bin/env bash
# 🐉 龍魂 · 协作数据双向同步（本地 ↔ 鲲鹏共享中枢）
# DNA: #龍芯⚡️丙午·丙申·己未·酉时-COLLAB-SYNC-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#
# 用法:
#   bash deploy/sync-collab.sh full   # 本地 → 鲲鹏（协作数据全量上推）
#   bash deploy/sync-collab.sh pull   # 鲲鹏 → 本地（新设备进场拉取）
#   bash deploy/sync-collab.sh check  # 只显示两端状态·不动数据
#
# 关键差异（vs sync-to-kunpeng.sh）:
#   ✅ 不排除 .asc —— GPG 签名必须跟着文档走
#   ✅ 双向 —— 支持 pull（新设备进场拉全量协作上下文）
#   ✅ 范围明确 —— 只同步"协作类"数据，不碰全仓
# 原则: 鲲鹏 /opt/longhun/shared/ 是唯一真相来源·本地是工作副本

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LONGHUN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/.kunpeng_config"

# ── 默认连接参数（仅密钥/IP 可用 deploy/.kunpeng_config 覆盖）──
KUNPENG_USER="root"
KUNPENG_MGMT_IP="119.13.90.27"
KUNPENG_SSH_PORT="22"
KUNPENG_KEY="${HOME}/.ssh/longhun_kunpeng_ed25519"

# ⚠️ 共享中枢固定落位（与 lh_handoff.py / DOCUMENT_MATRIX 写死一致，不被 config 的部署路径带偏）
SHARED_ROOT="/opt/longhun/shared"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✅${NC} $*"; }
warn() { echo -e "${YELLOW}⚠️${NC}  $*"; }
fail() { echo -e "${RED}🔴${NC} $*"; exit 1; }
info() { echo -e "${CYAN}▶${NC}  $*"; }

# 优先加载 deploy/.kunpeng_config（仅取连接参数，不取部署路径）
if [[ -f "$CONFIG_FILE" ]]; then
    # shellcheck disable=SC1090
    source "$CONFIG_FILE"
    KUNPENG_SSH_PORT="${KUNPENG_SSH_PORT:-22}"
fi

KUNPENG_REMOTE="${KUNPENG_USER}@${KUNPENG_MGMT_IP}"

SSH_BASE=(ssh -p "${KUNPENG_SSH_PORT}" -i "${KUNPENG_KEY}"
    -o StrictHostKeyChecking=no -o ConnectTimeout=10 "${KUNPENG_REMOTE}")
RSYNC_SSH="ssh -p ${KUNPENG_SSH_PORT} -i ${KUNPENG_KEY} -o StrictHostKeyChecking=no"

REMOTE_SHARED="${KUNPENG_REMOTE}:${SHARED_ROOT}/"

# ── 本地要上推的协作数据（相对 LONGHUN_ROOT）──
LOCAL_ITEMS=(
    "12_DOCS/collab/"
    "12_DOCS/handoffs/"
    "01_protocols/LH-AI-HANDOFF-v1.0.md"
    "01_protocols/LH-AI-HANDOFF-v1.0.md.asc"
    "01_protocols/LH-AI-COLLABORATION-v1.0.md"
    "01_protocols/LH-AI-COLLABORATION-v1.0.md.asc"
    ".codebuddy/COMMAND_INDEX.md"
    ".codebuddy/COMMAND_INDEX.md.asc"
    "STATE.md"
    "AGENTS.md"
    "AGENTS.md.asc"
    "12_DOCS/DIRECTORY_INDEX.md"
    "12_DOCS/DIRECTORY_INDEX.md.asc"
)

# 顶层协作文件 → 直接放 shared 根（不保留 .codebuddy 相对路径）
TOPLVL_FILES=(
    ".codebuddy/COMMAND_INDEX.md"
    ".codebuddy/COMMAND_INDEX.md.asc"
    "STATE.md"
    "AGENTS.md"
    "AGENTS.md.asc"
)

# 路径映射（与 lh_handoff.py / DOCUMENT_MATRIX 写死一致）:
#   12_DOCS/collab/  → shared/collab/        （Web /collab/）
#   12_DOCS/handoffs/ → shared/handoffs/     （lh handoff load --remote 依赖）
#   01_protocols/LH-AI-* → shared/collaboration/
declare -A PATH_MAP=(
    ["12_DOCS/collab/"]="collab/"
    ["12_DOCS/handoffs/"]="handoffs/"
    ["01_protocols/LH-AI-HANDOFF-v1.0.md"]="collaboration/LH-AI-HANDOFF-v1.0.md"
    ["01_protocols/LH-AI-HANDOFF-v1.0.md.asc"]="collaboration/LH-AI-HANDOFF-v1.0.md.asc"
    ["01_protocols/LH-AI-COLLABORATION-v1.0.md"]="collaboration/LH-AI-COLLABORATION-v1.0.md"
    ["01_protocols/LH-AI-COLLABORATION-v1.0.md.asc"]="collaboration/LH-AI-COLLABORATION-v1.0.md.asc"
)

# 上推：把每个本地条目 rsync 到鲲鹏 shared 的对应相对路径
do_push() {
    info "上推协作数据 → 鲲鹏 ${REMOTE_SHARED}"
    # 预建所有远端父目录（rsync 不会创建中间层）
    local parents=""
    for item in "${LOCAL_ITEMS[@]}"; do
        [[ -e "${LONGHUN_ROOT}/${item}" ]] || continue
        local map_target="${PATH_MAP[${item}]:-${item}}"
        local rel_dir
        if [[ -d "${LONGHUN_ROOT}/${item}" ]]; then
            rel_dir="$(dirname "$map_target")"
        else
            rel_dir="$(dirname "$map_target")"
        fi
        [[ "$rel_dir" == "." || "$rel_dir" == "/" ]] && continue
        parents="${parents} ${SHARED_ROOT}/${rel_dir}"
    done
    [[ -n "$parents" ]] && "${SSH_BASE[@]}" "mkdir -p ${parents}"

    for item in "${LOCAL_ITEMS[@]}"; do
        local_src="${LONGHUN_ROOT}/${item}"
        [[ -e "$local_src" ]] || { warn "跳过(本地不存在): ${item}"; continue; }
        local map_target="${PATH_MAP[${item}]:-${item}}"
        if [[ -d "$local_src" ]]; then
            rsync -a --delete -e "${RSYNC_SSH}" "${local_src%/}/" "${REMOTE_SHARED}${map_target%/}/"
        else
            if [[ " ${TOPLVL_FILES[*]} " == *" ${item} "* ]]; then
                rsync -a -e "${RSYNC_SSH}" "$local_src" "${REMOTE_SHARED}$(basename "$map_target")"
            else
                rel_dir="$(dirname "$map_target")"
                if [[ "$rel_dir" == "." || "$rel_dir" == "/" ]]; then
                    rsync -a -e "${RSYNC_SSH}" "$local_src" "${REMOTE_SHARED}$(basename "$map_target")"
                else
                    rsync -a -e "${RSYNC_SSH}" "$local_src" "${REMOTE_SHARED}${map_target}"
                fi
            fi
        fi
    done
    ok "上推完成 → ${KUNPENG_REMOTE}:${SHARED_ROOT}/"
}

# 下拉：把鲲鹏 shared 全量拉回本地（新设备进场用）
do_pull() {
    info "下拉协作数据 ← 鲲鹏"
    local dest_dir="${LONGHUN_ROOT}/12_DOCS/collab_pull"
    mkdir -p "$dest_dir"
    rsync -a -e "${RSYNC_SSH}" "${REMOTE_SHARED}" "$dest_dir/"
    ok "下拉完成 → ${dest_dir}/"
    warn "交接包已入 ${dest_dir}/handoffs/，需要时手动放回 12_DOCS/handoffs/ 或直接 lh handoff load --remote"
}

do_check() {
    info "本地侧（12_DOCS/collab + handoffs）:"
    ls -la "${LONGHUN_ROOT}/12_DOCS/collab/" 2>/dev/null | head -10 || warn "本地 collab 不存在"
    echo
    info "鲲鹏侧（shared）:"
    "${SSH_BASE[@]}" "ls -la ${SHARED_ROOT}/ 2>/dev/null || echo '（鲲鹏 shared 尚未创建）'"
}

case "${1:-full}" in
    full|push) do_push ;;
    pull)      do_pull ;;
    check)     do_check ;;
    *) echo "用法: full | pull | check"; exit 1 ;;
esac
