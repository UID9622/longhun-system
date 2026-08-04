#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ============================================
# 龍魂系统 · DNA 客户端验证脚本 v2.0
# 每次运行系统前调用，验证 DNA 是否有效
# 集成方式: source this_script || exit 1
# UID9622 | 龍芯北辰
# DNA: #龍芯⚡️丙午·辛未·乙酉·亥时·豫-DNA-VERIFY-v2.0
# ============================================
set -euo pipefail

# ── 配置 ──
# 优先用环境变量，否则用默认值
SERVER_URL="${LH_DNA_SERVER_URL:-http://119.13.90.27:7700}"
DNA_CONST_FILE="${LH_DNA_CONST_FILE:-${HOME}/longhun-system/data/sources/dna_const.sh}"
CURL_TIMEOUT=10
MAX_RETRIES=3

# ── 颜色 ──
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ═══════════════════════════════════════════
# 干支计算（与服务器对齐）
# ═══════════════════════════════════════════
get_ganzhi() {
    python3 << 'PYEOF'
import datetime

tiangan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
dizhi   = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

now = datetime.datetime.now()
y, m, d, h = now.year, now.month, now.day, now.hour

# 年干支 (1984=甲子)
base = 1984
offset = y - base
year_gz = tiangan[offset % 10] + dizhi[offset % 12]

# 月干支
month_dz = (m + 1) % 12
month_gz = tiangan[(offset % 10 * 2 + m) % 10] + dizhi[month_dz]

# 日干支 (1984-01-01=甲子日)
ref = datetime.datetime(1984, 1, 1)
day_offset = (now - ref).days
day_gz = tiangan[day_offset % 10] + dizhi[day_offset % 12]

# 时干支
hour_dz_idx = (h + 1) // 2 % 12
hour_gz = tiangan[(day_offset % 10 * 2 + hour_dz_idx) % 10] + dizhi[hour_dz_idx]

print(f"{year_gz}·{month_gz}·{hour_gz}")
PYEOF
}

# ═══════════════════════════════════════════
# Step 0: 检查 DNA 常量文件
# ═══════════════════════════════════════════
if [[ ! -f "$DNA_CONST_FILE" ]]; then
    echo -e "${RED}❌ DNA 常量文件不存在: ${DNA_CONST_FILE}${NC}"
    echo ""
    echo "  可能原因:"
    echo "    1. 尚未运行 dna-generator.sh 生成 DNA"
    echo "    2. DNA 常量文件被删除（DNA 被抹除）"
    echo ""
    echo "  处理: 运行 bash dna-generator.sh 重新生成并注册"
    exit 1
fi

# shellcheck source=/dev/null
source "$DNA_CONST_FILE"

# ═══════════════════════════════════════════
# Step 1: 检查本地 DNA 完整性
# ═══════════════════════════════════════════
if [[ -z "${LONGHUN_DNA_SHORT:-}" ]] || [[ -z "${LONGHUN_DEVICE_HASH:-}" ]]; then
    echo -e "${RED}❌ 本地 DNA 不完整，可能已被抹除${NC}"
    echo ""
    echo "  LONGHUN_DNA_SHORT=${LONGHUN_DNA_SHORT:-<空>}"
    echo "  LONGHUN_DEVICE_HASH=${LONGHUN_DEVICE_HASH:-<空>}"
    exit 1
fi

# ═══════════════════════════════════════════
# Step 2: 检查网络连通性
# ═══════════════════════════════════════════
check_server() {
    curl -s -o /dev/null -w "%{http_code}" \
        --connect-timeout "$CURL_TIMEOUT" \
        --max-time "$CURL_TIMEOUT" \
        "${SERVER_URL}/health" 2>/dev/null || echo "000"
}

echo -n "🔗 连接 DNA 验证服务器..."

SERVER_CHECK=$(check_server)
if [[ "$SERVER_CHECK" != "200" ]]; then
    echo -e " ${RED}❌ 无法连接${NC} (HTTP ${SERVER_CHECK})"
    echo ""
    echo "  可能原因:"
    echo "    1. 服务器未启动   → SSH 到服务器: systemctl start longhun-dna"
    echo "    2. 网络不通       → ping ${SERVER_URL%%:*}"
    echo "    3. 端口未放行     → 华为云安全组是否放行 TCP 7000?"
    echo ""
    echo "  服务器地址: ${SERVER_URL}"
    echo "  可通过环境变量覆盖: export LH_DNA_SERVER_URL=http://..."
    exit 1
