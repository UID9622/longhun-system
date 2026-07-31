#!/bin/bash
# ============================================================================
# longhun-data-miner.sh — 龍魂本地数据挖掘 v1.0
# DNA: #龍芯⚡️丙午·辛未·DATA-MINER-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#
# 扫描：浏览器对话 → 本地AI应用 → 终端历史 → 龍魂系统自身
# 输出：data-miner/ 目录 + persona-chain/data-index.json
# ============================================================================

set -e
MINER_DIR="${HOME}/longhun-system/.data-miner"
PERSONA_DIR="${HOME}/longhun-system/persona-chain"
TIMESTAMP=$(date +%s)
DNA="UID9622-ONLY-ONCE🧬LK9X-772Z"

mkdir -p "$MINER_DIR" "$PERSONA_DIR"

log() { echo -e "\033[0;36m[$(date +%H:%M:%S)]\033[0m $1"; }
ok()  { echo -e "  \033[0;32m✅ $1\033[0m"; }
warn(){ echo -e "  \033[0;33m⚠️  $1\033[0m"; }

echo "🐉 龍魂数据挖掘启动"
echo "   DNA: $DNA"
echo ""

# ═══════════════════════════════════════════════════════
# 1. 浏览器对话数据（CodeBuddy/ChatGPT/Claude等本地缓存）
# ═══════════════════════════════════════════════════════
log "📂 扫描 CodeBuddy / AI IDE 对话数据..."

# CodeBuddy 对话目录（优先级最高）
CB_DIRS=(
    "$HOME/.codebuddy"
    "$HOME/Library/Application Support/CodeBuddy"
    "$HOME/Library/Application Support/CodeBuddy CN"
)
for dir in "${CB_DIRS[@]}"; do
    if [[ -d "$dir" ]]; then
        find "$dir" -maxdepth 5 -type f \( -name "*.json" -o -name "*.md" -o -name "*.jsonl" \) 2>/dev/null | while read f; do
            rel="${f#$dir/}"
            dest="$MINER_DIR/codebuddy_$(echo "$rel" | tr '/' '_')"
            cp "$f" "$dest" 2>/dev/null && ok "CodeBuddy: $rel" || true
        done
    fi
done

# Chrome/Chromium/Edge — IndexedDB + LocalStorage
CHROME_PROFILES=(
    "$HOME/Library/Application Support/Google/Chrome"
    "$HOME/Library/Application Support/Microsoft Edge"
    "$HOME/Library/Application Support/Chromium"
    "$HOME/Library/Application Support/BraveSoftware/Brave-Browser"
)

for profile_dir in "${CHROME_PROFILES[@]}"; do
    if [[ -d "$profile_dir" ]]; then
        # IndexedDB 中的AI对话数据
        find "$profile_dir" -path "*/IndexedDB/*" -type f 2>/dev/null | while read f; do
            cp "$f" "$MINER_DIR/chrome_idb_$(basename "$f")_${TIMESTAMP}" 2>/dev/null || true
        done

        # Local Storage (JSON格式)
        find "$profile_dir" -path "*/Local Storage/*" -name "*.localstorage" 2>/dev/null | while read f; do
            cp "$f" "$MINER_DIR/chrome_ls_$(basename "$f")_${TIMESTAMP}" 2>/dev/null || true
        done

        # SQLite 数据库
        find "$profile_dir" -maxdepth 6 -name "*.db" -o -name "*.sqlite" 2>/dev/null | while read f; do
            dest="$MINER_DIR/chrome_sqlite_$(basename "$f")_${TIMESTAMP}"
            sqlite3 "$f" ".dump" > "$dest" 2>/dev/null && ok "Chrome SQLite: $(basename "$f")" || true
        done
    fi
done

# Safari
if [[ -d "$HOME/Library/Safari" ]]; then
    find "$HOME/Library/Safari" -maxdepth 5 -name "*.db" 2>/dev/null | while read f; do
        dest="$MINER_DIR/safari_$(basename "$f")_${TIMESTAMP}.sql"
        sqlite3 "$f" ".dump" > "$dest" 2>/dev/null && ok "Safari: $(basename "$f")" || true
    done
fi

# Firefox
FIREFOX_DIR="$HOME/Library/Application Support/Firefox"
if [[ -d "$FIREFOX_DIR" ]]; then
    find "$FIREFOX_DIR" -maxdepth 5 -name "*.sqlite" -o -name "*.json" 2>/dev/null | while read f; do
        cp "$f" "$MINER_DIR/firefox_$(basename "$f")_${TIMESTAMP}" 2>/dev/null && ok "Firefox: $(basename "$f")" || true
    done
fi

# ═══════════════════════════════════════════════════════
# 2. 本地AI应用数据
# ═══════════════════════════════════════════════════════
log "📂 扫描本地 AI 应用..."

AI_APPS=(
    "Kimi"
    "ChatGPT"
    "Claude"
    "Cursor"
    "CodeBuddy CN"
)

for app in "${AI_APPS[@]}"; do
    app_dir="$HOME/Library/Application Support/$app"
    if [[ -d "$app_dir" ]]; then
        find "$app_dir" -maxdepth 5 -type f 2>/dev/null | while read f; do
            cp "$f" "$MINER_DIR/app_${app}_$(basename "$f")_${TIMESTAMP}" 2>/dev/null || true
        done
        ok "$app 数据"
    else
        warn "$app 未找到"
    fi
