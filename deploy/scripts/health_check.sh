# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# 加载鲲鹏环境变量
if [ -f /opt/longhun-system/.env.kunpeng ]; then
    set -a
    source /opt/longhun-system/.env.kunpeng
    set +a
fi

# ╔═══════════════════════════════════════════════════════════════╗
# ║  🐉 龙魂系统 · 鲲鹏健康检查 + Bark 推送                     ║
# ║  🏷️  版本: v1.2 · Bark                                      ║
# ║  🧬  DNA: #龍芯⚡️2026-07-11-HEALTHCHECK-BARK-v1.2           ║
# ║  👤  适用: UID9622 · 诸葛鑫                                  ║
# ╚═══════════════════════════════════════════════════════════════╝

# ────────────────────────────────────────────────────────────────
# 平台检测
# ────────────────────────────────────────────────────────────────
IS_MAC=false
if [[ "$(uname -s)" == "Darwin" ]]; then
    IS_MAC=true
fi

# ────────────────────────────────────────────────────────────────
# 配置区
# ────────────────────────────────────────────────────────────────
if $IS_MAC; then
    BASE_DIR="${HOME}/longhun-system"
    LOG_DIR="${HOME}/Library/Logs/longhun"
    PYTHON="$(which python3)"
else
    BASE_DIR="/opt/longhun-system"
    LOG_DIR="/var/log/longhun"
    PYTHON="/usr/bin/python3"
fi
ALARM_LOG="${LOG_DIR}/alarm.log"
HEALTH_LOG="${LOG_DIR}/health.log"
STATE_DIR="${LOG_DIR}/.alert_state"

# 资源阈值
CPU_THRESHOLD=80
MEM_THRESHOLD=80
DISK_THRESHOLD=85

# ── Bark 配置 ──
# 双模式：BARK_SERVER 设定 → 自建；否则走官方
BARK_KEY="${BARK_KEY:-xxxxxxxxxxxxxxxx}"
BARK_SERVER="${BARK_SERVER:-}"
if [ -n "${BARK_SERVER}" ]; then
    BARK_URL="${BARK_SERVER}/push"  # 自建 POST /push
else
    BARK_URL="https://api.day.app/${BARK_KEY}"  # 官方 API
fi

# ── 飞书 Webhook（可选，保留兼容）──
FEISHU_WEBHOOK="${FEISHU_WEBHOOK_URL:-}"

# 告警去重时间（分钟）
DEDUP_MINUTES=30

# 服务列表（加新服务在这里加）
SERVICES=("longhun-ant-colony" "longhun-api" "longhun-audit" "longhun-calendar" "longhun-core" "longhun-dashboard" "longhun-deepseek-executor" "longhun-gatekeeper" "longhun-local-gateway" "longhun-longzhishou" "longhun-orders" "longhun-portal" "longhun-sovereignty" "longhun-symbiote" "longhun-wechat" "longhun888")
SERVICE_PORTS=(80 443 8080 8081 8443 8444 8446 8777 9622 9623 9627 9677)

# ────────────────────────────────────────────────────────────────
# 初始化
# ────────────────────────────────────────────────────────────────
mkdir -p "${LOG_DIR}" "${STATE_DIR}"
TS="$(date '+%Y-%m-%d %H:%M:%S')"

ALARM_ITEMS=()
ALARM_COUNT=0
ALARM_LEVEL="green"

# ────────────────────────────────────────────────────────────────
# 工具函数
# ────────────────────────────────────────────────────────────────

add_alarm() {
    local level="$1"
    local item="$2"
    ALARM_ITEMS+=("${level}|${item}")
    ALARM_COUNT=$((ALARM_COUNT + 1))
    case "${level}" in
        critical) ALARM_LEVEL="red" ;;
        warn)     [ "${ALARM_LEVEL}" != "red" ] && ALARM_LEVEL="yellow" ;;
        info)     [ "${ALARM_LEVEL}" = "green" ] && ALARM_LEVEL="green" ;;
    esac
    echo "[$(echo ${level} | tr 'a-z' 'A-Z')] ${TS} ${item}" >> "${ALARM_LOG}"
}

