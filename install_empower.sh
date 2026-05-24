#!/bin/bash
set -e
echo "⚡ 龍魂赋能引擎 v1.5 安装开始..."
mkdir -p ~/longhun-system/{data,logs}
cd ~/longhun-system
pip3 install flask requests -q
chmod 600 config.json 2>/dev/null || true
echo '{"test":"ok"}' > ~/longhun-system/data/.init
echo "🟢 安装完成 | DNA: #龍芯⚡️2026-05-17-INSTALL"
echo "🟡 下一步：编辑 config.json 填 Notion Token"
echo "🟡 然后：sudo cp longhun.service /etc/systemd/system/ && sudo systemctl start longhun"
