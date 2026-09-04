#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷓观-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ═══════════════════════════════════════════════════════════
# 龍魂系统 · Bark 推送终端插件 v1.0
# UID: 9622 | 主权人格: ZHUGEXIN⚡️ | 用途: 本地→手机实时通道
# 部署: 华为云/本地服务器 | 协议: 不可撤销·出厂设置
# ═══════════════════════════════════════════════════════════

# ─── 配置区 ─── 修改此处即可 ───
BARK_SERVER="${BARK_SERVER:-http://localhost:8080}"   # 自建服务器地址
BARK_KEY="${BARK_KEY:-YOUR_DEVICE_KEY_HERE}"         # iOS Bark App 设备Key
BARK_TIMEOUT="${BARK_TIMEOUT:-10}"                   # 请求超时秒数
BARK_LOG_DIR="${BARK_LOG_DIR:-$HOME/.longhun/bark}"   # 日志归档目录

# ─── 颜色定义 ───
C_RED='\033[0;31m'
C_GREEN='\033[0;32m'
C_YELLOW='\033[0;33m'
C_CYAN='\033[0;36m'
C_RESET='\033[0m'

# ─── 初始化 ───
init_bark() {
    mkdir -p "$BARK_LOG_DIR"
    local today=$(date +%Y%m%d)
    BARK_LOG_FILE="$BARK_LOG_DIR/bark_${today}.log"

    # 首次运行检测
    if [[ "$BARK_KEY" == "YOUR_DEVICE_KEY_HERE" ]]; then
        echo -e "${C_RED}[龍魂·初始化]${C_RESET} BARK_KEY 未配置！"
        echo "  1. iOS 下载 Bark App，复制设备 Key"
        echo "  2. export BARK_KEY=你的Key"
        echo "  3. 重新运行脚本"
        return 1
    fi

    # 服务器连通检测
    if ! curl -s --max-time 3 "${BARK_SERVER}/ping" > /dev/null 2>&1; then
        echo -e "${C_YELLOW}[龍魂·告警]${C_RESET} Bark 服务器未响应: $BARK_SERVER"
        echo "  检查: 1.服务器是否启动 2.防火墙/安全组 3.地址是否正确"
        return 1
    fi

    echo -e "${C_GREEN}[龍魂·就绪]${C_RESET} Bark 通道已连接 | 日志: $BARK_LOG_FILE"
    return 0
}

# ─── 核心推送函数 ───
# 用法: bark_push "标题" "内容" [分组] [级别]
# 级别: info|warn|error|critical (默认 info)
bark_push() {
    local title="$1"
    local body="$2"
    local group="${3:-龍魂系统}"
    local level="${4:-info}"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local retry_count=0
    local max_retries=3
    local success=false

    # 参数校验
    if [[ -z "$title" || -z "$body" ]]; then
        echo -e "${C_RED}[龍魂·错误]${C_RESET} 标题和内容不能为空"
        return 1
    fi

    # URL编码处理
    local encoded_title=$(echo "$title" | sed 's/ /%20/g; s/!/%21/g; s/#/%23/g; s/\$/%24/g; s/&/%26/g; s/'/%27/g; s/(/%28/g; s/)/%29/g; s/\*/%2A/g; s/+/%2B/g; s/,/%2C/g; s/\//%2F/g; s/:/%3A/g; s/;/%3B/g; s/=/%3D/g; s/?/%3F/g; s/@/%40/g; s/\[/%5B/g; s/\]/%5D/g')
    local encoded_body=$(echo "$body" | sed 's/ /%20/g; s/!/%21/g; s/#/%23/g; s/\$/%24/g; s/&/%26/g; s/'/%27/g; s/(/%28/g; s/)/%29/g; s/\*/%2A/g; s/+/%2B/g; s/,/%2C/g; s/\//%2F/g; s/:/%3A/g; s/;/%3B/g; s/=/%3D/g; s/?/%3F/g; s/@/%40/g; s/\[/%5B/g; s/\]/%5D/g')

    # 构建请求URL
    local url="${BARK_SERVER}/${BARK_KEY}/${encoded_title}/${encoded_body}?group=${group}"

    # 级别颜色映射
    local level_color="$C_GREEN"
    case "$level" in
        warn) level_color="$C_YELLOW" ;;
        error) level_color="$C_RED" ;;
        critical) level_color="$C_RED" ;;
    esac

    # 重试机制
    while [[ $retry_count -lt $max_retries && "$success" == "false" ]]; do
        local response=$(curl -s --max-time "$BARK_TIMEOUT" "$url" 2>&1)
        local curl_exit=$?

        if [[ $curl_exit -eq 0 && "$response" == *""code":200"* ]]; then
            success=true
            echo -e "${level_color}[龍魂·推送]${C_RESET} [${group}] ${title} · ${level} · 成功"
        else
            retry_count=$((retry_count + 1))
            if [[ $retry_count -lt $max_retries ]]; then
                echo -e "${C_YELLOW}[龍魂·重试]${C_RESET} 第${retry_count}次重试..."
                sleep 1
            fi
        fi
    done

    # 日志归档
    local log_entry="[${timestamp}] [${level}] [${group}] 标题:${title} 内容:${body} 状态:$([[ "$success" == "true" ]] && echo "成功" || echo "失败[重试${retry_count}次]")"
    echo "$log_entry" >> "$BARK_LOG_FILE"

    # 失败告警（本地终端）
    if [[ "$success" == "false" ]]; then
        echo -e "${C_RED}[龍魂·失败]${C_RESET} 推送失败，已记录日志: $BARK_LOG_FILE"
        echo "  错误: $response"
        return 1
    fi

    return 0
}

