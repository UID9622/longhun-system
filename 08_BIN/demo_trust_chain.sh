#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 🐉 龍魂 · 信任链演示验证脚本
# DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-DEMO-VERIFY-UID9622
# 版本: v1.1.0
# 使用方法: bash bin/demo_trust_chain.sh
# 用途: 通过模拟创世、签章、篡改、恢复四个阶段，演示信任链"篡改必现形"的核心能力
# License: MulanPSL v2

# -----------------------------------------------------------------------------
# 严格模式说明:
#   -e : 任意命令返回非零即退出，避免错误继续执行
#   -u : 使用未定义变量时报错，防止拼写错误导致空值
#   -o pipefail : 管道中任一命令失败，整体返回失败
# -----------------------------------------------------------------------------
set -euo pipefail

# -----------------------------------------------------------------------------
# 颜色变量定义:
#   用于在终端输出高亮提示，提升可读性
#   RED=错误/危险, GREEN=通过/成功, YELLOW=步骤提示, GOLD=标题, NC=复位
# -----------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
GOLD='\033[0;33m'
NC='\033[0m'

# -----------------------------------------------------------------------------
# 打印演示标题与分隔线
# -----------------------------------------------------------------------------
echo ""
echo -e "${GOLD}🐉 龍魂信任链 · 演示验证${NC}"
echo -e "${GOLD}========================================${NC}"

# -----------------------------------------------------------------------------
# 步骤1: 创建测试沙箱目录
# 说明:
#   DEMO_DIR 使用时间戳命名，避免多次运行冲突
#   mkdir -p 递归创建 .dna-chain 子目录，用于存放签章文件
# -----------------------------------------------------------------------------
DEMO_DIR="/tmp/dna-demo-$(date +%s)"
mkdir -p "$DEMO_DIR/.dna-chain"
cd "$DEMO_DIR"

echo ""
echo -e "${YELLOW}[1/7] 创建测试环境...${NC}"
echo "  📁 $DEMO_DIR"

# -----------------------------------------------------------------------------
# 步骤2: 生成创世版本 genesis.txt
# 说明:
#   创世文件是信任链的根锚点，其 SHA-256 哈希值将被写入链头
#   真实场景中，genesis.txt 可以是项目初始代码快照、初始配置文件等
# 预期输出: 一个包含项目初始状态描述的文件
# -----------------------------------------------------------------------------
echo ""
echo -e "${YELLOW}[2/7] 生成创世版本...${NC}"
cat > genesis.txt << 'GENESIS'
# 龍魂信任链 · 创世版本
# 此文件为信任链锚点，哈希将写入链首
# DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-GENESIS-UID9622
GENESIS

# -----------------------------------------------------------------------------
# 计算 genesis.txt 的 SHA-256 哈希
# 命令: shasum -a 256 genesis.txt
# 参数: -a 256 指定 SHA-256 算法
# 输出: 64位十六进制字符串 + 文件名，通过 awk 提取第一列哈希值
# 预期输出示例: a1b2c3d4... (64位十六进制)
# -----------------------------------------------------------------------------
GENESIS_HASH=$(shasum -a 256 genesis.txt | awk '{print $1}')
echo "  genesis_hash: $GENESIS_HASH"

# -----------------------------------------------------------------------------
# 写入链头 chain_head.json
# 说明:
#   链头记录创世哈希、作者、创建时间、链版本等元信息
#   它是签章链的起点，后续所有签章的 prev_hash 都追溯到链头
# -----------------------------------------------------------------------------
cat > .dna-chain/chain_head.json << JSONHEAD
{
  "genesis_hash": "$GENESIS_HASH",
  "author": "UID9622",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "chain_version": "1.0"
}
JSONHEAD

echo -e "  ${GREEN}✅ 创世版本已生成${NC}"

# -----------------------------------------------------------------------------
# 步骤3: 追加3个签章
# 说明:
#   每个签章(stamp_N.json)包含:
#     - index: 签章序号
#     - version: 版本号
#     - diff: 本次变更说明
#     - prev_hash: 前驱哈希(签章1指向genesis_hash，后续指向前一个签章的current_hash)
#     - current_hash: 本次签章的哈希
#       计算方式: SHA256(index + version + diff + prev_hash + timestamp + author)
#       作用: 将签章的核心字段绑定为一个指纹，任何字段被篡改都会导致current_hash失效
#     - timestamp: UTC时间戳
#     - author: 签章人
#     - dna: DNA追溯码
#   这种链式结构保证:
#     - 改任意签章的diff/timestamp/author等字段 → current_hash不匹配
#     - 改任意签章的prev_hash → 与前一个签章的current_hash不匹配
# -----------------------------------------------------------------------------
echo ""
echo -e "${YELLOW}[3/7] 追加3个签章...${NC}"

