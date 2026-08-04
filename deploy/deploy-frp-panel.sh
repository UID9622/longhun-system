#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ============================================================================
# deploy-frp-panel.sh — 龍魂主题 Nginx 面板部署 v3.0
# DNA: #龍芯⚡️丙午·辛未·FRP-PANEL-v3.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#
# 在 frps 公网服务器上执行，部署：
#   - Nginx + 龍魂CSS主题 + v3.0 JS注入
#   - 人格验证 API 代理 (/persona-api → :9623)
#   - 底部栏实时人格匹配度 + 节点信任徽章
# 效果: http://你的IP/longhun/ → 深色龍魂主题 + 人格指纹实时显示
# ============================================================================

set -e

FRP_DIR="${FRP_DIR:-/opt/frp}"
THEME_DIR="${FRP_DIR}/web/longhun-theme"
PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || echo "YOUR_IP")

RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

echo ""
echo -e "${BOLD}🐉 龍魂主题 · Nginx 面板部署 v3.0${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "   DNA: ${CYAN}#龍芯⚡️丙午·辛未·FRP-PANEL-v3.0${NC}"
echo ""

# ─── 1. 安装依赖 ───
echo -e "${CYAN}[1/5] 安装依赖 (Nginx + Python3 + Redis)...${NC}"
if ! command -v nginx &>/dev/null; then
    if command -v apt-get &>/dev/null; then
        apt-get update -qq && apt-get install -y -qq nginx
    elif command -v yum &>/dev/null; then
        yum install -y nginx
    else
        echo -e "${RED}❌ 无法安装 nginx，请手动安装${NC}"
        exit 1
    fi
fi

# Python & Redis (人格验证服务依赖)
if command -v apt-get &>/dev/null; then
    apt-get install -y -qq python3-pip redis-server 2>/dev/null || true
elif command -v yum &>/dev/null; then
    yum install -y python3-pip redis 2>/dev/null || true
fi

pip3 install fastapi uvicorn redis requests 2>/dev/null || true

# 启动 Redis
if command -v systemctl &>/dev/null; then
    systemctl enable redis-server 2>/dev/null || systemctl enable redis 2>/dev/null || true
    systemctl start redis-server 2>/dev/null || systemctl start redis 2>/dev/null || true
fi

# ─── 2. 创建龍魂主题 ───
echo -e "${CYAN}[2/5] 部署龍魂 CSS + v3.0 JS...${NC}"
mkdir -p "$THEME_DIR"

tee "$THEME_DIR/longhun.css" << 'CSSEOF'
/* ═══════════════════════════════════════════════════════
 * 龍魂系統 · FRP 面板主题 v1.0
 * DNA: UID9622-ONLY-ONCE🧬LK9X-772Z
 * 配色: 深渊黑 + 龙血红 + 鎏金
 * ═══════════════════════════════════════════════════════ */

