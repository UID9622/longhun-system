#!/bin/bash
# ═══════════════════════════════════════════════════════
# 龍魂AI模型自进化系统一键部署
# DNA: UID9622-ONLY-ONCE🧬LK9X-772Z
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 功能: 看门狗 + 重训练器 + 验证服务v6 + 面板v5
# ═══════════════════════════════════════════════════════
set -e

LH_ROOT="$HOME/longhun-system"
SCRIPTS_DIR="$LH_ROOT/scripts"
LOG_DIR="$LH_ROOT/logs"
MODEL_DIR="$LH_ROOT/models"
mkdir -p "$LOG_DIR" "$MODEL_DIR" "$MODEL_DIR/archive"

echo "🐉 龍魂AI模型自进化系统部署"
echo "═══════════════════════════════════════════════════════"

# ── 1. 安装依赖 ──
echo ""
echo "📦 1/6 检查依赖..."
pip3 install -q scikit-learn numpy fastapi uvicorn 2>/dev/null || {
    echo "   安装依赖..."
    pip3 install scikit-learn numpy fastapi uvicorn --user
}
echo "   ✅ 依赖就绪"

# ── 2. 设置脚本权限 ──
echo ""
echo "🔐 2/6 设置执行权限..."
chmod +x "$SCRIPTS_DIR"/longhun-training-monitor.py \
         "$SCRIPTS_DIR"/longhun-model-watchdog.py \
         "$SCRIPTS_DIR"/longhun-model-watchdog-check.py \
         "$SCRIPTS_DIR"/longhun-appeal-retrainer-v2.py \
         "$SCRIPTS_DIR"/longhun-appeal-trainer.py \
         "$LH_ROOT/L6_同步层"/longhun-persona-verify-v6.py 2>/dev/null || true
echo "   ✅ 权限设置完成"

# ── 3. 首次训练模型（如果不存在） ──
echo ""
echo "🤖 3/6 检查AI初审模型..."
if [[ ! -f "$MODEL_DIR/appeal_classifier.pkl" ]]; then
    echo "   训练中..."
    cd "$LH_ROOT"
    python3 "$SCRIPTS_DIR/longhun-appeal-trainer.py" || {
        echo "   ⚠️ 训练跳过（可能缺少人格链数据）"
        echo "   提示: 先运行 longhun-persona-trainer.py 生成人格链"
    }
else
    echo "   ✅ 模型已存在: $(ls -lh "$MODEL_DIR/appeal_classifier.pkl" | awk '{print $5}')"
fi

# ── 4. 配置 LaunchAgent（Mac看门狗） ──
echo ""
echo "🖥️  4/6 配置看门狗守护进程..."
if [[ "$(uname)" == "Darwin" ]]; then
    cat > "$HOME/Library/LaunchAgents/com.longhun.model-watchdog.plist" << 'PLISTEOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.model-watchdog</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>REPLACE_LH_ROOT/scripts/longhun-model-watchdog.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>REPLACE_LH_ROOT/logs/watchdog.log</string>
    <key>StandardErrorPath</key>
    <string>REPLACE_LH_ROOT/logs/watchdog-error.log</string>
</dict>
</plist>
PLISTEOF
    # 替换路径
    sed -i '' "s|REPLACE_LH_ROOT|$LH_ROOT|g" "$HOME/Library/LaunchAgents/com.longhun.model-watchdog.plist"

    # 卸载旧版本（如果存在）
    launchctl unload "$HOME/Library/LaunchAgents/com.longhun.model-watchdog.plist" 2>/dev/null || true
    # 加载
    launchctl load "$HOME/Library/LaunchAgents/com.longhun.model-watchdog.plist"
    echo "   ✅ LaunchAgent 已加载"
    echo "   launchctl list | grep longhun.model-watchdog"
else
    echo "   ⚠️ 非 macOS，跳过 LaunchAgent（请手动配置 systemd）"
fi

# ── 5. 配置 crontab 双重保险 ──
echo ""
echo "⏰ 5/6 配置 crontab 双重保险..."
CRON_CMD="*/5 * * * * /usr/bin/python3 $SCRIPTS_DIR/longhun-model-watchdog-check.py >> $LOG_DIR/watchdog-cron.log 2>&1"

