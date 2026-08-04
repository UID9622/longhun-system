#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ============================================
# 龍魂系统 · DNA 生成器 v2.0
# 在客户端设备上运行，生成 DNA 常量文件
# 可选自动注册到服务器
# UID9622 | 龍芯北辰
# DNA: #龍芯⚡️丙午·辛未·乙酉·亥时·豫-DNA-GENERATOR-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ============================================
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ── 配置 ──
SERVER_URL="${LH_DNA_SERVER_URL:-http://119.13.90.27:7700}"
OUTPUT_DIR="${LH_DNA_OUTPUT_DIR:-${HOME}/longhun-system/data/sources}"
DNA_CONST_FILE="${OUTPUT_DIR}/dna_const.sh"
CURL_TIMEOUT=10

echo "╔══════════════════════════════════════════╗"
echo "║   龍魂系统 · DNA 生成器 v2.0            ║"
echo "║   生成设备 DNA + 设备指纹 + 注册        ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ═══════════════════════════════════════════
# 干支计算
# ═══════════════════════════════════════════
get_ganzhi() {
    python3 << 'PYEOF'
import datetime
tiangan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
dizhi   = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
now = datetime.datetime.now()
y, m, d, h = now.year, now.month, now.day, now.hour
base = 1984
offset = y - base
year_gz = tiangan[offset % 10] + dizhi[offset % 12]
month_dz = (m + 1) % 12
month_gz = tiangan[(offset % 10 * 2 + m) % 10] + dizhi[month_dz]
ref = datetime.datetime(1984, 1, 1)
day_offset = (now - ref).days
day_gz = tiangan[day_offset % 10] + dizhi[day_offset % 12]
hour_dz_idx = (h + 1) // 2 % 12
hour_gz = tiangan[(day_offset % 10 * 2 + hour_dz_idx) % 10] + dizhi[hour_dz_idx]
print(f"{year_gz}·{month_gz}·{hour_gz}")
PYEOF
}

GANZHI=$(get_ganzhi)

# ═══════════════════════════════════════════
# 收集设备指纹
# ═══════════════════════════════════════════
echo -e "${BLUE}[1/5]${NC} 收集设备指纹..."

# macOS
if [[ "$(uname -s)" == "Darwin" ]]; then
    HW_UUID=$(ioreg -d2 -c IOPlatformExpertDevice | awk -F'"' '/IOPlatformUUID/{print $4}' 2>/dev/null || echo "unknown")
    HW_MODEL=$(sysctl -n hw.model 2>/dev/null || echo "unknown")
    HW_SERIAL=$(system_profiler SPHardwareDataType | awk '/Serial Number/{print $NF}' 2>/dev/null || echo "unknown")
    HOSTNAME=$(hostname -s 2>/dev/null || echo "unknown")
    OS_VER=$(sw_vers -productVersion 2>/dev/null || echo "unknown")
    DEVICE_TYPE="macOS-${HW_MODEL}"

# Linux
elif [[ "$(uname -s)" == "Linux" ]]; then
    HW_UUID=$(cat /etc/machine-id 2>/dev/null || cat /var/lib/dbus/machine-id 2>/dev/null || echo "unknown")
    HW_MODEL=$(cat /sys/class/dmi/id/product_name 2>/dev/null || echo "unknown")
    HW_SERIAL=$(cat /sys/class/dmi/id/product_serial 2>/dev/null || echo "unknown")
    HOSTNAME=$(hostname -s 2>/dev/null || echo "unknown")
    OS_VER=$(cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d'"' -f2 || echo "unknown")
    DEVICE_TYPE="Linux-${HW_MODEL}"
else
    HW_UUID="unknown"
    HW_MODEL="unknown"
    HW_SERIAL="unknown"
    HOSTNAME="unknown"
    OS_VER="unknown"
    DEVICE_TYPE="Unknown"
fi