done

# Ollama 模型数据（元数据，不复制大模型文件）
OLLAMA_DIR="$HOME/.ollama"
if [[ -d "$OLLAMA_DIR" ]]; then
    # 只复制 manifests 和 modelfiles
    find "$OLLAMA_DIR" -name "Modelfile" -o -name "manifest" 2>/dev/null | while read f; do
        cp "$f" "$MINER_DIR/ollama_$(basename "$f")_${TIMESTAMP}" 2>/dev/null || true
    done
    ok "Ollama 元数据"
fi

# ═══════════════════════════════════════════════════════
# 3. 终端历史 + 会话日志
# ═══════════════════════════════════════════════════════
log "📂 扫描终端历史..."

# Zsh/Bash 历史
for hist in "$HOME/.zsh_history" "$HOME/.bash_history" "$HOME/.zsh_history_etag"; do
    if [[ -f "$hist" ]]; then
        cp "$hist" "$MINER_DIR/$(basename "$hist")_${TIMESTAMP}" 2>/dev/null
        ok "$(basename "$hist")"
    fi
done

# 龍魂项目相关终端日志
find "$HOME" -maxdepth 5 -name "*.session" -o -name "terminal*.log" 2>/dev/null | while read f; do
    cp "$f" "$MINER_DIR/term_$(basename "$f")_${TIMESTAMP}" 2>/dev/null || true
done

# ═══════════════════════════════════════════════════════
# 4. 龍魂系统自身数据
# ═══════════════════════════════════════════════════════
LONGHUN_ROOT="$HOME/longhun-system"
log "📂 扫描龍魂系统数据..."

# 执行记录/决策日志
for subdir in "02_執行記錄" "04_決策日誌" "05_系統報告"; do
    if [[ -d "$LONGHUN_ROOT/$subdir" ]]; then
        find "$LONGHUN_ROOT/$subdir" -type f \( -name "*.md" -o -name "*.json" \) 2>/dev/null | while read f; do
            cp "$f" "$MINER_DIR/longhun_$(basename "$f")_${TIMESTAMP}" 2>/dev/null || true
        done
        ok "$subdir"
    fi
done

# .codebuddy 对话记忆
if [[ -d "$LONGHUN_ROOT/.codebuddy/memory" ]]; then
    find "$LONGHUN_ROOT/.codebuddy/memory" -type f -name "*.md" 2>/dev/null | while read f; do
        cp "$f" "$MINER_DIR/memory_$(basename "$f")_${TIMESTAMP}" 2>/dev/null || true
    done
    ok ".codebuddy/memory"
fi

# 人格定义
if [[ -d "$LONGHUN_ROOT/personas" ]]; then
    find "$LONGHUN_ROOT/personas" -type f -name "*.md" 2>/dev/null | while read f; do
        cp "$f" "$MINER_DIR/persona_$(basename "$f")_${TIMESTAMP}" 2>/dev/null || true
    done
    ok "personas/"
fi

# 协议层
if [[ -d "$LONGHUN_ROOT/01_protocols" ]]; then
    find "$LONGHUN_ROOT/01_protocols" -maxdepth 3 -type f -name "*.md" 2>/dev/null | while read f; do
        cp "$f" "$MINER_DIR/proto_$(basename "$f")_${TIMESTAMP}" 2>/dev/null || true
    done
    ok "01_protocols/"
fi

# ═══════════════════════════════════════════════════════
# 5. 生成数据索引
# ═══════════════════════════════════════════════════════
log "📊 生成数据索引..."

TOTAL_FILES=$(find "$MINER_DIR" -type f 2>/dev/null | wc -l | tr -d ' ')
TOTAL_SIZE=$(du -sh "$MINER_DIR" 2>/dev/null | cut -f1)

cat > "$PERSONA_DIR/data-index.json" << INDEXEOF
{
    "dna": "$DNA",
    "timestamp": $TIMESTAMP,
    "miner_version": "1.0",
    "total_files": $TOTAL_FILES,
    "total_size": "$TOTAL_SIZE",
    "sources": {
        "browser": ["Chrome", "Edge", "Safari", "Firefox"],
        "apps": ["Kimi", "ChatGPT", "Claude", "Cursor", "CodeBuddy"],
        "terminal": ["zsh_history", "bash_history"],
        "longhun": ["execution_logs", "decision_logs", "personas", "protocols", "memory"]
    },
    "output_dir": "$MINER_DIR",
    "next_step": "python3 scripts/longhun-persona-trainer.py"
}
INDEXEOF

echo ""
echo "═══════════════════════════════════════════════════════"
echo "📊 数据挖掘报告"
echo "═══════════════════════════════════════════════════════"
echo "  总文件数: $TOTAL_FILES"
echo "  总大小:   $TOTAL_SIZE"
echo "  输出目录: $MINER_DIR"
echo "  索引文件: $PERSONA_DIR/data-index.json"
echo ""
echo "✅ 数据挖掘完成"
echo "下一步: python3 scripts/longhun-persona-trainer.py"