# 检查是否已有
if ! crontab -l 2>/dev/null | grep -q "longhun-model-watchdog-check"; then
    (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
    echo "   ✅ crontab 已添加 (每5分钟检查)"
else
    echo "   ✅ crontab 已存在"
fi

# ── 6. 测试启动 ──
echo ""
echo "🧪 6/6 验证服务..."


# 停止旧服务
pkill -f "longhun-persona-verify" 2>/dev/null || true
pkill -f "longhun-model-watchdog" 2>/dev/null || true
sleep 1

# 启动 v6 验证服务
echo "   启动验证服务 v6.0 (端口 9623)..."
cd "$LH_ROOT"
nohup python3 "$LH_ROOT/L6_同步层/longhun-persona-verify-v6.py" --port 9623 > "$LOG_DIR/persona-verify-v6.log" 2>&1 &
VERIFY_PID=$!
sleep 2

# 验证服务
if kill -0 $VERIFY_PID 2>/dev/null; then
    echo "   ✅ 验证服务 v6.0 启动成功 (PID: $VERIFY_PID)"
else
    echo "   ❌ 验证服务启动失败，检查日志: $LOG_DIR/persona-verify-v6.log"
fi

# 快速测试API
echo "   测试 API..."
sleep 1
HEALTH=$(curl -s http://localhost:9623/health 2>/dev/null || echo '{"error":"unreachable"}')
echo "   健康检查: $(echo $HEALTH | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('status','?'))" 2>/dev/null || echo 'unreachable')"

MODEL_VER=$(curl -s http://localhost:9623/model-version 2>/dev/null || echo '{"version":0}')
echo "   模型版本: v$(echo $MODEL_VER | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('version',0))" 2>/dev/null || echo '?')"

# 启动看门狗
echo "   启动看门狗..."
nohup python3 "$SCRIPTS_DIR/longhun-model-watchdog.py" > "$LOG_DIR/watchdog.log" 2>&1 &
WATCHDOG_PID=$!
sleep 1
if kill -0 $WATCHDOG_PID 2>/dev/null; then
    echo "   ✅ 看门狗启动成功 (PID: $WATCHDOG_PID)"
else
    echo "   ⚠️ 看门狗启动失败（LaunchAgent 会接管）"
fi

# ── 完成 ──
echo ""
echo "═══════════════════════════════════════════════════════"
echo "✅ 龍魂AI模型自进化系统部署完成!"
echo ""
echo "  核心服务:"
echo "    验证服务 v6.0:  http://localhost:9623"
echo "    模型版本:       curl localhost:9623/model-version"
echo "    训练状态:       curl localhost:9623/training/status"
echo "    健康检查:       curl localhost:9623/health"
echo ""
echo "  守护进程:"
echo "    看门狗:         launchctl list | grep longhun.model-watchdog"
echo "    Crontab:        crontab -l | grep watchdog-check"
echo ""
echo "  日志:"
echo "    验证服务:       tail -f $LOG_DIR/persona-verify-v6.log"
echo "    看门狗:         tail -f $LOG_DIR/watchdog.log"
echo ""
echo "  手动命令:"
echo "    查看状态:       python3 $SCRIPTS_DIR/longhun-training-monitor.py"
echo "    触发检测:       python3 $SCRIPTS_DIR/longhun-model-watchdog.py --once"
echo "    强制重训练:     python3 $SCRIPTS_DIR/longhun-appeal-retrainer-v2.py --version \$(python3 -c \"import json;v=json.load(open('$MODEL_DIR/model_version.json')).get('current_version',0);print(v+1)\") --from-version \$(python3 -c \"import json;print(json.load(open('$MODEL_DIR/model_version.json')).get('current_version',0))\")"
echo ""
echo "  面板:"
echo "    路径:           $LH_ROOT/deploy/longhun-theme/longhun-v5.js"
echo "    V5特性:         训练进度条 + 模型版本显示 + 完成通知"
echo ""
echo "  自进化流程:"
echo "    人格链更新 → 60秒检测 → 自动重训练 → A/B验证 → 原子切换"
echo "    面板实时显示: AIv3 → AIv4 训练中 █████░░ 52.3%"
echo ""
echo "  隔离不是惩罚，是保护。真金不怕火炼，真龍魂不怕隔离。"
echo "═══════════════════════════════════════════════════════"
