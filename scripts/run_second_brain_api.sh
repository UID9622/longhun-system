#!/usr/bin/env bash
# 🐉 龍魂第二大脑 · 本地 API 启动脚本
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
