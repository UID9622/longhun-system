#!/bin/bash
# 🐉 龍魂系统 · 乔哈里视窗 一键部署 v1.0
# DNA: #龍芯⚡️2026-08-31-JOHARI-DEPLOY-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622） 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2
# 功能: 生成数据 / 本地预览 / 鲲鹏部署（纯静态·零常驻·nginx 直接服务）
# 用法:
#   bash deploy/deploy_johari.sh sync     # 本地生成 johari_data.json
#   bash deploy/deploy_johari.sh local    # 本地预览（浏览器打开）
#   bash deploy/deploy_johari.sh kunpeng  # 部署鲲鹏 https://uid9622.cn/johari.html
set -e

LONGHUN_ROOT=~/longhun-system
REMOTE="root@119.13.90.27"
REMOTE_DIR="/opt/longhun-system"
SSH_KEY="$HOME/.ssh/longhun_kunpeng_ed25519"
SYNC_SCRIPT="$LONGHUN_ROOT/08_BIN/lh_johari_sync.py"
HTML="$LONGHUN_ROOT/10_PORTAL/johari.html"

echo "🐉 龍魂 · 乔哈里视窗 部署"
echo "确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

do_sync() {
  echo "[sync] 生成四象限数据…"
  python3 "$SYNC_SCRIPT" --out "$LONGHUN_ROOT/10_PORTAL/johari_data.json"
}

local_preview() {
  do_sync
  echo "[local] 打开本地预览…"
  open "$HTML"
}

kunpeng_deploy() {
  do_sync
  echo "[鲲鹏] 同步静态资产（johari.html + johari_data.json）…"
  rsync -az \
    -e "ssh -i $SSH_KEY" \
    "$HTML" \
    "$LONGHUN_ROOT/10_PORTAL/johari_data.json" \
    "$REMOTE:$REMOTE_DIR/portal/"
  echo "[鲲鹏] 验证访问…"
  curl -s --max-time 10 -o /dev/null -w "  johari.html        → %{http_code} (%{size_download}B)\n" \
    "https://uid9622.cn/johari.html"
  curl -s --max-time 10 -o /dev/null -w "  johari_data.json   → %{http_code} (%{size_download}B)\n" \
    "https://uid9622.cn/johari_data.json"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "✅ 乔哈里视窗已上线 → https://uid9622.cn/johari.html"
}

case "${1:-local}" in
  sync)    do_sync ;;
  local)   local_preview ;;
  kunpeng) kunpeng_deploy ;;
  *) echo "用法: $0 {sync|local|kunpeng}" ;;
esac
