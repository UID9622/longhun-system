#!/bin/bash
# 龍盾v2.0 · 一键转换粘贴板
# 双击即可把粘贴板内容转成AI通用格式
cd "$HOME/longhun-system/龍魂窗口护盾"
python3 longhun_shield_v2.py convert
echo ""
echo "✅ 粘贴板已转换为AI通用格式"
echo "   现在可以粘贴到任何AI对话框"
echo ""
read -r -p "按回车关闭..."
