# DNA: #龍芯⚡️丙午·乙未·乙丑·中孚-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
cd "$(dirname "$0")"
if [ -f .download_guard.pid ]; then
  kill "$(cat .download_guard.pid)" 2>/dev/null || true
  rm -f .download_guard.pid
fi
pkill -f "longhun_download_guard.py" 2>/dev/null || true
echo "龍魂下载守卫已停止"