echo "  主机名:  ${HOSTNAME}"
echo "  系统:    ${OS_VER}"
echo "  设备:    ${DEVICE_TYPE}"
echo "  UUID:    ${HW_UUID:0:16}..."

# ═══════════════════════════════════════════
# 生成设备指纹哈希
# ═══════════════════════════════════════════
DEVICE_SEED="${HW_UUID}|${HW_SERIAL}|${HW_MODEL}|${HOSTNAME}"
DEVICE_HASH=$(echo -n "${DEVICE_SEED}" | shasum -a 256 | awk '{print $1}' | cut -c1-32)

echo "  指纹:    ${DEVICE_HASH}"
echo ""

# ═══════════════════════════════════════════
# 生成 DNA
# ═══════════════════════════════════════════
echo -e "${BLUE}[2/5]${NC} 生成 DNA..."

# DNA 种子 = 设备指纹 + 时间戳 + 随机盐 + GANZHI
TIMESTAMP_NOW=$(date +%s)
RANDOM_SALT=$(head -c 16 /dev/urandom 2>/dev/null | base64 | tr -dc 'a-zA-Z0-9' | head -c 16 || python3 -c "import random,string;print(''.join(random.choice(string.ascii_letters+string.digits) for _ in range(16)))")
DNA_SEED="${DEVICE_HASH}|${TIMESTAMP_NOW}|${RANDOM_SALT}|${GANZHI}|longhun-dna-gen"

DNA_FULL=$(echo -n "${DNA_SEED}" | shasum -a 256 | awk '{print $1}')
DNA_SHORT=$(echo -n "${DNA_FULL}" | shasum -a 256 | awk '{print $1}' | cut -c1-32)

echo "  完整 DNA: ${DNA_FULL}"
echo "  短 DNA:   ${DNA_SHORT}"
echo ""

# ═══════════════════════════════════════════
# 生成 DNA 签章（用于注册时验证身份）
# ═══════════════════════════════════════════
DNA_SIGNATURE=$(python3 -c "
import hashlib
dna_full='${DNA_FULL}'
device_hash='${DEVICE_HASH}'
salt='${RANDOM_SALT}'
raw = f'{dna_full}|{device_hash}|{salt}|longhun-dna-register'
sig = hashlib.sha256(raw.encode()).hexdigest()[:32]
print(sig)
")

echo -e "${BLUE}[3/5]${NC} 询问设备别名..."
echo -n "  请输入设备别名 (如: Mac本地/鲲鹏服务器/办公室PC): "
read -r DEVICE_ALIAS
DEVICE_ALIAS="${DEVICE_ALIAS:-UNKNOWN}"
echo "  设备别名: ${DEVICE_ALIAS}"
echo ""

# ═══════════════════════════════════════════
# 写入本地常量文件
# ═══════════════════════════════════════════
echo -e "${BLUE}[4/5]${NC} 写入 DNA 常量文件..."

mkdir -p "$OUTPUT_DIR"

cat > "$DNA_CONST_FILE" << DNAEOF
#!/bin/bash
# ============================================
# 龍魂系统 · DNA 常量文件
# 生成时间: $(date '+%Y-%m-%d %H:%M:%S')
# 干支: ${GANZHI}
# 设备: ${DEVICE_ALIAS}
# ⚠️  此文件被删除/篡改 = DNA 抹除 = 系统失效
# ============================================
# DNA: #龍芯⚡️${GANZHI}-${DEVICE_TYPE}-DNA-GEN-v2.0

export LONGHUN_DNA_FULL="${DNA_FULL}"
export LONGHUN_DNA_SHORT="${DNA_SHORT}"
export LONGHUN_DEVICE_HASH="${DEVICE_HASH}"
export LONGHUN_DEVICE_ALIAS="${DEVICE_ALIAS}"
export LONGHUN_DEVICE_TYPE="${DEVICE_TYPE}"
export LONGHUN_OS_VERSION="${OS_VER}"
export LONGHUN_DNA_GANZHI="${GANZHI}"
export LONGHUN_DNA_SIGNATURE="${DNA_SIGNATURE}"
export LONGHUN_DNA_SALT="${RANDOM_SALT}"
export LONGHUN_DNA_CREATED_AT="${TIMESTAMP_NOW}"
DNAEOF

chmod 600 "$DNA_CONST_FILE"

echo -e "  ${GREEN}✅ 已写入: ${DNA_CONST_FILE}${NC}"
echo ""

# ═══════════════════════════════════════════
# 可选：自动注册到服务器
# ═══════════════════════════════════════════
echo -e "${BLUE}[5/5]${NC} 注册 DNA 到服务器..."
echo ""

# 检查服务器连通性
SERVER_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" \
    --connect-timeout "$CURL_TIMEOUT" \
    --max-time "$CURL_TIMEOUT" \
    "${SERVER_URL}/health" 2>/dev/null || echo "000")

if [[ "$SERVER_HEALTH" != "200" ]]; then
    echo -e "  ${YELLOW}⚠️  服务器不可达 (HTTP ${SERVER_HEALTH})，跳过自动注册${NC}"
    echo ""
    echo -e "  请稍后手动注册:"
    echo ""
    cat << REGCMD
  curl -X POST ${SERVER_URL}/dna/register \\
    -H "Content-Type: application/json" \\
    -d '{
      "dna_full": "${DNA_FULL}",
      "dna_short": "${DNA_SHORT}",
      "device_hash": "${DEVICE_HASH}",
      "device_alias": "${DEVICE_ALIAS}",
      "dna_signature": "${DNA_SIGNATURE}",
      "ganzhi": "${GANZHI}",
      "salt": "${RANDOM_SALT}",
      "timestamp": ${TIMESTAMP_NOW}
    }'
