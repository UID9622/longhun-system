#!/bin/bash
# 停止协议图谱本地服务 (端口 8890)
if [ -f /tmp/longhun_protocol_http.pid ]; then
  PID=$(cat /tmp/longhun_protocol_http.pid)
  kill "$PID" 2>/dev/null && echo "已停止协议图谱服务 PID=$PID"
  rm -f /tmp/longhun_protocol_http.pid
else
  pkill -f "http.server 8890" && echo "已停止(按端口匹配)" || echo "协议图谱服务未在运行"
fi
