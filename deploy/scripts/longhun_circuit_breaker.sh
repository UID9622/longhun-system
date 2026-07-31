#!/bin/bash
# 龍魂熔断守护 · longhun-circuit-breaker.sh
# DNA: #龍芯⚡️丙午·辛未·CIRCUIT-BREAKER-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -euo pipefail

LOG_DIR="/var/log/longhun/circuit-breaker"
FUSE_FLAG="/tmp/longhun-fuse-active"
LOG_FILE="${LOG_DIR}/circuit-breaker.log"
BARK_KEY="${BARK_KEY:-}"
MAX_FAIL=3
INTERVAL=30

# 国产节点
DOMESTIC=(
    "https://pangu.huaweicloud.com/health"
    "https://dashscope.aliyuncs.com/health"
    "https://aip.baidubce.com/health"
    "https://spark-api-open.xf-yun.com/health"
)

init() {
    mkdir -p "$LOG_DIR"
    echo $$ > /var/run/longhun-circuit-breaker.pid
    echo "[$(date '+%H:%M:%S')] 龍魂熔断守护启动 | DNA=#龍芯⚡️丙午·辛未 | 节点=${#DOMESTIC[@]}" | tee -a "$LOG_FILE"
}

check_domestic() {
    local fail=0
    for node in "${DOMESTIC[@]}"; do
        curl -sf -m 5 -o /dev/null "$node" 2>/dev/null || ((fail++))
    done
    echo "$fail"
}

bark() {
    [ -n "$BARK_KEY" ] && curl -s "https://api.day.app/${BARK_KEY}/$1/$2" >/dev/null 2>&1 || true
}

# 清理退出
cleanup() {
    rm -f /var/run/longhun-circuit-breaker.pid
    echo "[$(date '+%H:%M:%S')] 熔断守护停止" >> "$LOG_FILE"
    exit 0
}
trap cleanup SIGTERM SIGINT

# --- 主循环 ---
init
while true; do
    DOMESTIC_FAIL=$(check_domestic)

    if [ "$DOMESTIC_FAIL" -ge "$MAX_FAIL" ]; then
        # 国产大面积故障 → 降级，开放非国产
        rm -f "$FUSE_FLAG" 2>/dev/null
        echo "[$(date '+%H:%M:%S')] 🔴 国产节点故障 ${DOMESTIC_FAIL}/${#DOMESTIC[@]}，降级开放非国产通道" >> "$LOG_FILE"
        bark "龍魂熔断·降级" "国产节点故障${DOMESTIC_FAIL}个，已开放非国产"
    else
        # 国产正常 → 熔断非国产
        touch "$FUSE_FLAG"
        local ok=$(( ${#DOMESTIC[@]} - DOMESTIC_FAIL ))
        echo "[$(date '+%H:%M:%S')] 🟢 国产节点正常 ${ok}/${#DOMESTIC[@]}，非国产通道熔断" >> "$LOG_FILE"
    fi

    sleep "$INTERVAL"
done
