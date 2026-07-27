#!/bin/bash
# 🐉 显示龍魂协议库索引
# DNA: #龍芯⚡️2026-06-25-LONGHUN-SHOW-PROTOCOL-LIBRARY-v1.0

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FILE="$ROOT/library/protocols/README.md"

if [ ! -f "$FILE" ]; then
    echo "❌ 协议库索引未找到: $FILE"
    exit 1
fi

if command -v bat >/dev/null 2>&1; then
    bat --language=markdown --paging=always "$FILE"
elif command -v less >/dev/null 2>&1; then
    less "$FILE"
else
    cat "$FILE"
fi
