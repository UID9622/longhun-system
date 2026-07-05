#!/usr/bin/env bash
# 🐉 龍魂数学公式套件 · 定时审计脚本
#
# 用途：
#   由 cron / CI / git hook 调用，运行统一运行器并写入审计日志。
#   失败时返回非 0 退出码，便于外部告警。
#
# 审计日志：
#   longhun-system/audit/math_suite_cron.jsonl
#
# 用法：
#   bash scripts/run_math_suite_cron.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PYTHON="${PYTHON:-python3}"
RUNNER="${PROJECT_ROOT}/scripts/run_math_suite.py"
AUDIT_DIR="${PROJECT_ROOT}/audit"
AUDIT_LOG="${AUDIT_DIR}/math_suite_cron.jsonl"

mkdir -p "${AUDIT_DIR}"

cd "${PROJECT_ROOT}"

TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
RUN_ID="$(date +%s%N)"
TMP_OUT="$(mktemp)"
TMP_ERR="$(mktemp)"

cleanup() {
    rm -f "${TMP_OUT}" "${TMP_ERR}"
}
trap cleanup EXIT

# 运行统一运行器
set +e
"${PYTHON}" "${RUNNER}" >"${TMP_OUT}" 2>"${TMP_ERR}"
EXIT_CODE=$?
set -e

STDOUT_TAIL=$(tail -n 20 "${TMP_OUT}" | sed 's/"/\\"/g' | tr '\n' ' ')
STDERR_TAIL=$(tail -n 10 "${TMP_ERR}" | sed 's/"/\\"/g' | tr '\n' ' ')

# 从 stdout（CNSH JSON）解析关键字段
PARSED=$(TMP_OUT="${TMP_OUT}" "${PYTHON}" - <<'PY'
import os, re
text = open(os.environ['TMP_OUT']).read()
passed = re.search(r'"passed":\s*(\d+)', text)
total = re.search(r'"total":\s*(\d+)', text)
dna = re.search(r'"dna":\s*"([^"]+)"', text)
th = re.search(r'"trace_hash":\s*"([a-f0-9]+)"', text)
print(
    passed.group(1) if passed else "0",
    total.group(1) if total else "0",
    dna.group(1) if dna else "",
    th.group(1) if th else "",
    sep="|"
)
PY
)
IFS='|' read -r PASSED TOTAL DNA TRACE_HASH <<< "${PARSED}"

# 写入审计日志（JSON Lines）
cat >> "${AUDIT_LOG}" <<EOF
{"ts":"${TS}","run_id":"${RUN_ID}","exit_code":${EXIT_CODE},"passed":${PASSED:-0},"total":${TOTAL:-0},"dna":"${DNA}","trace_hash":"${TRACE_HASH}","summary":"${STDOUT_TAIL}","stderr":"${STDERR_TAIL}"}
EOF

# 简单日志轮转：超过 5000 行时截断保留最近 1000 行
if [[ -f "${AUDIT_LOG}" ]] && [[ $(wc -l <"${AUDIT_LOG}") -gt 5000 ]]; then
    tail -n 1000 "${AUDIT_LOG}" > "${AUDIT_LOG}.tmp"
    mv "${AUDIT_LOG}.tmp" "${AUDIT_LOG}"
fi

# 把本次运行输出也打印出来，方便 cron 邮件 / 日志收集
cat "${TMP_OUT}"

if [[ ${EXIT_CODE} -ne 0 ]]; then
    echo ""
    echo "🔴 龍魂数学公式套件定时审计失败，详见：${AUDIT_LOG}"
    exit ${EXIT_CODE}
fi

echo ""
echo "🟢 龍魂数学公式套件定时审计成功，已归档：${AUDIT_LOG}"

# 刷新编辑器算法公式卡片
UPDATE_SCRIPT="${PROJECT_ROOT}/scripts/update_editor_algorithm_card.py"
if [[ -f "${UPDATE_SCRIPT}" ]]; then
    echo ""
    echo "🔄 刷新编辑器算法公式卡片..."
    "${PYTHON}" "${UPDATE_SCRIPT}"
fi

# 同步 Obsidian 第二大脑（默认本地 TF-IDF+SVD，无需网络）
SECOND_BRAIN_SCRIPT="${PROJECT_ROOT}/scripts/sync_second_brain.py"
VENV_PYTHON="${PROJECT_ROOT}/.venv_longhun_math/bin/python"
if [[ -f "${SECOND_BRAIN_SCRIPT}" ]] && [[ -x "${VENV_PYTHON}" ]]; then
    echo ""
    echo "🧠 同步 Obsidian 第二大脑..."
    "${VENV_PYTHON}" "${SECOND_BRAIN_SCRIPT}"
fi
