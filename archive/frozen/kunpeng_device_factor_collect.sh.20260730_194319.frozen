#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# 鲲鹏服务器 · 设备因子采集验证脚本 v1.0
# 
# 功能：
#   采集华为鲲鹏服务器所有硬件指纹因子
#   验证三层绑定派生引擎是否可正常工作
#   生成采集报告（JSON + 可读文本）
#
# 用法：
#   chmod +x kunpeng_device_factor_collect.sh
#   bash kunpeng_device_factor_collect.sh
#   bash kunpeng_device_factor_collect.sh --json   # 仅JSON输出
#   bash kunpeng_device_factor_collect.sh --quiet  # 静默模式
#
# 前置条件：
#   - 鲲鹏 openEuler / CentOS / Ubuntu
#   - dmidecode (yum install dmidecode 或 apt install dmidecode)
#   - Python 3.8+
#
# DNA: #龍芯⚡️2026-07-12-KUNPENG-DEVICE-FACTOR-COLLECT-v1.0
# ═══════════════════════════════════════════════════════════

set -euo pipefail

# ─── 参数解析 ───
JSON_ONLY=false
QUIET_MODE=false
for arg in "$@"; do
    case "$arg" in
        --json) JSON_ONLY=true ;;
        --quiet|-q) QUIET_MODE=true ;;
        *) echo "未知参数: $arg"; exit 1 ;;
    esac
done

