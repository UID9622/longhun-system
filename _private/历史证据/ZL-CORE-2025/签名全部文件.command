#!/bin/bash
# ZL-CORE 原创证据 · GPG 批量签名脚本
# DNA: #龍芯⚡️2026-05-21-GPG-SIGN-SCRIPT
# 双击运行，输入一次 GPG 密码即可签名全部文件

cd "$(dirname "$0")"
echo ""
echo "🔐 ZL-CORE 原创证据 · GPG 签名"
echo "================================"
echo ""
echo "密钥: A2D0092CEE2E5BA87035600924C3704A8CC26D5F (诸葛鑫 · UID9622)"
echo ""

KEY="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
COUNT=0

for f in *.py; do
    echo "📝 签名: $f"
    gpg --detach-sign --armor --local-user "$KEY" "$f"
    if [ $? -eq 0 ]; then
        ((COUNT++))
        echo "   ✅ → $f.asc"
    else
        echo "   ❌ 签名失败"
    fi
done

echo ""
echo "================================"
echo "✅ 完成: $COUNT 个文件已签名"
echo ""
ls -la *.asc 2>/dev/null
echo ""
read -r -p "按回车关闭..."
