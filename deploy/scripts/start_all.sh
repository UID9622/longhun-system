#!/bin/bash
# 🐉 龍魂 · 开机自启动+守护焊死脚本 v1.0
# DNA: #龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-BOOT-SERVICES-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 幂等:端口已监听则跳过,避免重复启动冲突
# 用途:开机自动拉起核心服务 + watchdog每5分钟调用一次做自动修复

LONGHUN_ROOT="/Users/zuimeidedeyihan/longhun-system"
PY="/usr/local/bin/python3"
LOG_DIR="$LONGHUN_ROOT/logs"
mkdir -p "$LOG_DIR"

# 启动服务(幂等)
start_if_down() {
    local port="$1" name="$2"; shift 2
    if lsof -nP -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1; then
        echo "[$(date '+%F %T')] ✅ $name 已在运行(:$port)"
    else
        echo "[$(date '+%F %T')] 🚀 启动 $name (:$port)"
        cd "$LONGHUN_ROOT" && nohup "$PY" "$@" > "$LOG_DIR/$name.log" 2>&1 &
        sleep 2
        if lsof -nP -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1; then
            echo "[$(date '+%F %T')] ✅ $name 启动成功"
        else
            echo "[$(date '+%F %T')] ⚠️ $name 启动失败,查看 $LOG_DIR/$name.log"
        fi
    fi
}

echo "[$(date '+%F %T')] 🐉 龍魂服务启动检查开始"
# 核心服务(真实存在·参数已验证)
start_if_down 8767 knowledge 08_BIN/lh_knowledge_graph_v2.py --server 8767
start_if_down 8766 gateway 08_BIN/lh_sovereign_gateway.py
start_if_down 8080 dashboard 08_BIN/lh_transparent_dashboard.py --host 0.0.0.0 --port 8080
start_if_down 8090 search 08_BIN/search/lh_search_engine.py --server --host 0.0.0.0 --port 8090
echo "[$(date '+%F %T')] ✅ 龍魂服务启动检查完成"
