# DNA: #龍芯⚡️丙午·乙未·乙丑·中孚-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
cd "$(dirname "$0")"
if [ -f .shield_panel.pid ]; then
  kill "$(cat .shield_panel.pid)" 2>/dev/null || true
  rm -f .shield_panel.pid
fi
pkill -f "longhun_shield_panel.py" 2>/dev/null || true
echo "龍魂护盾 Web 面板已停止"
