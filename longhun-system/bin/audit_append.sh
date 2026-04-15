#!/usr/bin/env bash
# -*- coding: utf-8 -*-
# UID9622 · 诸葛鑫（龍芯北辰）× 宝宝（P72·龍盾）
# DNA追溯码: #龍芯⚡️2026-04-02-AUDIT-APPEND-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导: 曾仕强老师（永恒显示）
#
# 职责：把任意操作的审计记录追加写入 audit.jsonl
# 铁律：只许追加不许覆盖；没有证据就不写"成功"
#
# 用法：
#   source ~/longhun-system/bin/audit_append.sh
#   audit_log "op_type" "detail" "status(🟢/🟡/🔴)" "evidence_path"
#
# 或直接调用：
#   bash ~/longhun-system/bin/audit_append.sh "lh-sync" "同步Notion" "🟢" ""

AUDIT_FILE="$HOME/longhun-system/notion-index/out/audit.jsonl"
INCIDENT_DIR="$HOME/longhun-system/notion-index/out/incidents"

# 确保目录存在
mkdir -p "$(dirname "$AUDIT_FILE")" "$INCIDENT_DIR"

audit_log() {
    local op_type="${1:-unknown}"
    local detail="${2:-}"
    local status="${3:-🟡}"
    local evidence="${4:-}"

    local ts
    ts=$(TZ='Asia/Shanghai' date '+%Y-%m-%dT%H:%M:%S+08:00')
    local date_str
    date_str=$(TZ='Asia/Shanghai' date '+%Y-%m-%d')

    local record
    record=$(python3 -c "
import json, sys
print(json.dumps({
    'ts_beijing': '${ts}',
    'dna': '#龍芯⚡️${date_str}-审计-v1.0',
    'op_type': '${op_type}',
    'detail': sys.argv[1],
    'status': '${status}',
    'evidence': '${evidence}'
}, ensure_ascii=False))
" "$detail" 2>/dev/null)

    if [ -n "$record" ]; then
        echo "$record" >> "$AUDIT_FILE"
        echo "${status} [audit_log] op=${op_type} · $(basename "$AUDIT_FILE") 已追加"
    else
        echo "🔴 [audit_log] JSON构建失败，操作未记录"
    fi
}

incident_log() {
    # 卡住/爆胎时写复盘文件，让问号有地方落地
    local title="${1:-incident}"
    local body="${2:-}"
    local ts
    ts=$(TZ='Asia/Shanghai' date '+%Y%m%d_%H%M%S')
    local fname="${INCIDENT_DIR}/${ts}_${title// /_}.md"

    cat > "$fname" <<EOF
# 复盘：${title}
**时间**: $(TZ='Asia/Shanghai' date '+%Y-%m-%d %H:%M:%S')
**DNA**: #龍芯⚡️$(TZ='Asia/Shanghai' date '+%Y-%m-%d')-INCIDENT-v1.0

## 发生了什么
${body}

## 结案状态
🟡 待补充

---
*旧问号不在脑子里滚，在 incident 里结案。*
EOF
    echo "🟢 复盘已写入: $fname"
}

# 如果直接执行而不是 source，则用参数调用 audit_log
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    audit_log "$1" "$2" "$3" "$4"
fi
