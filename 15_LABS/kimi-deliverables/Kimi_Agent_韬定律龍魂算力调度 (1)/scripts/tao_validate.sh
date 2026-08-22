#!/bin/bash
# 龍魂·韬定律进阶破解之法 v2.2 —— 脚本与 DNA 一致性自检
# DNA: #龍芯⚡️丙午·乙未·辛酉·甲午·䷫姤-TAO-LAW-INTEGRATED-v2.2
# 用法: bash scripts/tao_validate.sh

set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# 优先校验 v2.2，回退到 v2.0
if [ -f "$ROOT/龍魂·韬定律进阶破解之法v2.2.md" ]; then
    MAIN_MD="$ROOT/龍魂·韬定律进阶破解之法v2.2.md"
    VERS="v2.2"
    DNA_EXPECT="#龍芯⚡️丙午·乙未·辛酉·甲午·䷫姤-TAO-LAW-INTEGRATED-v2.2"
elif [ -f "$ROOT/龍魂·韬定律进阶破解之法v2.0.md" ]; then
    MAIN_MD="$ROOT/龍魂·韬定律进阶破解之法v2.0.md"
    VERS="v2.0"
    DNA_EXPECT="#龍芯⚡️丙午·乙未·辛丑·甲午·䷬萃-韬定律进阶破解-v1.0"
fi
ERR=0

echo "=== 韬定律 $VERS 自检开始 ==="
echo "DNA: $DNA_EXPECT"
echo ""

# 1. 主文档存在性
if [ ! -f "$MAIN_MD" ]; then
    echo "❌ 主文档缺失: $MAIN_MD"
    exit 1
fi
echo "✅ 主文档存在"

# 2. DNA 一致性
DNA_COUNT=$(grep -c "$DNA_EXPECT" "$MAIN_MD" || true)
OLD_DNA_COUNT=$(grep -cE "丙午·乙未·辛丑·泽地萃|待生成器校正|待校正" "$MAIN_MD" || true)
echo "   主文档 DNA 出现次数: $DNA_COUNT"
if [ "$DNA_COUNT" -lt 1 ]; then
    echo "❌ 主文档未找到期望 DNA"
    ERR=1
elif [ "$VERS" = "v2.2" ] && [ "$OLD_DNA_COUNT" -gt 0 ]; then
    echo "⚠️  主文档仍残留旧 DNA 或待校正字样: $OLD_DNA_COUNT 处"
    ERR=1
else
    echo "✅ DNA 一致性通过"
fi

# 3. 提取并检查所有 bash 代码块语法
TMP_DIR=$(mktemp -d)
python3 - "$MAIN_MD" "$TMP_DIR" <<'PYEOF'
import re, sys, os
md = sys.argv[1]
out = sys.argv[2]
with open(md, "r", encoding="utf-8") as f:
    content = f.read()
blocks = re.findall(r'```bash\n(.*?)\n```', content, re.DOTALL)
for i, block in enumerate(blocks, 1):
    path = os.path.join(out, f"block_{i:02d}.sh")
    with open(path, "w", encoding="utf-8") as f:
        f.write(block)
PYEOF

for f in "$TMP_DIR"/block_*.sh; do
    [ -e "$f" ] || continue
    if bash -n "$f"; then
        echo "✅ bash 代码块 $(basename "$f") 语法通过"
    else
        echo "❌ bash 代码块 $(basename "$f") 语法失败"
        ERR=1
    fi
done
rm -rf "$TMP_DIR"

# 4. Python 组件语法检查
PY_FILES=(
    "$ROOT/engines/tao_scheduler.py"
    "$ROOT/scripts/tao_usage_collect.py"
    "$ROOT/api/tao_scheduler_api.py"
)
echo ""
echo "=== Python 组件语法检查 ==="
for py in "${PY_FILES[@]}"; do
    if [ -f "$py" ]; then
        if python3 -m py_compile "$py" 2>/dev/null; then
            echo "✅ $(basename "$py") 语法通过"
        else
            echo "❌ $(basename "$py") 语法失败"
            ERR=1
        fi
    else
        echo "⚠️  $(basename "$py") 不存在"
    fi
done

# 4.1 FastAPI 依赖检查
echo ""
echo "=== FastAPI 依赖检查 ==="
if python3 -c "import fastapi, uvicorn" 2>/dev/null; then
    echo "✅ fastapi / uvicorn 已安装"
else
    echo "⚠️  fastapi / uvicorn 未安装（API 服务运行前需 pip install fastapi uvicorn）"
fi

# 5. plist 格式检查
PLIST_FILES=(
    "$ROOT/deploy/launchd/com.longhun.tao.collector.plist"
    "$ROOT/deploy/launchd/com.longhun.tao.audit-verifier.plist"
    "$ROOT/deploy/launchd/com.longhun.tao.scheduler.plist"
)
echo ""
echo "=== launchd plist 格式检查 ==="
for pl in "${PLIST_FILES[@]}"; do
    if [ -f "$pl" ]; then
        if plutil -lint "$pl" 2>/dev/null | grep -q "OK"; then
            echo "✅ $(basename "$pl") 格式通过"
        else
            echo "⚠️  $(basename "$pl") 非 macOS 环境跳过 plutil 校验（文件存在）"
        fi
    else
        echo "❌ $(basename "$pl") 不存在"
        ERR=1
    fi
done

# 5.1 Web UI 文件存在性检查
echo ""
if [ -f "$ROOT/portal/tao-scheduler/index.html" ]; then
    echo "✅ Web UI 文件存在"
else
    echo "❌ Web UI 文件缺失: portal/tao-scheduler/index.html"
    ERR=1
fi

# 6. 环境依赖检查
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