is_deduped() {
    local alert_key="$1"
    local hash_cmd="md5sum"
    $IS_MAC && hash_cmd="md5"
    local state_file="${STATE_DIR}/$(echo -n "${alert_key}" | ${hash_cmd} | cut -d' ' -f1)"
    if [ -f "${state_file}" ]; then
        local last_ts=$(cat "${state_file}")
        local now_ts=$(date +%s)
        local elapsed=$(( (now_ts - last_ts) / 60 ))
        [ "${elapsed}" -lt "${DEDUP_MINUTES}" ] && return 0
    fi
    return 1
}

mark_sent() {
    local alert_key="$1"
    local state_file="${STATE_DIR}/$(echo -n "${alert_key}" | md5sum | cut -d' ' -f1)"
    date +%s > "${state_file}"
}

# ── Bark 推送（汇总）──
send_bark() {
    # 检测配置：自建模式需 BARK_SERVER，官方模式需 BARK_KEY
    local has_config=false
    if [ -n "${BARK_SERVER}" ]; then
        has_config=true
    elif [ -n "${BARK_KEY}" ] && [ "${BARK_KEY}" != "xxxxxxxxxxxxxxxx" ]; then
        has_config=true
    fi

    if [ "${has_config}" = false ]; then
        echo "[SKIP] ${TS} Bark 未配置，跳过推送" >> "${HEALTH_LOG}"
        return
    fi

    if [ ${ALARM_COUNT} -eq 0 ]; then
        # 没告警不发，保持安静
        return
    fi

    # 构造摘要标题
    local title="🐉 龙魂系统告警"
    case "${ALARM_LEVEL}" in
        red)    title="🔴 龙魂系统 · ${ALARM_COUNT}条严重告警" ;;
        yellow) title="🟡 龙魂系统 · ${ALARM_COUNT}条警告" ;;
        green)  title="🟢 龙魂系统 · 一切正常" ;;
    esac

    # 构造详情
    local body=""
    for alert in "${ALARM_ITEMS[@]}"; do
        IFS='|' read -r level text <<< "${alert}"
        case "${level}" in
            critical) body="${body}
🔴 ${text}" ;;
            warn)     body="${body}
🟡 ${text}" ;;
            info)     body="${body}
🟢 ${text}" ;;
        esac
    done

    # 追加资源摘要
    local cpu_now=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'.' -f1)
    [ -z "${cpu_now}" ] && cpu_now="N/A"
    local mem_now=$(free -h | grep Mem | awk '{print $3 "/" $2}')
    local disk_now=$(df -h /data 2>/dev/null | tail -1 | awk '{print $3 "/" $2}')
    local uptime_str=$(uptime -p | sed 's/up //')

    body="${body}

📊 CPU: ${cpu_now}% | 内存: ${mem_now}
💾 磁盘: ${disk_now} | 运行: ${uptime_str}"
    body="${body}

${TS} · 鲲鹏 TaiShan 200"

    # 使用 POST JSON 推送（避免 URL 过长）
    local json_payload
    json_payload=$(python3 -c "
import json, sys
title = sys.argv[1]
body = sys.argv[2]
print(json.dumps({'title': title, 'body': body, 'group': '龙魂系统', 'sound': 'alarm', 'autoCopy': True}))
" "${title}" "${body}")

    local http_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${BARK_URL}"         -H "Content-Type: application/json"         -d "${json_payload}" 2>/dev/null)

    if [ "${http_code}" = "200" ]; then
        echo "[BARK] ${TS} 推送成功（${ALARM_COUNT} 条告警）" >> "${HEALTH_LOG}"
    else
        echo "[BARK] ${TS} 推送失败，HTTP ${http_code}" >> "${HEALTH_LOG}"
    fi
}

