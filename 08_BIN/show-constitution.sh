#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 显示龍魂系统宪法
# DNA: #龍芯⚡️丙午·甲午·庚午·壬午·䷳艮为山-LONGHUN-SHOW-CONSTITUTION-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FILE="$ROOT/CONSTITUTION.md"

if [ ! -f "$FILE" ]; then
    echo "❌ 宪法文件未找到: $FILE"
    exit 1
fi

if command -v bat >/dev/null 2>&1; then
    bat --language=markdown --paging=always "$FILE"
elif command -v less >/dev/null 2>&1; then
    less "$FILE"
else
    cat "$FILE"
fi
