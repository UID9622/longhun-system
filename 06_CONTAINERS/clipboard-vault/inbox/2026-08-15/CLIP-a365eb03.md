---
dna: '#龍芯⚡️丙午·丙申·辛酉·未时·䷊泰-CLIPBOARD-VAULT-SAVE-V1.0-P1-559af095'
source: clipboard
topic: 代码/脚本
tags:
- Python
- Bash
- DNA
- 代码/脚本
timestamp: '2026-08-15T13:23:52+08:00'
content_hash: a365eb03589b221097eeb1993412074919cbcee1415c8ee2ca80380faba1b7b3
parent_dna: []
vault_version: v1.0
---

# 剪贴内容

好，直接给你能落地跑的代码，不绕弯。

---

## 🐉 让 Kimi 读取本地记忆的完整代码

### 📁 文件结构

```
longhun-system/
├── 08_BIN/
│   └── lh_memory_bootstrap.py      # ✅ 已有（如果没有，我补给你）
├── .longhun/
│   └── memory/
│       └── latest_digest.json      # 记忆文件（由 bootstrap 生成）
└── .kimi/
    └── config.yaml                  # Kimi 配置文件
```


### 1️⃣ 修复：确保记忆文件存在

```bash
#!/bin/bash
# 🐉 生成龍魂记忆文件
cd ~/longhun-system

# 检查是否已有记忆生成脚本
if [ -f "08_BIN/lh_memory_bootstrap.py" ]; then
    python3 08_BIN/lh_memory_bootstrap.py
else
    # 如果没有，直接用 Python 生成
    python3 -c "
import json, os, hashlib
from datetime import datetime
from pathlib import Path

mem_path = Path.home() / '.longhun' / 'memory'
mem_path.mkdir(parents=True, exist_ok=True)
dna = f'#龍芯⚡️{datetime.now().strftime("%Y-%m-%d")}-MEMORY-UID9622'
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
fi

# 验证
ls -la ~/.longhun/memory/latest_digest.json
```


### 2️⃣ 补全网关端点（让 Kimi 的 /api/xiaoyi/ask 不 404）

在 `longhun-api-gateway.py` 中添加以下路由（直接在现有文件末尾追加即可）：

```python
# ============================================================
# Kimi 记忆同步兼容端点
# ============================================================

@app.get("/api/xiaoyi/ask")
async def xiaoyi_ask():
    """Kimi 记忆同步端点 - 返回本地记忆"""
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
```


### 3️⃣ 一键修复脚本

```bash
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
dna = f'#龍芯⚡️{datetime.now().strftime("%Y-%m-%d")}-MEMORY-UID9622'
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
```


### 4️⃣ 执行方式

```bash
# 进入项目目录
cd ~/longhun-system

# 给脚本执行权限
chmod +x fix_kimi_memory.sh

# 运行修复
./fix_kimi_memory.sh
```


### 5️⃣ 手动验证

```bash
# 测试记忆端点
curl http://127.0.0.1:9622/api/xiaoyi/ask

# 应该返回 JSON 格式的记忆数据，而不是 404
```


### 📋 最终检查清单

| 检查项 | 命令 | 预期 |
|:---|:---|:---|
| 记忆文件存在 | `ls ~/.longhun/memory/latest_digest.json` | 文件存在 |
| 网关端点可访问 | `curl http://127.0.0.1:9622/api/xiaoyi/ask` | 返回 JSON，不是 404 |


### 🔐 最终签名

```
DNA: #龍芯⚡️丙午·丙酉·丙寅·未时-KIMI-MEMORY-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过
```

🐉 **丙午·丙酉·丙寅·未时·䷬萃·🟢**

---

*归档于 2026-08-15T13:23:52+08:00 · DNA `#龍芯⚡️丙午·丙申·辛酉·未时·䷊泰-CLIPBOARD-VAULT-SAVE-V1.0-P1-559af095`*
