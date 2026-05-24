#!/usr/bin/env bash
# 龍魂 · 指纹三测 · 本机自跑 A
# DNA: #龍芯⚡2026-05-19-FINGERPRINT-SNAPSHOT-v1.0
set -euo pipefail
LONGHUN_ROOT="$HOME/longhun-system"
LOGDIR="$LONGHUN_ROOT/日志"
DATE=$(date +%Y%m%d)
OUT="$LOGDIR/指纹快照_${DATE}.txt"
mkdir -p "$LOGDIR"

{
  echo "════════════════════════════════════════"
  echo "龍魂指纹快照 · $DATE · $(date '+%H:%M:%S %z')"
  echo "DNA: #龍芯⚡2026-05-19-FINGERPRINT-SNAPSHOT-v1.0"
  echo "════════════════════════════════════════"
  echo ""
  echo "【网络 · 公网出口】"
  curl -sS --max-time 12 https://ifconfig.me/ip 2>/dev/null && echo " ← ifconfig.me" || echo "(ifconfig.me 超时)"
  curl -sS --max-time 12 https://api.ipify.org 2>/dev/null && echo " ← ipify" || true
  echo ""
  echo "【时区 / 语言环境】"
  echo "TZ=${TZ:-$(readlink /etc/localtime 2>/dev/null || echo 系统默认)}"
  date
  echo "LANG=$LANG"
  echo ""
  echo "【browserleaks 探测】(HTML 摘要·完整请浏览器开 browserleaks.com/webrtc)"
  curl -sS --max-time 15 -A "Mozilla/5.0" https://browserleaks.com/ip 2>/dev/null | \
    grep -Eo '(IPv4|IPv6|Country|ISP|Timezone)[^<]*' | head -12 || echo "(需联网·或用手动三测)"
  echo ""
  echo "【本机硬件 · system_profiler】"
  system_profiler SPHardwareDataType SPDisplaysDataType 2>/dev/null | \
    grep -E 'Model Name|Chip|Memory|Serial|Graphics|Metal' | head -20
  echo ""
  echo "【网卡 MAC · 活跃接口】"
  ifconfig 2>/dev/null | awk '/^[a-z]/{iface=$1} /ether/{print iface, $2}' | head -8
  echo ""
  echo "【主机名】"
  scutil --get ComputerName 2>/dev/null || hostname
  echo ""
  echo "── 完 · 日志: $OUT"
} | tee "$OUT"

echo ""
echo "✅ 摘要已写入: $OUT"
