#!/bin/bash
# 🐉 显示龍魂产出标准
# DNA: #龍芯⚡️2026-06-25-LONGHUN-SHOW-STANDARD-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FILE="$ROOT/STANDARD.md"

if [ ! -f "$FILE" ]; then
    echo "❌ 标准文件未找到: $FILE"
    exit 1
fi

if command -v bat >/dev/null 2>&1; then
    bat --language=markdown --paging=always "$FILE"
elif command -v less >/dev/null 2>&1; then
    less "$FILE"
else
    cat "$FILE"
fi
