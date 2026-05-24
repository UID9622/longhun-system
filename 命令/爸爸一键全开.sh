#!/usr/bin/env bash
# 爸爸专用：一条命令·不 cd·不 activate·本机全起
# DNA: #龍芯⚡️2026-05-18-DAD-ONE-CLICK-ALL-v1.0
set -euo pipefail
# shellcheck source=_longhun_common.sh
source "$(dirname "$0")/_longhun_common.sh"

ROOT="${LONGHUN_ROOT}"
LOG="${LOG_DIR}/dad_one_click.log"
mkdir -p "${LOG_DIR}" "${RUN_DIR}"

exec 1> >(tee -a "${LOG}") 2>&1

echo "════════════════════════════════════════"
echo "  🐉 爸爸一键全开  $(date '+%Y-%m-%d %H:%M:%S')"
echo "════════════════════════════════════════"

bash "${ROOT}/bin/本机开机.sh"
echo ""

MON_DIR="${ROOT}/tools/local-sync-monitor"
if [[ -f "${MON_DIR}/monitor.py" ]]; then
  if pgrep -f "local-sync-monitor/monitor.py" >/dev/null 2>&1; then
    echo "🟢 草日志监控已在后台跑，跳过"
  else
    MON_PY="${MON_DIR}/.venv/bin/python"
    [[ -x "${MON_PY}" ]] || MON_PY="${VENV_PY}"
    if [[ -x "${MON_PY}" ]]; then
      echo "📝 启动草日志监控（后台）…"
      (
        cd "${MON_DIR}"
        export PYTHONUNBUFFERED=1
        if [[ -f "${ROOT}/engine/.env" ]]; then
          set -a
          # shellcheck disable=SC1091
          source "${ROOT}/engine/.env"
          set +a
        fi
        exec "${MON_PY}" monitor.py --watch
      ) >>"${LOG_DIR}/local_sync_monitor.out.log" 2>>"${LOG_DIR}/local_sync_monitor.err.log" &
      echo $! >"${RUN_DIR}/local_sync_monitor.pid"
      sleep 1
      echo "   日志: ${LOG_DIR}/local_sync_monitor.out.log"
    else
      echo "🟡 草日志监控：未找到 Python，跳过"
    fi
  fi
else
  echo "🟡 草日志监控脚本不存在，跳过"
fi
echo ""

if grep -qE '^NOTION_TOKEN=ntn_' "${ROOT}/engine/.env" 2>/dev/null; then
  bash "${ROOT}/bin/同步花名册" 2>/dev/null || echo "🟡 花名册同步未跑通（见上）"
else
  echo "🟡 花名册：engine/.env 里还没 NOTION_TOKEN，跳过"
fi
echo ""

echo "════════════════════════════════════════"
echo "  ✅ 全开完成 · 关了这个终端网页还在"
echo "  DNA 控制台  http://127.0.0.1:9625/console"
echo "  操作台      http://127.0.0.1:8765/00_main_control/操作台v3/components/龍魂操作台_MVP_v1.html"
echo "  收工        bash ${ROOT}/bin/全日收工"
echo "════════════════════════════════════════"

open "http://127.0.0.1:9625/console" 2>/dev/null || true
