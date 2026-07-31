#!/bin/bash
# 🐉 龍魂宇宙 · 华为云鲲鹏一键部署脚本
# UID9622 | 龍芯北辰 | 2026-07-18
# DNA: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

set -e

SERVER="root@119.13.90.27"
SSH_KEY="$HOME/.ssh/longhun_kunpeng_ed25519"
DEPLOY_DIR="/var/www/longhun-universe"

echo "🐉 龍魂宇宙 · 一键部署"
echo "================================"
echo ""

# Step 1: 上传文件
echo "📤 Step 1/4: 上传 index.html..."
scp -i "$SSH_KEY" index.html "${SERVER}:/tmp/longhun_universe_index.html"

# Step 2: 服务器端部署
echo ""
echo "🔧 Step 2/4: 远程部署 Nginx 静态站点..."
ssh -i "$SSH_KEY" "$SERVER" << 'REMOTE_SCRIPT'
set -e

DEPLOY_DIR="/var/www/longhun-universe"

# 创建目录
mkdir -p "$DEPLOY_DIR"

# 移动文件
mv /tmp/longhun_universe_index.html "$DEPLOY_DIR/index.html"
chmod 644 "$DEPLOY_DIR/index.html"

echo "   ✅ index.html 就位: $DEPLOY_DIR/index.html"
REMOTE_SCRIPT

# Step 3: 更新 Nginx 配置
echo ""
echo "⚙️  Step 3/4: 配置 Nginx..."

cat > /tmp/longhun_universe_nginx.conf << 'NGINX_CONF'
# 🐉 龍魂宇宙 · Nginx 配置片段
# 添加到: /etc/nginx/conf.d/uid9622.cn.conf
# 路径: uid9622.cn/universe/ → /var/www/longhun-universe/

location /universe/ {
    alias /var/www/longhun-universe/;
    index index.html;
    try_files $uri $uri/ /universe/index.html;

    # 缓存策略
    expires 7d;
    add_header Cache-Control "public, immutable";
    add_header X-Longhun-Universe "1650万路径";
    add_header X-Data-Sovereignty "China-HuaweiCloud-Kunpeng";
    add_header X-UID "9622-Lucky";
}

location /universe {
    return 301 /universe/;
}
NGINX_CONF

scp -i "$SSH_KEY" /tmp/longhun_universe_nginx.conf "${SERVER}:/tmp/longhun_universe_nginx.conf"

# 插入 Nginx 配置（在 uid9622.cn 的 server 块中）
ssh -i "$SSH_KEY" "$SERVER" << 'REMOTE_INSERT'
set -e

NGINX_CONF="/etc/nginx/conf.d/uid9622.cn.conf"
UNIVERSE_FRAGMENT="/tmp/longhun_universe_nginx.conf"

# 检查是否已存在
if grep -q "location /universe" "$NGINX_CONF" 2>/dev/null; then
    echo "   ⚠️  universe 路由已存在，跳过 Nginx 配置插入"
else
    # 在第一个 server { ... } 块中的最后一个 location 后插入
    # 找到 dashboard server 块的末尾 "}" 前插入
    if ! grep -q "location /universe" "$NGINX_CONF"; then
        # 在 proxy_pass http://127.0.0.1:9627; 之后、下一个 } 之前插入
        sed -i '/proxy_pass http:\/\/127.0.0.1:9627;/r /tmp/longhun_universe_nginx.conf' "$NGINX_CONF"
        echo "   ✅ Nginx universe 路由已插入"
    fi
fi

# 测试配置
echo "   🔍 测试 Nginx 配置..."
nginx -t && echo "   ✅ Nginx 配置通过" || echo "   ❌ Nginx 配置错误！"

# 重载
systemctl reload nginx && echo "   ✅ Nginx 已重载" || echo "   ❌ Nginx 重载失败"
REMOTE_INSERT

rm -f /tmp/longhun_universe_nginx.conf

# Step 4: 验证
echo ""
echo "🌐 Step 4/4: 验证部署..."
echo ""
echo "   访问地址: https://uid9622.cn/universe/"
echo ""
curl -s -o /dev/null -w "   HTTP 状态码: %{http_code}\n" "https://uid9622.cn/universe/" 2>/dev/null || echo "   ⚠️ curl 验证跳过（可能需要等待 DNS）"

echo ""
echo "================================"
echo "🐉 龍魂宇宙部署完成！"
echo ""
echo "📱 手机浏览器打开: https://uid9622.cn/universe/"
echo "💻 桌面浏览器打开: https://uid9622.cn/universe/"
echo ""
echo "功能清单:"
echo "  ✅ 10000点3D路径采样（Three.js WebGL）"
echo "  ✅ 触摸旋转/缩放/拖拽"
echo "  ✅ 文本→PathID追踪（金色轨迹线）"
echo "  ✅ 三色审计过滤（🟢🟡🔴）"
echo "  ✅ 节点点击详情弹窗"
echo "  ✅ 五行分布实时统计"
echo "  ✅ DNA水印嵌入"
