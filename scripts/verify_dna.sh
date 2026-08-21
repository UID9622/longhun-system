#!/bin/bash
# 🐉 DNA引擎一键验证脚本
# DNA: #龍芯⚡️2026-08-21-VERIFY-v1.0

echo "=============================================="
echo "  🐉 DNA引擎 · 集成验证 v1.0"
echo "==============================================" 

cd ~/longhun-system || exit 1

# 1. 自测核心引擎
echo ""
echo "[1/4] 核心引擎自测..."
python3 bin/lh_dna_ref_impl.py --selftest
if [ $? -ne 0 ]; then
    echo "❌ 核心引擎自测失败"
    exit 1
fi

# 2. 测试DNA助手
echo ""
echo "[2/4] DNA助手测试..."
python3 -c "
from dna_helper import make_dna, append_with_dna
dna = make_dna('验证测试', 'system', 'verify')
print(f'  生成DNA: {dna}')
append_with_dna('✅ DNA引擎集成验证通过', source='test', category='system', action='验证')
print('  ✅ MEMORY写入成功')
"

# 3. 检查MEMORY.md
echo ""
echo "[3/4] MEMORY.md 检查..."
if [ -f MEMORY.md ]; then
    LINES=$(wc -l < MEMORY.md 2>/dev/null || echo 0)
    echo "  ✅ MEMORY.md 存在 ($LINES 行)"
    echo "  最近3条:"
    tail -n 12 MEMORY.md | head -n 8 | sed 's/^/    /'
else
    echo "  ⚠️ MEMORY.md 尚未生成（首次运行会自动创建）"
fi

# 4. 测试视觉（可选）
echo ""
echo "[4/4] 视觉模块检查..."
if command -v ollama &> /dev/null; then
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        MODEL=$(ollama list | grep moondream | awk '{print $1}' || echo 'moondream未拉取')
        echo "  ✅ Ollama 运行中 (模型: $MODEL)"
    else
        echo "  ⚠️ Ollama 未运行，视觉功能不可用"
        echo "    启动: ollama serve"
    fi
else
    echo "  ⚠️ Ollama 未安装，视觉功能不可用"
fi

echo ""
echo "=============================================="
echo "  ✅ 验证完成"
echo "  DNA: #龍芯⚡️2026-08-21-VERIFY-DONE"
echo "=============================================="
