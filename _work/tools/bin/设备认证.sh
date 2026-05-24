#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# 龍魂设备认证脚本 v1.0
# DNA: #龍芯⚡️2026-05-23-DEVICE-AUTH-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
#
# 创建者: UID9622 诸葛鑫
# 理论指导: 曾仕强老师（永恒显示）
# ═══════════════════════════════════════════════════════════════════════════

# 颜色
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 时间戳
NOW=$(date '+%Y-%m-%d %H:%M:%S')

echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}    🐲 龍魂设备认证 · UID9622 · ${NOW}${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# macOS版本
echo -e "${GREEN}§ 系统版本${NC}"
sw_vers
echo ""

# 硬件信息
echo -e "${GREEN}§ 硬件信息${NC}"
system_profiler SPHardwareDataType 2>/dev/null | grep -E "Model|Chip|Cores|Memory|Serial"
echo ""

# CPU
echo -e "${GREEN}§ CPU${NC}"
echo "  品牌: $(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo 'Apple Silicon')"
echo "  物理核/逻辑核: $(sysctl -n hw.physicalcpu) / $(sysctl -n hw.logicalcpu)"
echo ""

# 内存
echo -e "${GREEN}§ 内存${NC}"
MEM_GB=$(echo "scale=2; $(sysctl -n hw.memsize)/1073741824" | bc)
echo "  总内存: ${MEM_GB} GB"
echo ""

# 磁盘
echo -e "${GREEN}§ 磁盘${NC}"
df -h | grep -E "^/dev/disk|Filesystem"
echo ""

# 显卡
echo -e "${GREEN}§ 显卡${NC}"
system_profiler SPDisplaysDataType 2>/dev/null | grep -E "Chipset|VRAM|Resolution" | head -5
echo ""

# 电池
echo -e "${GREEN}§ 电池${NC}"
pmset -g batt 2>/dev/null | head -3 || echo "  无电池信息"
echo ""

# 设备指纹
echo -e "${YELLOW}§ 设备指纹${NC}"
SERIAL=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Serial Number" | awk '{print $NF}')
HARDWARE_UUID=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Hardware UUID" | awk '{print $NF}')
FINGERPRINT=$(echo "${SERIAL}-${HARDWARE_UUID}-UID9622" | shasum -a 256 | cut -c1-16)
echo "  序列号: ${SERIAL}"
echo "  硬件UUID: ${HARDWARE_UUID}"
echo "  龍魂指纹: ${FINGERPRINT}"
echo ""

echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}    ✅ 设备认证通过 · UID9622 诸葛鑫 · 龍魂系统${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"

# 写入认证日志
AUTH_LOG="$HOME/longhun-system/logs/device_auth.log"
mkdir -p "$(dirname "$AUTH_LOG")"
echo "[${NOW}] 设备认证 | 序列号:${SERIAL} | 指纹:${FINGERPRINT} | UID9622" >> "$AUTH_LOG"
