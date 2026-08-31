#!/bin/bash
# 🐉 龍魂 K线 系统 · 一键部署 v1.0
# DNA: #龍芯⚡️2026-08-31-KLINE-DEPLOY-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622） 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2
# 功能: 本地启动 / 鲲鹏部署（rsync + systemd + nginx 反代）
# 用法:
#   bash deploy/deploy_kline.sh local     # 本地启动（macOS，后台守护）
#   bash deploy/deploy_kline.sh kunpeng   # 部署鲲鹏 119.13.90.27
#   bash deploy/deploy_kline.sh stop      # 停止
set -e

LONGHUN_ROOT=~/longhun-system
REMOTE="root@119.13.90.27"
REMOTE_DIR="/opt/longhun-system"
SSH_KEY="$HOME/.ssh/longhun_kunpeng_ed25519"
# 端口：8899 被 docker-proxy 占用（鲲鹏），kline 专用 8895 REST / 8894 WS
KLINE_PORT="${KLINE_PORT:-8895}"
KLINE_WS_PORT="${KLINE_WS_PORT:-8894}"

echo "🐉 龍魂 K线 系统部署"
echo "确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

local_start() {
  echo "[本地] 启动 K线 服务 (8899 REST / 8890 WS)"
  pkill -f lh_kline_server.py 2>/dev/null || true
  sleep 1
  nohup python3 "$LONGHUN_ROOT/08_BIN/lh_kline_server.py" > /tmp/kline_server.log 2>&1 &
  sleep 2
  curl -s http://127.0.0.1:8899/api/kline/health && echo ""
  echo "✅ 本地已启动 → http://127.0.0.1:8899/kline.html"
}

local_stop() {
  pkill -f lh_kline_server.py 2>/dev/null || true
  echo "已停止"
}

kunpeng_deploy() {
  echo "[鲲鹏] 同步代码与静态资产…"
  rsync -az --delete \
    -e "ssh -i $SSH_KEY" \
    "$LONGHUN_ROOT/08_BIN/lh_kline_fetcher.py" \
    "$LONGHUN_ROOT/08_BIN/lh_kline_server.py" \
    "$REMOTE:$REMOTE_DIR/08_BIN/"

  echo "[鲲鹏] 同步 portal 静态资产…"
  rsync -az --delete \
    -e "ssh -i $SSH_KEY" \
    "$LONGHUN_ROOT/10_PORTAL/kline.html" \
    "$LONGHUN_ROOT/10_PORTAL/assets/vendor/echarts.min.js" \
    "$LONGHUN_ROOT/10_PORTAL/assets/fonts/" \
    "$REMOTE:$REMOTE_DIR/portal/"

  echo "[鲲鹏] 安装 systemd 服务…"
  ssh -i "$SSH_KEY" "$REMOTE" "cat > /etc/systemd/system/longhun-kline.service << 'EOF'
[Unit]
Description=Longhun KLine Data Service
After=network.target

[Service]
WorkingDirectory=$REMOTE_DIR/08_BIN
ExecStart=/usr/bin/python3 $REMOTE_DIR/08_BIN/lh_kline_server.py
Restart=always
RestartSec=5
Environment=KLINE_PORT=$KLINE_PORT
Environment=KLINE_WS_PORT=$KLINE_WS_PORT

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable longhun-kline
systemctl restart longhun-kline
sleep 3
systemctl is-active longhun-kline
curl -s http://127.0.0.1:$KLINE_PORT/api/kline/health && echo ''
"

  echo "[鲲鹏] 配置 nginx 反代 /api/kline → $KLINE_PORT…"
  ssh -i "$SSH_KEY" "$REMOTE" "
CFG=/etc/nginx/conf.d/nginx-uid9622.cn.conf
if ! grep -q 'api/kline' \$CFG 2>/dev/null; then
  python3 - << PY
p = '$CFG'
s = open(p).read()
kline_block = '''
        location /api/kline/ {
            proxy_pass http://127.0.0.1:$KLINE_PORT/api/kline/;
            proxy_set_header Host \\\$host;
            proxy_set_header X-Real-IP \\\$remote_addr;
            proxy_read_timeout 10s;
        }
'''
if 'location /api/kline/' not in s:
    s = s.replace('location /', kline_block + '\n        location /', 1)
    open(p, 'w').write(s)
    print('已注入反代段到 ' + p)
PY
  nginx -t && systemctl reload nginx
else
  echo 'nginx 已含 /api/kline 反代'
fi
"

  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "✅ 部署完成 → https://uid9622.cn/kline.html"
}

kunpeng_fix() {
  echo "[鲲鹏] 端口修复 + 依赖安装 ($KLINE_PORT/$KLINE_WS_PORT)…"
  ssh -i "$SSH_KEY" "$REMOTE" "
    pip3 install -q --break-system-packages flask-cors websockets 2>&1 | tail -1
    sed -i 's/KLINE_PORT=.*/KLINE_PORT=$KLINE_PORT/; s/KLINE_WS_PORT=.*/KLINE_WS_PORT=$KLINE_WS_PORT/' /etc/systemd/system/longhun-kline.service
    CFG=/etc/nginx/conf.d/nginx-uid9622.cn.conf
    python3 - << 'PY'
import os, re
p = '/etc/nginx/conf.d/nginx-uid9622.cn.conf'
port = os.environ.get('KLINE_PORT', '8895')
s = open(p).read()
# 1. 清除所有现存 api/kline 块（含坏块）→ 统一重建
s = re.sub(r'\n?[ \t]*location /api/kline/ \{.*?\n[ \t]*\}', '', s, flags=re.S)
block = f'''
        location /api/kline/ {{
            proxy_pass http://127.0.0.1:{port}/api/kline/;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_read_timeout 10s;
        }}
'''
changed = False
anchor80 = '        location / {\n'
anchor443 = '    ssl_certificate /etc/letsencrypt/live/uid9622.cn/fullchain.pem;'
if anchor80 in s:
    idx = s.index(anchor80)
    if 'api/kline' not in s[max(0, idx - 400):idx]:
        s = s.replace(anchor80, block + '\n' + anchor80, 1)
        changed = True
if anchor443 in s:
    idx = s.index(anchor443)
    if 'api/kline' not in s[idx:idx + 200]:
        s = s.replace(anchor443, block + '\n' + anchor443, 1)
        changed = True
if changed:
    open(p, 'w').write(s)
    print('已重建反代段(80+443)到 ' + p)
PY
    sed -i 's|proxy_pass http://127.0.0.1:88[0-9]*/api/kline/;|proxy_pass http://127.0.0.1:'$KLINE_PORT'/api/kline/;|' \$CFG
    systemctl daemon-reload && systemctl restart longhun-kline
    sleep 4
    systemctl is-active longhun-kline
    curl -s --max-time 8 http://127.0.0.1:$KLINE_PORT/api/kline/health && echo ''
    nginx -t 2>&1 | tail -1 && systemctl reload nginx && echo NGINX_OK
  "
  echo "✅ 修复完成 → https://uid9622.cn/kline.html"
}

case "${1:-local}" in
  local) local_start ;;
  stop)  local_stop ;;
  kunpeng) kunpeng_deploy ;;
  fix) kunpeng_fix ;;
  *) echo "用法: $0 {local|kunpeng|fix|stop}" ;;
esac