:root {
    --lh-bg-primary: #0a0a0f;
    --lh-bg-secondary: #12121a;
    --lh-bg-card: #1a1a24;
    --lh-bg-hover: #252530;
    --lh-border: #2a2a3a;
    --lh-text-primary: #e8e8f0;
    --lh-text-secondary: #8a8a9a;
    --lh-text-muted: #5a5a6a;
    --lh-dragon-red: #c41e3a;
    --lh-dragon-red-glow: #ff2d55;
    --lh-dragon-red-dim: rgba(196, 30, 58, 0.5);
    --lh-gold: #d4af37;
    --lh-gold-dim: #8b7355;
    --lh-online: #00c853;
    --lh-offline: #ff1744;
    --lh-warning: #ff9100;
    --lh-radius: 8px;
    --lh-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

body {
    background: var(--lh-bg-primary) !important;
    color: var(--lh-text-primary) !important;
    font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif !important;
}

body::before {
    content: "龍魂系统 UID9622 龍芯北辰";
    position: fixed; bottom: 20px; right: 100px;
    font-size: 12px; color: var(--lh-text-muted);
    opacity: 0.43; z-index: 9999; pointer-events: none;
    letter-spacing: 2px;
}
body::after {
    content: "🐉";
    position: fixed; bottom: 16px; right: 74px;
    font-size: 16px; opacity: 0.25; z-index: 9999; pointer-events: none;
}

/* 页头 */
.ant-layout-header, header, .navbar {
    background: var(--lh-bg-secondary) !important;
    border-bottom: 1px solid var(--lh-border) !important;
    box-shadow: 0 2px 8px var(--lh-dragon-red-dim) !important;
}
.logo, .header-title {
    color: var(--lh-dragon-red) !important; font-weight: 700 !important; letter-spacing: 1px;
}

/* 侧边栏 */
.ant-menu, .ant-layout-sider, .sider, .sidebar {
    background: var(--lh-bg-secondary) !important;
    border-right: 1px solid var(--lh-border) !important;
}
.ant-menu-item, .nav-item { color: var(--lh-text-secondary) !important; }
.ant-menu-item:hover, .nav-item:hover {
    background: var(--lh-bg-hover) !important;
    color: var(--lh-dragon-red) !important;
}
.ant-menu-item-selected, .nav-item.active {
    background: rgba(196, 30, 58, 0.15) !important;
    color: var(--lh-dragon-red) !important;
    border-left: 3px solid var(--lh-dragon-red) !important;
}

/* 主内容 */
.ant-layout-content, .content, .main-content { background: var(--lh-bg-primary) !important; }

/* 卡片 */
.ant-card, .card, .panel, .widget {
    background: var(--lh-bg-card) !important;
    border: 1px solid var(--lh-border) !important;
    border-radius: var(--lh-radius) !important;
    box-shadow: var(--lh-shadow) !important;
}
.ant-card-head, .card-header, .panel-header {
    background: var(--lh-bg-secondary) !important;
    border-bottom: 1px solid var(--lh-border) !important;
}

/* 统计数字 */
.ant-statistic-content-value, .stat-value, .metric-value {
    color: var(--lh-gold) !important; font-weight: 700 !important;
    text-shadow: 0 0 10px rgba(212, 175, 55, 0.3) !important;
}

/* 表格 */
.ant-table, table, .data-table { background: var(--lh-bg-card) !important; }
.ant-table-thead > tr > th, th, .table-header {
    background: var(--lh-bg-secondary) !important;
    color: var(--lh-text-primary) !important;
    border-bottom: 1px solid var(--lh-border) !important;
}
.ant-table-tbody > tr > td, td {
    color: var(--lh-text-secondary) !important;
    border-bottom: 1px solid var(--lh-border) !important;
}
.ant-table-tbody > tr:hover > td, tr:hover td { background: var(--lh-bg-hover) !important; }

/* 状态 */
.status-online, .tag-green, .badge-success {
    background: rgba(0,200,83,0.15) !important;
    color: var(--lh-online) !important;
    border: 1px solid rgba(0,200,83,0.3) !important;
}
.status-offline, .tag-red, .badge-error {
    background: rgba(255,23,68,0.15) !important;
    color: var(--lh-offline) !important;
    border: 1px solid rgba(255,23,68,0.3) !important;
}
.status-warning, .tag-orange, .badge-warning {
    background: rgba(255,145,0,0.15) !important;
    color: var(--lh-warning) !important;
    border: 1px solid rgba(255,145,0,0.3) !important;
}

/* 按钮 */
.ant-btn-primary, .btn-primary, button[type="submit"] {
    background: var(--lh-dragon-red) !important;
    border-color: var(--lh-dragon-red) !important;
    box-shadow: 0 0 8px rgba(196,30,58,0.4) !important;
}
.ant-btn-primary:hover, .btn-primary:hover {
    background: var(--lh-dragon-red-glow) !important;
    box-shadow: 0 0 16px rgba(255,45,85,0.6) !important;
}

/* 输入框 */
.ant-input, .ant-select-selector, input, select, textarea {
    background: var(--lh-bg-secondary) !important;
    border: 1px solid var(--lh-border) !important;
    color: var(--lh-text-primary) !important;
}
.ant-input:focus, input:focus, textarea:focus {
    border-color: var(--lh-dragon-red) !important;
    box-shadow: 0 0 0 2px rgba(196,30,58,0.2) !important;
}

/* 滚动条 */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--lh-bg-primary) !important; }
::-webkit-scrollbar-thumb { background: var(--lh-border) !important; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--lh-dragon-red) !important; }

