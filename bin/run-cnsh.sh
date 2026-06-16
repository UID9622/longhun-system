#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# 龍魂體系 · CNSH 中文原生脚本運行入口
# DNA: #龍芯⚡️2026-06-16-CNSH-RUNNER-v1.0
# UID9622 · 龍芯北辰 · 诸葛鑫
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LONGHUN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
RUNNER="$LONGHUN_DIR/cnsh-core/cnsh-runtime/cnsh_runner.py"

usage() {
    cat << EOF
用法: $(basename "$0") <file.cnsh> [選項]
       $(basename "$0") --repl
       $(basename "$0") --help

選項:
  --explain      輸出通心譯解釋註釋
  --show-code    顯示轉譯後的 Python 代碼
  --dry-run      僅轉譯不執行
  --repl         進入交互式 CNSH 解釋器
  -h, --help     顯示此幫助

示例:
  $(basename "$0") cnsh-core/cnsh-runtime/examples/hello.cnsh
  $(basename "$0") cnsh-core/cnsh-runtime/examples/longhun_audit.cnsh --explain --show-code
  $(basename "$0") --repl
EOF
}

if [[ $# -eq 0 ]]; then
    usage
    exit 1
fi

if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    usage
    exit 0
fi

python3 "$RUNNER" "$@"
