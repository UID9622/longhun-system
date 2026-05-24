#!/usr/bin/env bash
# 主场开发环境 · 开机查验 + 留痕
# DNA: #龍芯⚡2026-05-18-HOME-BATTLEFIELD-CHECK-v1.0
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./_longhun_common.sh
source "${SCRIPT_DIR}/_longhun_common.sh"

TRACE="${LOG_DIR}/home_battlefield_trace.jsonl"
STAMP="$(date '+%Y-%m-%dT%H:%M:%S%z')"
CONFIRM_TAG='#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z'

mkdir -p "${LOG_DIR}" "${RUN_DIR}"

log() {
  printf '{"ts":"%s","event":"%s","detail":"%s","dna":"#龍芯⚡2026-05-18-HOME-BATTLEFIELD-CHECK-v1.0"}\n' \
    "$STAMP" "$1" "${2//\"/\\\"}" >>"$TRACE"
}

port_ok() {
  local p="$1"
  if lsof -nP -iTCP:"$p" -sTCP:LISTEN >/dev/null 2>&1; then echo "🟢 LISTEN"; else echo "⚪ down"; fi
}

# 数字根（仅取数字；与公式 dr(n)=1+((n-1) mod 9) 对齐）
dr_from_text() {
  local t="$1"
  local digits sum n
  digits="$(echo -n "$t" | tr -cd '0-9')"
  if [[ -z "$digits" ]]; then echo 0; return; fi
  sum=0
  for ((i = 0; i < ${#digits}; i++)); do
    sum=$((sum + ${digits:i:1}))
  done
  while ((sum >= 10)); do
    n=0
    while ((sum > 0)); do
      n=$((n + sum % 10))
      sum=$((sum / 10))
    done
    sum=$n
  done
  if ((sum == 0)); then echo 9; else echo "$sum"; fi
}

echo "=== 主场开发环境查验 ==="
echo "时间: $STAMP"
echo "仓库: $LONGHUN_ROOT"
log "start" "主场开机查验"

echo ""
echo "【L1 硬件 / L2 系统】"
echo "本机: $(uname -n)"
port_ok 9625 | xargs echo -n "9625 "; port_ok 8765 | xargs echo -n "8765 "
port_ok 11434 | xargs echo -n "11434 "; port_ok 9623 | xargs echo -n "9623"

echo ""
echo "【L3 工具】"
test -x "${LONGHUN_ROOT}/bin/爸爸一键全开.sh" && echo "爸爸一键全开.sh: 🟢" || echo "爸爸一键全开.sh: 🔴"
test -f "${LONGHUN_ROOT}/engine/.env" && echo "engine/.env: 🟢 (存在)" || echo "engine/.env: 🟡 缺失"

echo ""
echo "【L4 知识 / L5 输出】"
if [[ -f "${LONGHUN_ROOT}/longhun-system/BehavCrypto_v1.0/CANONICAL_SHA256" ]]; then
  if (cd "${LONGHUN_ROOT}/longhun-system" && bash scripts/canonical-sha256/verify.sh >/dev/null 2>&1); then
    echo "BehavCrypto SHA256: 🟢 verify OK"
    log "sha256" "BehavCrypto verify OK"
  else
    echo "BehavCrypto SHA256: 🟡 verify FAIL"
    log "sha256" "BehavCrypto verify FAIL"
  fi
else
  echo "BehavCrypto CANONICAL: ⚪ 未找到 nested 包"
fi

echo ""
echo "【五道闸门 G1–G5】"
if bash "${LONGHUN_ROOT}/bin/龍字符律扫描.sh" >/dev/null 2>&1; then
  echo "G5 字符律: 🟢 龍字符律扫描通过"
  log "gate" "G5 long-char-law OK"
else
  echo "G5 字符律: 🔴 发现简体「龍」误用 · 运行: bash ${LONGHUN_ROOT}/bin/龍字符律扫描.sh"
  log "gate" "G5 long-char-law FAIL"
fi

DR="$(dr_from_text "$CONFIRM_TAG")"
echo "CONFIRM 数字根 dr=$DR"
if [[ "$DR" == 3 || "$DR" == 9 ]]; then
  echo "数字根闸门: 🔴 dr∈{3,9} 建议熔断复核"
  log "gate" "dr fuse zone dr=$DR"
else
  echo "数字根闸门: 🟢"
  log "gate" "dr pass dr=$DR"
fi

echo ""
echo "留痕: $TRACE"
log "done" "主场开机查验 complete"
echo ""
echo "=== 完成 · 三色见日志 ==="