# ── 飞书推送（保留兼容，Bark 不可用时备用）──
send_feishu() {
    if [ -z "${FEISHU_WEBHOOK}" ]; then
        return
    fi
    if [ ${ALARM_COUNT} -eq 0 ]; then
        return
    fi

    local detail=""
    for alert in "${ALARM_ITEMS[@]}"; do
        IFS='|' read -r level text <<< "${alert}"
        case "${level}" in
            critical) detail="${detail}\\n🔴 **${text}**" ;;
            warn)     detail="${detail}\\n🟡 ${text}" ;;
            info)     detail="${detail}\\n🟢 ${text}" ;;
        esac
    done

    local cpu_now=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'.' -f1)
    [ -z "${cpu_now}" ] && cpu_now="N/A"
    local mem_now=$(free -h | grep Mem | awk '{print $3 "/" $2}')
    local disk_now=$(df -h /data 2>/dev/null | tail -1 | awk '{print $3 "/" $2}')

    local payload=$(cat << EOF
{
    "msg_type": "interactive",
    "card": {
        "header": {
            "title": {"tag": "plain_text", "content": "🐉 龙魂系统 · 健康检查报告"},
            "template": "${ALARM_LEVEL}"
        },
        "elements": [
            {"tag": "div", "fields": [
                {"is_short": true, "text": {"tag": "lark_md", "content": "**📊 检查时间**\\n${TS}"}},
                {"is_short": true, "text": {"tag": "lark_md", "content": "**⚠️ 告警数量**\\n${ALARM_COUNT} 条"}}
            ]},
            {"tag": "hr"},
            {"tag": "div", "fields": [
                {"is_short": true, "text": {"tag": "lark_md", "content": "**CPU**\\n${cpu_now}%"}},
                {"is_short": true, "text": {"tag": "lark_md", "content": "**内存**\\n${mem_now}"}},
                {"is_short": true, "text": {"tag": "lark_md", "content": "**磁盘**\\n${disk_now}"}},
                {"is_short": true, "text": {"tag": "lark_md", "content": "**运行时长**\\n$(uptime -p | sed 's/up //')"}}
            ]},
            {"tag": "hr"},
            {"tag": "markdown", "content": "**📋 告警详情**\\n${detail}"},
            {"tag": "note", "elements": [{"tag": "plain_text", "content": "龙魂系统 · 鲲鹏 TaiShan 200 · ${TS}"}]}
        ]
    }
}
EOF
)
    curl -s -o /dev/null -X POST "${FEISHU_WEBHOOK}" \
        -H "Content-Type: application/json" \
        -d "${payload}" > /dev/null 2>&1
}

# ────────────────────────────────────────────────────────────────
# 1. 服务状态检查
# ────────────────────────────────────────────────────────────────
check_services() {
    echo "[CHECK] ${TS} 开始检查服务状态" >> "${HEALTH_LOG}"

    if $IS_MAC; then
        # Mac: 使用 launchctl 检查 launchd 服务
        for svc in "${SERVICES[@]}"; do
            local label="com.longhun.${svc}"
            if launchctl list "${label}" &>/dev/null; then
                local pid=$(launchctl list "${label}" 2>/dev/null | awk 'NR>1{print $1}')
                if [ -n "${pid}" ] && [ "${pid}" != "-" ] && [ "${pid}" != "0" ]; then
                    echo "  ✅ ${svc} 运行正常 (PID:${pid})" >> "${HEALTH_LOG}"
                else
                    local msg="${svc} 服务未运行"
                    add_alarm "critical" "${msg}"
                fi
            else
                # launchd 服务不存在，跳过（Mac上可能未部署全部服务）
                echo "  ⚠️ ${svc} 未注册为 launchd 服务（跳过）" >> "${HEALTH_LOG}"
            fi
        done
    else
        for svc in "${SERVICES[@]}"; do
            if systemctl is-active --quiet "${svc}"; then
                echo "  ✅ ${svc} 运行正常" >> "${HEALTH_LOG}"
            else
                local msg="${svc} 服务异常，已自动重启"
                add_alarm "critical" "${msg}"
                systemctl restart "${svc}" 2>/dev/null
                sleep 2
                if systemctl is-active --quiet "${svc}"; then
                    add_alarm "warn" "${svc} 重启成功"
                else
                    add_alarm "critical" "${svc} 重启失败，需人工介入"
                fi
            fi
        done
    fi
}

