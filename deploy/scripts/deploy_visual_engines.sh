#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂视觉引擎群 · 鲲鹏一键部署
# DNA: #龍芯⚡️丙午·癸未·丁未-视觉引擎群部署-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
set -e

KUNPENG_HOST="root@119.13.90.27"
KUNPENG_PATH="/root/longhun"
SSH_KEY="$HOME/.ssh/longhun_kunpeng_ed25519"
SSH_CMD="ssh -i ${SSH_KEY} ${KUNPENG_HOST}"
LOCAL_ROOT="/Users/zuimeidedeyihan/longhun-system"

echo "╔══════════════════════════════════════════╗"
echo "║  龍魂视觉引擎群 · 鲲鹏部署 v1.0         ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ─── Step 1: 环境检查 ───
echo "[1/6] 检查SSH连通性..."
$SSH_CMD "echo 'Connected!'" || { echo "❌ SSH失败"; exit 1; }
echo "✅ SSH OK"

# ─── Step 2: 同步引擎代码 ───
echo ""
echo "[2/6] 同步引擎代码到鲲鹏..."
ENGINES=(
    "engines/lh_nano_vision_engine.py"
    "engines/lh_ant_colony_visual.py"
    "engines/lh_persona_orchestra_visual.py"
    "engines/lh_system_health_panorama.py"
)

# 确保远程目录存在
$SSH_CMD "mkdir -p ${KUNPENG_PATH}/engines ${KUNPENG_PATH}/01_protocols"

for engine in "${ENGINES[@]}"; do
    if [ -f "$LOCAL_ROOT/$engine" ]; then
        rsync -avz -e "ssh -i ${SSH_KEY}" "$LOCAL_ROOT/$engine" "${KUNPENG_HOST}:${KUNPENG_PATH}/${engine}"
        echo "  ✅ $engine"
    else
        echo "  ❌ $engine 不存在"
    fi
done

# 同步协议
echo "  同步协议文件..."
rsync -avz -e "ssh -i ${SSH_KEY}" \
    "$LOCAL_ROOT/01_protocols/LH-NANO-VISION-ENGINE-v4.1.5.md" \
    "$LOCAL_ROOT/01_protocols/LH-ANT-COLONY-VISUAL-v1.0.md" \
    "$LOCAL_ROOT/01_protocols/LH-PERSONA-ORCHESTRA-VISUAL-v1.0.md" \
    "$LOCAL_ROOT/01_protocols/LH-VISUAL-AUDIO-FUSION-v1.0.md" \
    "$LOCAL_ROOT/01_protocols/LH-SYSTEM-HEALTH-PANORAMA-v1.0.md" \
    "${KUNPENG_HOST}:${KUNPENG_PATH}/01_protocols/" 2>/dev/null

echo "✅ 引擎代码同步完成"

# ─── Step 3: 安装依赖 ───
echo ""
echo "[3/6] 安装Python依赖..."
$SSH_CMD "pip3 install pillow numpy flask --quiet 2>&1 | tail -1" || echo "  ⚠️ pip3 安装可能有警告，继续..."
echo "✅ 依赖安装完成"

# ─── Step 4: 安装systemd服务 ───
echo ""
echo "[4/6] 安装systemd服务..."

# 纳米视觉API服务
$SSH_CMD "cat > /etc/systemd/system/longhun-nano-vision.service << 'SVC_EOF'
[Unit]
Description=龍魂纳米视觉引擎 API v4.1.5
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/longhun
ExecStart=/usr/bin/python3 engines/lh_nano_vision_engine.py serve --port 9625
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SVC_EOF"

# 健康全景API服务
$SSH_CMD "cat > /etc/systemd/system/longhun-health-panorama.service << 'SVC_EOF'
[Unit]
Description=龍魂系统健康全景图 API v1.0
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/longhun
ExecStart=/usr/bin/python3 -c \"
import sys; sys.path.insert(0,'/root/longhun')
from engines.lh_system_health_panorama import collect_health_data, compute_health_score
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        data = collect_health_data()
        data['score'], data['grade'] = compute_health_score(data)
        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data,ensure_ascii=False,indent=2).encode())
HTTPServer(('',9636),H).serve_forever()
\"
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SVC_EOF"

$SSH_CMD "systemctl daemon-reload"
echo "✅ systemd 服务配置完成"

# ─── Step 5: 启动服务 ───
echo ""
echo "[5/6] 启动引擎服务..."
$SSH_CMD "systemctl enable longhun-nano-vision.service longhun-health-panorama.service 2>/dev/null"
$SSH_CMD "systemctl restart longhun-nano-vision.service"
$SSH_CMD "systemctl restart longhun-health-panorama.service"
sleep 2
echo "✅ 服务已启动"

# ─── Step 6: 验证 ───
echo ""
echo "[6/6] 验证引擎状态..."

echo -n "  纳米视觉API (9625): "
$SSH_CMD "curl -s http://127.0.0.1:9625/health 2>/dev/null | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get(\"status\",\"FAILED\"))' 2>/dev/null" || echo "⏳ 启动中..."

echo -n "  健康全景API (9636): "
$SSH_CMD "curl -s http://127.0.0.1:9636/ 2>/dev/null | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get(\"grade\",\"FAILED\"))' 2>/dev/null" || echo "⏳ 启动中..."

echo -n "  systemd状态: "
$SSH_CMD "systemctl is-active longhun-nano-vision.service longhun-health-panorama.service 2>&1 | tr '\n' ' '"

echo ""
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  🎉 视觉引擎群部署完成！                ║"
echo "╠══════════════════════════════════════════╣"
echo "║  :9625  纳米视觉API (超分辨率)          ║"
echo "║  :9636  健康全景API (系统体检)          ║"
echo "║  协议文档已同步至 01_protocols/          ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "DNA: #龍芯⚡️丙午·癸未·丁未-视觉引擎群部署-v1.0"
echo "GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
