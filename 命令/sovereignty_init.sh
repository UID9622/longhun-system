#!/usr/bin/env bash
# 设备主权锚点 · #ZERO-REGION-NEGOTIATION v1.0
# DNA: #龲芯⚡2026-05-20-ZERO-REGION-NEGOTIATION-v1.0
# 用法: source ~/longhun-system/bin/sovereignty_init.sh
set -euo pipefail

export TZ="${TZ:-Asia/Shanghai}"
export LANG="${LANG:-zh_CN.UTF-8}"
export LC_ALL="${LC_ALL:-zh_CN.UTF-8}"
export LC_CTYPE="${LC_CTYPE:-zh_CN.UTF-8}"
export LC_NUMERIC="${LC_NUMERIC:-zh_CN.UTF-8}"
export LC_TIME="${LC_TIME:-zh_CN.UTF-8}"
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8

# 禁止僭越开关（谁设了谁进黑池）
unset LONGHUN_FORCE_EN_LOCALE 2>/dev/null || true

export LONGHUN_REGION_DNA="#龲芯⚡2026-05-20-ZERO-REGION-NEGOTIATION-v1.0"
export LONGHUN_TZ_ANCHOR="UTC+8"
export LONGHUN_NO_DST=1
export LONGHUN_CURRENCY=CNY
export LONGHUN_WEEK_START=Monday
export LONGHUN_PATH_SEP=/

if [[ "${LONGHUN_REGION_QUIET:-0}" != "1" ]]; then
  echo "🐉 地区主权已锁 · TZ=$TZ · LANG=$LANG · 继承设备锚 UTC+8 无 DST"
  echo "   $LONGHUN_REGION_DNA"
fi
