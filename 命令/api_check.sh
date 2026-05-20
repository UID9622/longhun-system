#!/usr/bin/env bash
# API 联动检测 · 与 ~/.claude/skills/api-check 对齐
# DNA: #龍芯⚡2026-05-20-API-CHECK-v1.5
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "${SCRIPT_DIR}/主场全链路自检.sh" "$@"
