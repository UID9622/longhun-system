# DNA: #龍芯⚡️丙午·乙未·乙丑·坎-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# 龍魂 · 本地法律引擎启动脚本
nohup python3 "$(dirname "$0")/api_server.py" --port 9634 > "$(dirname "$0")/api_server.log" 2>&1 &
echo $! > "$(dirname "$0")/api_server.pid"
echo "🐉 本地法律引擎已启动: http://127.0.0.1:9634/"
echo "API: POST /query {\"question\":\"...\", \"tone\":\"大白话\"}"
echo "PID: $(cat "$(dirname "$0")/api_server.pid")"
