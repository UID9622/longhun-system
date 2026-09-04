# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·甲子·甲戌·䷍大有-CODE-补DNA-f1a1ec26
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# 🐉 龍魂记忆修复脚本
# 执行方式: ./fix_kimi_memory.sh

echo "🐉 修复 Kimi 记忆同步..."

# 1. 确保记忆文件存在
echo "📁 检查记忆文件..."
cd ~/longhun-system
python3 08_BIN/lh_memory_bootstrap.py 2>/dev/null || python3 -c "
import json, os, hashlib
from datetime import datetime
from pathlib import Path
mem_path = Path.home() / '.longhun' / 'memory'
mem_path.mkdir(parents=True, exist_ok=True)
dna = f'#龍芯⚡️{datetime.now().strftime(\"%Y-%m-%d\")}-MEMORY-UID9622'
data = {
    'dna': dna,
    'digest': '龍魂系统记忆已初始化',
    'timestamp': datetime.now().isoformat(),
    'source': 'bootstrap'
}
with open(mem_path / 'latest_digest.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('✅ 记忆文件已生成')
"

# 2. 补全网关端点（如果网关文件存在）
if [ -f "08_BIN/longhun-api-gateway.py" ]; then
    # 检查是否已存在 /api/xiaoyi/ask 路由
    if ! grep -q "/api/xiaoyi/ask" "08_BIN/longhun-api-gateway.py"; then
        echo "🔧 补全网关端点..."
        cat >> "08_BIN/longhun-api-gateway.py" << 'EOF'

# ============================================================
# Kimi 记忆同步兼容端点
# ============================================================

@app.get("/api/xiaoyi/ask")
async def xiaoyi_ask():
    """Kimi 记忆同步端点 - 返回本地记忆"""
    from pathlib import Path
    import json
    mem_path = Path.home() / ".longhun" / "memory" / "latest_digest.json"
    if mem_path.exists():
        with open(mem_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "status": "empty",
        "dna": generate_dna(),
        "digest": "暂无记忆数据",
        "timestamp": datetime.now().isoformat()
    }
EOF
        echo "✅ 网关端点已补全"
    else
        echo "✅ 网关端点已存在"
    fi
else
    echo "⚠️ 未找到 longhun-api-gateway.py，请手动创建或忽略"
fi

# 3. 重启网关服务
echo "🔄 重启网关服务..."
pkill -f "longhun-api-gateway.py" 2>/dev/null
cd ~/longhun-system
nohup python3 08_BIN/longhun-api-gateway.py > /dev/null 2>&1 &
sleep 2

# 4. 测试
echo "🧪 测试记忆端点..."
curl -s http://127.0.0.1:9622/api/xiaoyi/ask | head -20

echo ""
echo "✅ 修复完成！现在 kimi 可以读取记忆了。"
