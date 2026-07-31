#!/bin/bash
# 龍魂·韬定律进阶破解之法 v2.1 —— 脚本与 DNA 一致性自检
# DNA: #龍芯⚡️丙午·乙未·辛酉·屯-TAO-LAW-CRACK-v2.1
# 用法: bash scripts/tao_validate.sh

set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# 优先校验 v2.1，回退到 v2.0
if [ -f "$ROOT/龍魂·韬定律进阶破解之法v2.1.md" ]; then
    MAIN_MD="$ROOT/龍魂·韬定律进阶破解之法v2.1.md"
elif [ -f "$ROOT/龍魂·韬定律进阶破解之法v2.0.md" ]; then
    MAIN_MD="$ROOT/龍魂·韬定律进阶破解之法v2.0.md"
fi
DNA_EXPECT="#龍芯⚡️丙午·乙未·辛酉·屯-TAO-LAW-CRACK-v2.1"
ERR=0

echo "=== 韬定律 v2.1 自检开始 ==="
echo "DNA: $DNA_EXPECT"
echo ""

# 1. 主文档存在性
if [ ! -f "$MAIN_MD" ]; then
    echo "❌ 主文档缺失: $MAIN_MD"
    exit 1
fi
echo "✅ 主文档存在"

# 2. DNA 一致性：主文档内所有 DNA 出现次数应相同
DNA_COUNT=$(grep -c "$DNA_EXPECT" "$MAIN_MD" || true)
OLD_DNA_COUNT=$(grep -cE "丙午·乙未·辛丑·泽地萃|待生成器校正|待校正" "$MAIN_MD" || true)
echo "   主文档 DNA 出现次数: $DNA_COUNT"
if [ "$DNA_COUNT" -lt 1 ]; then
    echo "❌ 主文档未找到期望 DNA"
    ERR=1
elif [ "$OLD_DNA_COUNT" -gt 0 ]; then
    echo "⚠️  主文档仍残留旧 DNA 或待校正字样: $OLD_DNA_COUNT 处"
    ERR=1
else
    echo "✅ DNA 一致性通过"
fi

# 3. tao_route.sh 语法检查（从主文档提取）
TMP_ROUTE=$(mktemp)
grep -A 40 "# 龍魂韬定律路由脚本" "$MAIN_MD" | sed -n '/```bash/,/```/p' | sed '1d;$d' > "$TMP_ROUTE"
if bash -n "$TMP_ROUTE"; then
    echo "✅ tao_route.sh 语法通过"
else
    echo "❌ tao_route.sh 语法失败"
    ERR=1
fi
rm -f "$TMP_ROUTE"

# 4. 用量采集脚本语法检查
grep -A 20 "# 采集 用量" "$MAIN_MD" > /dev/null
TMP_USAGE=$(mktemp)
grep -A 20 "# 采集 用量" "$MAIN_MD" | sed -n '/```bash/,/```/p' | sed '1d;$d' > "$TMP_USAGE"
if bash -n "$TMP_USAGE"; then
    echo "✅ 用量采集脚本语法通过"
else
    echo "❌ 用量采集脚本语法失败"
    ERR=1
fi
rm -f "$TMP_USAGE"

# 5. 环境依赖检查
echo ""
echo "=== 环境依赖检查（仅供参考，非强制）==="
if command -v ollama >/dev/null 2>&1; then
    echo "✅ ollama 已安装"
else
    echo "⚠️  ollama 未安装（部署前需安装）"
fi

if command -v npu-smi >/dev/null 2>&1; then
    echo "✅ npu-smi 已安装"
else
    echo "⚠️  npu-smi 未安装（昇腾驱动未就绪）"
fi

if [ -d /sys/fs/cgroup/cpu ]; then
    echo "ℹ️  cgroup v1 控制器存在"
elif [ -f /sys/fs/cgroup/cgroup.controllers ]; then
    echo "ℹ️  cgroup v2 统一层级存在（请按 v2 语法调整配额命令）"
else
    echo "⚠️  未检测到 cgroup 层级信息"
fi

echo ""
if [ "$ERR" -eq 0 ]; then
    echo "=== ✅ 全部自检通过 ==="
    exit 0
else
    echo "=== ❌ 自检发现异常 ==="
    exit 1
fi
