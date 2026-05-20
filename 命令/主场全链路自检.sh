#!/usr/bin/env bash
# 主场全链路自检 · 一条命令查全仓+能修就修
# DNA: #龍芯⚡2026-05-20-HOME-FULL-CHAIN-AUTO-v1.0
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./_longhun_common.sh
source "${SCRIPT_DIR}/_longhun_common.sh"

[ -f "$HOME/.longhun/secrets.env" ] && set -a && source "$HOME/.longhun/secrets.env" && set +a

exec "${VENV_PY:-python3}" "${SCRIPT_DIR}/主场全链路自检.py" "$@"