fi
echo -e " ${GREEN}✅${NC}"

# ═══════════════════════════════════════════
# Step 3: 发送 DNA 验证请求（带重试）
# ═══════════════════════════════════════════
TIMESTAMP=$(date +%s)
GANZHI=$(get_ganzhi)

verify_dna() {
    curl -s \
        --connect-timeout "$CURL_TIMEOUT" \
        --max-time "$CURL_TIMEOUT" \
        -X POST "${SERVER_URL}/dna/verify" \
        -H "Content-Type: application/json" \
        -d "{
            \"dna_short\": \"${LONGHUN_DNA_SHORT}\",
            \"device_hash\": \"${LONGHUN_DEVICE_HASH}\",
            \"timestamp\": ${TIMESTAMP},
            \"ganzhi\": \"${GANZHI}\"
        }" 2>/dev/null
}

echo -n "🔐 验证 DNA..."
VERIFY_COUNT=0
RESPONSE=""

for attempt in $(seq 1 $MAX_RETRIES); do
    RESPONSE=$(verify_dna)
    HTTP_CODE=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('code','000'))" 2>/dev/null || echo "000")

    if [[ "$HTTP_CODE" == "200" ]]; then
        VERIFY_COUNT=$attempt
        break
    fi

    if [[ $attempt -lt $MAX_RETRIES ]]; then
        echo -n "."
        sleep 2
    fi
done

# ═══════════════════════════════════════════
# Step 4: 解析结果
# ═══════════════════════════════════════════
parse_field() {
    echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('$1',''))" 2>/dev/null || echo "未知"
}

STATUS=$(parse_field "status")
VERIFY=$(parse_field "dna_verify")
DEVICE_ALIAS="${LONGHUN_DEVICE_ALIAS:-$(parse_field 'device_alias')}"
REMAINING=$(parse_field "remaining_days")
VERIFY_COUNT_OUT=$(parse_field "verify_count")

if [[ "$VERIFY" == "True" ]]; then
    echo -e " ${GREEN}✅ 通过${NC}"
    echo "╔══════════════════════════════════════════╗"
    echo "║  龍魂 DNA 验证通过                       ║"
    echo "╠══════════════════════════════════════════╣"
    echo "║  设备: ${DEVICE_ALIAS}"
    echo "║  验证: 第 ${VERIFY_COUNT_OUT} 次"
    echo "║  干支: ${GANZHI}"
    echo "║  剩余: ${REMAINING} 天"
    echo "╚══════════════════════════════════════════╝"
    exit 0
fi

# ═══════════════════════════════════════════
# Step 5: 失败处理
# ═══════════════════════════════════════════
MESSAGE=$(parse_field "message")
ACTION=$(parse_field "action_required")

echo -e " ${RED}❌ 失败${NC}"
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  ❌ 龍魂 DNA 验证失败                    ║"
echo "╠══════════════════════════════════════════╣"

case "$STATUS" in
    NOT_FOUND)
        echo "║  原因: DNA 未注册或已被抹除              ║"
        echo "║  结果: 系统已失效                        ║"
        ;;
    EXPIRED)
        echo "║  原因: DNA 已过期                        ║"
        echo "║  结果: 系统已失效                        ║"
        ;;
    FORBIDDEN)
        echo "║  原因: 设备指纹不匹配                    ║"
        echo "║  结果: 请在原设备上运行                  ║"
        ;;
    TIME_MISMATCH)
        echo "║  原因: 本地时间与服务器时间偏差过大       ║"
        echo "║  处理: 同步系统时间                      ║"
        ;;
    RATE_LIMITED)
        echo "║  原因: 请求过于频繁                      ║"
        echo "║  处理: 稍等60秒后重试                    ║"
        ;;
    *)
        echo "║  状态: ${STATUS}                         ║"
        echo "║  详情: ${MESSAGE}                        ║"
        ;;
esac

echo "║                                          ║"
echo "║  处理: ${ACTION}                         ║"
echo "║  重试次数: ${VERIFY_COUNT}/${MAX_RETRIES}           ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "  服务器响应原文:"
echo "  ${RESPONSE}"
echo ""

if [[ -n "${ACTION:-}" ]]; then
    echo "  ${ACTION}"
fi

exit 1
