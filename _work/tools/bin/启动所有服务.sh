#!/usr/bin/env bash
# 启动 longhun-system 所需的守护与服务（示例骨架）
set -euo pipefail

echo "启动 agent_daemon.py..."
if [ -f "$(pwd)/agent_daemon.py" ]; then
  nohup python3 $(pwd)/agent_daemon.py >/tmp/longhun_agent_daemon.log 2>&1 &
  echo "agent_daemon started (logs -> /tmp/longhun_agent_daemon.log)"
else
  echo "warning: agent_daemon.py not found in repo root"
fi

echo "（示例）启动 webhooks 或其他服务请在此添加具体命令"

echo "done"
