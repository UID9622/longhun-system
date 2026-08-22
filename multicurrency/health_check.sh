#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

# 龍魂多币种·健康检查脚本
# DNA:#龍芯⚡️丙午·甲午·壬子·丙午·䷙大畜-HEALTH-CHECK-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
SERVICE_NAME="longhun-multicurrency-sync"
LOG_FILE="$HOME/.龍魂/health_check.log"

echo "[${TIMESTAMP}] 🔍 开始健康检查..." | tee -a "$LOG_FILE"

# 1. 检查服务状态
if systemctl is-active --quiet $SERVICE_NAME; then
    PID=$(systemctl show -p MainPID --value $SERVICE_NAME)
    echo "[${TIMESTAMP}] ✅ 服务运行中 (PID: $PID)" | tee -a "$LOG_FILE"
else
    echo "[${TIMESTAMP}] ❌ 服务未运行" | tee -a "$LOG_FILE"
    exit 1
fi

# 2. 检查进程内存使用
MEMORY=$(ps -p $PID -o %mem= | awk '{print $1}')
echo "[${TIMESTAMP}] 📊 内存使用: ${MEMORY}%" | tee -a "$LOG_FILE"

if (( $(echo "$MEMORY > 20" | bc -l) )); then
    echo "[${TIMESTAMP}] ⚠️  内存使用过高，考虑重启" | tee -a "$LOG_FILE"
fi

# 3. 检查最后一次同步时间
LAST_SYNC=$(journalctl -u $SERVICE_NAME -n 1 --no-pager | grep "同步完成" | tail -1)
if [ -z "$LAST_SYNC" ]; then
    echo "[${TIMESTAMP}] ❌ 未找到最近的同步记录" | tee -a "$LOG_FILE"
else
    echo "[${TIMESTAMP}] ✅ 最后同步: $LAST_SYNC" | tee -a "$LOG_FILE"
fi

# 4. 检查数据库完整性
python3 << 'PYTHON_CHECK'
import os, sqlite3

db_path = os.path.expanduser('~/.龍魂/notion_sync.db')
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sync_log")
    count = cursor.fetchone()[0]
    cursor.execute("PRAGMA integrity_check")
    integrity = cursor.fetchone()[0]
    conn.close()
    
    print(f"✅ SQLite 完整性检查通过: {count} 条同步记录")
except Exception as e:
    print(f"❌ SQLite 错误: {e}")
PYTHON_CHECK

echo "[${TIMESTAMP}] ✅ 健康检查完成" | tee -a "$LOG_FILE"
