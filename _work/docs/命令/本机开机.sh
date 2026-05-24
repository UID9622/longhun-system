#!/usr/bin/env bash
# 只开本机网页（不依赖公网隧道）· 新开终端也能用
# DNA: #龍芯⚡️2026-05-18-LOCAL-BOOT-v1.0
set -euo pipefail
# shellcheck source=_longhun_common.sh
source "$(dirname "$0")/_longhun_common.sh"

echo "════════════════════════════════════════"
echo "  🐉 龍魂本机开机（9625 + 官网 + 操作台）"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "════════════════════════════════════════"
echo ""

echo "① 9625 龍魂引擎"
bash "${LONGHUN_ROOT}/bin/开龍魂9625" || true
echo ""

echo "② 官网 :9626"
bash "${LONGHUN_ROOT}/bin/开官网" || true
echo ""

echo "③ 操作台 :8765"
bash "${LONGHUN_ROOT}/bin/开操作台" || true
echo ""

echo "════════════════════════════════════════"
echo "  浏览器打开："
echo "  DNA 控制台  http://127.0.0.1:9625/console"
echo "  操作台      http://127.0.0.1:8765/00_main_control/操作台v3/components/龍魂操作台_MVP_v1.html"
echo "  官网        http://127.0.0.1:9626/"
echo "════════════════════════════════════════"
echo "✅ 本机开机完成（公网隧道未启动·不影响本机用）"
