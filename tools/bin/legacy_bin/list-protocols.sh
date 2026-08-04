#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 列出龍魂协议库全部协议
# DNA: #龍芯⚡️2026-06-25-LONGHUN-LIST-PROTOCOLS-v1.0

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INDEX="$ROOT/library/protocols/00_CANONICAL_INDEX.md"

if [ ! -f "$INDEX" ]; then
    echo "❌ 协议索引未找到: $INDEX"
    exit 1
fi

echo "📚 龍魂协议库 - 全部协议清单"
echo "=============================="

# 列出所有 markdown 协议文件
find "$ROOT/library/protocols" -type f -name "*.md" | sort | while read -r f; do
    rel="${f#$ROOT/library/protocols/}"
    # 提取 DNA 第一行
    dna=$(grep -m 1 -oE '#龍芯⚡️[^[:space:]]+' "$f" 2>/dev/null || echo "-")
    echo ""
    echo "文件: $rel"
    echo "DNA : $dna"
done

echo ""
echo "🛡️  使用条款: library/protocols/PROTOCOL_USAGE_TERMS.md"
