#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂创作者保护协议 · GPG 签名助手
# DNA: #龍芯⚡️2026-06-21-SIGN-CREATOR-PROTECTION-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -euo pipefail

cd "$(dirname "$0")/.."

PROTOCOL="01_protocols/LONGHUN-CREATOR-PROTECTION-v1.0.md"
SIG="01_protocols/LONGHUN-CREATOR-PROTECTION-v1.0.md.asc"
FPR="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

if [[ ! -f "$PROTOCOL" ]]; then
    echo "❌ 协议文件不存在: $PROTOCOL"
    exit 1
fi

if [[ -f "$SIG" ]]; then
    echo "🗑️  删除旧签名: $SIG"
    rm "$SIG"
fi

echo "🔐 正在为协议生成 GPG detached 签名..."
echo "   密钥指纹: $FPR"
echo "   如果系统询问密码，请输入 GPG 私钥密码。"
echo ""

gpg --armor --detach-sign --local-user "$FPR" -o "$SIG" "$PROTOCOL"

echo ""
echo "✅ 签名已生成: $SIG"
echo "🔍 正在验证..."
gpg --verify "$SIG" "$PROTOCOL"
