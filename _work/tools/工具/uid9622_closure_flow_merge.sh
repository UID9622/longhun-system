#!/usr/bin/env bash
set -euo pipefail

# 收口：主权容器 + 95/5 + CNSH文明论 v2.0 融入 flow_port
ACTION_TAG="${1:-FLOW-MERGE-95-5-CNSH-v2}"
ACTION_DESC="${2:-融合主权容器·95/5·文明论文·单口流场}"

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$HOME/Desktop/UID9622_DAILY_EXEC_LOGS"
DATE_STR="$(date +%Y-%m-%d)"
TS_ISO="$(date +%Y-%m-%dT%H:%M:%S%z)"
LOG_PATH="$LOG_DIR/${DATE_STR}_closure_flow_merge.md"

DNA="#龍芯⚡️2026-05-15-SOVEREIGN-95-5-CNSH-FLOW-MERGE-v1.0"
CONFIRM="#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL="#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

cd "$ROOT_DIR"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "[ERROR] 不是 git 仓库"
  exit 1
fi

STAGE_PATHS=(
  "01_protocols/cnsh/PROTOCOL__SOVEREIGN-CONTAINER-v1.0.md"
  "01_protocols/cnsh/PROTOCOL__95-5-ROOT-RATIO-v2.0.md"
  "01_protocols/cnsh/PROTOCOL__CNSH-PROTOCOL-LAYER-CIVILIZATION-v2.0.md"
  "01_protocols/IPA-ROUTE-REGISTRY.local.md"
  "cnsh/sovereign"
  "cnsh/flow_field"
  "cnsh/root_ratio"
  "cnsh/flow_decision/dna_tag_policy.py"
  "cnsh/flow_decision/cnsh_flow_decision_core.py"
  "engines/cnsh_gateway.py"
  "tools/uid9622_closure_flow_merge.sh"
)

# 仅扫描本次收口路径（排除 .env.example / env.template 误杀）
DANGEROUS_REGEX='(^|/)\.env$|/\.env\.|credentials\.json|id_rsa|private[_-]?key|/secrets?/'
for p in "${STAGE_PATHS[@]}"; do
  if [[ -f "$p" ]] && echo "$p" | grep -E "$DANGEROUS_REGEX" >/dev/null 2>&1; then
    echo "[BLOCKED] 危险文件: $p"
    exit 1
  fi
done

for f in \
  ".cursorrules" \
  "01_protocols/cnsh/PROTOCOL__SOVEREIGN-CONTAINER-v1.0.md" \
  "01_protocols/cnsh/PROTOCOL__95-5-ROOT-RATIO-v2.0.md" \
  "01_protocols/cnsh/PROTOCOL__CNSH-PROTOCOL-LAYER-CIVILIZATION-v2.0.md" \
  "01_protocols/IPA-ROUTE-REGISTRY.local.md" \
  "cnsh/sovereign/container_policy.py" \
  "cnsh/sovereign/__init__.py" \
  "cnsh/sovereign/tests/test_container_policy.py" \
  "cnsh/flow_field/port.py" \
  "cnsh/flow_field/__init__.py" \
  "cnsh/flow_field/tests/test_flow_port.py" \
  "cnsh/root_ratio/engine.py" \
  "cnsh/root_ratio/__init__.py" \
  "cnsh/root_ratio/tests/test_root_ratio.py" \
  "cnsh/flow_decision/dna_tag_policy.py" \
  "cnsh/flow_decision/cnsh_flow_decision_core.py" \
  "engines/cnsh_gateway.py" \
  "tools/uid9622_closure_flow_merge.sh"
do
  [[ -f "$ROOT_DIR/$f" ]] || { echo "[ERROR] 缺少 $f"; exit 1; }
done

echo "[INFO] 运行单元测试..."
python3 -m unittest discover -s cnsh/sovereign/tests -p 'test_*.py' -q
python3 -m unittest discover -s cnsh/root_ratio/tests -p 'test_*.py' -q
python3 -m unittest discover -s cnsh/flow_field/tests -p 'test_*.py' -q
python3 -m unittest discover -s cnsh/flow_decision/tests -p 'test_*.py' -q

git add "${STAGE_PATHS[@]}"

if git diff --cached --quiet; then
  COMMIT_HASH="$(git rev-parse --short HEAD)"
  COMMIT_MSG="[NOOP] 无新增变更"
else
  COMMIT_MSG="收口: ${ACTION_TAG} | DNA=${DNA} | CONFIRM=${CONFIRM} | SEAL=${SEAL} | STOP_ON_SUCCESS"
  git commit -m "$COMMIT_MSG"
  COMMIT_HASH="$(git rev-parse --short HEAD)"
fi

mkdir -p "$LOG_DIR"
cat > "$LOG_PATH" <<EOF
# UID9622 流场融合收口日志

- ts: ${TS_ISO}
- action_tag: ${ACTION_TAG}
- action_desc: ${ACTION_DESC}
- commit_hash: ${COMMIT_HASH}
- commit_message: ${COMMIT_MSG}
- dna: ${DNA}
- confirm: ${CONFIRM}
- seal: ${SEAL}
- protocols:
  - SOVEREIGN-CONTAINER-v1.0
  - 95-5-ROOT-RATIO-v2.0
  - CNSH-CIVILIZATION-v2.0
- engine: cnsh/flow_field/port.py + cnsh/root_ratio/
- stop_on_success: true
EOF

printf '%s\n' "SUCCESS_RECEIPT"
printf '%s\n' "commit_hash=${COMMIT_HASH}"
printf '%s\n' "log_path=${LOG_PATH}"
printf '%s\n' "dna=${DNA}"
printf '%s\n' "confirm=${CONFIRM}"
printf '%s\n' "seal=${SEAL}"
printf '%s\n' "STOP_ON_SUCCESS"