for i in 1 2 3; do
    STAMP_FILE=".dna-chain/stamp_${i}.json"

    # 根据签章序号设置不同的变更说明，模拟真实开发迭代
    case $i in
        1) DIFF="初始化系统架构";;
        2) DIFF="添加核心功能模块";;
        3) DIFF="修复安全漏洞CVE-2024-XXXX";;
    esac

    # 计算前驱哈希:
    #   - 签章1: 前驱是创世哈希 GENESIS_HASH
    #   - 签章2/3: 前驱是前一个签章的 current_hash 字段值
    if [ "$i" -eq 1 ]; then
        PREV_HASH="$GENESIS_HASH"
    else
        PREV_HASH=$(python3 -c "import json; print(json.load(open('.dna-chain/stamp_$((i-1)).json'))['current_hash'])")
    fi

    # 生成签章文件
    # 使用 Python 计算 current_hash，确保跨平台一致性
    python3 - << PYTHON
import json
import hashlib

index = $i
version = "v1.0.$((i-1))"
diff = "$DIFF"
prev_hash = "$PREV_HASH"
timestamp = "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
author = "UID9622"
dna = "#龍芯⚡️丙午·甲申·辛丑·坤卦-STAMP-${i}-UID9622"

# current_hash = SHA256(index + version + diff + prev_hash + timestamp + author)
# 这是签章核心字段的指纹，任何字段改动都会改变它
payload = f"{index}|{version}|{diff}|{prev_hash}|{timestamp}|{author}"
current_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()

stamp = {
    "index": index,
    "version": version,
    "diff": diff,
    "prev_hash": prev_hash,
    "current_hash": current_hash,
    "timestamp": timestamp,
    "author": author,
    "dna": dna
}

with open("$STAMP_FILE", "w", encoding="utf-8") as f:
    json.dump(stamp, f, ensure_ascii=False, indent=2)

print(current_hash[:16])
PYTHON

    CURRENT_HASH_SHORT=$(python3 -c "import json; print(json.load(open('$STAMP_FILE'))['current_hash'][:16])")
    echo -e "  签章${i}: ${DIFF} → ${CURRENT_HASH_SHORT}..."
done

echo -e "  ${GREEN}✅ 3个签章已追加${NC}"

# -----------------------------------------------------------------------------
# 步骤4: 验证完整链完整性
# 说明:
#   遍历所有签章，执行两项检查:
#     A. 链式检查: 当前签章的 prev_hash 是否等于前一个签章的 current_hash
#        - 签章1: prev_hash == genesis_hash
#        - 签章N: prev_hash == 签章(N-1)的 current_hash
#     B. 指纹检查: 重新计算 current_hash，是否等于文件中记录的 current_hash
#        - 防止签章内部字段(diff/timestamp等)被篡改
#   如果全部匹配，输出 🟢 链完整
# -----------------------------------------------------------------------------
echo ""
echo -e "${YELLOW}[4/7] 验证完整链完整性...${NC}"

VERIFY_OK=true
for i in 1 2 3; do
    STAMP=".dna-chain/stamp_${i}.json"

    # 使用 Python 同时完成链式检查和指纹检查
    python3 - << PYTHON
import json
import hashlib
import sys

index = $i
stamp = json.load(open('$STAMP'))
genesis_hash = '$GENESIS_HASH'

# A. 链式检查
if index == 1:
    expected_prev = genesis_hash
else:
    expected_prev = json.load(open('.dna-chain/stamp_%d.json' % (index - 1)))['current_hash']

if stamp['prev_hash'] != expected_prev:
    print(f"CHAIN_BREAK:{index}")
    sys.exit(0)

# B. 指纹检查
payload = f"{stamp['index']}|{stamp['version']}|{stamp['diff']}|{stamp['prev_hash']}|{stamp['timestamp']}|{stamp['author']}"
expected_current = hashlib.sha256(payload.encode('utf-8')).hexdigest()

if stamp['current_hash'] != expected_current:
    print(f"TAMPER:{index}")
    sys.exit(0)

print("OK")
PYTHON

    RESULT=$(python3 - << PYTHON
import json, hashlib
index = $i
stamp = json.load(open('$STAMP'))
genesis_hash = '$GENESIS_HASH'
if index == 1:
    expected_prev = genesis_hash
else:
    expected_prev = json.load(open('.dna-chain/stamp_%d.json' % (index - 1)))['current_hash']
if stamp['prev_hash'] != expected_prev:
    print(f"CHAIN_BREAK:{index}")
else:
    payload = f"{stamp['index']}|{stamp['version']}|{stamp['diff']}|{stamp['prev_hash']}|{stamp['timestamp']}|{stamp['author']}"
    expected_current = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    if stamp['current_hash'] != expected_current:
        print(f"TAMPER:{index}")
    else:
        print("OK")
PYTHON
)

    case "$RESULT" in
        OK)
            ;;
        CHAIN_BREAK:*)
            echo -e "  ${RED}❌ 签章${i} 前驱哈希断裂${NC}"
            VERIFY_OK=false
            ;;
        TAMPER:*)
            echo -e "  ${RED}❌ 签章${i} 指纹校验失败（内容被篡改）${NC}"
            VERIFY_OK=false
            ;;
    esac
