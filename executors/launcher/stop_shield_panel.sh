#!/bin/bash
cd "$(dirname "$0")"
if [ -f .shield_panel.pid ]; then
  kill "$(cat .shield_panel.pid)" 2>/dev/null || true
  rm -f .shield_panel.pid
fi
pkill -f "longhun_shield_panel.py" 2>/dev/null || true
echo "龍魂护盾 Web 面板已停止"
