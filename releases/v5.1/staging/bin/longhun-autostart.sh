#!/usr/bin/env bash
# 龍魂系统开机自启动脚本
# 启动控制台、CNSH 任务执行引擎与基础服务
# DNA:#龍芯⚡️2026-06-17-LONGHUN-AUTOSTART-v1.0

cd "$(dirname "$0")/.."
ROOT="$(pwd)"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

echo "🐉 龍魂系统开机自启动" >> "$LOG_DIR/autostart.log"
date >> "$LOG_DIR/autostart.log"

# 启动龍魂操作台（统一 API 入口）
if ! lsof -ti:9622 >/dev/null 2>&1; then
    echo "[+] 启动龍魂操作台 :9622" >> "$LOG_DIR/autostart.log"
    cd "$ROOT/control-panel"
    nohup python3 main.py >> "$LOG_DIR/control-panel.log" 2>&1 &
else
    echo "[ok] 龍魂操作台已在运行" >> "$LOG_DIR/autostart.log"
fi

# 执行一次 CNSH 整合任务引擎自检
echo "[+] 执行 CNSH 自检" >> "$LOG_DIR/autostart.log"
python3 "$ROOT/CNSH/task_executor_v9_integrated.py" >> "$LOG_DIR/cnsh-autostart.log" 2>&1

# 执行一次龍魂每日审计
echo "[+] 执行每日审计" >> "$LOG_DIR/autostart.log"
bash "$ROOT/bin/longhun-daily-audit.sh" >> "$LOG_DIR/daily-audit.log" 2>&1

echo "✅ 开机自启动完成" >> "$LOG_DIR/autostart.log"
echo "" >> "$LOG_DIR/autostart.log"
