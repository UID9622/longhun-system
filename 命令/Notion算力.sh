#!/usr/bin/env bash
# Notion 免费算力 · 四用法入口
# DNA: #龍芯⚡2026-05-19-NOTION-FREE-COMPUTE-v1.0

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="$REPO_ROOT/skills${PYTHONPATH:+:$PYTHONPATH}"

cmd="${1:-help}"
shift || true

case "$cmd" in
  all)        python3 "$REPO_ROOT/skills/notion_power/free_compute.py" all "$@" ;;
  dict|用法1) python3 "$REPO_ROOT/skills/notion_power/free_compute.py" dict-export "$@" ;;
  board|用法2) python3 "$REPO_ROOT/skills/notion_power/free_compute.py" execute-board "$@" ;;
  identity|用法3) python3 "$REPO_ROOT/skills/notion_power/free_compute.py" identity-board "$@" ;;
  kanban|用法4)
    sub="${1:-pull}"
    shift || true
    if [ "$sub" = "run" ]; then
      python3 "$REPO_ROOT/skills/notion_power/free_compute.py" kanban-run "$@"
    else
      python3 "$REPO_ROOT/skills/notion_power/free_compute.py" kanban-pull "$@"
    fi
    ;;
  help|-h)
    cat <<'EOF'
Notion 免费算力 · 本机算 · Notion 存 · 0 LLM

  Notion算力 all              用法1-4 一次导出
  Notion算力 dict [--push]    通心译 → CSV/MD（可选 API 推字典库）
  Notion算力 board            执行日志 → 看板 MD
  Notion算力 identity [--snapshot]  身份审计 MD
  Notion算力 kanban           拉任务 JSON（或离线模板）
  Notion算力 kanban run FILE  跑任务队列 + 五色审计

配置: config.json (token) · config/notion_power.json (database_id)
导出: 数据/notion_export/
EOF
    ;;
  *)
    echo "未知: $cmd · Notion算力 help" >&2
    exit 1
    ;;
esac
