#!/bin/bash
cd "$(dirname "$0")"
if [ -f .download_guard.pid ]; then
  kill "$(cat .download_guard.pid)" 2>/dev/null || true
  rm -f .download_guard.pid
fi
pkill -f "longhun_download_guard.py" 2>/dev/null || true
echo "龍魂下载守卫已停止"
