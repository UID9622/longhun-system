#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ═══════════════════════════════════════════════════════════════════════════════
# 龍魂体系 · 待融入包监控器本地运行脚本
# DNA:#龍芯⚡️丙午·甲午·辛酉·甲午·䷨损-PACKAGE-WATCHER-RUNNER-FILE1-FILE1-v1.0
# UID9622 · 龍芯北辰 · 诸葛鑫
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LONGHUN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
MODE="${1:-local}"   # local 或 container

usage() {
    cat << EOF
用法: $(basename "$0") [local|container|once|help]

  local      直接运行 Python 监控器一次（默认）
  container  使用 Docker Compose 启动容器化监控
  once       运行一次后退出
  help       显示此帮助

环境变数：
  WATCH_INTERVAL   循环监控间隔秒数（默认 300）
EOF
}

case "$MODE" in
    help|-h|--help)
        usage
        exit 0
        ;;
    local)
        echo "🐉 本地运行待融入包监控器..."
        python3 "$LONGHUN_DIR/bin/package-watcher.py" \
            --watch-dir "$HOME/Downloads" \
            --watch-dir "$HOME" \
            --output-dir "$LONGHUN_DIR/docs" \
            --prune \
            --once
        echo ""
        echo "✅ 监控完成"
        echo "   报告: $LONGHUN_DIR/docs/package-watcher-report.md"
        echo "   队列: $LONGHUN_DIR/docs/package-integration-queue.json"
        ;;
    once)
        echo "🐉 本地运行一次..."
        python3 "$LONGHUN_DIR/bin/package-watcher.py" \
            --watch-dir "$HOME/Downloads" \
            --watch-dir "$HOME" \
            --output-dir "$LONGHUN_DIR/docs" \
            --prune \
            --once
        ;;
    container)
        echo "🐳 启动容器化监控器..."
        cd "$LONGHUN_DIR/docker"
        docker compose up -d --build
        echo ""
        echo "✅ 容器已启动"
        echo "   查看日志: docker compose logs -f package-watcher"
        echo "   停止容器: docker compose down"
        ;;
    *)
        echo "未知模式: $MODE"
        usage
        exit 1
        ;;
esac
