#!/bin/bash
# ═══════════════════════════════════════════════════════
# 龍魂AI申诉初审系统 · 一键部署脚本 v1.0
# DNA: #龍芯⚡️丙午·辛未·APPEAL-DEPLOY-v1.0
# ═══════════════════════════════════════════════════════

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}🐉 龍魂AI申诉初审系统 · 一键部署 v1.0${NC}"
echo "============================================"

LONGHUN_ROOT="$HOME/longhun-system"
FRP_DIR="/opt/frp"

# ── 1. 检查环境 ──
echo -e "\n${YELLOW}[1/7]${NC} 检查环境..."

# Python3
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}❌ python3 未安装${NC}"
    exit 1
fi
echo -e "  ${GREEN}✅${NC} python3: $(python3 --version)"

# pip
if ! python3 -m pip --version &>/dev/null; then
    echo -e "${RED}❌ pip 不可用${NC}"
    exit 1
fi

# Redis
if redis-cli ping &>/dev/null 2>&1; then
    echo -e "  ${GREEN}✅${NC} Redis: 运行中"
else
    echo -e "  ${YELLOW}⚠️${NC} Redis: 未运行（将使用内存模式，重启丢失状态）"
fi

# ── 2. 安装Python依赖 ──
echo -e "\n${YELLOW}[2/7]${NC} 安装Python依赖..."
python3 -m pip install scikit-learn numpy fastapi uvicorn redis 2>/dev/null || \
    pip3 install scikit-learn numpy fastapi uvicorn redis 2>/dev/null || \
    pip install scikit-learn numpy fastapi uvicorn redis

echo -e "  ${GREEN}✅${NC} 依赖安装完成"

# ── 3. 训练AI初审模型 ──
echo -e "\n${YELLOW}[3/7]${NC} 训练AI初审模型..."

cd "$LONGHUN_ROOT"

if [[ -f "$LONGHUN_ROOT/scripts/longhun-appeal-trainer.py" ]]; then
    python3 "$LONGHUN_ROOT/scripts/longhun-appeal-trainer.py" || {
        echo -e "  ${YELLOW}⚠️${NC} 训练有警告，但继续部署"
    }
else
    echo -e "  ${RED}❌${NC} 训练脚本未找到: scripts/longhun-appeal-trainer.py"
    exit 1
fi

if [[ -f "$LONGHUN_ROOT/models/appeal_classifier.pkl" ]]; then
    SIZE=$(ls -lh "$LONGHUN_ROOT/models/appeal_classifier.pkl" | awk '{print $5}')
    echo -e "  ${GREEN}✅${NC} 模型文件: $SIZE"
else
    echo -e "  ${RED}❌${NC} 模型训练失败"
    exit 1
fi

# ── 4. 部署验证服务 ──
echo -e "\n${YELLOW}[4/7]${NC} 部署人格验证服务 v4.0..."

# 停止旧服务
pkill -f "longhun-persona-verify" 2>/dev/null || true
sleep 1

# 启动新服务
LOG_DIR="${FRP_DIR}/logs"
mkdir -p "$LOG_DIR"

nohup python3 "$LONGHUN_ROOT/L6_同步层/longhun-persona-verify-v4.py" \
    --port 9623 --host 0.0.0.0 \
    > "$LOG_DIR/persona-verify-v4.log" 2>&1 &

sleep 2

# 验证服务
if curl -s http://localhost:9623/health | grep -q "v4"; then
    echo -e "  ${GREEN}✅${NC} 验证服务 v4.0 已启动 :9623"
else
    echo -e "  ${YELLOW}⚠️${NC} 服务启动中，检查日志: tail -f $LOG_DIR/persona-verify-v4.log"
fi

# ── 5. 部署面板JS ──
echo -e "\n${YELLOW}[5/7]${NC} 部署面板JS v4.0..."

