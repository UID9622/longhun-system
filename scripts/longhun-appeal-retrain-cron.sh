#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ═══════════════════════════════════════════════════════
# 龍魂AI初审模型 · 定期自动重训练脚本 v1.0
# DNA: #龍芯⚡️丙午·辛未·APPEAL-RETRAIN-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#
# 触发条件：
#   1. 人格链有更新（persona-chain-latest.json 修改时间变化）
#   2. 每天定时（cron: 0 3 * * *）
#   3. 手动触发: --force
#
# 重训练后自动重载验证服务，无缝切换模型。
# ═══════════════════════════════════════════════════════

set -e

LONGHUN_ROOT="$HOME/longhun-system"
PERSONA_CHAIN="$LONGHUN_ROOT/persona-chain/persona-chain-latest.json"
MODEL_FILE="$LONGHUN_ROOT/models/appeal_classifier.pkl"
STATE_FILE="$LONGHUN_ROOT/.appeal-retrain-state"
LOG_FILE="/opt/frp/logs/appeal-retrain.log"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "🐉 龍魂AI初审模型重训练检查"

# ── 强制模式 ──
if [[ "$1" == "--force" ]]; then
    log "🔄 强制重训练模式"
    FORCE=true
else
    FORCE=false
fi

# ── 检查人格链是否存在 ──
if [[ ! -f "$PERSONA_CHAIN" ]]; then
    log "⚠️ 人格链未找到: $PERSONA_CHAIN"
    log "   请先运行: python3 scripts/longhun-persona-pipeline.sh"
    exit 1
fi

# ── 检查是否需要重训练 ──
CHAIN_MTIME=$(stat -f %m "$PERSONA_CHAIN" 2>/dev/null || stat -c %Y "$PERSONA_CHAIN" 2>/dev/null)

if [[ -f "$STATE_FILE" ]]; then
    LAST_MTIME=$(cat "$STATE_FILE")
    if [[ "$CHAIN_MTIME" == "$LAST_MTIME" ]] && [[ "$FORCE" != "true" ]]; then
        log "✅ 人格链未变化，跳过重训练"
        exit 0
    fi
fi

# ── 检查训练脚本 ──
TRAINER="$LONGHUN_ROOT/scripts/longhun-appeal-trainer.py"
if [[ ! -f "$TRAINER" ]]; then
    log "❌ 训练脚本未找到: $TRAINER"
    exit 1
fi

# ── 执行重训练 ──
log "🔄 开始重训练..."

cd "$LONGHUN_ROOT"

# 备份旧模型
if [[ -f "$MODEL_FILE" ]]; then
    BACKUP="$MODEL_FILE.bak.$(date +%Y%m%d_%H%M%S)"
    cp "$MODEL_FILE" "$BACKUP"
    log "   📦 旧模型备份: $BACKUP"
fi

# 训练
if python3 "$TRAINER" --force >> "$LOG_FILE" 2>&1; then
    log "✅ 重训练完成"

    # 更新状态
    echo "$CHAIN_MTIME" > "$STATE_FILE"

    # 检查模型
    if [[ -f "$MODEL_FILE" ]]; then
        NEW_SIZE=$(ls -lh "$MODEL_FILE" | awk '{print $5}')
        log "   📊 新模型大小: $NEW_SIZE"
    fi

    # 重载验证服务（发送SIGHUP或重启）
    PID=$(pgrep -f "longhun-persona-verify-v4" | head -1)
    if [[ -n "$PID" ]]; then
        log "   🔄 重载验证服务 (PID: $PID)"
        kill -HUP "$PID" 2>/dev/null || {
            # 如果SIGHUP不支持，重启
            log "   ⚠️ SIGHUP不支持，重启服务"
            kill "$PID" 2>/dev/null || true
            sleep 2
            nohup python3 "$LONGHUN_ROOT/L6_同步层/longhun-persona-verify-v4.py" \
                --port 9623 --host 0.0.0.0 \
                >> /opt/frp/logs/persona-verify-v4.log 2>&1 &
            log "   ✅ 服务已重启"
        }
    else
        log "   ⚠️ 验证服务未运行，启动中..."
        nohup python3 "$LONGHUN_ROOT/L6_同步层/longhun-persona-verify-v4.py" \
            --port 9623 --host 0.0.0.0 \
            >> /opt/frp/logs/persona-verify-v4.log 2>&1 &
        log "   ✅ 服务已启动"
    fi

    # 验证模型加载
    sleep 2
    if curl -s http://localhost:9623/health | grep -q "ai_model_loaded.*true"; then
        log "   ✅ AI模型已加载"
    else
        log "   ⚠️ 模型加载状态待确认"
    fi

    log "🏆 龍魂AI初审模型自动重训练完成"

else
    log "❌ 重训练失败"

    # 恢复旧模型
    if [[ -f "$BACKUP" ]]; then
        cp "$BACKUP" "$MODEL_FILE"
        log "   ↩️ 已恢复旧模型"
    fi

    exit 1
fi
