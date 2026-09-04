#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════╗
# ║  🐉 龍魂·每日早报 v1.0 — 每天8:00推送                         ║
# ║  Daily Report · 服务器状态 · 服务概览 · 资源使用               ║
# ╠═══════════════════════════════════════════════════════════════╣
# ║  DNA: #龍芯⚡️丙午·乙未·丁亥·丙午·䷚颐-BARK-DAILY-REPORT-v1.0               ║
# ║  运行: crontab -e 添加 0 8 * * * /opt/longhun-system/executors/bark/daily_report.sh ║
# ╚═══════════════════════════════════════════════════════════════╝

set -euo pipefail

BASE_DIR="/opt/longhun-system"
BARK_SENDER="${BASE_DIR}/executors/bark/bark_send.py"
LOG_DIR="/var/log/longhun"
mkdir -p "${LOG_DIR}"

TS=$(date '+%Y-%m-%d %H:%M:%S')
DATE_CN=$(date '+%Y年%m月%d日')

# ── 系统信息 ──
HOSTNAME=$(hostname)
UPTIME=$(uptime -p | sed 's/up //')
OS_INFO=$(cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d'"' -f2 || echo "Linux")

# ── CPU ──
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'.' -f1)
if [ -z "${CPU_USAGE}" ]; then
    CPU_USAGE="N/A"
fi
CPU_MODEL=$(grep "model name" /proc/cpuinfo 2>/dev/null | head -1 | cut -d':' -f2 | xargs || echo "Kunpeng 920")
CPU_CORES=$(nproc)

# ── 内存 ──
MEM_TOTAL=$(free -h | grep Mem | awk '{print $2}')
MEM_USED=$(free -h | grep Mem | awk '{print $3}')
MEM_PERCENT=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')

# ── 磁盘 ──
DISK_ROOT=$(df -h / | tail -1 | awk '{print $3 "/" $2 " (" $5 ")"}')
DISK_DATA="未挂载"
if mountpoint -q /data 2>/dev/null; then
    DISK_DATA=$(df -h /data | tail -1 | awk '{print $3 "/" $2 " (" $5 ")"}')
fi

# ── 服务状态 ──
SERVICES=("longhun-api" "longhun-audit" "longhun-calendar" "longhun-core"
          "longhun-dashboard" "longhun-deepseek-executor" "longhun-gatekeeper"
          "longhun-local-gateway" "longhun-longzhishou" "longhun-orders"
          "longhun-portal" "longhun-sovereignty" "longhun-symbiote"
          "longhun-wechat" "longhun888")

RUNNING_COUNT=0
FAILED_SERVICES=""
for svc in "${SERVICES[@]}"; do
    if systemctl is-active --quiet "${svc}" 2>/dev/null; then
        RUNNING_COUNT=$((RUNNING_COUNT + 1))
    else
        FAILED_SERVICES="${FAILED_SERVICES}\n  ❌ ${svc}"
    fi
done

# ── 端口监听 ──
CRITICAL_PORTS=(80 443 8080 8081 8443 8777 9627)
PORT_STATUS=""
for port in "${CRITICAL_PORTS[@]}"; do
    if ss -tlnp | grep -q ":${port} "; then
        PORT_STATUS="${PORT_STATUS}\n  ✅ :${port}"
    else
        PORT_STATUS="${PORT_STATUS}\n  ❌ :${port}"
    fi
done

# ── 进程TOP ──
TOP_PROCESSES=$(ps aux --sort=-%cpu | head -6 | tail -5 | awk '{printf "  %s  CPU:%.1f%%  MEM:%.1f%%\n", $11, $3, $4}')

# ── 网络 ──
NET_IP=$(ip addr show | grep "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}')

# ── 构造推送内容 ──
BODY="📅 ${DATE_CN} 早报

━━━━ 🖥 系统概要 ━━━━
主机: ${HOSTNAME}
系统: ${OS_INFO}
IP: ${NET_IP}
运行: ${UPTIME}
CPU: ${CPU_MODEL}
核心: ${CPU_CORES}核

━━━━ 📊 资源使用 ━━━━
CPU: ${CPU_USAGE}%
内存: ${MEM_USED}/${MEM_TOTAL} (${MEM_PERCENT}%)
系统盘: ${DISK_ROOT}
数据盘: ${DISK_DATA}

━━━━ 🔧 服务状态 ━━━━
运行中: ${RUNNING_COUNT}/${#SERVICES[@]}"
if [ -n "${FAILED_SERVICES}" ]; then
    BODY="${BODY}
异常:${FAILED_SERVICES}"
else
    BODY="${BODY}
✅ 全部服务正常"
fi

BODY="${BODY}

━━━━ 🌐 关键端口 ━━━━${PORT_STATUS}

━━━━ 📈 进程TOP5 ━━━━
${TOP_PROCESSES}

━━━━━━━━━━━━━━━━━━
${TS} · 鲲鹏 · 龍魂系统
UID9622 · 诸葛鑫"

# ── 发送 ──
TITLE="🐉 龍魂早报 · ${DATE_CN}"

echo "${BODY}" | python3 "${BARK_SENDER}" "${TITLE}" --stdin --group "龍魂日报" 2>&1 | tee -a "${LOG_DIR}/daily_report.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 早报已推送 · 服务 ${RUNNING_COUNT}/${#SERVICES[@]} · CPU ${CPU_USAGE}%" >> "${LOG_DIR}/daily_report.log"