# ────────────────────────────────────────────────────────────────
# 2. 端口检查
# ────────────────────────────────────────────────────────────────
check_ports() {
    if $IS_MAC; then
        for port in "${SERVICE_PORTS[@]}"; do
            if lsof -iTCP:"${port}" -sTCP:LISTEN &>/dev/null; then
                echo "  ✅ 端口 ${port} 正常" >> "${HEALTH_LOG}"
            else
                # Mac上端口监听较少是正常的
                echo "  ⚠️ 端口 ${port} 未监听（Mac本地·正常）" >> "${HEALTH_LOG}"
            fi
        done
    else
        for port in "${SERVICE_PORTS[@]}"; do
            if ss -tlnp | grep -q ":${port} "; then
                echo "  ✅ 端口 ${port} 正常" >> "${HEALTH_LOG}"
            else
                add_alarm "critical" "端口 ${port} 未监听"
            fi
        done
    fi
}

# ────────────────────────────────────────────────────────────────
# 3. 资源检查
# ────────────────────────────────────────────────────────────────
check_resources() {
    echo "" >> "${HEALTH_LOG}"
    echo "  === 资源检查 ===" >> "${HEALTH_LOG}"

    if $IS_MAC; then
        # Mac: 使用 top -l 1 和 vm_stat
        local cpu_raw=$(top -l 1 2>/dev/null | grep "CPU usage" | awk '{print $3}' | cut -d'%' -f1 | tr -d ' ')
        local cpu_usage=$(echo "${cpu_raw}" | cut -d'.' -f1)
        [ -z "${cpu_usage}" ] && cpu_usage=0
        echo "  📊 CPU: ${cpu_usage}%" >> "${HEALTH_LOG}"

        if [ "${cpu_usage}" -gt "${CPU_THRESHOLD}" ]; then
            local key="cpu_${cpu_usage}"
            if ! is_deduped "${key}"; then
                add_alarm "warn" "CPU ${cpu_usage}%（阈值 ${CPU_THRESHOLD}%）"
                mark_sent "${key}"
            fi
        fi

        # Mac 内存：使用 vm_stat
        local page_size=$(vm_stat 2>/dev/null | grep "page size" | awk '{print $8}')
        [ -z "${page_size}" ] && page_size=16384
        local free_pages=$(vm_stat 2>/dev/null | grep "Pages free" | awk '{print $3}' | tr -d '.')
        local used_pages=$(vm_stat 2>/dev/null | grep "Pages active" | awk '{print $3}' | tr -d '.')
        local wired_pages=$(vm_stat 2>/dev/null | grep "Pages wired" | awk '{print $4}' | tr -d '.')
        local compressed_pages=$(vm_stat 2>/dev/null | grep "Pages occupied by compressor" | awk '{print $5}' | tr -d '.')
        [ -z "${free_pages}" ] && free_pages=0
        [ -z "${used_pages}" ] && used_pages=0
        [ -z "${wired_pages}" ] && wired_pages=0
        [ -z "${compressed_pages}" ] && compressed_pages=0
        local total_mem=$(( (free_pages + used_pages + wired_pages + compressed_pages) * page_size / 1024 / 1024 ))
        local used_mem=$(( (used_pages + wired_pages + compressed_pages) * page_size / 1024 / 1024 ))
        local mem_usage=$(( used_mem * 100 / total_mem )) 2>/dev/null
        [ -z "${mem_usage}" ] && mem_usage=0
        echo "  📊 内存: ${used_mem}M/${total_mem}M (${mem_usage}%)" >> "${HEALTH_LOG}"

        if [ "${mem_usage}" -gt "${MEM_THRESHOLD}" ]; then
            local key="mem_${mem_usage}"
            if ! is_deduped "${key}"; then
                add_alarm "warn" "内存 ${mem_usage}%（阈值 ${MEM_THRESHOLD}%）"
                mark_sent "${key}"
            fi
        fi

        # Mac 磁盘
        local disk_usage=$(df -h / 2>/dev/null | tail -1 | awk '{print $5}' | cut -d'%' -f1)
        [ -z "${disk_usage}" ] && disk_usage=0
        local disk_detail=$(df -h / 2>/dev/null | tail -1 | awk '{print $3 "/" $2}')
        echo "  📊 磁盘(/): ${disk_detail} (${disk_usage}%)" >> "${HEALTH_LOG}"

        if [ "${disk_usage}" -gt "${DISK_THRESHOLD}" ]; then
            local key="disk_${disk_usage}"
            if ! is_deduped "${key}"; then
                add_alarm "warn" "磁盘 ${disk_usage}%（阈值 ${DISK_THRESHOLD}%）"
                mark_sent "${key}"
            fi
        fi
    else
        # Linux: 使用 top -bn1 和 free
        local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'.' -f1)
        [ -z "${cpu_usage}" ] && cpu_usage=0
        echo "  📊 CPU: ${cpu_usage}%" >> "${HEALTH_LOG}"

        if [ "${cpu_usage}" -gt "${CPU_THRESHOLD}" ]; then
            local key="cpu_${cpu_usage}"
            if ! is_deduped "${key}"; then
                add_alarm "warn" "CPU ${cpu_usage}%（阈值 ${CPU_THRESHOLD}%）"
                mark_sent "${key}"
            fi
        fi

        local mem_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
        [ -z "${mem_usage}" ] && mem_usage=0
        local mem_detail=$(free -h | grep Mem | awk '{print $3 "/" $2}')
        echo "  📊 内存: ${mem_detail} (${mem_usage}%)" >> "${HEALTH_LOG}"

        if [ "${mem_usage}" -gt "${MEM_THRESHOLD}" ]; then
            local key="mem_${mem_usage}"
            if ! is_deduped "${key}"; then
                add_alarm "warn" "内存 ${mem_usage}%（阈值 ${MEM_THRESHOLD}%）"
                mark_sent "${key}"
            fi
        fi

        local disk_usage=$(df -h /data 2>/dev/null | tail -1 | awk '{print $5}' | cut -d'%' -f1)
        [ -z "${disk_usage}" ] && disk_usage=0
        local disk_detail=$(df -h /data 2>/dev/null | tail -1 | awk '{print $3 "/" $2}')
        echo "  📊 磁盘: ${disk_detail} (${disk_usage}%)" >> "${HEALTH_LOG}"

        if [ "${disk_usage}" -gt "${DISK_THRESHOLD}" ]; then
            local key="disk_${disk_usage}"
            if ! is_deduped "${key}"; then
                add_alarm "warn" "磁盘 ${disk_usage}%（阈值 ${DISK_THRESHOLD}%）"
                mark_sent "${key}"
            fi
        fi
    fi
}

