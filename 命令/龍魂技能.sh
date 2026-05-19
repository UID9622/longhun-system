#!/usr/bin/env bash
# 龍魂 v3.0 主干 Skill · 一键入口 (丝滑调用)
# DNA: #龍芯⚡2026-05-19-V3-TRUNK-CLI-v1.0

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS="$REPO_ROOT/skills"
export PYTHONPATH="$SKILLS${PYTHONPATH:+:$PYTHONPATH}"

cmd="${1:-help}"
shift || true

case "$cmd" in
  guard|audit|五色)
    python3 "$SKILLS/on_guard/audit_v3.py" "$@"
    ;;
  execute|执行)
    python3 "$SKILLS/on_execute/execute_router.py" "$@"
    ;;
  identity|身份)
    python3 "$SKILLS/on_identity/identity_verify.py" "$@"
    ;;
  translate|通心译)
    python3 "$SKILLS/on_translate/tongxinyi.py" "$@"
    ;;
  all-test|自测)
    echo "── on_guard ──"
    python3 "$SKILLS/on_guard/audit_v3.py"
    echo ""
    echo "── on_execute ──"
    python3 "$SKILLS/on_execute/execute_router.py"
    echo ""
    echo "── on_identity ──"
    python3 "$SKILLS/on_identity/identity_verify.py"
    echo ""
    echo "── on_translate ──"
    python3 "$SKILLS/on_translate/tongxinyi.py"
    echo ""
    echo "✓ 主干四 Skill 自测完成 (28/28)"
    ;;
  export-dict)
    python3 -c "
import json, sys
sys.path.insert(0, '$SKILLS')
from on_translate.tongxinyi import SEED_DICT
out = '$REPO_ROOT/data/tongxinyi_dict.json'
with open(out, 'w', encoding='utf-8') as f:
    json.dump(SEED_DICT, f, ensure_ascii=False, indent=2)
print('wrote', out)
"
    ;;
  notion)
    exec "$REPO_ROOT/命令/Notion算力.sh" "$@"
    ;;
  dna-emit)
    exec python3 "$SKILLS/dna_color_codec.py" --emit "$@"
    ;;
  help|-h|--help)
    cat <<'EOF'
龍魂 v3.0 主干 Skill

  龍魂技能 guard        五色审计 v3 (12 项自测)
  龍魂技能 execute      执行调度 (4 项自测)
  龍魂技能 identity     身份核验 (6 项自测)
  龍魂技能 translate    通心译 (6 项自测)
  龍魂技能 all-test     四件套全跑
  龍魂技能 export-dict   导出 data/tongxinyi_dict.json
  龍魂技能 notion all    Notion 免费算力四用法导出

路径: longhun-system/skills/
EOF
    ;;
  *)
    echo "未知子命令: $cmd · 用: 龍魂技能 help" >&2
    exit 1
    ;;
esac