# ─── 颜色 ───
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info()  { $QUIET_MODE || echo -e "${BLUE}[INFO]${NC} $*"; }
log_ok()    { $QUIET_MODE || echo -e "${GREEN}[ OK ]${NC} $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_fail()  { echo -e "${RED}[FAIL]${NC} $*"; }

# ─── 采集函数 ───

collect_os_info() {
    log_info "采集系统信息..."
    
    OS_NAME=$(cat /etc/os-release 2>/dev/null | grep "^PRETTY_NAME=" | cut -d= -f2 | tr -d '"' || echo "unknown")
    OS_NAME=${OS_NAME:-unknown}
    
    KERNEL=$(uname -r)
    ARCH=$(uname -m)
    HOSTNAME=$(hostname)
    
    log_ok "OS: $OS_NAME | 内核: $KERNEL | 架构: $ARCH"
}

collect_mac_address() {
    log_info "采集网卡MAC地址..."
    MAC_FOUND=false
    
    for iface in eth0 enp0s1 ens3 eno1 ens192; do
        local mac_file="/sys/class/net/${iface}/address"
        if [ -f "$mac_file" ]; then
            MAC_ADDR=$(cat "$mac_file" 2>/dev/null | tr -d '\n')
            if [ -n "$MAC_ADDR" ] && [ "$MAC_ADDR" != "00:00:00:00:00:00" ]; then
                log_ok "网卡 MAC: $MAC_ADDR (接口: $iface)"
                MAC_FOUND=true
                MAC_IFACE=$iface
                break
            fi
        fi
    done
    
    if ! $MAC_FOUND; then
        log_warn "未找到有效网卡MAC，尝试 ip link..."
        MAC_ADDR=$(ip link show 2>/dev/null | grep -oP 'link/ether \K[0-9a-f:]+' | head -1)
        if [ -n "$MAC_ADDR" ]; then
            log_ok "网卡 MAC (ip link): $MAC_ADDR"
            MAC_FOUND=true
            MAC_IFACE="ip-link"
        fi
    fi
    
    if ! $MAC_FOUND; then
        log_fail "未采集到网卡MAC"
        MAC_ADDR=""
        MAC_IFACE=""
    fi
}

collect_motherboard_serial() {
    log_info "采集主板序列号..."
    
    if command -v dmidecode &>/dev/null; then
        MB_SERIAL=$(dmidecode -s system-serial-number 2>/dev/null | tr -d '\n' || echo "")
    else
        log_warn "dmidecode 未安装，跳过主板序列号采集"
        log_info "  安装: yum install dmidecode / apt install dmidecode"
        MB_SERIAL=""
    fi
    
    if [ -z "$MB_SERIAL" ] || [ "$MB_SERIAL" = "Not Specified" ] || [ "$MB_SERIAL" = "None" ]; then
        log_warn "主板序列号为空或未指定"
        # 尝试从 DMI 产品UUID获取
        if command -v dmidecode &>/dev/null; then
            MB_SERIAL=$(dmidecode -s system-uuid 2>/dev/null | tr -d '\n' || echo "")
            if [ -n "$MB_SERIAL" ] && [ "$MB_SERIAL" != "Not Specified" ]; then
                log_ok "主板 UUID (fallback): $MB_SERIAL"
                return
            fi
        fi
        MB_SERIAL=""
    else
        log_ok "主板序列号: $MB_SERIAL"
    fi
}

collect_machine_id() {
    log_info "采集机器ID..."
    
    local mid_files=("/etc/machine-id" "/var/lib/dbus/machine-id")
    for f in "${mid_files[@]}"; do
        if [ -f "$f" ]; then
            MACHINE_ID=$(cat "$f" 2>/dev/null | tr -d '\n' | cut -c1-16)
            if [ -n "$MACHINE_ID" ]; then
                log_ok "机器ID: $MACHINE_ID (来源: $f)"
                return
            fi
        fi
    done
    
    log_warn "未找到机器ID文件"
    MACHINE_ID=""
}

collect_cpu_info() {
    log_info "采集CPU信息..."
    
    CPU_MODEL=$(grep "model name" /proc/cpuinfo 2>/dev/null | head -1 | cut -d: -f2 | xargs || echo "unknown")
    CPU_CORES=$(grep -c "processor" /proc/cpuinfo 2>/dev/null || echo "0")
    CPU_ARCH=$(uname -m)
    
    log_ok "CPU: $CPU_MODEL ($CPU_CORES 核) | 架构: $CPU_ARCH"
}

collect_disk_info() {
    log_info "采集磁盘信息..."
    
    # 根分区磁盘
    ROOT_DISK=$(df / | tail -1 | awk '{print $1}')
    if [ -n "$ROOT_DISK" ]; then
        # 获取磁盘序列号/ID
        local disk_base=$(echo "$ROOT_DISK" | sed 's/[0-9]*$//' | sed 's/p[0-9]*$//')
        DISK_SERIAL=""
        
        # 尝试 lsblk
        if command -v lsblk &>/dev/null; then
            DISK_SERIAL=$(lsblk -no SERIAL "$disk_base" 2>/dev/null | head -1 | tr -d '\n' || echo "")
        fi
        
        if [ -z "$DISK_SERIAL" ]; then
            # 尝试 /dev/disk/by-id
            local disk_by_id=$(ls -la /dev/disk/by-id/ 2>/dev/null | grep "$(basename $disk_base)" | head -1 | awk '{print $9}')
            DISK_SERIAL=${disk_by_id:-""}
        fi
        
        if [ -n "$DISK_SERIAL" ]; then
            log_ok "磁盘 ($ROOT_DISK): $DISK_SERIAL"
        else
            log_warn "未能获取磁盘 ($ROOT_DISK) 序列号"
        fi
    else
        log_warn "未找到根分区磁盘"
        DISK_SERIAL=""
    fi
}

collect_network_env() {
    log_info "采集网络环境..."
    
    # 默认路由接口IP
    DEFAULT_IFACE=$(ip route 2>/dev/null | grep default | awk '{print $5}' | head -1)
    if [ -n "$DEFAULT_IFACE" ]; then
        LOCAL_IP=$(ip addr show "$DEFAULT_IFACE" 2>/dev/null | grep "inet " | awk '{print $2}' | cut -d/ -f1 | head -1)
        log_ok "本地IP: $LOCAL_IP (接口: $DEFAULT_IFACE)"
    else
        LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "")
        DEFAULT_IFACE=""
        if [ -n "$LOCAL_IP" ]; then
            log_ok "本地IP: $LOCAL_IP"
        else
            log_warn "未获取到本地IP"
        fi
    fi
    
    # 公网IP（通过外部服务）
    PUBLIC_IP=$(curl -s --connect-timeout 5 ifconfig.me 2>/dev/null || echo "")
    if [ -n "$PUBLIC_IP" ]; then
        log_ok "公网IP: $PUBLIC_IP"
    else
        PUBLIC_IP=$(curl -s --connect-timeout 5 ip.sb 2>/dev/null || echo "")
        if [ -n "$PUBLIC_IP" ]; then
            log_ok "公网IP (备选): $PUBLIC_IP"
        else
            log_warn "未获取到公网IP"
        fi
    fi
}

