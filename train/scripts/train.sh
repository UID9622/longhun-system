#!/usr/bin/env bash
# 🐉 龍魂本地训练引擎 · 一键训练脚本
# DNA: #龍芯⚡️2026-06-28-LONGHUN-TRAIN-SCRIPT-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🐉 龍魂本地训练启动"
echo "   项目目录: $PROJECT_DIR"
echo "   DNA: #龍芯⚡️2026-06-28-LONGHUN-TRAIN-SCRIPT-v1.0"

cd "$PROJECT_DIR"

# 检查语料
if [ ! "$(ls -A data/raw/*.txt data/raw/*.md 2>/dev/null)" ]; then
    echo "🔴 data/raw/ 下没有 .txt 或 .md 语料，请先放语料。"
    exit 1
fi

# 运行训练
python3 src/trainer.py

echo "✅ 训练脚本执行完毕"