# ────────────────────────────────────────────────────────────────
# 4. 数据盘检查
# ────────────────────────────────────────────────────────────────
check_mount() {
    if $IS_MAC; then
        echo "  ⚠️ 数据盘检查跳过（Mac 本地环境）" >> "${HEALTH_LOG}"
        return
    fi
    if mountpoint -q /data 2>/dev/null; then
        echo "  ✅ 数据盘 /data 挂载正常" >> "${HEALTH_LOG}"
    else
        add_alarm "critical" "数据盘 /data 未挂载，尝试自动挂载"
        mount /dev/sdb /data 2>/dev/null
        sleep 2
        if mountpoint -q /data 2>/dev/null; then
            add_alarm "info" "数据盘自动挂载成功"
        else
            add_alarm "critical" "数据盘挂载失败，需人工介入"
        fi
    fi
}

# ────────────────────────────────────────────────────────────────
# 5. 龙魂引擎自检
# ────────────────────────────────────────────────────────────────
check_longhun_engine() {
    if [ -f "${BASE_DIR}/bin/lh_auto_heal.py" ]; then
        local result
        result=$(${PYTHON} "${BASE_DIR}/bin/lh_auto_heal.py" --quick 2>&1 | tail -3)
        if [ $? -eq 0 ]; then
            echo "  ✅ 自愈引擎扫描通过" >> "${HEALTH_LOG}"
        else
            add_alarm "warn" "自愈引擎扫描异常: ${result}"
        fi
    else
        echo "  ⚠️  自愈引擎未部署，跳过" >> "${HEALTH_LOG}"
    fi
}

