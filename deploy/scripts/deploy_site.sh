#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════════════
# 龍魂·官网静态部署到鲲鹏
# 用法: bash deploy/scripts/deploy_site.sh [build|deploy|all]
# DNA: #龍芯⚡️丙午·丙申·癸丑·戊午·䷨损-DEPLOY-SITE-SCRIPT-v1.0
# ═══════════════════════════════════════════════════════

set -euo pipefail
LH_ROOT="$(cd "$(dirname "$0")/../../" && pwd)"
SITE_DIR="$LH_ROOT/web_apps/longhun-dna-generator/app"
KUNPENG_KEY="${KUNPENG_KEY:-$HOME/.ssh/longhun_kunpeng_ed25519}"
KUNPENG_TARGET="/opt/longhun/portal/dna-site"
MODE="${1:-all}"

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║  🐉 龍魂官网部署 · uid9622.cn         ║"
echo "║  模式: $MODE                           ║"
echo "╚═══════════════════════════════════════╝"

# ── Build ──
build_site() {
  echo "🔨 构建静态站点..."
  cd "$SITE_DIR"
  npx vite build
  echo "✅ 构建完成 ($(du -sh dist/ | cut -f1))"
}

# ── Deploy to Kunpeng ──
deploy_site() {
  echo "📤 部署到鲲鹏 119.13.90.27..."

  if ! ssh -i "$KUNPENG_KEY" -o ConnectTimeout=5 root@119.13.90.27 "echo ok" 2>/dev/null; then
    echo "❌ 鲲鹏不可达"
    exit 1
  fi

  # 创建目录
  ssh -i "$KUNPENG_KEY" root@119.13.90.27 "mkdir -p $KUNPENG_TARGET"

  # 同步文件（排除 assets/ 哈希文件名保留旧版）
  rsync -az --delete --progress -e "ssh -i $KUNPENG_KEY" \
    "$SITE_DIR/dist/" "root@119.13.90.27:$KUNPENG_TARGET/"

  # 设置nginx权限
  ssh -i "$KUNPENG_KEY" root@119.13.90.27 "chown -R nginx:nginx $KUNPENG_TARGET 2>/dev/null || chown -R www-data:www-data $KUNPENG_TARGET 2>/dev/null || true"

  # Nginx热重载
  if ssh -i "$KUNPENG_KEY" root@119.13.90.27 "nginx -t 2>&1 && nginx -s reload 2>&1"; then
    echo "✅ Nginx 热重载完成"
  else
    echo "⚠️ Nginx 重载失败（检查配置）"
  fi

  echo "✅ 部署完成 → https://uid9622.cn/"
}

case "$MODE" in
  build) build_site ;;
  deploy) deploy_site ;;
  all)
    build_site
    deploy_site
    ;;
  *)
    echo "用法: $0 [build|deploy|all]"
    exit 1
    ;;
esac

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║  ✅ 部署流程完成                       ║"
echo "║  站点: https://uid9622.cn/             ║"
echo "╚═══════════════════════════════════════╝"
