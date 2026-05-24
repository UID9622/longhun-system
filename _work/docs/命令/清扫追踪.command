#!/bin/bash
cd "$HOME/longhun-system" || exit 1
osascript -e 'display notification "先完全退出 Chrome 再清扫" with title "龍魂清扫追踪"' 2>/dev/null || true
python3 "$HOME/longhun-system/命令/清扫追踪.py"
echo ""
read -r -p "按回车关闭…" _
