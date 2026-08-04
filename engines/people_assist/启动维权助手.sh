#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·观-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# 龍魂 · 老百姓维权助手启动脚本
nohup python3 "$(dirname "$0")/web_app.py" --port 9633 > "$(dirname "$0")/web_app.log" 2>&1 &
echo $! > "$(dirname "$0")/web_app.pid"
echo "🐉 维权助手已启动: http://127.0.0.1:9633/"
echo "PID: $(cat "$(dirname "$0")/web_app.pid")"
