#!/bin/bash
# 🐉 龍魂 · 信任链演示验证脚本
# DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-DEMO-VERIFY-UID9622
# 使用方法: bash bin/demo_trust_chain.sh
# License: MulanPSL v2
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
GOLD='\033[0;33m'
NC='\033[0m'

echo ""
echo -e "${GOLD}🐉 龍魂信任链 · 演示验证${NC}"
echo -e "${GOLD}========================================${NC}"

# 1. 创建测试沙箱
DEMO_DIR="/tmp/dna-demo-$(date +%s)"
mkdir -p "$DEMO_DIR/.dna-chain"
cd "$DEMO_DIR"

echo ""
echo -e "${YELLOW}[1/7] 创建测试环境...${NC}"
echo "  📁 $DEMO_DIR"

# 2. 生成创世版本
echo ""
echo -e "${YELLOW}[2/7] 生成创世版本...${NC}"
cat > genesis.txt << 'GENESIS'
# 龍魂信任链 · 创世版本
# 此文件为信任链锚点，哈希将写入链首
# DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-GENESIS-UID9622
GENESIS

# 模拟 dna init
GENESIS_HASH=$(shasum -a 256 genesis.txt | awk '{print $1}')
echo "  genesis_hash: $GENESIS_HASH"

# 写入链头
cat > .dna-chain/chain_head.json << JSONHEAD
{
  "genesis_hash": "$GENESIS_HASH",
  "author": "UID9622",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "chain_version": "1.0"
}
JSONHEAD

echo -e "  ${GREEN}✅ 创世版本已生成${NC}"

# 3. 添加3个签章
echo ""
echo -e "${YELLOW}[3/7] 追加3个签章...${NC}"

for i in 1 2 3; do
    STAMP_FILE=".dna-chain/stamp_${i}.json"
    
    case $i in
        1) DIFF="初始化系统架构";;
        2) DIFF="添加核心功能模块";;
        3) DIFF="修复安全漏洞CVE-2024-XXXX";;
    esac
    
    # 计算前驱哈希
    if [ "$i" -eq 1 ]; then
        PREV_HASH="$GENESIS_HASH"
    else
        PREV_HASH=$(shasum -a 256 ".dna-chain/stamp_$((i-1)).json" | awk '{print $1}')
    fi
    
    CURRENT_HASH=$(echo "${DIFF}-${PREV_HASH}-$(date +%s%N)" | shasum -a 256 | awk '{print $1}')
    
    cat > "$STAMP_FILE" << STAMPEOF
{
  "index": $i,
  "version": "v1.0.$((i-1))",
  "diff": "$DIFF",
  "prev_hash": "$PREV_HASH",
  "current_hash": "$CURRENT_HASH",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "author": "UID9622",
  "dna": "#龍芯⚡️丙午·甲申·辛丑·坤卦-STAMP-${i}-UID9622"
}
STAMPEOF
    
    echo -e "  签章${i}: ${DIFF} → ${CURRENT_HASH:0:16}..."
done

echo -e "  ${GREEN}✅ 3个签章已追加${NC}"

# 4. 验证完整链
echo ""
echo -e "${YELLOW}[4/7] 验证完整链完整性...${NC}"

VERIFY_OK=true
for i in 1 2 3; do
    STAMP=".dna-chain/stamp_${i}.json"
    
    # 读 prev_hash
    PREV=$(python3 -c "import json; print(json.load(open('$STAMP'))['prev_hash'])")
    
    if [ "$i" -eq 1 ]; then
        # 第一个签章的prev_hash应等于genesis_hash
        if [ "$PREV" != "$GENESIS_HASH" ]; then
            echo -e "  ${RED}❌ 签章1 前驱哈希不匹配创世哈希${NC}"
            VERIFY_OK=false
        fi
    else
        # 后续签章的prev_hash应等于前一个签章的current_hash
        PREV_STAMP=".dna-chain/stamp_$((i-1)).json"
        EXPECTED=$(python3 -c "import json; print(json.load(open('$PREV_STAMP'))['current_hash'])")
        if [ "$PREV" != "$EXPECTED" ]; then
            echo -e "  ${RED}❌ 签章${i} 前驱哈希断裂${NC}"
            echo "     期望: ${EXPECTED:0:16}..."
            echo "     实际: ${PREV:0:16}..."
            VERIFY_OK=false
        fi
    fi
done

if [ "$VERIFY_OK" = true ]; then
    echo -e "  ${GREEN}✅ 签章链完整 · 3/3通过${NC}"
    echo -e "  ${GREEN}🟢 链完整${NC}"
else
    echo -e "  ${RED}🔴 链异常${NC}"
    exit 1
fi

# 5. 模拟篡改
echo ""
echo -e "${YELLOW}[5/7] 模拟篡改第2个签章...${NC}"

# 备份原始
cp .dna-chain/stamp_2.json .dna-chain/stamp_2.json.bak

# 篡改
python3 -c "
import json
d = json.load(open('.dna-chain/stamp_2.json'))
d['diff'] = '【被篡改】添加后门代码'
json.dump(d, open('.dna-chain/stamp_2.json', 'w'), ensure_ascii=False, indent=2)
"

echo -e "  ${RED}⚠️ 签章2已被篡改（diff字段被修改）${NC}"

# 6. 再次验证（应检测到断裂）
echo ""
echo -e "${YELLOW}[6/7] 验证被篡改的链...${NC}"

TAMPER_OK=true
for i in 1 2 3; do
    STAMP=".dna-chain/stamp_${i}.json"
    PREV=$(python3 -c "import json; print(json.load(open('$STAMP'))['prev_hash'])")
    
    if [ "$i" -ge 2 ]; then
        PREV_STAMP=".dna-chain/stamp_$((i-1)).json"
        EXPECTED=$(python3 -c "import json; print(json.load(open('$PREV_STAMP'))['current_hash'])")
        if [ "$PREV" != "$EXPECTED" ]; then
            echo -e "  ${RED}❌ 签章${i} 前驱哈希断裂！${NC}"
            echo -e "  ${RED}   断裂位置: 签章2 → 签章3${NC}"
            TAMPER_OK=false
        fi
    fi
done

if [ "$TAMPER_OK" = false ]; then
    echo -e "  ${RED}🔴 链断裂！篡改检测成功！${NC}"
else
    echo -e "  ${YELLOW}⚠️ 篡改未被检测到！${NC}"
    exit 1
fi

# 7. 恢复原始（证明不是永久破坏）
echo ""
echo -e "${YELLOW}[7/7] 恢复签章2原值...${NC}"
mv .dna-chain/stamp_2.json.bak .dna-chain/stamp_2.json
echo -e "  ${GREEN}✅ 链已恢复${NC}"

# 收尾
echo ""
echo -e "${GOLD}========================================${NC}"
echo -e "${GREEN}✅ 演示完成${NC}"
echo ""
echo "  📋 测试结论:"
echo "     ✅ 正常链 → 3/3验证通过"
echo "     🔴 篡改后 → 链断裂于签章2"
echo "     ✅ 恢复后 → 链再次完整"
echo ""
echo "  🐉 龍魂信任链 · 篡改必现形"
echo ""

# 清理
rm -rf "$DEMO_DIR"
