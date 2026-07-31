# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════╗
# ║  🐉 龙魂·Bark 推送插件 v2.0 — 自建服务器版                    ║
# ║  Longhun Bark Plugin · Self-Hosted Bark Server               ║
# ╠═══════════════════════════════════════════════════════════════╣
# ║  DNA: #龍芯⚡️丙午·辛未·BARK-PLUGIN-SELF-HOSTED-v2.0         ║
# ║  作者: UID9622 · 诸葛鑫                                       ║
# ║  目标: 华为云自建 Bark 服务器 + 鲲鹏本地终端                     ║
# ║  依赖: curl, jq (可选)                                        ║
# ╠═══════════════════════════════════════════════════════════════╣
# ║  加载: source ~/.longhun/longhun_bark_plugin.sh              ║
# ║  环境: BARK_SERVER=http://华为云IP:8080                       ║
# ║        BARK_KEY=你的iOS设备Key                                 ║
# ╠═══════════════════════════════════════════════════════════════╣
# ║  铁律: 不自建不推送 · 不审计不存储 · 仅通道 · DNA嵌入            ║
# ╚═══════════════════════════════════════════════════════════════╝

set -euo pipefail

# ═══════════════════════════════════════════════════════════════
# 配置区
# ═══════════════════════════════════════════════════════════════

# 日志目录
BARK_LOG_DIR="${HOME}/.longhun/bark"
BARK_LOG_FILE="${BARK_LOG_DIR}/bark_$(date +%Y%m%d).log"
BARK_ERR_LOG="${BARK_LOG_DIR}/bark_error_$(date +%Y%m%d).log"

# 重试配置
BARK_MAX_RETRIES=3
BARK_RETRY_DELAY=2

# 分组定义
declare -A BARK_GROUPS=(
    ["运维"]="龙魂运维"
    ["告警"]="龙魂告警"
    ["财务"]="龙魂财务"
    ["开发"]="龙魂开发"
    ["紧急"]="龙魂紧急"
)

# 级别颜色映射 (Bark 暂不支持颜色，保留用于日志标注)
declare -A BARK_LEVELS=(
    ["info"]="🟢"
    ["warn"]="🟡"
    ["error"]="🔴"
    ["critical"]="🔴"
)

# ═══════════════════════════════════════════════════════════════
# 内部函数
# ═══════════════════════════════════════════════════════════════

_bark_log() {
    local level="$1"; shift
    mkdir -p "${BARK_LOG_DIR}"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [${level}] $*" >> "${BARK_LOG_FILE}"
}

_bark_err_log() {
    mkdir -p "${BARK_LOG_DIR}"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $*" >> "${BARK_ERR_LOG}"
}

# 检测服务器连通性
_bark_ping() {
    if [ -z "${BARK_SERVER:-}" ]; then
        return 1
    fi
    local ping_url="${BARK_SERVER}/ping"
    curl -s --connect-timeout 5 --max-time 10 "${ping_url}" > /dev/null 2>&1 && return 0 || return 1
}

# 获取 Bark 推送 URL
_bark_get_url() {
    # 自建服务器 POST API: POST /push
    # 官方服务器 GET API: https://api.day.app/{key}/{title}/{body}
    if [ -n "${BARK_SERVER:-}" ]; then
        echo "${BARK_SERVER}/push"
    else
        echo "https://api.day.app/${BARK_KEY:-}"
    fi
}

