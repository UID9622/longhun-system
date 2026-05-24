#!/usr/bin/env bash
# 鲁班绿闸：CNSW（暂存补丁）+ 提交说明 dr + 涉密路径 → 全绿才 git commit（不 push）
# 用法：bash /Users/zuimeidedeyihan/longhun-system/bin/luban_green_commit.sh -m "提交说明"
# 预览：LUBAN_DRY_RUN=1 bash ...
# 本机 GPG 卡住：LUBAN_NO_GPG=1 bash ...
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}${PYTHONPATH:+:$PYTHONPATH}"
exec python3 -m cnsh.cnsw.luban_commit "$@"
