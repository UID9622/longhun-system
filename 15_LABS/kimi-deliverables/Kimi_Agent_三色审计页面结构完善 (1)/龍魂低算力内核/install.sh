# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-1e142e62
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# 🐉 longhun-core v1.0.0 一键安装
# 治大国若烹小鲜 ——《道德经》第60章
set -e
echo "🐉 龍魂低算力内核安装"
python3 --version || { echo "❌ 需要 Python ≥3.11"; exit 1; }
DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir -p ~/.longhun/bin
cp -r "$DIR/core/longhun_core" ~/.longhun/
cp "$DIR/lh" ~/.longhun/bin/lh
chmod +x ~/.longhun/bin/lh
grep -q 'longhun/bin' ~/.bashrc 2>/dev/null || echo 'export PATH="$HOME/.longhun/bin:$PATH"' >> ~/.bashrc
export PATH="$HOME/.longhun/bin:$PATH"
python3 ~/.longhun/bin/lh selftest && echo "✅ 安装完成 · 三色🟢" || { echo "❌ 自测失败"; exit 1; }