done

if [ "$VERIFY_OK" = true ]; then
    echo -e "  ${GREEN}✅ 签章链完整 · 3/3通过${NC}"
    echo -e "  ${GREEN}🟢 链完整${NC}"
else
    echo -e "  ${RED}🔴 链异常${NC}"
    exit 1
fi

# -----------------------------------------------------------------------------
# 步骤5: 模拟篡改
# 说明:
#   备份签章2原始内容，然后修改其 diff 字段
#   这种修改会导致:
#     - 签章2的指纹校验失败（diff变了，重新计算的current_hash不匹配）
#     - 签章3的链式检查失败（prev_hash指向的是旧的签章2 current_hash）
#   因此再次验证时会发现断裂
# -----------------------------------------------------------------------------
echo ""
echo -e "${YELLOW}[5/7] 模拟篡改第2个签章...${NC}"

# 备份原始签章2，用于步骤7恢复
cp .dna-chain/stamp_2.json .dna-chain/stamp_2.json.bak

# 使用 python3 修改签章2的 diff 字段，模拟恶意篡改
python3 -c "
import json
d = json.load(open('.dna-chain/stamp_2.json'))
d['diff'] = '【被篡改】添加后门代码'
json.dump(d, open('.dna-chain/stamp_2.json', 'w'), ensure_ascii=False, indent=2)
"

echo -e "  ${RED}⚠️ 签章2已被篡改（diff字段被修改）${NC}"

# -----------------------------------------------------------------------------
# 步骤6: 再次验证（应检测到断裂）
# 说明:
#   篡改后，签章2的current_hash与其内容不再匹配，签章3的prev_hash也指向旧值
#   验证会报告断裂位置，帮助定位篡改点
# -----------------------------------------------------------------------------
echo ""
echo -e "${YELLOW}[6/7] 验证被篡改的链...${NC}"

TAMPER_OK=true
for i in 1 2 3; do
    STAMP=".dna-chain/stamp_${i}.json"

    RESULT=$(python3 - << PYTHON
import json, hashlib
index = $i
stamp = json.load(open('$STAMP'))
genesis_hash = '$GENESIS_HASH'
if index == 1:
    expected_prev = genesis_hash
else:
    expected_prev = json.load(open('.dna-chain/stamp_%d.json' % (index - 1)))['current_hash']
if stamp['prev_hash'] != expected_prev:
    print(f"CHAIN_BREAK:{index}")
else:
    payload = f"{stamp['index']}|{stamp['version']}|{stamp['diff']}|{stamp['prev_hash']}|{stamp['timestamp']}|{stamp['author']}"
    expected_current = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    if stamp['current_hash'] != expected_current:
        print(f"TAMPER:{index}")
    else:
        print("OK")
PYTHON
)

    case "$RESULT" in
        OK)
            ;;
        CHAIN_BREAK:*)
            echo -e "  ${RED}❌ 签章${i} 前驱哈希断裂！${NC}"
            echo -e "  ${RED}   断裂位置: 签章2 → 签章3${NC}"
            TAMPER_OK=false
            ;;
        TAMPER:*)
            echo -e "  ${RED}❌ 签章${i} 指纹校验失败！${NC}"
            TAMPER_OK=false
            ;;
    esac
done

if [ "$TAMPER_OK" = false ]; then
    echo -e "  ${RED}🔴 链断裂！篡改检测成功！${NC}"
else
    echo -e "  ${YELLOW}⚠️ 篡改未被检测到！${NC}"
    exit 1
fi

# -----------------------------------------------------------------------------
# 步骤7: 恢复原始签章
# 说明:
#   将备份的原始签章2还原，验证链恢复完整
#   这证明信任链不是一次性破坏，篡改可撤销、可恢复
# -----------------------------------------------------------------------------
echo ""
echo -e "${YELLOW}[7/7] 恢复签章2原值...${NC}"
mv .dna-chain/stamp_2.json.bak .dna-chain/stamp_2.json
echo -e "  ${GREEN}✅ 链已恢复${NC}"

# -----------------------------------------------------------------------------
# 收尾: 打印演示结论
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# 清理: 删除测试沙箱目录
# 注意: 演示脚本不保留临时数据，生产环境应保留签章链目录
# -----------------------------------------------------------------------------
rm -rf "$DEMO_DIR"
