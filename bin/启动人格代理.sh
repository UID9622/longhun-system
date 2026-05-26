#!/usr/bin/env bash
# 启动并激活龙魂人格代理，同时生成审核激活日志
# 适用于: /Users/zuimeidedeyihan/longhun-system

set -euo pipefail
BASE_DIR="$HOME/longhun-system"
LOG_DIR="$BASE_DIR/logs"
LOG_FILE="$LOG_DIR/persona_activation_$(date +'%Y%m%d_%H%M%S').log"

mkdir -p "$LOG_DIR"
cd "$BASE_DIR"

echo "[START] 人格激活流程 $(date '+%Y-%m-%d %H:%M:%S')" | tee "$LOG_FILE"
echo "工作目录: $BASE_DIR" | tee -a "$LOG_FILE"

echo "1) 激活人格全景系统" | tee -a "$LOG_FILE"
python3 cnsh/persona_cnsh_activation.py 2>&1 | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "2) 生成审计提交摘要" | tee -a "$LOG_FILE"
python3 - <<'PY' 2>&1 | tee -a "$LOG_FILE"
import json
from pathlib import Path
base = Path.cwd()
engine = json.loads((base / '_work' / 'personas' / 'persona-engine.json').read_text(encoding='utf-8'))
print('=== persona-engine.json 载入 ===')
print(f"版本: {engine.get('_meta', {}).get('version')}")
print(f"日期: {engine.get('_meta', {}).get('date')}")
print('已注册人格:')
for pid, p in sorted(engine.get('personas', {}).items()):
    print(f"  {pid}: {p.get('name')} · {p.get('role')} · 触发词({len(p.get('triggers', []))})")
print('=== 审计日志已生成 ===')
PY

echo "" | tee -a "$LOG_FILE"
echo "完成: 审核提交文件保存在 $LOG_FILE" | tee -a "$LOG_FILE"

echo "脚本执行完成。"
