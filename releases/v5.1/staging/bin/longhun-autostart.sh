#!/usr/bin/env bash
# 龍魂系統開機自啟動腳本
# 啟動控制台、CNSH 任務執行引擎與基礎服務
# DNA:#龍芯⚡️2026-06-17-LONGHUN-AUTOSTART-v1.0

cd "$(dirname "$0")/.."
ROOT="$(pwd)"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

echo "🐉 龍魂系統開機自啟動" >> "$LOG_DIR/autostart.log"
date >> "$LOG_DIR/autostart.log"

# 啟動龍魂操作台（統一 API 入口）
if ! lsof -ti:9622 >/dev/null 2>&1; then
    echo "[+] 啟動龍魂操作台 :9622" >> "$LOG_DIR/autostart.log"
    cd "$ROOT/control-panel"
    nohup python3 main.py >> "$LOG_DIR/control-panel.log" 2>&1 &
else
    echo "[ok] 龍魂操作台已在運行" >> "$LOG_DIR/autostart.log"
fi

# 執行一次 CNSH 整合任務引擎自檢
echo "[+] 執行 CNSH 自檢" >> "$LOG_DIR/autostart.log"
python3 "$ROOT/CNSH/task_executor_v9_integrated.py" >> "$LOG_DIR/cnsh-autostart.log" 2>&1

# 執行一次龍魂每日審計
echo "[+] 執行每日審計" >> "$LOG_DIR/autostart.log"
bash "$ROOT/bin/longhun-daily-audit.sh" >> "$LOG_DIR/daily-audit.log" 2>&1

echo "✅ 開機自啟動完成" >> "$LOG_DIR/autostart.log"
echo "" >> "$LOG_DIR/autostart.log"
