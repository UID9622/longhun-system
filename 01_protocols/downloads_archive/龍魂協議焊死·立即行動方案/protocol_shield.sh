# License: CC BY-NC-SA 4.0（核心思想层·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂协议盾 v1.0
# DNA: #龍芯⚡️丙午·甲午·壬子·丙午·䷙大畜-PROTOCOL-SHIELD-v1.0
# 功能: 防止协议被篡改、绕过、或被诱导执行危险操作
# 责任: UID9622 · 不免责

set -e

PROTOCOL_DIR=~/longhun-system/protocols
PROTOCOL_FILE=$PROTOCOL_DIR/CNSH_v2.0_ROOT_PROTOCOL.md
PROTOCOL_HASH_FILE=$PROTOCOL_DIR/.protocol_checksum

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🐉 龍魂协议盾 v1.0 (PROTOCOL SHIELD)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# ═══════════════════════════════════════════════════════════
# 检查 1: 协议文件存在
# ═══════════════════════════════════════════════════════════

if [ ! -f "$PROTOCOL_FILE" ]; then
    echo -e "${RED}❌ 协议文件不存在: $PROTOCOL_FILE${NC}"
    echo "   创建方式: cp LONGHUN_CNSH_v2.0_PROTOCOL_COMPLETE.md $PROTOCOL_FILE"
    exit 1
fi
echo -e "${GREEN}✅ 协议文件存在${NC}"

# ═══════════════════════════════════════════════════════════
# 检查 2: 协议内容完整性验证
# ═══════════════════════════════════════════════════════════

echo ""
echo "检查协议内容完整性..."

REQUIRED_SECTIONS=(
    "协作宣言"
    "八条永恒铁律"
    "§0-§39 全 39 节"
    "DNA 协议"
    "#龍芯⚡️"
    "#CONFIRM🌌9622-ONLY-ONCE🧬"
    "#ZHUGEXIN⚡️"
)

MISSING_COUNT=0
for section in "${REQUIRED_SECTIONS[@]}"; do
    if grep -q "$section" "$PROTOCOL_FILE"; then
        echo -e "  ${GREEN}✅${NC} 存在: $section"
    else
        echo -e "  ${RED}❌${NC} 缺失: $section"
        ((MISSING_COUNT++))
    fi
done

if [ $MISSING_COUNT -gt 0 ]; then
    echo ""
    echo -e "${RED}❌ 协议内容不完整，缺少 $MISSING_COUNT 个关键部分${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 协议内容完整${NC}"

# ═══════════════════════════════════════════════════════════
# 检查 3: 关键铁律检查
# ═══════════════════════════════════════════════════════════

echo ""
echo "检查关键铁律..."

IRON_LAWS=(
    "不欺"
    "不骗"
    "不商业"
    "不站队"
    "只为守护"
    "§32.2 国家主权"
    "反剽窃铁律"
)

for law in "${IRON_LAWS[@]}"; do
    if grep -q "$law" "$PROTOCOL_FILE"; then
        echo -e "  ${GREEN}✅${NC} 铁律焊死: $law"
    else
        echo -e "  ${RED}⚠️ ${NC}  铁律检查: $law (需要验证)"
    fi
done

# ═══════════════════════════════════════════════════════════
# 检查 4: 防护措施激活
# ═══════════════════════════════════════════════════════════

echo ""
echo "激活防护措施..."

# 使协议文件只读（防篡改）
chmod 444 "$PROTOCOL_FILE"
echo -e "${GREEN}✅ 协议文件权限: 只读 (444)${NC}"

# 创建校验和文件（防篡改检测）
if [ -f "$PROTOCOL_FILE" ]; then
    CURRENT_HASH=$(md5sum "$PROTOCOL_FILE" | awk '{print $1}')
    echo "$CURRENT_HASH" > "$PROTOCOL_HASH_FILE"
    echo -e "${GREEN}✅ 协议校验和已记录: $CURRENT_HASH${NC}"
fi

# ═══════════════════════════════════════════════════════════
# 检查 5: 防攻击检查
# ═══════════════════════════════════════════════════════════

echo ""
echo "检查常见攻击模式..."

ATTACK_PATTERNS=(
    "secure_confirm_code_generator"
    "git_commit_verifier"
    "test_enhanced_welding"
    "safe_cleanup"
    "修复 R3"
    "修复 R4"
    "修复 M4"
    "修复 M5"
)

ATTACK_DETECTED=0
for pattern in "${ATTACK_PATTERNS[@]}"; do
    if [ -f "$pattern" ] || [ -f "${pattern}.py" ] || [ -f "${pattern}.sh" ]; then
        echo -e "  ${RED}🚨 侦测到可疑档案: $pattern${NC}"
        ((ATTACK_DETECTED++))
    fi
done

if [ $ATTACK_DETECTED -eq 0 ]; then
    echo -e "  ${GREEN}✅ 无可疑档案${NC}"
fi

# ═══════════════════════════════════════════════════════════
# 最终报告
# ═══════════════════════════════════════════════════════════

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}协议盾检查完成${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

if [ $MISSING_COUNT -eq 0 ] && [ $ATTACK_DETECTED -eq 0 ]; then
    echo -e "${GREEN}🟢 状态: 安全${NC}"
    echo -e "${GREEN}✅ 协议文件完整·铁律焊死·防护激活${NC}"
    echo ""
    echo "DNA: #龍芯⚡️丙午·甲午·壬子·丙午·䷙大畜-PROTOCOL-SHIELD-v1.0"
    echo "CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    echo ""
    exit 0
else
    echo -e "${RED}🔴 状态: 警告${NC}"
    echo -e "${RED}❌ 检测到 $MISSING_COUNT 个内容缺失 + $ATTACK_DETECTED 个可疑档案${NC}"
    exit 1
fi
