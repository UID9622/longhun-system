#!/bin/bash
# 🐉 显示 P0 永恒锁协议
# DNA: #龍芯⚡️2026-06-25-LONGHUN-SHOW-ETERNAL-LOCK-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FILE="$ROOT/P0_ETERNAL_LOCK.md"

if [ ! -f "$FILE" ]; then
    echo "❌ 永恒锁文件未找到: $FILE"
    exit 1
fi

if command -v bat >/dev/null 2>&1; then
    bat --language=markdown --paging=always "$FILE"
elif command -v less >/dev/null 2>&1; then
    less "$FILE"
else
    cat "$FILE"
fi
