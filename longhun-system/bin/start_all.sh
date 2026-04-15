#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 龍魂一鍵啟動 · 全部服務
# DNA: #龍芯⚡️2026-04-03-START-ALL-v4.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 創建者: UID9622 諸葛鑫
# 理論指導: 曾仕強老師（永恆顯示）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# 使用方式:
#   ~/longhun-system/start_all.sh
#
# 啟動的服務:
#   8000  龍魂主引擎        (app.py · DeepSeek+雙門+易經推演)
#   8765  龍魂本地服務      (記憶/知識庫/情緒時間線)
#   9622  CNSH-64治理引擎   (本地MVP+龍盾+人格路由+三才流場API)
#   8080  Open WebUI        (完整聊天界面 · 已接龍魂引擎)
#   8081  龍魂8081中樞門戶   (靜態頁面+DeepSeek API代理+系統狀態聚合)
#   11434 Ollama            (本地9個模型)
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -euo pipefail

HOME_DIR="$HOME"
LH_DIR="$HOME_DIR/longhun-system"
LOG_DIR="$LH_DIR/logs"
SCAN_REPORT="$LOG_DIR/服务扫描报告.log"

mkdir -p "$LOG_DIR"

# ── macOS 通知 ─────────────────────────────────────────
通知() {
    osascript -e "display notification \"$2\" with title \"🐉 龍魂\" subtitle \"$1\"" 2>/dev/null || true
}

# ── 輔助函數：端口檢測 ─────────────────────────────────
端口占用() { lsof -ti :"$1" >/dev/null 2>&1; }
端口进程名() { ps -p "$(lsof -ti :"$1" 2>/dev/null)" -o comm= 2>/dev/null || echo "未知"; }

# ── 輔助函數：健康檢查 ─────────────────────────────────
健康檢查() {
    local PORT=$1 ENDPOINT=$2 TIMEOUT=${3:-3}
    curl -s --max-time "$TIMEOUT" "http://127.0.0.1:${PORT}${ENDPOINT}" >/dev/null 2>&1
}

# ════════════════════════════════════════════════════════
# 第零步：預掃描 + 環境清理
# ════════════════════════════════════════════════════════
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🔍 預掃描 · $(date '+%Y-%m-%d %H:%M:%S')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 端口:服務名:類型(managed/zombie/optional)
declare -A KNOWN_PORTS
KNOWN_PORTS[8000]="龍魂主引擎:managed"
KNOWN_PORTS[8765]="龍魂本地服務:managed"
KNOWN_PORTS[9622]="CNSH-64治理引擎:managed"
KNOWN_PORTS[8080]="Open WebUI:managed"
KNOWN_PORTS[8081]="龍魂8081中樞門戶:managed"
KNOWN_PORTS[11434]="Ollama:managed"
KNOWN_PORTS[8188]="ComfyUI圖像引擎:optional"
KNOWN_PORTS[8089]="Locust壓測殭屍:zombie"

WARN_COUNT=0
ZOMBIE_COUNT=0

while IFS= read -r PORT; do
    [ -z "$PORT" ] && continue
    if [[ -n "${KNOWN_PORTS[$PORT]:-}" ]]; then
        TYPE="${KNOWN_PORTS[$PORT]##*:}"
        NAME="${KNOWN_PORTS[$PORT]%%:*}"
        if [ "$TYPE" = "zombie" ]; then
            echo "  🔴 :$PORT $NAME → 殭屍，將清理"
            ((ZOMBIE_COUNT++))
        elif [ "$TYPE" = "optional" ]; then
            echo "  ⚪ :$PORT $NAME → 可選模組，不強制"
        fi
    else
        PROC=$(端口进程名 "$PORT")
        echo "  🟡 :$PORT 未登記端口 (进程: ${PROC}) → 僅報告，不干預"
        echo "$(date '+%Y-%m-%d %H:%M:%S') 未知端口 :$PORT 进程:${PROC}" >> "$SCAN_REPORT"
        ((WARN_COUNT++))
    fi
done < <(lsof -iTCP -sTCP:LISTEN -P -n 2>/dev/null | awk 'NR>1{match($9, /:([0-9]+)$/, a); if(a[1]!="") print a[1]}' | sort -nu)

