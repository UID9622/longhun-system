#!/bin/zsh
read -s -p "AppSecret: " SECRET
echo ""
echo "WX_APP_SECRET=$SECRET" >> ~/longhun-system/longhun_config.env
echo "已存入 ✅"
