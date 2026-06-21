#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# 龍魂體系 · 待融入包監控器本地運行腳本
# DNA:#龍芯⚡️2026-06-16-PACKAGE-WATCHER-RUNNER-FILE1-v1.0
# UID9622 · 龍芯北辰 · 诸葛鑫
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LONGHUN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
MODE="${1:-local}"   # local 或 container

usage() {
    cat << EOF
用法: $(basename "$0") [local|container|once|help]

  local      直接運行 Python 監控器一次（默認）
  container  使用 Docker Compose 啟動容器化監控
  once       運行一次後退出
  help       顯示此幫助

環境變數：
  WATCH_INTERVAL   循環監控間隔秒數（默認 300）
EOF
}

case "$MODE" in
    help|-h|--help)
        usage
        exit 0
        ;;
    local)
        echo "🐉 本地運行待融入包監控器..."
        python3 "$LONGHUN_DIR/bin/package-watcher.py" \
            --watch-dir "$HOME/Downloads" \
            --watch-dir "$HOME" \
            --output-dir "$LONGHUN_DIR/docs" \
            --prune \
            --once
        echo ""
        echo "✅ 監控完成"
        echo "   報告: $LONGHUN_DIR/docs/package-watcher-report.md"
        echo "   隊列: $LONGHUN_DIR/docs/package-integration-queue.json"
        ;;
    once)
        echo "🐉 本地運行一次..."
        python3 "$LONGHUN_DIR/bin/package-watcher.py" \
            --watch-dir "$HOME/Downloads" \
            --watch-dir "$HOME" \
            --output-dir "$LONGHUN_DIR/docs" \
            --prune \
            --once
        ;;
    container)
        echo "🐳 啟動容器化監控器..."
        cd "$LONGHUN_DIR/docker"
        docker compose up -d --build
        echo ""
        echo "✅ 容器已啟動"
        echo "   查看日誌: docker compose logs -f package-watcher"
        echo "   停止容器: docker compose down"
        ;;
    *)
        echo "未知模式: $MODE"
        usage
        exit 1
        ;;
esac
