#!/usr/bin/env bash
# 🐉 龍魂 · Notion 知识库索引同步 v1.0（本地 → 鲲鹏）
# DNA: #龍芯⚡️丙午·丙申·丁丑·戊寅·䷓观-KB-SYNC-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#
# 用法:
#   bash bin/lh_kb_sync.sh sync   # 本地同步索引（跑 lh_notion_kb.py sync）
#   bash bin/lh_kb_sync.sh push   # 推送本地索引 → 鲲鹏（默认索引路径）
#   bash bin/lh_kb_sync.sh all    # sync + push 全链路（launchd 默认）
#   bash bin/lh_kb_sync.sh check  # 只对比本地 vs 远端·不动数据
#   bash bin/lh_kb_sync.sh status # 显示两端索引信息

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LONGHUN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

LOCAL_INDEX="${LONGHUN_ROOT}/data/notion_kb/index.json"
REMOTE_INDEX_DIR="/root/.longhun/data/notion_kb"
AUDIT_LOG="${LONGHUN_ROOT}/.audit/kb_sync.log"

KUNPENG_HOST="root@119.13.90.27"
KUNPENG_PORT="${KUNPENG_SSH_PORT:-22}"
KUNPENG_IDENTITY="${KUNPENG_KEY:-$HOME/.ssh/longhun_kunpeng_ed25519}"
KUNPENG_IDENTITY="${KUNPENG_IDENTITY/#\~/$HOME}"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
ok()   { echo -e "${GREEN}OK ${NC}$*"; }
warn() { echo -e "${YELLOW}WARN ${NC}$*"; }
fail() { echo -e "${RED}FAIL ${NC}$*"; exit 1; }
info() { echo ">> $*"; }

SSH_BASE=(ssh -p "${KUNPENG_PORT}" -i "${KUNPENG_IDENTITY}"
    -o StrictHostKeyChecking=no -o ConnectTimeout=10 "${KUNPENG_HOST}")
RSYNC_SSH="ssh -p ${KUNPENG_PORT} -i ${KUNPENG_IDENTITY} -o StrictHostKeyChecking=no"

log() { mkdir -p "$(dirname "${AUDIT_LOG}")"; echo "[$(date '+%F %T')] $*" >> "${AUDIT_LOG}"; }

check_local_index() {
    [[ -f "$LOCAL_INDEX" ]] || fail "本地索引不存在: ${LOCAL_INDEX}（先跑 sync）"
}

cmd_sync() {
    info "本地同步（lh_notion_kb.py sync）..."
    mkdir -p "$(dirname "$LOCAL_INDEX")"
    ( cd "$LONGHUN_ROOT" && python3 bin/lh_notion_kb.py sync )
    local n
    n="$(python3 -c "import json;d=json.load(open('$LOCAL_INDEX'));print(len(d.get('entries',d.get('pages',d.get('items',[])))))" 2>/dev/null || echo "?")"
    ok "本地索引就绪 · entries=${n}"
}

cmd_push() {
    check_local_index
    "${SSH_BASE[@]}" "mkdir -p ${REMOTE_INDEX_DIR}" >/dev/null 2>&1 || fail "鲲鹏不可达"
    rsync -a -e "${RSYNC_SSH}" "$LOCAL_INDEX" "${KUNPENG_HOST}:${REMOTE_INDEX_DIR}/index.json"
    local rsize lsize
    rsize="$("${SSH_BASE[@]}" "wc -c < ${REMOTE_INDEX_DIR}/index.json" 2>/dev/null | tr -d ' ' || echo 0)"
    lsize="$(wc -c < "$LOCAL_INDEX" | tr -d ' ')"
    if [[ "$rsize" == "$lsize" ]]; then
        log "push OK index.json ${lsize}B"
        ok "推送完成 · 远端 ${rsize}B == 本地 ${lsize}B"
    else
        warn "尺寸不一致（远端 ${rsize} vs 本地 ${lsize}），检查网络"
    fi
}

cmd_all() { cmd_sync; cmd_push; }

cmd_check() {
    info "本地: ${LOCAL_INDEX}"
    [[ -f "$LOCAL_INDEX" ]] && ls -la "$LOCAL_INDEX" || warn "本地索引不存在"
    info "鲲鹏: ${REMOTE_INDEX_DIR}/index.json"
    "${SSH_BASE[@]}" "ls -la ${REMOTE_INDEX_DIR}/index.json 2>/dev/null || echo '（鲲鹏索引不存在）'"
}

cmd_status() {
    info "本地索引摘要:"
    python3 -c "
import json
d=json.load(open('$LOCAL_INDEX'))
print('  generated_at:', d.get('meta',{}).get('generated_at'))
print('  total:', d.get('meta',{}).get('total'), '· entries:', len(d.get('entries',d.get('pages',d.get('items',[])))))
" 2>/dev/null || echo "  （本地索引不可读）"
    info "鲲鹏索引摘要:"
    "${SSH_BASE[@]}" "python3 -c \"
import json
d=json.load(open('${REMOTE_INDEX_DIR}/index.json'))
print('  generated_at:', d.get('meta',{}).get('generated_at'))
print('  total:', d.get('meta',{}).get('total'), '· entries:', len(d.get('entries',d.get('pages',d.get('items',[])))))
\" 2>/dev/null" 2>/dev/null || echo "  （鲲鹏索引不可读或不存在）"
}

case "${1:-all}" in
    sync)   cmd_sync ;;
    push)   cmd_push ;;
    all)    cmd_all ;;
    check)  cmd_check ;;
    status) cmd_status ;;
    *) echo "用法: sync|push|all|check|status"; exit 1 ;;
esac
