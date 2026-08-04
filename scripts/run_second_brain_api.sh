#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂第二大脑 · 本地 API 启动脚本
# DNA: #龍芯⚡️2026-07-06-SECOND-BRAIN-API-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色审计: 🟢 通过
# 用法: bash scripts/run_second_brain_api.sh [port]
#
# 默认使用本地 TF-IDF+SVD 嵌入（无需网络）。
# 如需 sentence-transformers，先设置: export SECOND_BRAIN_USE_ST=1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PORT="${1:-8787}"
VENV_PYTHON="${PROJECT_ROOT}/.venv_longhun_math/bin/python"

cd "${PROJECT_ROOT}"

export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH:-}"

echo "🧠 启动龍魂第二大脑 API: http://127.0.0.1:${PORT}"
"${VENV_PYTHON}" -m uvicorn second_brain.api:app --host 127.0.0.1 --port "${PORT}"
