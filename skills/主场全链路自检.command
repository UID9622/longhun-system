#!/bin/bash
cd "$HOME/longhun-system" || exit 1
bash bin/主场全链路自检.sh --fix
echo ""
read -r -p "按回车关闭…" _