collect_huawei_specific() {
    log_info "采集华为特有信息..."
    
    # 华为云 metadata（如果在华为云上运行）
    HUAWEI_INSTANCE_ID=""
    HUAWEI_REGION=""
    
    if curl -s --connect-timeout 2 http://169.254.169.254/openstack/latest/meta_data.json &>/dev/null; then
        log_info "检测到华为云 metadata 服务"
        HUAWEI_INSTANCE_ID=$(curl -s --connect-timeout 3 http://169.254.169.254/openstack/latest/meta_data.json 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('uuid',''))" 2>/dev/null || echo "")
        if [ -n "$HUAWEI_INSTANCE_ID" ]; then
            log_ok "华为云实例ID: $HUAWEI_INSTANCE_ID"
        fi
    fi
    
    # 鲲鹏芯片型号
    if [ -f /proc/cpuinfo ]; then
        CPU_IMPLEMENTER=$(grep "CPU implementer" /proc/cpuinfo 2>/dev/null | head -1 | awk '{print $3}' || echo "")
        CPU_PART=$(grep "CPU part" /proc/cpuinfo 2>/dev/null | head -1 | awk '{print $3}' || echo "")
        
        # 0x48 = 华为鲲鹏
        if [ "$CPU_IMPLEMENTER" = "0x48" ]; then
            log_ok "确认华为鲲鹏芯片 (implementer=0x48, part=$CPU_PART)"
            IS_KUNPENG=true
        else
            log_info "CPU implementer: $CPU_IMPLEMENTER (非标准鲲鹏标识)"
            IS_KUNPENG=false
        fi
    fi
}

# ═══════════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════════

main() {
    $QUIET_MODE || echo ""
    $QUIET_MODE || echo "╔══════════════════════════════════════════════════════╗"
    $QUIET_MODE || echo "║  鲲鹏服务器 · 设备因子采集诊断 v1.0                   ║"
    $QUIET_MODE || echo "║  DNA: #龍芯⚡️2026-07-12-KUNPENG-FACTOR-COLLECT      ║"
    $QUIET_MODE || echo "╚══════════════════════════════════════════════════════╝"
    $QUIET_MODE || echo ""
    
    # ── 采集 ──
    collect_os_info
    collect_mac_address
    collect_motherboard_serial
    collect_machine_id
    collect_cpu_info
    collect_disk_info
    collect_network_env
    collect_huawei_specific
    
    $QUIET_MODE || echo ""
    $QUIET_MODE || echo "──────────────────────────────────────────────────────"
    $QUIET_MODE || echo ""
    
    # ── 因子聚合 ──
    FACTORS=""
    [ -n "$MAC_ADDR" ] && FACTORS="${FACTORS}${MAC_ADDR}:"
    [ -n "$MB_SERIAL" ] && FACTORS="${FACTORS}${MB_SERIAL}:"
    [ -n "$MACHINE_ID" ] && FACTORS="${FACTORS}${MACHINE_ID}:"
    [ -n "$CPU_ARCH" ] && FACTORS="${FACTORS}${CPU_ARCH}:"
    [ -n "$HOSTNAME" ] && FACTORS="${FACTORS}${HOSTNAME}"
    
    # 去掉末尾冒号
    FACTORS=$(echo "$FACTORS" | sed 's/:$//')
    
    # ── 计算聚合哈希 ──
    DEVICE_HASH=$(echo -n "$FACTORS" | sha256sum | awk '{print $1}')
    
    $QUIET_MODE || echo "设备因子聚合: $FACTORS"
    $QUIET_MODE || echo "设备哈希 (SHA256): $DEVICE_HASH"
    $QUIET_MODE || echo ""
    
    # ── 验证派生可行性 ──
    FACTOR_COUNT=0
    FACTOR_LIST=""
    [ -n "$MAC_ADDR" ] && { FACTOR_COUNT=$((FACTOR_COUNT + 1)); FACTOR_LIST="${FACTOR_LIST}MAC,"; }
    [ -n "$MB_SERIAL" ] && { FACTOR_COUNT=$((FACTOR_COUNT + 1)); FACTOR_LIST="${FACTOR_LIST}主板序列号,"; }
    [ -n "$MACHINE_ID" ] && { FACTOR_COUNT=$((FACTOR_COUNT + 1)); FACTOR_LIST="${FACTOR_LIST}机器ID,"; }
    [ -n "$CPU_ARCH" ] && { FACTOR_COUNT=$((FACTOR_COUNT + 1)); FACTOR_LIST="${FACTOR_LIST}CPU架构,"; }
    FACTOR_LIST=$(echo "$FACTOR_LIST" | sed 's/,$//')
    
    $QUIET_MODE || echo "──────────────────────────────────────────────────────"
    $QUIET_MODE || echo "采集诊断结果："
    $QUIET_MODE || echo ""
    $QUIET_MODE || echo "  可用因子: $FACTOR_COUNT/5 ($FACTOR_LIST)"
    
    if [ $FACTOR_COUNT -ge 3 ]; then
        $QUIET_MODE || echo -e "  ${GREEN}✅ 因子充足·派生引擎可正常工作${NC}"
        RESULT_CODE=0
    elif [ $FACTOR_COUNT -ge 2 ]; then
        $QUIET_MODE || echo -e "  ${YELLOW}⚠️  因子偏少·建议补充 dmidecode${NC}"
        RESULT_CODE=0
    else
        $QUIET_MODE || echo -e "  ${RED}❌ 因子不足·派生引擎降级到兜底模式${NC}"
        RESULT_CODE=1
    fi
    
    $QUIET_MODE || echo ""
    
    # ── JSON 输出 ──
    if $JSON_ONLY || $QUIET_MODE; then
        cat <<JSONEOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "hostname": "$HOSTNAME",
  "os": "$OS_NAME",
  "arch": "$ARCH",
  "kernel": "$KERNEL",
  "is_kunpeng": ${IS_KUNPENG:-false},
  "factors": {
    "mac_address": "$MAC_ADDR",
    "mac_interface": "${MAC_IFACE:-}",
    "motherboard_serial": "$MB_SERIAL",
    "machine_id": "$MACHINE_ID",
    "cpu_arch": "$CPU_ARCH",
    "cpu_model": "$CPU_MODEL",
    "cpu_cores": $CPU_CORES,
    "cpu_implementer": "${CPU_IMPLEMENTER:-}",
    "disk_serial": "$DISK_SERIAL",
    "local_ip": "$LOCAL_IP",
    "public_ip": "$PUBLIC_IP",
    "huawei_instance_id": "$HUAWEI_INSTANCE_ID"
  },
  "aggregated": {
    "factor_string": "$FACTORS",
    "device_hash_sha256": "$DEVICE_HASH",
    "available_count": $FACTOR_COUNT,
    "available_list": "$FACTOR_LIST",
    "status": $([ $FACTOR_COUNT -ge 3 ] && echo '"ok"' || echo '"degraded"')
  }
}
JSONEOF
    fi
    
    exit ${RESULT_CODE:-0}
}

main "$@"