[ "$WARN_COUNT" -gt 0 ] && echo "  ⚠️  發現 $WARN_COUNT 個未登記端口，已記錄到 $SCAN_REPORT"
[ "$ZOMBIE_COUNT" -gt 0 ] && echo "  🧹 發現 $ZOMBIE_COUNT 個殭屍端口，準備清理"
[ "$WARN_COUNT" -eq 0 ] && [ "$ZOMBIE_COUNT" -eq 0 ] && echo "  ✅ 環境乾淨，無異常"

# 清理殭屍
for ZOMBIE_PORT in 8089; do
    if 端口占用 "$ZOMBIE_PORT"; then
        kill $(lsof -ti :"$ZOMBIE_PORT") 2>/dev/null || true
        echo "  🧹 已清理殭屍端口 :$ZOMBIE_PORT"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🚀 開始啟動全部服務"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ════════════════════════════════════════════════════════
# 第一步：龍魂主引擎 (8000)
# ════════════════════════════════════════════════════════
if 端口占用 8000; then
    if 健康檢查 8000 /v1/models; then
        echo "  ✅ 龍魂主引擎 · 已在運行 (8000)"
    else
        echo "  🔄 龍魂主引擎端口占用但無響應，重啟..."
        kill $(lsof -ti :8000) 2>/dev/null || true
        sleep 1
        cd "$LH_DIR" && nohup python3 app.py > "$LOG_DIR/app.log" 2>&1 &
        sleep 2
        echo "  ✅ 龍魂主引擎 · 重啟完成 (8000)"
    fi
else
    cd "$LH_DIR" && nohup python3 app.py > "$LOG_DIR/app.log" 2>&1 &
    sleep 2
    echo "  ✅ 龍魂主引擎 · 啟動成功 (8000)"
fi

# ════════════════════════════════════════════════════════
# 第二步：龍魂本地服務 (8765)
# ════════════════════════════════════════════════════════
if 端口占用 8765; then
    echo "  ✅ 龍魂本地服務 · 已在運行 (8765)"
else
    cd "$LH_DIR" && nohup python3 longhun_local_service.py > "$LOG_DIR/local_service.log" 2>&1 &
    sleep 2
    if 端口占用 8765; then
        echo "  ✅ 龍魂本地服務 · 啟動成功 (8765)"
    else
        echo "  🟡 龍魂本地服務 · 啟動中，請稍等..."
    fi
fi

# ════════════════════════════════════════════════════════
# 第三步：CNSH-64 Governance Engine (9622)
# 包含：本地MVP + 龍盾 + 人格路由 + 三才流場API
# ════════════════════════════════════════════════════════
CNSH_CORE="$LH_DIR/cnsh-core"
if 端口占用 9622; then
    if 健康檢查 9622 /persona/stats; then
        echo "  ✅ CNSH-64治理引擎 · 已在運行 (9622)"
    else
        echo "  🔄 CNSH-64 端口占用但無響應，重啟..."
        kill $(lsof -ti :9622) 2>/dev/null || true
        sleep 1
        cd "$CNSH_CORE" && nohup python3 -m uvicorn api.main:app --host 127.0.0.1 --port 9622 --log-level warning > "$LOG_DIR/cnsh9622.log" 2>&1 &
        sleep 2
        echo "  ✅ CNSH-64治理引擎 · 重啟完成 (9622)"
    fi
elif [ -d "$CNSH_CORE" ]; then
    cd "$CNSH_CORE" && nohup python3 -m uvicorn api.main:app --host 127.0.0.1 --port 9622 --log-level warning > "$LOG_DIR/cnsh9622.log" 2>&1 &
    sleep 2
    if 端口占用 9622; then
        echo "  ✅ CNSH-64治理引擎 · 啟動成功 (9622)"
    else
        echo "  🔴 CNSH-64 啟動失敗 · 查看 logs/cnsh9622.log"
    fi
else
    echo "  ⚪ cnsh-core 目錄不存在，跳過"
fi

# ════════════════════════════════════════════════════════
# 第四步：Ollama (11434)
# ════════════════════════════════════════════════════════
if 端口占用 11434; then
    echo "  ✅ Ollama · 已在運行 (11434)"
else
    if command -v ollama &>/dev/null; then
        nohup ollama serve > "$LOG_DIR/ollama输出.log" 2>&1 &
        sleep 2
        echo "  ✅ Ollama · 已啟動 (11434)"
    else
        echo "  ⚠️  Ollama 未安裝，跳過"
    fi
fi

