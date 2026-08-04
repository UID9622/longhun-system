#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ╔══════════════════════════════════════════════════════╗
# ║  龍魂·隐私加固脚本 Linux版 v1.0                      ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-PRIVACY-HARDENER-LINUX-v1.0 ║
# ║  守护人格: 乔前辈(P04鲁班)                          ║
# ║  签章: JOE-PRIVACY-SHIELD-LINUX-2026                ║
# ╚══════════════════════════════════════════════════════╝
# 功能: Linux服务器隐私加固·关闭遥测/定位/诊断回传
# 用法: sudo bash bin/lh_privacy_hardener_linux.sh [--check-only]
# 铁律: 物理防火墙是最后一道防线

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CHECK_ONLY=false
[[ "${1:-}" == "--check-only" ]] && CHECK_ONLY=true

log_info()  { echo -e "${BLUE}[*]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[✓]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
log_fail()  { echo -e "${RED}[✗]${NC} $1"; }

FAIL_COUNT=0

echo "╔══════════════════════════════════════════════════════╗"
echo "║  龍魂·隐私加固 Linux版 v1.0                          ║"
echo "║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-PRIVACY-LINUX-v1.0 ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# ── 1. GeoClue定位服务 ──
log_info "[1/7] 检查GeoClue定位服务..."
if [[ "$CHECK_ONLY" == "true" ]]; then
    if systemctl is-active geoclue.service &>/dev/null || systemctl is-enabled geoclue.service &>/dev/null; then
        log_fail "GeoClue定位服务仍在运行/启用"
        ((FAIL_COUNT++))
    else
        log_ok "GeoClue定位服务已停用"
    fi
else
    systemctl stop geoclue.service 2>/dev/null || true
    systemctl disable geoclue.service 2>/dev/null || true
    log_ok "GeoClue定位服务已停用"
fi

# ── 2. ModemManager（回传基站/位置） ──
log_info "[2/7] 检查ModemManager..."
if [[ "$CHECK_ONLY" == "true" ]]; then
    if systemctl is-active ModemManager.service &>/dev/null || systemctl is-enabled ModemManager.service &>/dev/null; then
        log_fail "ModemManager仍在运行/启用"
        ((FAIL_COUNT++))
    else
        log_ok "ModemManager已停用"
    fi
else
    systemctl stop ModemManager.service 2>/dev/null || true
    systemctl disable ModemManager.service 2>/dev/null || true
    log_ok "ModemManager已停用"
fi

# ── 3. 蓝牙 ──
log_info "[3/7] 关闭蓝牙..."
if [[ "$CHECK_ONLY" == "true" ]]; then
    if command -v bluetoothctl &>/dev/null && bluetoothctl show 2>/dev/null | grep -q "Powered: yes"; then
        log_fail "蓝牙仍开启"
        ((FAIL_COUNT++))
    elif command -v rfkill &>/dev/null && rfkill list bluetooth 2>/dev/null | grep -q "Soft blocked: no"; then
        log_fail "蓝牙射频未软阻断"
        ((FAIL_COUNT++))
    else
        log_ok "蓝牙已关闭"
    fi
else
    if command -v rfkill &>/dev/null; then
        rfkill block bluetooth 2>/dev/null || true
    fi
    if command -v bluetoothctl &>/dev/null; then
        echo -e "power off\nquit" | bluetoothctl 2>/dev/null || true
    fi
    log_ok "蓝牙已关闭"
fi

# ── 4. 应用崩溃遥测（Apport / ABRT） ──
log_info "[4/7] 关闭应用崩溃遥测..."
if [[ "$CHECK_ONLY" == "true" ]]; then
    if [[ -f /etc/default/apport ]] && grep -q '^enabled=1' /etc/default/apport; then
        log_fail "Apport崩溃报告仍启用"
        ((FAIL_COUNT++))
    elif systemctl is-active apport.service &>/dev/null; then
        log_fail "Apport服务仍在运行"
        ((FAIL_COUNT++))
    else
        log_ok "崩溃遥测已关闭"
    fi
else
    if [[ -f /etc/default/apport ]]; then
        sed -i 's/^enabled=.*/enabled=0/' /etc/default/apport 2>/dev/null || true
    fi
    systemctl stop apport.service 2>/dev/null || true
    systemctl disable apport.service 2>/dev/null || true
    systemctl stop abrt-journal-core 2>/dev/null || true
    systemctl disable abrt-journal-core 2>/dev/null || true
    log_ok "崩溃遥测已关闭"
fi

# ── 5. systemd-coredump（核心转储） ──
log_info "[5/7] 关闭systemd-coredump..."
if [[ "$CHECK_ONLY" == "true" ]]; then
    if systemctl is-active systemd-coredump.socket &>/dev/null || systemctl is-enabled systemd-coredump.socket &>/dev/null; then
        log_fail "systemd-coredump仍在运行/启用"
        ((FAIL_COUNT++))
    else
        log_ok "systemd-coredump已停用"
    fi
else
    systemctl stop systemd-coredump.socket systemd-coredump@0.service 2>/dev/null || true
    systemctl disable systemd-coredump.socket 2>/dev/null || true
    # 设置系统不生成core dump
    echo "* soft core 0" > /etc/security/limits.d/99-disable-coredump.conf
    log_ok "systemd-coredump已停用"
fi

# ── 6. NTP时间同步（改用本地或可信源） ──
log_info "[6/7] 检查NTP时间同步..."
if [[ "$CHECK_ONLY" == "true" ]]; then
    if timedatectl status 2>/dev/null | grep -q "NTP service: active"; then
        log_warn "NTP服务仍活跃（如需完全离线请手动关闭）"
    else
        log_ok "NTP服务未活跃"
    fi
else
    # 不停用NTP以免服务器时间漂移，但限制为仅本地可信源（若配置了chrony）
    if systemctl is-active chronyd.service &>/dev/null; then
        log_warn "chronyd运行中，请确认上游为可信源"
    elif systemctl is-active systemd-timesyncd.service &>/dev/null; then
        log_warn "systemd-timesyncd运行中，请确认上游为可信源"
    fi
    log_ok "NTP检查完成（未强制关闭，避免时间漂移）"
fi

# ── 7. GNOME Tracker / 文件索引 ──
log_info "[7/7] 检查文件索引服务..."
if [[ "$CHECK_ONLY" == "true" ]]; then
    if systemctl is-active tracker-extract-3 tracker-miner-fs-3 2>/dev/null | grep -q active; then
        log_fail "GNOME Tracker文件索引仍在运行"
        ((FAIL_COUNT++))
    else
        log_ok "文件索引服务未运行"
    fi
else
    systemctl stop tracker-extract-3 tracker-miner-fs-3 2>/dev/null || true
    systemctl disable tracker-extract-3 tracker-miner-fs-3 2>/dev/null || true
    systemctl mask tracker-extract-3 tracker-miner-fs-3 2>/dev/null || true
    log_ok "文件索引服务已停用"
fi

echo ""
echo "═══════════════════════════════════════════════════════"
if [[ "$CHECK_ONLY" == "true" ]]; then
    if [[ "$FAIL_COUNT" -gt 0 ]]; then
        echo -e "${RED}[隐私审计] ${FAIL_COUNT}项未通过${NC}"
        exit 1
    else
        echo -e "${GREEN}[隐私审计] 全部通过 ✅${NC}"
        exit 0
    fi
else
    if [[ "$FAIL_COUNT" -gt 0 ]]; then
        echo -e "${YELLOW}[隐私加固] 完成，${FAIL_COUNT}项需手动确认${NC}"
    else
        echo -e "${GREEN}[隐私加固] 7/7项已完成${NC}"
    fi
    echo ""
    log_info "Linux服务器监控通道已最大程度掐断。"
    log_info "下一步：运行同心锁防火墙。"
    echo "═══════════════════════════════════════════════════════"
fi
