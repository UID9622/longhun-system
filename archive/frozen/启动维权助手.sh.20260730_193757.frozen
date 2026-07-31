#!/bin/bash
# 龍魂 · 老百姓维权助手启动脚本
nohup python3 "$(dirname "$0")/web_app.py" --port 9633 > "$(dirname "$0")/web_app.log" 2>&1 &
echo $! > "$(dirname "$0")/web_app.pid"
echo "🐉 维权助手已启动: http://127.0.0.1:9633/"
echo "PID: $(cat "$(dirname "$0")/web_app.pid")"