REGCMD
else
    echo -n "  正在注册..."

    REGISTER_RESP=$(curl -s \
        --connect-timeout "$CURL_TIMEOUT" \
        --max-time "$CURL_TIMEOUT" \
        -X POST "${SERVER_URL}/dna/register" \
        -H "Content-Type: application/json" \
        -d "{
            \"dna_full\": \"${DNA_FULL}\",
            \"dna_short\": \"${DNA_SHORT}\",
            \"device_hash\": \"${DEVICE_HASH}\",
            \"device_alias\": \"${DEVICE_ALIAS}\",
            \"dna_signature\": \"${DNA_SIGNATURE}\",
            \"ganzhi\": \"${GANZHI}\",
            \"salt\": \"${RANDOM_SALT}\",
            \"timestamp\": ${TIMESTAMP_NOW}
        }" 2>/dev/null)

    REG_STATUS=$(echo "$REGISTER_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status','ERROR'))" 2>/dev/null || echo "ERROR")

    if [[ "$REG_STATUS" == "REGISTERED" ]] || [[ "$REG_STATUS" == "RENEWED" ]]; then
        echo -e " ${GREEN}✅ ${REG_STATUS}${NC}"
        echo ""
        echo "  $(echo "$REGISTER_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('message',''))" 2>/dev/null)"
    else
        echo -e " ${RED}❌ 失败${NC}"
        echo ""
        echo "  服务器响应: ${REGISTER_RESP}"
    fi
fi

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  DNA 生成完成                            ║"
echo "╠══════════════════════════════════════════╣"
echo "║  设备: ${DEVICE_ALIAS}"
echo "║  指纹: ${DEVICE_HASH:0:16}..."
echo "║  DNA:  ${DNA_SHORT:0:16}..."
echo "║  干支: ${GANZHI}"
echo "╠══════════════════════════════════════════╣"
echo "║  常量文件: ${DNA_CONST_FILE}            ║"
echo "║                                          ║"
echo "║  在启动脚本中添加:                       ║"
echo "║  source longhun_dna_verify.sh || exit 1  ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "  下次启动时，DNA 会自动验证。"
echo "  删除 ${DNA_CONST_FILE} = DNA 被抹除 = 系统失效"
