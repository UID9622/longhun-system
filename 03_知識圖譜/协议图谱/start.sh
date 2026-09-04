#!/bin/bash
# 协议图谱本地服务器 (端口 8890) — 复用 docs.longhun888.com 同源机制
# 用法: bash start.sh  |  停止: bash stop.sh
cd "$(dirname "$0")"
PORT=8890
# 若已占用先释放, 避免端口冲突
pkill -f "http.server $PORT" 2>/dev/null
sleep 0.5
echo "启动协议图谱本地服务 :$PORT ..."
nohup python3 -m http.server $PORT --bind 0.0.0.0 > /tmp/longhun_protocol_http.log 2>&1 &
echo $! > /tmp/longhun_protocol_http.pid
sleep 1
curl -s -o /dev/null -w "本地访问验证: HTTP %{http_code}\n" "http://127.0.0.1:$PORT/graph.html"
echo "PID: $(cat /tmp/longhun_protocol_http.pid)"
echo "浏览器打开: http://127.0.0.1:$PORT/graph.html"
echo "对外映射(公网): 参照 docs.longhun888.com, 用 cloudflared 命名隧道 'longhun-protocol' 接子域 protocol.longhun888.com"