# ════════════════════════════════════════════════════════
# 第五步：Open WebUI (8080)
# ════════════════════════════════════════════════════════
OPENWEBUI="/Library/Frameworks/Python.framework/Versions/3.11/bin/open-webui"
if 端口占用 8080; then
    echo "  ✅ Open WebUI · 已在運行 (8080)"
elif [ -f "$OPENWEBUI" ]; then
    nohup "$OPENWEBUI" serve > "$LOG_DIR/openwebui输出.log" 2>&1 &
    sleep 3
    if 端口占用 8080; then
        echo "  ✅ Open WebUI · 啟動成功 (8080)"
    else
        echo "  🟡 Open WebUI · 啟動中，請稍等..."
    fi
else
    echo "  ⚪ open-webui 未找到，跳過"
fi

# ════════════════════════════════════════════════════════
# 第六步：龍魂8081中樞門戶部署 (8081)
# ════════════════════════════════════════════════════════
WEB_DIR="$LH_DIR/web"
mkdir -p "$WEB_DIR"

# 自動複製三才流場到 web 目錄
for src in "$LH_DIR/三才流场_v3.0.html" "$LH_DIR/algorithmic-art/三才流場_v6_优化版.html"; do
    if [ -f "$src" ]; then
        filename=$(basename "$src")
        cp "$src" "$WEB_DIR/$filename"
    fi
done

# 複製 index.html（如果 web 目錄還沒有）
if [ ! -f "$WEB_DIR/index.html" ] && [ -f "$LH_DIR/web/index.html" ]; then
    true  # 已存在
fi

if 端口占用 8081; then
    echo "  ✅ 龍魂8081中樞門戶 · 已在運行 (8081)"
else
    cd "$LH_DIR" && nohup python3 bin/portal_engine_8081.py > "$LOG_DIR/portal_8081.log" 2>&1 &
    sleep 2
    echo "  ✅ 龍魂8081中樞門戶 · 啟動成功 (8081)"
fi

# ════════════════════════════════════════════════════════
# 第七步：ComfyUI 圖像引擎（可選，按需啟動）
# ════════════════════════════════════════════════════════
COMFY_SCRIPT="$LH_DIR/bin/comfyui_start.sh"
if [ -f "$COMFY_SCRIPT" ]; then
    if 端口占用 8188; then
        echo "  ✅ ComfyUI圖像引擎 · 已在運行 (8188) [可選]"
    else
        echo "  ⚪ ComfyUI圖像引擎 · 未啟動，如需使用請執行: $COMFY_SCRIPT"
    fi
fi

# ════════════════════════════════════════════════════════
# 最終狀態匯總
# ════════════════════════════════════════════════════════
sleep 2

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🐉 龍魂全服務狀態一覽"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

状态行() {
    local PORT=$1 NAME=$2 URL=$3
    if 端口占用 "$PORT"; then
        printf "  🟢 %-6s %-22s %s\n" ":$PORT" "$NAME" "$URL"
    else
        printf "  🔴 %-6s %-22s %s\n" ":$PORT" "$NAME" "(未運行)"
    fi
}

状态行 8000  "龍魂主引擎"      "http://localhost:8000"
状态行 8765  "龍魂本地服務"    "http://localhost:8765"
状态行 9622  "CNSH-64治理引擎" "http://localhost:9622"
状态行 8080  "Open WebUI"      "http://localhost:8080"
状态行 8081  "龍魂8081中樞門戶"  "http://localhost:8081"
状态行 11434 "Ollama"          "http://localhost:11434"

if 端口占用 8188; then
    printf "  🟢 %-6s %-22s %s\n" ":8188" "ComfyUI圖像引擎" "http://localhost:8188 [可選]"
fi

echo ""
echo "  📍 常用入口："
echo "     龍魂對話    → http://localhost:8081"
echo "     Open WebUI  → http://localhost:8080"
echo "     MVP造物界面 → http://localhost:9622/mvp/static/index.html"
echo "     龍盾狀態    → http://localhost:9622/shield/status"
echo "     三才流場v3  → http://localhost:8081/三才流场_v3.0.html"
echo "     三才流場v6  → http://localhost:8081/三才流場_v6_优化版.html"

echo ""
通知 "服務啟動完成" "龍魂全系統已在後台運行"
echo "  ✅ 完成 · DNA: #龍芯⚡️$(date +%Y%m%d)-START-ALL-v4.0-UID9622"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
