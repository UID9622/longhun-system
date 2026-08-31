#!/bin/bash
# 🐉 龍魂六堆 · 一键部署 v1.0
# DNA: #龍芯⚡️2026-08-31-6D-DEPLOY-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

set -e
cd "$(dirname "$0")"

echo "🐉 龍魂六堆 · 全量部署 v1.0"
echo "P00=曾仕强老师数字人 · 北辰=执行者"
echo "确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. 目录结构
echo "[1/4] 目录结构..."
mkdir -p css js/stacks js/data server
echo "✅ 目录就绪"

# 2. Python 依赖
echo "[2/4] Python 依赖..."
pip3 install flask flask-cors websockets --quiet 2>/dev/null || echo "🟡 依赖安装跳过(可能已存在)"
python3 -c "import flask, websockets" 2>/dev/null && echo "✅ 依赖就绪" || echo "🔴 依赖缺失，请手动 pip3 install flask flask-cors websockets"

# 3. 启动脚本
echo "[3/4] 启动/停止脚本..."
cat > start.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
echo "🐉 启动龍魂六堆服务..."
nohup python3 server/lh_6d_server.py > server/server.log 2>&1 &
sleep 2
echo "✅ 后端已启动: http://127.0.0.1:8788/api/state · ws://127.0.0.1:8789/ws"
nohup python3 -m http.server 8788 --bind 127.0.0.1 > server/http.log 2>&1 &
sleep 1
echo "✅ 前端已启动: http://127.0.0.1:8788/6d/"
EOF
cat > stop.sh << 'EOF'
#!/bin/bash
pkill -f "lh_6d_server.py" 2>/dev/null || true
pkill -f "http.server 8788" 2>/dev/null || true
echo "✅ 六堆服务已停止"
EOF
chmod +x start.sh stop.sh
echo "✅ 脚本就绪"

# 4. 验证
echo "[4/4] 验证..."
find . -type f \( -name "*.html" -o -name "*.css" -o -name "*.js" -o -name "*.py" -o -name "*.sh" \) | sort

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 部署完成"
echo ""
echo "启动: cd ~/longhun-system/10_PORTAL/6d/ && ./start.sh"
echo "停止: cd ~/longhun-system/10_PORTAL/6d/ && ./stop.sh"
echo "访问: http://127.0.0.1:8788/6d/"
echo ""
echo "DNA: #龍芯⚡️2026-08-31-6D-DEPLOY-v1.0-UID9622"