THEME_DIR="${FRP_DIR}/web/longhun-theme"
mkdir -p "$THEME_DIR"

cp "$LONGHUN_ROOT/deploy/longhun-theme/longhun-v4.js" "$THEME_DIR/"

echo -e "  ${GREEN}✅${NC} longhun-v4.js → $THEME_DIR/"

# ── 6. 更新Nginx配置 ──
echo -e "\n${YELLOW}[6/7]${NC} 更新Nginx配置..."

NGINX_CONF="/etc/nginx/sites-available/longhun-frp"
if [[ -f "$NGINX_CONF" ]]; then
    # 更新JS引用
    if grep -q "longhun-v3.js" "$NGINX_CONF"; then
        sudo sed -i 's/longhun-v3\.js/longhun-v4.js/g' "$NGINX_CONF"
        echo -e "  ${GREEN}✅${NC} Nginx: v3 → v4"
    elif grep -q "longhun-v4.js" "$NGINX_CONF"; then
        echo -e "  ${GREEN}✅${NC} Nginx: 已是 v4"
    else
        echo -e "  ${YELLOW}⚠️${NC} Nginx配置中未找到龙魂JS引用，请手动添加"
    fi

    # 测试并重载
    if sudo nginx -t 2>/dev/null; then
        sudo systemctl reload nginx 2>/dev/null || sudo nginx -s reload 2>/dev/null
        echo -e "  ${GREEN}✅${NC} Nginx 重载完成"
    else
        echo -e "  ${RED}❌${NC} Nginx 配置测试失败"
    fi
else
    echo -e "  ${YELLOW}⚠️${NC} Nginx配置未找到: $NGINX_CONF"
fi

# ── 7. 设置定期重训练 ──
echo -e "\n${YELLOW}[7/7]${NC} 配置定期自动重训练..."

CRON_SCRIPT="$LONGHUN_ROOT/scripts/longhun-appeal-retrain-cron.sh"

if [[ -f "$CRON_SCRIPT" ]]; then
    chmod +x "$CRON_SCRIPT"

    # 检查是否已有crontab
    if crontab -l 2>/dev/null | grep -q "appeal-retrain"; then
        echo -e "  ${GREEN}✅${NC} Cron已配置"
    else
        # 每天凌晨3点自动重训练
        (crontab -l 2>/dev/null; echo "0 3 * * * $CRON_SCRIPT >> $LOG_DIR/appeal-retrain.log 2>&1") | crontab -
        echo -e "  ${GREEN}✅${NC} Cron已添加: 每天03:00自动重训练"
    fi
else
    echo -e "  ${YELLOW}⚠️${NC} 重训练脚本未找到，跳过cron配置"
fi

# ── 最终验证 ──
echo -e "\n${CYAN}════════════════════════════════════════════${NC}"
echo -e "${CYAN}  部署完成！验证结果:${NC}"

echo -e "\n  API测试:"
curl -s http://localhost:9623/health | python3 -m json.tool 2>/dev/null || \
    curl -s http://localhost:9623/health

echo -e "\n  ${YELLOW}手动测试命令:${NC}"
echo "  # 测试验证"
echo "  curl -X POST http://localhost:9623/verify -H 'Content-Type: application/json' \\"
echo "    -d '{\"node_id\":\"hacker-node\",\"value_fingerprint\":\"0000000000000000\",\"emotion_fingerprint\":\"0000000000000000\",\"decision_count\":0}'"
echo ""
echo "  # 查看隔离列表"
echo "  curl http://localhost:9623/quarantine/list"
echo ""
echo "  # 查看申诉队列"
echo "  curl 'http://localhost:9623/appeal/queue?admin_key=UID9622_ADMIN_APPEAL'"
echo ""
echo "  # 查看告警"
echo "  curl http://localhost:9623/alerts"

echo -e "\n  ${GREEN}🐉 龍魂AI申诉初审系统 v4.0 部署完成${NC}"
