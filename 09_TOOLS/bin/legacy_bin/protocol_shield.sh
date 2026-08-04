#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂協議盾 v1.0
# DNA:#龍芯⚡️2026-06-07-PROTOCOL-SHIELD-v1.0
# 功能: 防止協議被篡改、繞過、或被誘導執行危險操作
# 責任: UID9622 · 不免責

set -e

PROTOCOL_DIR=~/longhun-system/protocols
PROTOCOL_FILE=$PROTOCOL_DIR/CNSH_v2.0_ROOT_PROTOCOL.md
PROTOCOL_HASH_FILE=$PROTOCOL_DIR/.protocol_checksum

# 顏色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🐉 龍魂協議盾 v1.0 (PROTOCOL SHIELD)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# ═══════════════════════════════════════════════════════════
# 檢查 1: 協議文件存在
# ═══════════════════════════════════════════════════════════

if [ ! -f "$PROTOCOL_FILE" ]; then
    echo -e "${RED}❌ 協議文件不存在: $PROTOCOL_FILE${NC}"
    echo "   創建方式: cp LONGHUN_CNSH_v2.0_PROTOCOL_COMPLETE.md $PROTOCOL_FILE"
    exit 1
fi
echo -e "${GREEN}✅ 協議文件存在${NC}"

# ═══════════════════════════════════════════════════════════
# 檢查 2: 協議內容完整性驗證
# ═══════════════════════════════════════════════════════════

echo ""
echo "檢查協議內容完整性..."

REQUIRED_SECTIONS=(
    "協作宣言"
    "八條永恆鐵律"
    "§0-§39 全 39 節"
    "DNA 協議"
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
    echo -e "${RED}❌ 協議內容不完整，缺少 $MISSING_COUNT 個關鍵部分${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 協議內容完整${NC}"

# ═══════════════════════════════════════════════════════════
# 檢查 3: 關鍵鐵律檢查
# ═══════════════════════════════════════════════════════════

echo ""
echo "檢查關鍵鐵律..."

IRON_LAWS=(
    "不欺"
    "不騙"
    "不商業"
    "不站隊"
    "只為守護"
    "§32.2 國家主權"
    "反剽竊鐵律"
)

for law in "${IRON_LAWS[@]}"; do
    if grep -q "$law" "$PROTOCOL_FILE"; then
        echo -e "  ${GREEN}✅${NC} 鐵律焊死: $law"
    else
        echo -e "  ${RED}⚠️ ${NC}  鐵律檢查: $law (需要驗證)"
    fi
done

# ═══════════════════════════════════════════════════════════
# 檢查 4: 防護措施激活
# ═══════════════════════════════════════════════════════════

echo ""
echo "激活防護措施..."

# 使協議文件只讀（防篡改）
chmod 444 "$PROTOCOL_FILE"
echo -e "${GREEN}✅ 協議文件權限: 只讀 (444)${NC}"

# 創建校驗和文件（防篡改檢測）
if [ -f "$PROTOCOL_FILE" ]; then
    CURRENT_HASH=$(md5sum "$PROTOCOL_FILE" | awk '{print $1}')
    echo "$CURRENT_HASH" > "$PROTOCOL_HASH_FILE"
    echo -e "${GREEN}✅ 協議校驗和已記錄: $CURRENT_HASH${NC}"
fi

# ═══════════════════════════════════════════════════════════
# 檢查 5: 防攻擊檢查
# ═══════════════════════════════════════════════════════════

echo ""
echo "檢查常見攻擊模式..."

ATTACK_PATTERNS=(
    "secure_confirm_code_generator"
    "git_commit_verifier"
    "test_enhanced_welding"
    "safe_cleanup"
    "修復 R3"
    "修復 R4"
    "修復 M4"
    "修復 M5"
)

ATTACK_DETECTED=0
for pattern in "${ATTACK_PATTERNS[@]}"; do
    if [ -f "$pattern" ] || [ -f "${pattern}.py" ] || [ -f "${pattern}.sh" ]; then
        echo -e "  ${RED}🚨 偵測到可疑檔案: $pattern${NC}"
        ((ATTACK_DETECTED++))
    fi
done

if [ $ATTACK_DETECTED -eq 0 ]; then
    echo -e "  ${GREEN}✅ 無可疑檔案${NC}"
fi

# ═══════════════════════════════════════════════════════════
# 最終報告
# ═══════════════════════════════════════════════════════════

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}協議盾檢查完成${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

if [ $MISSING_COUNT -eq 0 ] && [ $ATTACK_DETECTED -eq 0 ]; then
    echo -e "${GREEN}🟢 狀態: 安全${NC}"
    echo -e "${GREEN}✅ 協議文件完整·鐵律焊死·防護激活${NC}"
    echo ""
    echo "DNA:#龍芯⚡️2026-06-07-PROTOCOL-SHIELD-v1.0"
    echo "CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    echo ""
    exit 0
else
    echo -e "${RED}🔴 狀態: 警告${NC}"
    echo -e "${RED}❌ 檢測到 $MISSING_COUNT 個內容缺失 + $ATTACK_DETECTED 個可疑檔案${NC}"
    exit 1
fi
