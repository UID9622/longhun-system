#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# 龍魂体系 · CNSH 中文原生脚本运行入口
# DNA:#龍芯⚡️2026-06-16-CNSH-RUNNER-FILE1-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# UID9622 · 龍芯北辰 · 诸葛鑫
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LONGHUN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
RUNNER="$LONGHUN_DIR/cnsh/core/cnsh-runtime/cnsh_runner.py"

usage() {
    cat << EOF
用法: $(basename "$0") <file.cnsh> [选项]
       $(basename "$0") --repl
       $(basename "$0") --help

选项:
  --explain      输出通心译解释注释
  --show-code    显示转译后的 Python 代码
  --dry-run      仅转译不执行
  --repl         进入交互式 CNSH 解释器
  -h, --help     显示此帮助

示例:
  $(basename "$0") cnsh/core/cnsh-runtime/examples/hello.cnsh
  $(basename "$0") cnsh/core/cnsh-runtime/examples/longhun_audit.cnsh --explain --show-code
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