/* 加载+分页+弹窗 */
.ant-spin-dot-item { background: var(--lh-dragon-red) !important; }
.ant-pagination-item { background: var(--lh-bg-card) !important; border: 1px solid var(--lh-border) !important; }
.ant-pagination-item-active { background: var(--lh-dragon-red) !important; border-color: var(--lh-dragon-red) !important; }
.ant-modal-content, .ant-drawer-content, .modal, .dialog { background: var(--lh-bg-card) !important; border: 1px solid var(--lh-border) !important; }
.ant-modal-header, .ant-drawer-header, .modal-header { background: var(--lh-bg-secondary) !important; border-bottom: 1px solid var(--lh-border) !important; }
canvas, svg, .chart { filter: hue-rotate(340deg) saturate(1.2) !important; }
.ant-layout-footer, footer, .footer { background: var(--lh-bg-secondary) !important; border-top: 1px solid var(--lh-border) !important; color: var(--lh-text-muted) !important; }

@media (max-width: 768px) {
    body::before { font-size: 10px; bottom: 8px; right: 8px; }
}
CSSEOF

# 复制 v3.0 JS 注入脚本（如果存在）
V3_JS_SRC="$(cd "$(dirname "$0")" && pwd)/longhun-theme/longhun-v3.js"
if [[ -f "$V3_JS_SRC" ]]; then
    cp "$V3_JS_SRC" "$THEME_DIR/longhun-v3.js"
    echo "  ✅ longhun-v3.js → $THEME_DIR/"
else
    echo "  ⚠️  longhun-v3.js 未找到，请手动复制到 $THEME_DIR/"
fi

# ─── 3. Nginx 配置 v3.0 ───
echo -e "${CYAN}[3/5] 配置 Nginx v3.0 (人格验证+主题注入)...${NC}"

FRP_WEB_PORT=7500

