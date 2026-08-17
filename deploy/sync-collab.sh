#!/usr/bin/env bash
# 🐉 龍魂 · 协作数据双向同步 v2.0（本地 ↔ 鲲鹏共享中枢）
# DNA: #龍芯⚡️丙午·丙申·己未·亥时-COLLAB-SYNC-v2.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#
# 用法:
#   bash deploy/sync-collab.sh push|full  # 本地 → 鲲鹏（自动生成校验和 + 一致性校验）
#   bash deploy/sync-collab.sh pull       # 鲲鹏 → 本地（新设备进场拉取）
#   bash deploy/sync-collab.sh check      # 只显示两端状态·不动数据
#   bash deploy/sync-collab.sh status     # sha256 对比本地 vs 远端
#
# v2.0 变更（2026-08-13）:
#   ✅ 配置加载三级 fallback: ① ~/.longhun/lh.env > ② deploy/.kunpeng_config > ③ 内置默认
#   ✅ push 后自动生成 .audit/checksums.txt + status 一致性校验
#   ✅ v1.0 精准路径映射（PATH_MAP）完整保留 · 原则不变（鲲鹏是唯一真相来源）
#
# 关键差异（vs sync-to-kunpeng.sh）:
#   ✅ 不排除 .asc —— GPG 签名必须跟着文档走
#   ✅ 双向 —— 支持 pull（新设备进场拉全量协作上下文）
#   ✅ 范围明确 —— 只同步"协作类"数据，不碰全仓

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LONGHUN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── 配置加载（三级 fallback · v2.0 新增）──
if [[ -f "$HOME/.longhun/lh.env" ]]; then
    # ① 统一配置源（最高优先）
    # shellcheck disable=SC1091
    source "$HOME/.longhun/lh.env"
elif [[ -f "${SCRIPT_DIR}/.kunpeng_config" ]]; then
    # ② 兼容旧配置（仅连接参数，历史遗留保留）
    # shellcheck disable=SC1091
    source "${SCRIPT_DIR}/.kunpeng_config"
    KUNPENG_HOST="${KUNPENG_USER}@${KUNPENG_MGMT_IP:-119.13.90.27}"
    KUNPENG_PORT="${KUNPENG_SSH_PORT:-22}"
    KUNPENG_IDENTITY="${KUNPENG_KEY:-$HOME/.ssh/longhun_kunpeng_ed25519}"
else
    # ③ 内置默认（兜底）
    KUNPENG_HOST="root@119.13.90.27"
    KUNPENG_PORT="22"
    KUNPENG_IDENTITY="$HOME/.ssh/longhun_kunpeng_ed25519"
fi

# 归一化（lh.env 的 ~ 带引号不展开，手动展开）
KUNPENG_HOST="${KUNPENG_HOST:-root@119.13.90.27}"
KUNPENG_PORT="${KUNPENG_PORT:-22}"
KUNPENG_IDENTITY="${KUNPENG_IDENTITY/#\~/$HOME}"
KUNPENG_IDENTITY="${KUNPENG_IDENTITY:-$HOME/.ssh/longhun_kunpeng_ed25519}"

# ⚠️ 共享中枢固定落位（lh.env 可覆盖，默认 /opt/longhun/shared，不被部署路径带偏）
SHARED_ROOT="${SHARED_ROOT:-/opt/longhun/shared}"
LOCAL_SHARED_ROOT="${LOCAL_SHARED_ROOT:-${LONGHUN_ROOT}/12_DOCS/collab}"
LOCAL_HANDOFFS="${LONGHUN_ROOT}/12_DOCS/handoffs"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✅${NC} $*"; }
warn() { echo -e "${YELLOW}⚠️${NC}  $*"; }
fail() { echo -e "${RED}🔴${NC} $*"; exit 1; }
info() { echo -e "${CYAN}▶${NC}  $*"; }

KUNPENG_REMOTE="${KUNPENG_HOST}"

SSH_BASE=(ssh -p "${KUNPENG_PORT}" -i "${KUNPENG_IDENTITY}"
    -o StrictHostKeyChecking=no -o ConnectTimeout=10 "${KUNPENG_REMOTE}")
RSYNC_SSH="ssh -p ${KUNPENG_PORT} -i ${KUNPENG_IDENTITY} -o StrictHostKeyChecking=no"

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

# 鲲鹏连通检查（v2.0 新增）
check_connection() { "${SSH_BASE[@]}" "echo ok" >/dev/null 2>&1; }

# 预建远端父目录 + .audit 审计区（v2.0 新增）
ensure_remote_dirs() {
    "${SSH_BASE[@]}" "mkdir -p ${SHARED_ROOT}/{collab,handoffs,collaboration,.audit}"
}

# 生成远端校验和（审计留痕 · v2.0 新增）
gen_checksums() {
    "${SSH_BASE[@]}" "cd ${SHARED_ROOT} && find . -type f ! -path './.audit/*' -exec sha256sum {} \; | sort > .audit/checksums.txt"
}

# 上推：把每个本地条目 rsync 到鲲鹏 shared 的对应相对路径
do_push() {
    info "上推协作数据 → 鲲鹏 ${REMOTE_SHARED}"
    check_connection || fail "鲲鹏不可达，终止推送"
    ensure_remote_dirs

    # 预建所有远端父目录（rsync 不会创建中间层）
    local parents=""
    for item in "${LOCAL_ITEMS[@]}"; do
        [[ -e "${LONGHUN_ROOT}/${item}" ]] || continue
        local map_target="${PATH_MAP[${item}]:-${item}}"
        local rel_dir
        rel_dir="$(dirname "$map_target")"
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

    # v2.0 新增: 自动生成校验和 + 一致性对比
    gen_checksums
    cmd_status
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
    echo
    info "鲲鹏审计区（.audit）:"
    "${SSH_BASE[@]}" "ls -la ${SHARED_ROOT}/.audit/ 2>/dev/null || echo '（.audit 尚未生成，push 后自动创建）'"
}

# 本地 vs 远端内容指纹对比（v2.0 新增 · 只比内容集合不比路径）
cmd_status() {
    info "对比本地 vs 远端（sha256 内容指纹）..."
    local local_hash remote_hash
    if [[ -d "${LOCAL_SHARED_ROOT}" && -d "${LOCAL_HANDOFFS}" ]]; then
        local_hash="$( ( find "${LOCAL_SHARED_ROOT}" -type f -exec sha256sum {} \; 2>/dev/null; find "${LOCAL_HANDOFFS}" -type f -exec sha256sum {} \; 2>/dev/null ) | awk '{print $1}' | sort | sha256sum | cut -d' ' -f1 )"
    else
        local_hash="none"
    fi
    remote_hash="$("${SSH_BASE[@]}" "cd ${SHARED_ROOT} && find ./collab ./handoffs -type f -exec sha256sum {} \; 2>/dev/null | awk '{print \$1}' | sort | sha256sum | cut -d' ' -f1" 2>/dev/null || echo "none")"
    if [[ "$local_hash" == "$remote_hash" && "$remote_hash" != "none" ]]; then
        ok "本地与远端一致 ✅"
    else
        warn "本地与远端不一致（请运行 sync-collab.sh push）"
        info "本地: ${local_hash:-none}"
        info "远端: ${remote_hash:-none}"
    fi
}

case "${1:-full}" in
    push|full) do_push ;;
    pull)      do_pull ;;
    check)     do_check ;;
    status)    cmd_status ;;
    *) echo "用法: push|full | pull | check | status"; exit 1 ;;
esac
