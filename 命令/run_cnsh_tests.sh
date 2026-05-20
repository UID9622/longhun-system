#!/usr/bin/env bash
# CNSH 闸门/流场/三才 单元测试 · PR 验收用
set -euo pipefail
ROOT="/Users/zuimeidedeyihan/longhun-system"
PY="${ROOT}/venv/bin/python"
export PYTHONPATH="${ROOT}"

if ! "${PY}" -c "import pytest" 2>/dev/null; then
  echo "正在安装 pytest（仅首次）…"
  "${PY}" -m pip install -q -r "${ROOT}/requirements-dev.txt"
fi

cd "${ROOT}"
exec "${PY}" -m pytest \
  CNSH/gate_v3/tests \
  CNSH/flow_field/tests \
  CNSH/algorithms/tests \
  CNSH/root_ratio/tests \
  CNSH/sovereign/tests \
  -q "$@"
