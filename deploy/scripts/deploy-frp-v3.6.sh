#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# deploy-frp-v3.6.sh
# 部署frp面板 v3.6 — 训练进度可视化 + Canvas进化时间轴
# DNA: #龍芯⚡️丙午·辛未·DEPLOY-v3.6
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
set -e

echo "🐉 龍魂面板 v3.6 部署"
echo "═══════════════════════════════════════════════════════"

LONGHUN_ROOT="$HOME/longhun-system"
SCRIPTS_DIR="$LONGHUN_ROOT/scripts"
FRP_DIR="/opt/frp"
WEB_DIR="$FRP_DIR/web/longhun-theme"

# 1. 复制训练监控模块（已升级 v1.0 → 含TrainingHistory）
echo ""
echo "📦 [1/6] 训练监控模块..."
cp "$SCRIPTS_DIR/longhun-training-monitor.py" "$FRP_DIR/scripts/" 2>/dev/null || {
    mkdir -p "$FRP_DIR/scripts"
    cp "$SCRIPTS_DIR/longhun-training-monitor.py" "$FRP_DIR/scripts/"
    echo "   创建 $FRP_DIR/scripts/"
}

# 2. 复制重训练器v2
echo "📦 [2/6] 增量重训练器v2..."
cp "$SCRIPTS_DIR/longhun-appeal-retrainer-v2.py" "$FRP_DIR/scripts/"

# 3. 部署验证服务v6
echo "📦 [3/6] 验证服务v6..."
cp "$SCRIPTS_DIR/longhun-persona-verify-v6.py" "$FRP_DIR/scripts/"

# 4. 复制面板JS v3.6
echo "📦 [4/6] 面板JS v3.6..."
mkdir -p "$WEB_DIR"
cp "$LONGHUN_ROOT/deploy/scripts/longhun-v3.6.js" "$WEB_DIR/"

# 5. 更新Nginx（添加training-api反向代理）
echo "📦 [5/6] Nginx配置..."
NGINX_CONF="/etc/nginx/sites-available/longhun-frp"
if [ -f "$NGINX_CONF" ]; then
    # 检查是否已有 training-api 配置
    if ! grep -q "training-api" "$NGINX_CONF"; then
        echo "   添加 training-api 路由..."
        sudo sed -i '/location \/ {/i\
    # 训练状态API（面板轮询）\
    location /training-api/ {\
        proxy_pass http://127.0.0.1:9623/;\
        proxy_set_header Host $host;\
        proxy_set_header X-Real-IP $remote_addr;\
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\
        proxy_cache_valid 200 1s;\
    }' "$NGINX_CONF"
    else
        echo "   training-api 路由已存在，跳过"
    fi
else
    echo "   ⚠️ Nginx配置文件不存在，跳过Nginx配置"
fi

# 6. 重启服务
echo "📦 [6/6] 重启服务..."

# 停旧验证服务
pkill -f "longhun-persona-verify" 2>/dev/null || true
sleep 1

# 起新验证服务v6
mkdir -p "$FRP_DIR/logs"
nohup python3 "$FRP_DIR/scripts/longhun-persona-verify-v6.py" > "$FRP_DIR/logs/persona-verify-v6.log" 2>&1 &
echo "   验证服务v6 PID: $!"

# 重载Nginx
if sudo nginx -t 2>/dev/null; then
    sudo systemctl reload nginx 2>/dev/null || sudo nginx -s reload
    echo "   Nginx重载完成"
else
    echo "   ⚠️ Nginx配置检查失败，跳过重载"
fi

echo ""
echo "✅ 龍魂面板 v3.6 部署完成"
echo "═══════════════════════════════════════════════════════"
echo "  训练进度显示:"
echo "    🐉 龍魂AI模型进化中"
echo "    AIv3 → AIv4"
echo "    ██████████░░░░░░░░░░ 52.3%"
echo "    训练模型... 6/10"
echo "    预计剩余: 2m34s"
echo ""
echo "  Canvas时间轴图表:"
echo "    📈 准确率进化曲线（红色发光）"
echo "    📊 样本增长柱状图（底部）"
echo "    ⏱️  训练耗时散点（右上）"
echo "    ↗️  趋势线（绿色虚线）"
echo ""
echo "  交互:"
echo "    点击底部栏 AI版本 → 打开进化时间轴"
echo "    或按 Alt+T 快捷键"
echo "    鼠标悬停数据点 → 显示详细数值"
echo "    点击数据点 → 滚动到对应版本卡片"
echo "    入场动画 → 1.5秒渐进绘制"
echo ""
echo "  API端点:"
echo "    GET /training-api/training/status    (面板轮询)"
echo "    GET /training-api/training/timeline  (时间轴数据)"
echo "    GET /training-api/model/version      (当前版本)"
echo "    GET /training-api/health             (健康检查)"
echo ""
echo "  完成显示:"
echo "    ✅ 模型进化完成"
echo "    AIv3 → AIv4"
echo "    准确率: 94.2% | 样本: 3,147"
echo ""
echo "  错误显示:"
echo "    ❌ 训练失败"
echo "    已回滚至 AIv3"
echo "═══════════════════════════════════════════════════════"
