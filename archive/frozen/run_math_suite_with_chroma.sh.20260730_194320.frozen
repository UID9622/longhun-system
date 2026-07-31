#!/usr/bin/env bash
# 🧮 龍魂数学公式套件统一运行器（Chroma 向量检索启用版）
# DNA: #龍芯⚡️2026-07-06-MATH-SUITE-CHROMA-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色审计: 🟢 通过
#
# 说明：
#   系统默认 Python 可能未安装 chromadb + sentence-transformers，
#   本脚本使用项目隔离虚拟环境 .venv_longhun_math 运行统一运行器，
#   从而激活 terminology_bank 的 Chroma 向量搜索能力。
#
# 用法：
#   bash scripts/run_math_suite_with_chroma.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
VENV_DIR="${PROJECT_ROOT}/.venv_longhun_math"
PYTHON="${VENV_DIR}/bin/python"

if [[ ! -x "${PYTHON}" ]]; then
    echo "🔴 未找到隔离 venv：${VENV_DIR}"
    echo "   请先创建并安装依赖："
    echo "   python3 -m venv ${VENV_DIR}"
    echo "   ${VENV_DIR}/bin/pip install chromadb sentence-transformers"
    exit 1
fi

# 国内网络环境下优先使用 HuggingFace 镜像下载嵌入模型
export HF_ENDPOINT="${HF_ENDPOINT:-https://hf-mirror.com}"

echo "🐉 使用隔离 venv 运行龍魂数学公式套件：${VENV_DIR}"
exec "${PYTHON}" "${SCRIPT_DIR}/run_math_suite.py"
