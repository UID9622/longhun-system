#!/usr/bin/env bash
# 语义协议 Hook 点 Phase 1 烟测
set -euo pipefail
ROOT="/Users/zuimeidedeyihan/longhun-system"
PY="${ROOT}/venv/bin/python"
if [[ ! -x "$PY" ]]; then
  PY="$(command -v python3)"
fi
export PYTHONPATH="${ROOT}${PYTHONPATH:+:${PYTHONPATH}}"
SAMPLE="语义Hook烟测·$(date +%Y-%m-%dT%H:%M:%S)"
echo "▶ Hook 烟测: ${SAMPLE}"
"$PY" -m cnsh.semantic_protocol.hook_point "$SAMPLE"
TRACE="${ROOT}/logs/semantic_hook_trace.jsonl"
if [[ -f "$TRACE" ]]; then
  echo "▶ 末行留痕:"
  tail -n 1 "$TRACE"
else
  echo "✗ 未生成 ${TRACE}" >&2
  exit 1
fi
echo "✓ 语义 Hook Phase 1 OK"
