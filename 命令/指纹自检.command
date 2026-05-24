#!/bin/bash
cd "$HOME/longhun-system" || exit 1
bash "$HOME/longhun-system/命令/指纹自检.sh"
echo ""
read -r -p "按回车关闭…" _