# ────────────────────────────────────────────────────────────────
# 6. CNSH & 搜索模块完整性检查
# ────────────────────────────────────────────────────────────────
check_cnsh_search_modules() {
    local modules=(
        "${BASE_DIR}/bin/lh_cnsh_compiler.py"
        "${BASE_DIR}/bin/lh_cnsh_run.sh"
        "${BASE_DIR}/bin/lh_global_search_v2.py"
    )
    for mod in "${modules[@]}"; do
        if [ -f "${mod}" ]; then
            echo "  ✅ ${mod##*/} 存在" >> "${HEALTH_LOG}"
        else
            add_alarm "warn" "模块缺失: ${mod##*/}"
        fi
    done
}

# ────────────────────────────────────────────────────────────────
# 7. SSL证书过期检查（新增 v1.3）
# ────────────────────────────────────────────────────────────────
check_ssl_certs() {
    if $IS_MAC; then
        echo "  ⚠️ SSL证书检查跳过（Mac 本地·证书在鲲鹏）" >> "${HEALTH_LOG}"
        return
    fi
    local cert_dirs=("/etc/letsencrypt/live/uid9622.cn" "/etc/letsencrypt/live/longhun888.com")
    for cert_dir in "${cert_dirs[@]}"; do
        local cert_file="${cert_dir}/cert.pem"
        if [ ! -f "${cert_file}" ]; then
            add_alarm "warn" "SSL证书缺失: ${cert_dir##*/}"
            continue
        fi
        local end_date=$(openssl x509 -enddate -noout -in "${cert_file}" 2>/dev/null | cut -d= -f2)
        local end_sec=$(date -d "${end_date}" +%s 2>/dev/null)
        local now_sec=$(date +%s)
        local days_left=$(( (end_sec - now_sec) / 86400 ))
        local domain="${cert_dir##*/}"
        echo "  📅 SSL ${domain}: ${days_left}天 (${end_date})" >> "${HEALTH_LOG}"
        if [ "${days_left}" -le 7 ]; then
            add_alarm "critical" "SSL ${domain} 仅剩${days_left}天！立即续期"
        elif [ "${days_left}" -le 21 ]; then
            add_alarm "warn" "SSL ${domain} 剩余${days_left}天（建议续期）"
        elif [ "${days_left}" -le 30 ]; then
            add_alarm "info" "SSL ${domain} 剩余${days_left}天（即将进入续期窗口）"
        fi
    done
}

# ────────────────────────────────────────────────────────────────
# 主流程
# ────────────────────────────────────────────────────────────────
main() {
    echo ""
    echo "══════════════════════════════════════════════════"
    echo "  🐉 龙魂系统 · 鲲鹏健康检查"
    echo "  ${TS}"
    echo "══════════════════════════════════════════════════"
    echo ""

    check_services
    check_ports
    check_resources
    check_mount
    check_ssl_certs
    check_longhun_engine
    check_cnsh_search_modules

    echo "[HEALTH] ${TS} 检查完成，告警 ${ALARM_COUNT} 条，级别 ${ALARM_LEVEL}" >> "${HEALTH_LOG}"

    # 推送到 Bark（主力）
    send_bark

    # 飞书备用（如果有配的话）
    send_feishu

    # 控制台输出
    echo ""
    echo "──────────────────────────────────────────────"
    if [ ${ALARM_COUNT} -eq 0 ]; then
        echo "  ✅ 一切正常，无告警"
    else
        echo "  ⚠️  共 ${ALARM_COUNT} 条告警（级别: ${ALARM_LEVEL}）"
        for alert in "${ALARM_ITEMS[@]}"; do
            IFS='|' read -r level text <<< "${alert}"
            echo "    [${level}] ${text}"
        done
    fi
    echo "──────────────────────────────────────────────"
    echo ""
    echo "  Bark: $(if [ -n "${BARK_KEY}" ] && [ "${BARK_KEY}" != "xxxxxxxxxxxxxxxx" ]; then echo '✅ 已配置'; else echo '⚠️ 未配置'; fi)"
    echo "  飞书: $(if [ -n "${FEISHU_WEBHOOK}" ]; then echo '✅ 已配置（备用）'; else echo '⚠️ 未配置'; fi)"
    echo "  去重: ${DEDUP_MINUTES} 分钟"
    echo "  健康日志: ${HEALTH_LOG}"
    echo ""
}

main "$@"