cat > /etc/nginx/sites-available/longhun-frp << NGXEOF
# 龍魂系統 · FRP 面板 Nginx 代理 v3.0
server {
    listen 80;
    server_name _;

    location /longhun/ {
        default_type text/html;
        return 200 '<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>🐉 龍魂隧道监控台 | UID9622</title>
    <link rel="stylesheet" href="/longhun-theme/longhun.css">
    <style>
        body { margin:0; padding:0; overflow:hidden; background:#0a0a0f; }
        #frp-frame { width:100vw; height:calc(100vh - 36px); border:none; }
        .lh-loading { position:fixed; top:50%; left:50%; transform:translate(-50%,-50%);
            color:#c41e3a; font-size:18px; letter-spacing:4px;
            animation:lh-load 1.5s ease-in-out infinite; }
        @keyframes lh-load { 0%,100%{opacity:0.5;} 50%{opacity:1;text-shadow:0 0 20px #c41e3a;} }
    </style>
</head>
<body>
    <div class="lh-loading" id="loading">🐉 龍魂系统加载中...</div>
    <iframe id="frp-frame" src="/frp-internal/"
        onload="document.getElementById(\"loading\").style.display=\"none\""></iframe>
    <script src="/longhun-theme/longhun-v3.js"></script>
</body>
</html>';
    }

    location /longhun-theme/ {
        alias ${THEME_DIR}/;
        expires 1h;
    }

    location /persona-api/ {
        proxy_pass http://127.0.0.1:9623/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }

    location /frp-internal/ {
        proxy_pass http://127.0.0.1:${FRP_WEB_PORT}/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        sub_filter '</head>' '<link rel="stylesheet" href="/longhun-theme/longhun.css"><script src="/longhun-theme/longhun-v3.js"></script></head>';
        sub_filter_once on;
        proxy_set_header Accept-Encoding "";
    }

    location /health {
        access_log off;
        return 200 '{"status":"longhun-panel-v3","dna":"UID9622","persona_verify":true}';
        add_header Content-Type application/json;
    }

    location / {
        return 302 /longhun/;
    }
}
NGXEOF

# 启用配置
if [ -d /etc/nginx/sites-enabled ]; then
    ln -sf /etc/nginx/sites-available/longhun-frp /etc/nginx/sites-enabled/longhun-frp
    rm -f /etc/nginx/sites-enabled/default 2>/dev/null || true
elif [ -d /etc/nginx/conf.d ]; then
    ln -sf /etc/nginx/sites-available/longhun-frp /etc/nginx/conf.d/longhun-frp.conf
fi

nginx -t && systemctl reload nginx

# ─── 4. 人格验证服务 ───
echo -e "${CYAN}[4/5] 部署人格验证服务...${NC}"

PERSONA_VERIFY_SRC="${HOME}/longhun-system/L6_同步层/longhun-persona-verify.py"
PERSONA_VERIFY_DST="/opt/frp/longhun-persona-verify.py"

if [[ -f "$PERSONA_VERIFY_SRC" ]]; then
    cp "$PERSONA_VERIFY_SRC" "$PERSONA_VERIFY_DST"
    chmod +x "$PERSONA_VERIFY_DST"
    echo "  ✅ longhun-persona-verify.py → $PERSONA_VERIFY_DST"
else
    echo "  ⚠️  本地未找到验证脚本，请手动复制到 $PERSONA_VERIFY_DST"
fi

cat > /etc/systemd/system/longhun-persona-verify.service << 'SVC_EOF'
[Unit]
Description=龍魂人格验证服务 v1.0
After=network.target redis-server.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/frp
ExecStart=/usr/bin/python3 /opt/frp/longhun-persona-verify.py --port 9623
Restart=always
RestartSec=10
StandardOutput=append:/opt/frp/logs/persona-verify.log
StandardError=append:/opt/frp/logs/persona-verify.log

[Install]
WantedBy=multi-user.target
SVC_EOF

mkdir -p /opt/frp/logs
systemctl daemon-reload
systemctl enable longhun-persona-verify 2>/dev/null || true
echo "  ✅ systemd 服务已配置 (longhun-persona-verify)"

# ─── 5. 安全加固 ───
echo -e "${CYAN}[5/5] 安全加固...${NC}"

if grep -q 'webServer.addr = "0.0.0.0"' "${FRP_DIR}/frps.toml" 2>/dev/null; then
    echo "   限制 frps 面板仅本地访问（通过 Nginx 代理）"
    sed -i 's/webServer.addr = "0.0.0.0"/webServer.addr = "127.0.0.1"/' "${FRP_DIR}/frps.toml"
    systemctl restart frps 2>/dev/null || true
fi

# ─── 完成 ───
echo ""
echo "════════════════════════════════════════════════"
echo -e "${BOLD}🐉 龍魂面板 v3.0 人格验证版 部署完成${NC}"
echo "════════════════════════════════════════════════"
echo ""
echo -e "  面板: ${GREEN}http://${PUBLIC_IP}/longhun/${NC}"
echo -e "  API:  ${GREEN}http://${PUBLIC_IP}/persona-api/health${NC}"
echo ""
echo "  v3.0 新增:"
echo "    🔐 底部栏实时显示人格匹配度"
echo "    👑 主控节点 100% 皇冠标记"
echo "    ✅ 可信节点绿色标记"
echo "    ⚠️  一般节点橙色警告"
echo "    ❌ 未验证节点红色闪烁"
echo ""
echo "  启动人格验证服务:"
echo -e "    ${CYAN}systemctl start longhun-persona-verify${NC}"
echo ""
echo "  各节点运行上报:"
echo -e "    ${CYAN}python3 scripts/longhun-node-reporter.py --server http://${PUBLIC_IP}:9623${NC}"
echo ""
echo "  本地一键流水线:"
echo -e "    ${CYAN}bash scripts/longhun-persona-pipeline.sh --open${NC}"
echo ""
echo -e "  DNA: #龍芯⚡️丙午·辛未·FRP-PANEL-v3.0"
echo ""

# 防火墙放行 80
if command -v ufw &>/dev/null; then
    ufw allow 80/tcp 2>/dev/null || true
elif command -v firewall-cmd &>/dev/null; then
    firewall-cmd --permanent --add-port=80/tcp 2>/dev/null || true
    firewall-cmd --reload 2>/dev/null || true
fi