# ─── 快捷推送函数 ─── 按场景封装 ───

# 运维通知
bark_ops() {
    bark_push "$1" "$2" "运维" "info"
}

# 告警通知
bark_alert() {
    bark_push "$1" "$2" "告警" "warn"
}

# 错误通知
bark_error() {
    bark_push "$1" "$2" "错误" "error"
}

# 严重告警（带声音）
bark_critical() {
    bark_push "$1" "$2" "紧急" "critical"
}

# 财务通知
bark_finance() {
    bark_push "$1" "$2" "财务" "info"
}

# 开发通知
bark_dev() {
    bark_push "$1" "$2" "开发" "info"
}

# ─── 批量推送 ─── 从文件读取 ───
# 文件格式: 标题|内容|分组|级别
bark_batch() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        echo -e "${C_RED}[龍魂·错误]${C_RESET} 文件不存在: $file"
        return 1
    fi

    local count=0
    local success=0
    while IFS='|' read -r title body group level; do
        [[ -z "$title" || "$title" == \#* ]] && continue
        count=$((count + 1))
        bark_push "$title" "$body" "${group:-龍魂系统}" "${level:-info}" && success=$((success + 1))
    done < "$file"

    echo -e "${C_CYAN}[龍魂·批量]${C_RESET} 完成: ${success}/${count} 条推送成功"
}

# ─── 日志查询 ───
bark_logs() {
    local lines="${1:-50}"
    local today=$(date +%Y%m%d)
    local log_file="$BARK_LOG_DIR/bark_${today}.log"

    if [[ -f "$log_file" ]]; then
        echo -e "${C_CYAN}[龍魂·日志]${C_RESET} 今日推送记录 (最近${lines}条):"
        tail -n "$lines" "$log_file" | while read line; do
            echo "  $line"
        done
    else
        echo -e "${C_YELLOW}[龍魂·日志]${C_RESET} 今日暂无推送记录"
    fi
}

# ─── 状态检测 ───
bark_status() {
    echo -e "${C_CYAN}[龍魂·状态]${C_RESET} Bark 通道诊断:"
    echo "  服务器: $BARK_SERVER"
    echo "  设备Key: ${BARK_KEY:0:8}****"
    echo "  日志目录: $BARK_LOG_DIR"

    if curl -s --max-time 3 "${BARK_SERVER}/ping" > /dev/null 2>&1; then
        echo -e "  服务器状态: ${C_GREEN}在线${C_RESET}"
    else
        echo -e "  服务器状态: ${C_RED}离线${C_RESET}"
    fi

    local today=$(date +%Y%m%d)
    local log_file="$BARK_LOG_DIR/bark_${today}.log"
    if [[ -f "$log_file" ]]; then
        local count=$(wc -l < "$log_file" | tr -d ' ')
        echo "  今日推送: ${count}条"
    fi
}

# ─── 帮助 ───
bark_help() {
    cat << 'EOF'
╔═══════════════════════════════════════════════════════════╗
║  龍魂系统 · Bark 推送终端插件 v1.0                        ║
║  UID: 9622 | 主权人格: ZHUGEXIN⚡️                         ║
╚═══════════════════════════════════════════════════════════╝

【配置】
  export BARK_SERVER=http://你的服务器:8080
  export BARK_KEY=你的iOS设备Key

【核心函数】
  bark_push "标题" "内容" [分组] [级别]
    级别: info(默认) | warn | error | critical

【快捷函数】
  bark_ops "标题" "内容"      → 运维分组
  bark_alert "标题" "内容"    → 告警分组
  bark_error "标题" "内容"    → 错误分组
  bark_critical "标题" "内容" → 紧急分组
  bark_finance "标题" "内容"  → 财务分组
  bark_dev "标题" "内容"      → 开发分组

【批量推送】
  bark_batch /path/to/file.txt
    文件格式: 标题|内容|分组|级别

【工具】
  bark_status           → 通道状态诊断
  bark_logs [行数]      → 查看今日推送日志
  bark_help             → 显示此帮助

【示例】
  source longhun_bark_plugin.sh
  init_bark
  bark_ops "备份完成" "华为云数据备份成功，耗时3分12秒"
  bark_alert "磁盘告警" "使用率85%，建议清理"
  bark_critical "服务宕机" "nginx进程异常退出，请立即检查"

EOF
}

# ─── 如果直接执行此脚本，显示帮助 ───
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    bark_help
fi
