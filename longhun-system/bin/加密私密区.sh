#!/bin/bash
# 把私密区打包成加密磁盘镜像 · 需要密码才能打开
# 用完卸载，别人看到只是个.dmg文件，打不开

SRC="$HOME/longhun-system/私密区/影像库"
OUT="$HOME/longhun-system/私密区/影像库_加密.dmg"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🔐 创建加密磁盘镜像"
echo "  源目录: $SRC"
echo "  输出: $OUT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  设置密码（输入时不显示）："

hdiutil create \
    -srcfolder "$SRC" \
    -format UDZO \
    -encryption AES-256 \
    -stdinpass \
    -o "$OUT"

if [ $? -eq 0 ]; then
    echo ""
    echo "  ✅ 加密完成：$OUT"
    echo ""
    echo "  打开方式：双击 .dmg 输入密码"
    echo "  用完记得弹出（Finder侧边栏点⏏️）"
else
    echo "  ❌ 失败，请重试"
fi