# 核心推送函数
_bark_push() {
    local title="$1"
    local body="$2"
    local group="${3:-龙魂系统}"
    local level="${4:-info}"
    local sound="${5:-alarm}"

    # 截断过长内容
    if [ ${#body} -gt 4000 ]; then
        body="${body:0:3900}\n\n... (截断)"
    fi

    local bark_url
    bark_url=$(_bark_get_url)
    local icon="${BARK_LEVELS[${level}]:-🟢}"

    # 推送方式选择：自建 POST JSON vs 官方 GET URL
    if [ -n "${BARK_SERVER:-}" ]; then
        # 自建服务器：POST JSON
        _bark_push_self_hosted "${title}" "${body}" "${group}" "${level}" "${sound}" "${icon}"
    else
        # 官方服务器：GET URL
        _bark_push_official "${title}" "${body}" "${group}" "${level}" "${sound}" "${icon}"
    fi
}

_bark_push_self_hosted() {
    local title="$1"
    local body="$2"
    local group="$3"
    local level="$4"
    local sound="$5"
    local icon="$6"

    local payload
    payload=$(python3 -c "
import json, sys
payload = {
    'title': sys.argv[1],
    'body': sys.argv[2],
    'group': sys.argv[3],
    'level': sys.argv[4],
    'sound': sys.argv[5],
    'icon': sys.argv[6],
    'autoCopy': True,
    'badge': 1
}
print(json.dumps(payload, ensure_ascii=False))
" "${icon} ${title}" "${body}" "${group}" "${level}" "${sound}" "${icon}")

    local http_code
    http_code=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST "${BARK_SERVER}/push" \
        -H "Content-Type: application/json; charset=utf-8" \
        -d "${payload}" \
        --connect-timeout 10 --max-time 15 2>/dev/null)

    if [ "${http_code}" = "200" ]; then
        return 0
    else
        _bark_err_log "自建Bark推送失败 HTTP_${http_code}"
        return 1
    fi
}

_bark_push_official() {
    local title="$1"
    local body="$2"
    local group="$3"
    local level="$4"
    local sound="$5"
    local icon="$6"

    # 官方 API: POST JSON 到 https://api.day.app/{key}
    local payload
    payload=$(python3 -c "
import json, sys
payload = {
    'title': sys.argv[1],
    'body': sys.argv[2],
    'group': sys.argv[3],
    'sound': sys.argv[4],
    'autoCopy': True
}
print(json.dumps(payload, ensure_ascii=False))
" "${icon} ${title}" "${body}" "${group}" "${sound}")

    local http_code
    http_code=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST "https://api.day.app/${BARK_KEY:-}" \
        -H "Content-Type: application/json; charset=utf-8" \
        -d "${payload}" \
        --connect-timeout 10 --max-time 15 2>/dev/null)

    if [ "${http_code}" = "200" ]; then
        return 0
    else
        _bark_err_log "官方Bark推送失败 HTTP_${http_code}"
        return 1
    fi
}

# 带重试的推送
_bark_push_with_retry() {
    local title="$1"
    local body="$2"
    local group="${3:-龙魂系统}"
    local level="${4:-info}"
    local sound="${5:-alarm}"

    local attempt=0
    while [ $attempt -lt ${BARK_MAX_RETRIES} ]; do
        if _bark_push "${title}" "${body}" "${group}" "${level}" "${sound}"; then
            _bark_log "SUCCESS" "推送成功 title=\"${title}\" group=\"${group}\" attempt=$((attempt+1))"
            return 0
        fi
        attempt=$((attempt + 1))
        _bark_log "RETRY" "推送重试 title=\"${title}\" attempt=${attempt}/${BARK_MAX_RETRIES}"
        sleep ${BARK_RETRY_DELAY}
    done

    _bark_log "FAILED" "推送最终失败 title=\"${title}\" group=\"${group}\" attempts=${BARK_MAX_RETRIES}"
    return 1
}

# ═══════════════════════════════════════════════════════════════
# 公开 API
# ═══════════════════════════════════════════════════════════════

# 初始化检测
init_bark() {
    echo "╔══════════════════════════════════════════════════╗"
    echo "║  🐉 龙魂 Bark 插件 · 初始化检测                   ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo ""
    echo "📋 环境检测:"

    # 检查 BARK_SERVER
    if [ -n "${BARK_SERVER:-}" ]; then
        echo "  ✅ BARK_SERVER: ${BARK_SERVER}"
        SERVER_MODE="自建"
    else
        echo "  ⚠️  BARK_SERVER: 未配置 (将使用官方 api.day.app)"
        SERVER_MODE="官方"
    fi

    # 检查 BARK_KEY
    if [ -n "${BARK_KEY:-}" ]; then
        echo "  ✅ BARK_KEY: ${BARK_KEY:0:8}****"
    else
        echo "  ❌ BARK_KEY: 未配置 — 无法推送！"
        echo ""
        echo "  请设置环境变量:"
        echo "    export BARK_SERVER=\"http://你的华为云IP:8080\""
        echo "    export BARK_KEY=\"你的iOS设备Key\""
        return 1
    fi

    # 检查依赖
    echo ""
    echo "🔧 依赖检测:"
    if command -v curl &> /dev/null; then
        echo "  ✅ curl: $(curl --version | head -1 | awk '{print $1, $2}')"
    else
        echo "  ❌ curl: 未安装"
        return 1
    fi

    if command -v python3 &> /dev/null; then
        echo "  ✅ python3: $(python3 --version)"
    else
        echo "  ⚠️  python3: 未安装 (非必须)"
    fi

    # 连通性检测
    echo ""
    echo "📡 连通性检测 (${SERVER_MODE}模式):"
    if [ "${SERVER_MODE}" = "自建" ]; then
        if _bark_ping; then
            echo "  ✅ 自建 Bark 服务器连通"
        else
            echo "  ❌ 自建 Bark 服务器无法连通: ${BARK_SERVER}"
            return 1
        fi
    else
        if curl -s --connect-timeout 5 "https://api.day.app/ping" > /dev/null 2>&1; then
            echo "  ✅ 官方 Bark API 连通"
        else
            echo "  ⚠️  官方 Bark API 可能不可达 (网络问题)"
        fi
    fi

    # 日志目录
    echo ""
    echo "📁 日志目录:"
    echo "  📋 主日志: ${BARK_LOG_FILE}"
    echo "  📋 错误日志: ${BARK_ERR_LOG}"
    mkdir -p "${BARK_LOG_DIR}"
    echo "  ✅ 日志目录已就绪"

    echo ""
    echo "══════════════════════════════════════════════════"
    echo "  🐉 龙魂 Bark 插件 v2.0 · 初始化完成"
    echo "  DNA: #龍芯⚡️丙午·辛未·BARK-SELF-HOSTED-v2.0"
    echo "  $(date '+%Y-%m-%d %H:%M:%S')"
    echo "══════════════════════════════════════════════════"

    return 0
}

# 运维通知 (info 级别)
bark_ops() {
    local title="${1:-运维通知}"
    local body="${2:-}"
    local group="${3:-运维}"
    local resolved_group="${BARK_GROUPS[${group}]:-龙魂系统}"

    if [ -z "${body}" ]; then
        echo "用法: bark_ops \"标题\" \"内容\" [分组]" >&2
        return 1
    fi

    _bark_push_with_retry "${title}" "${body}" "${resolved_group}" "info" "alarm"
}

# 告警通知 (warn 级别)
bark_alert() {
    local title="${1:-告警通知}"
    local body="${2:-}"
    local group="${3:-告警}"
    local resolved_group="${BARK_GROUPS[${group}]:-龙魂系统}"

    if [ -z "${body}" ]; then
        echo "用法: bark_alert \"标题\" \"内容\" [分组]" >&2
        return 1
    fi

    _bark_push_with_retry "${title}" "${body}" "${resolved_group}" "warn" "alarm"
}

# 紧急通知 (critical 级别)
bark_critical() {
    local title="${1:-紧急通知}"
    local body="${2:-}"
    local group="${3:-紧急}"
    local resolved_group="${BARK_GROUPS[${group}]:-龙魂系统}"

    if [ -z "${body}" ]; then
        echo "用法: bark_critical \"标题\" \"内容\" [分组]" >&2
        return 1
    fi

    _bark_push_with_retry "${title}" "${body}" "${resolved_group}" "critical" "alarm"
}

# 自定义推送
bark_custom() {
    local title="${1:-通知}"
    local body="${2:-}"
    local group="${3:-龙魂系统}"
    local level="${4:-info}"
    local sound="${5:-alarm}"

    if [ -z "${body}" ]; then
        echo "用法: bark_custom \"标题\" \"内容\" [分组] [级别] [声音]" >&2
        echo "级别: info | warn | error | critical" >&2
        return 1
    fi

    _bark_push_with_retry "${title}" "${body}" "${group}" "${level}" "${sound}"
}

# 状态诊断
bark_status() {
    echo "╔══════════════════════════════════════════════════╗"
    echo "║  🐉 龙魂 Bark 插件 · 状态诊断                     ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo ""

    # 环境变量
    echo "📋 配置:"
    if [ -n "${BARK_SERVER:-}" ]; then
        echo "  模式:    自建服务器"
        echo "  Server:  ${BARK_SERVER}"
    else
        echo "  模式:    官方 API (api.day.app)"
    fi
    echo "  Key:     ${BARK_KEY:0:8}****"

    # 连通性
    echo ""
    echo "📡 连通性:"
    if [ -n "${BARK_SERVER:-}" ]; then
        if _bark_ping; then
            echo "  ✅ 服务器连通 (${BARK_SERVER})"
        else
            echo "  ❌ 服务器不通 (${BARK_SERVER})"
        fi
    else
        if curl -s --connect-timeout 5 "https://api.day.app/ping" > /dev/null 2>&1; then
            echo "  ✅ 官方 API 连通"
        else
            echo "  ❌ 官方 API 不可达"
        fi
    fi

    # 今日统计
    echo ""
    echo "📊 今日推送统计:"
    if [ -f "${BARK_LOG_FILE}" ]; then
        local total
        total=$(wc -l < "${BARK_LOG_FILE}" 2>/dev/null || echo 0)
        local success_count
        success_count=$(grep -c "SUCCESS" "${BARK_LOG_FILE}" 2>/dev/null || echo 0)
        local fail_count
        fail_count=$(grep -c "FAILED" "${BARK_LOG_FILE}" 2>/dev/null || echo 0)
        echo "  总次数:  ${total}"
        echo "  成功:    ${success_count}"
        echo "  失败:    ${fail_count}"
        echo "  成功率:  $(if [ "${total}" -gt 0 ]; then echo "scale=1; ${success_count}*100/${total}" | bc 2>/dev/null || python3 -c "print(f'{${success_count}*100/${total}:.1f}%')"; else echo "N/A"; fi)"
    else
        echo "  今日暂无推送记录"
    fi

    # 日志信息
    echo ""
    echo "📁 日志:"
    echo "  主日志:   ${BARK_LOG_FILE}"
    echo "  错误日志: ${BARK_ERR_LOG}"
    echo "  归档目录: ${BARK_LOG_DIR}/"

    echo ""
    echo "══════════════════════════════════════════════════"
}

# 查看日志
bark_logs() {
    local lines="${1:-20}"

    echo "📋 Bark 日志 (最近 ${lines} 条):"
    echo "══════════════════════════════════════════════════"

    if [ -f "${BARK_LOG_FILE}" ]; then
        tail -n "${lines}" "${BARK_LOG_FILE}"
    else
        echo "  暂无日志"
    fi

    # 错误日志
    echo ""
    echo "⚠️  最近错误:"
    if [ -f "${BARK_ERR_LOG}" ] && [ -s "${BARK_ERR_LOG}" ]; then
        tail -n 5 "${BARK_ERR_LOG}"
    else
        echo "  ✅ 无错误记录"
    fi
}

# 批量推送
bark_batch() {
    local batch_file="${1:-}"
    if [ -z "${batch_file}" ] || [ ! -f "${batch_file}" ]; then
        echo "用法: bark_batch batch.txt" >&2
        echo "" >&2
        echo "batch.txt 格式 (每行一条，|分隔):" >&2
        echo "  标题|内容|分组|级别" >&2
        echo "" >&2
        echo "级别: info | warn | error | critical" >&2
        echo "分组: 运维 | 告警 | 财务 | 开发 | 紧急" >&2
        return 1
    fi

    echo "📋 批量推送开始..."
    local total=0 success=0 fail=0

    while IFS='|' read -r title body group level; do
        # 跳过空行和注释
        [ -z "${title}" ] && continue
        [[ "${title}" =~ ^# ]] && continue

        total=$((total + 1))
        echo -n "  [${total}] ${title:0:40}..."

        if _bark_push_with_retry "${title}" "${body}" "${group:-龙魂系统}" "${level:-info}"; then
            echo " ✅"
            success=$((success + 1))
        else
            echo " ❌"
            fail=$((fail + 1))
        fi

        # 避免过快
        sleep 0.5
    done < "${batch_file}"

    echo ""
    echo "══════════════════════════════════════════════════"
    echo "  批量推送完成: 总计 ${total} | 成功 ${success} | 失败 ${fail}"
    echo "══════════════════════════════════════════════════"
}

# 测试推送
bark_test() {
    echo "🧪 发送测试推送..."

    if [ -n "${BARK_SERVER:-}" ]; then
        echo "  目标: ${BARK_SERVER} (自建)"
    else
        echo "  目标: api.day.app (官方)"
    fi

    if _bark_push_with_retry "🐉 龙魂测试" "Bark 插件 v2.0 已就绪 · $(date '+%Y-%m-%d %H:%M:%S') · 鲲鹏" "龙魂系统" "info"; then
        echo "✅ 测试推送成功！请查看你的 iPhone Bark App"
    else
        echo "❌ 测试推送失败，请检查配置"
    fi
}

# ═══════════════════════════════════════════════════════════════
# 加载时执行
# ═══════════════════════════════════════════════════════════════

# 静默初始化日志目录
mkdir -p "${BARK_LOG_DIR}"

# 如果 BARK_SERVER 和 BARK_KEY 都设置好了，静默验证
if [ -n "${BARK_SERVER:-}" ] && [ -n "${BARK_KEY:-}" ]; then
    _bark_log "LOADED" "插件已加载 server=${BARK_SERVER} key=${BARK_KEY:0:8}****"
fi

# ═══════════════════════════════════════════════════════════════
# 帮助
# ═══════════════════════════════════════════════════════════════

bark_help() {
    cat << 'HELP'
╔═══════════════════════════════════════════════════════════════╗
║  🐉 龙魂 Bark 推送插件 v2.0 · 使用帮助                        ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  📋 环境变量:                                                 ║
║    export BARK_SERVER="http://华为云IP:8080"  # 自建服务器     ║
║    export BARK_KEY="你的iOS设备Key"            # iOS设备Key    ║
║                                                               ║
║  🚀 快速开始:                                                 ║
║    source ~/.longhun/longhun_bark_plugin.sh   # 加载插件       ║
║    init_bark                                 # 初始化检测       ║
║    bark_test                                 # 测试推送         ║
║                                                               ║
║  📢 推送命令:                                                 ║
║    bark_ops "标题" "内容" [分组]              # 运维通知(info)  ║
║    bark_alert "标题" "内容" [分组]            # 告警(warn)      ║
║    bark_critical "标题" "内容" [分组]         # 紧急(critical)  ║
║    bark_custom "标题" "内容" [分组] [级别]    # 自定义          ║
║                                                               ║
║  🎯 分组: 运维 | 告警 | 财务 | 开发 | 紧急                    ║
║  🎨 级别: info | warn | error | critical                      ║
║                                                               ║
║  🛠️  工具命令:                                                ║
║    bark_status                               # 状态诊断         ║
║    bark_logs [行数]                          # 查看日志         ║
║    bark_batch batch.txt                      # 批量推送         ║
║    bark_test                                 # 测试推送         ║
║    bark_help                                 # 显示帮助         ║
║                                                               ║
║  📁 日志: ~/.longhun/bark/                                    ║
║  🔄 自动重试: 3次, 间隔2秒                                    ║
║                                                               ║
║  DNA: #龍芯⚡️丙午·辛未·BARK-PLUGIN-SELF-HOSTED-v2.0          ║
║  UID9622 · 诸葛鑫 · 龙魂系统                                  ║
╚═══════════════════════════════════════════════════════════════╝
HELP
}

# 导出所有公开函数
export -f init_bark bark_ops bark_alert bark_critical bark_custom
export -f bark_status bark_logs bark_batch bark_test bark_help
export -f _bark_push _bark_push_self_hosted _bark_push_official
export -f _bark_push_with_retry _bark_ping _bark_get_url
export -f _bark_log _bark_err_log
